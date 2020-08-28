import sys
import re

# converts tracklist from lyrics form to cuesheet

if len(sys.argv) < 4:
	print("too few arguments")
	print("arg1 = target track filename")
	print("arg2 = input - lyrics filename ([00:00.00]Artist - Title, or [00:00.00]Title)")
	print("arg3 = oputput - cue filename")
	exit()

with open(sys.argv[2], "r") as f_lyrics:
	with open(sys.argv[3], "w") as f_cue:
		f_cue.write("FILE \"%s\" WAVE\n" % sys.argv[1])
		i = 0
		errors = 0
		for line in f_lyrics:
			line = line.strip()
			i += 1
			matches = re.findall(r"^\[(\d{2}):(\d{2})\.(\d{2})\]", line)
			if len(matches) == 1:
				matches = matches[0]
				hh = int(matches[0])
				mm = int(matches[1])
				ss = int(matches[2])
			else:
				# fallback to version with hours:
				matches = re.findall(r"^\[(\d+):(\d+):(\d+)\.(\d+)\]", line)
				if len(matches) == 1:
					matches = matches[0]
					hh = int(matches[0]) * 60 + int(matches[1])
					mm = int(matches[2])
					ss = int(matches[3])
				else:
					print("can't find timestamp in line %d: %s" % (i, line))
					f_cue.write("  TRACK %02d AUDIO\n    PERFORMER FIXME\n    TITLE FIXME\n    INDEX 01 00:00:00\n" % i)
					errors += 1
					continue

			matches = re.findall(r"^\[[^\]]+\]([^-]+) - (.+)$", line)
			if len(matches) == 1:
				matches = matches[0]
				artist_line = "\n    PERFORMER %s" % matches[0]
				title = matches[1]
			else:
				# try version without "-"
				matches = re.findall(r"^\[[^\]]+\](.+)$", line)
				if len(matches) == 1:
					artist_line = ""
					title = matches[0] # so it turns out that when group cnt==1 then it's different :()
				else:
					print("can't find trak info in line %d: %s" % (i, line))
					f_cue.write("  TRACK %02d AUDIO\n    PERFORMER FIXME\n    TITLE FIXME\n    INDEX 01 %02d:%02d:%02d\n" % (i, hh, mm, ss))
					errors += 1
					continue

			f_cue.write("  TRACK %02d AUDIO%s\n    TITLE %s\n    INDEX 01 %02d:%02d:%02d\n" % (i, artist_line, title, hh, mm, ss))
		if errors > 0:
			print("completed with %d errors, pls fix cuesheet manually" % errors)
