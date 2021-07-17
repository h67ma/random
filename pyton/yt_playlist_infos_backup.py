import os
import json
import re
from datetime import datetime
import requests
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

# TODO also dump "saved" playlists - load list of manually prepared playlists from textfile

def sanitize_filename_input(input: str) -> str:
	return re.sub("[^\w\-_\., \(\)[\]!'&+]", "_", input)


root_dirname = "yt_playlists_dump_%s" % datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
print(root_dirname)
root_dirname = "yt_playlists_dump"
IMG_DIR = "imgs"
img_dirname = os.path.join(root_dirname, IMG_DIR)
html_dumps_dirname = os.path.join(root_dirname, "html")
json_filename = os.path.join(root_dirname, "dump.json")

os.makedirs(img_dirname, exist_ok=True)
os.makedirs(html_dumps_dirname, exist_ok=True)

CLIENT_SECRETS_FILE = "sikret.json"
scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

# authenticate and create api bobject
flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, scopes)
credentials = flow.run_console()
youtube = googleapiclient.discovery.build("youtube", "v3", credentials=credentials)

dumped_playlists = []
playlist_next_page_token = None
while True:
	request = youtube.playlists().list(
		part="snippet,status",
		maxResults=50, # 50 is max
		mine=True,
		pageToken=playlist_next_page_token
	)
	playlist_response = request.execute()

	for playlist in playlist_response["items"]:
		playlist_id = playlist["id"]
		playlist_channel = playlist["snippet"]["channelTitle"]
		playlist_privacy_status = playlist["status"]["privacyStatus"]
		playlist_title = playlist["snippet"]["title"]
		playlist_desc = playlist["snippet"]["description"]

		print("processing", playlist_title)

		videos_on_playlist = []
		playlist_content_next_page_token = None
		while True:
			request = youtube.playlistItems().list(
				part="snippet,status,contentDetails",
				maxResults=50, # 50 is max
				playlistId=playlist_id,
				pageToken=playlist_content_next_page_token
			)
			playlist_content_response = request.execute()

			for video in playlist_content_response["items"]:
				vid_id = video["contentDetails"]["videoId"]
				vid_data = {
					"url": "https://www.youtube.com/watch?v=" + vid_id,
					"title": video["snippet"].get("title", "???"),
					"channelName": video["snippet"].get("videoOwnerChannelTitle", "???"),
					"channelUrl": "https://www.youtube.com/channel/" + video["snippet"].get("videoOwnerChannelId", "???"),
					"published": video["contentDetails"].get("videoPublishedAt", "???"),
					"addedToPlaylist": video["snippet"].get("publishedAt", "???"),
					"description": video["snippet"].get("description", "???"),
					"visibility": video["status"].get("privacyStatus", "???"),
					"position": video["snippet"].get("position", "???")
				}

				if "note" in video["contentDetails"]:
					vid_data["note"] = video["contentDetails"]["note"]

				vid_data["thumbnails"] = []
				best_thumb_filename = ""
				if "thumbnails" in video["snippet"] and len(video["snippet"]["thumbnails"]) > 0:
					thumbs = video["snippet"]["thumbnails"]
					vid_data["thumbnails"] = [thumb["url"] for thumb in thumbs.values()]

					# find thumb of biggest size - this kinda messy but works
					best_size = sorted(thumbs, key=lambda k: thumbs[k]["width"], reverse=True)[0]
					best_thumb_url = thumbs[best_size]["url"]
					best_thumb_filename = vid_id + ".jpg"

					# download thumb
					if not os.path.exists(os.path.join(img_dirname, best_thumb_filename)):
						remote_file = requests.get(best_thumb_url)
						with open(os.path.join(img_dirname, best_thumb_filename), "wb") as f:
							f.write(remote_file.content)
				vid_data["best_thumb_filename"] = best_thumb_filename

				# TODO get vid duration *sigh* from individual video resource

				videos_on_playlist.append(vid_data)

			if "nextPageToken" in playlist_content_response:
				playlist_content_next_page_token = playlist_content_response["nextPageToken"]
			else:
				break
		
		dumped_playlists.append({
			"url": "https://www.youtube.com/playlist?list=" + playlist_id,
			"channel": playlist["snippet"]["channelTitle"],
			"channelUrl": "https://www.youtube.com/channel/" + playlist["snippet"]["channelId"],
			"visibility": playlist["status"]["privacyStatus"],
			"title": playlist["snippet"]["title"],
			"description": playlist["snippet"]["description"],
			"videos": videos_on_playlist
		})

	if "nextPageToken" in playlist_response:
		playlist_next_page_token = playlist_response["nextPageToken"]
	else:
		break

with open(json_filename, "w", encoding="UTF-8") as out_f:
	json.dump(dumped_playlists, out_f, ensure_ascii=False, indent=2)

# generate html report for each playlist
for playlist in dumped_playlists:
	html_list = """<!DOCTYPE html><html><head><title>%s</title></head><body><div>
		title: <a href="%s">%s</a><br />
		channel: <a href="%s">%s</a></br />
		visibility: %s</br />
		description: %s
	<table border="1"><tr>
		<th>#</th>
		<th>title</th>
		<th>channel</th>
		<th>visibility</th>
		<th>published</th>
		<th>addedToPlaylist</th>
		<th>duration</th>
		<th>thumbnails</th>
		<th>description</th>
	</tr>""" % (
		playlist["title"],
		playlist["url"],
		playlist["title"],
		playlist["channelUrl"],
		playlist["channel"],
		playlist["visibility"],
		playlist["description"]
	)

	for video in playlist["videos"]:
		html_list += """<tr>
			<td>%s</td>
			<td><a href="%s">
				<img src="../%s/%s"/ width="400"><br />%s
			</a></td>
			<td><a href="%s">%s</a></td>
			<td>%s</td>
			<td>%s</td>
			<td>%s</td>
			<td>%s</td>
			<td>%s</td>
			<td>%s</td>
		</tr>""" % (
			video["position"],
			video["url"],
			IMG_DIR,
			video["best_thumb_filename"],
			video["title"],
			video["channelUrl"],
			video["channelName"],
			video["visibility"],
			video["published"],
			video["addedToPlaylist"],
			"??:??",
			"<br />".join(["""<a href="%s">[%d]</a>""" % (thumb_url, i) for i, thumb_url in enumerate(video["thumbnails"])]),
			video["description"]
		)
	
	html_list += "</table></body></html>"

	with open(os.path.join(html_dumps_dirname, sanitize_filename_input(playlist["title"] + ".html")), "w", encoding="UTF-8") as f:
		f.write(html_list)
