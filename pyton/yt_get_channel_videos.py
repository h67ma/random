import json
import re
import argparse
from urllib.request import Request, urlopen

VIDEOS_PER_PAGE = 50 # max allowed
API_KEY_NAME = "yt_api_key.txt"

def sanitize_filename(filename: str) -> str:
	return re.sub("[^\w\-_\., \(\)[\]!'&+]", "_", filename)


def make_channel_nfos_url(api_key, channel_id):
	return "https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&id=%s&key=%s" % (channel_id, api_key)


def make_uploads_req_url(api_key, playlist_id, next_page_token):
	uploads_req_url = "https://youtube.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults=%d&playlistId=%s&key=%s" % (VIDEOS_PER_PAGE, playlist_id, api_key)
	if next_page_token is not None:
		uploads_req_url += "&pageToken=" + next_page_token
	return uploads_req_url


# read the api key
with open(API_KEY_NAME, "r") as f:
	api_key = f.readline().strip()

# parse args
parser = argparse.ArgumentParser()
parser.add_argument("-c", "--channel", action="store", required=True, type=str, help=("Youtube channel id"))
parser.add_argument("-f", "--file", action="store_true", help=("Write results to file instead of stdout"))
args = parser.parse_args()
channel_id = args.channel

# get uploads playlist id from channel infos
channel_req_url = make_channel_nfos_url(api_key, channel_id)
req = Request(channel_req_url)
response = json.loads(urlopen(req).read().decode())
uploads_playlist_id = response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

# get videos
vedio_names = []
next_page_token = None
while True:
	uploads_req_url = make_uploads_req_url(api_key, uploads_playlist_id, next_page_token)
	req = Request(uploads_req_url)
	response = json.loads(urlopen(req).read().decode())

	for vedio in response["items"]:
		vedio_names.append(vedio["snippet"]["title"])

	if "nextPageToken" in response:
		next_page_token = response["nextPageToken"]
	else:
		break

# print or write results
if args.file:
	out_name = sanitize_filename(channel_id) + ".log"
	with open(out_name, "w", encoding="UTF-8") as f:
		for name in vedio_names:
			f.write(name + '\n')
else:
	print('\n')
	for name in vedio_names:
		print(name)
	print('\n')

# print summary
print("total: %d videos" % len(vedio_names))
