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
			i += 1
			matches = re.findall(r"\[(\d{2}):(\d{2})\.(\d{2})\]([^-]+) - ([^\n]+)\n", line)
			if len(matches) < 1:
				# first try to find a version with hours:
				matches = re.findall(r"\[(\d+):(\d+):(\d+)\.(\d+)\]([^-]+) - ([^\n]+)\n", line)
				if len(matches) < 1:
					print("can't parse line %d: %s" % (i, line), end='')
					f_cue.write("  TRACK %02d AUDIO\n    PERFORMER FIXME\n    TITLE FIXME\n    INDEX 01 00:00:00\n" % i)
					errors += 1
					continue
				matches = matches[0]
				f_cue.write("  TRACK %02d AUDIO\n    PERFORMER %s\n    TITLE %s\n    INDEX 01 %02d:%02d:%02d\n" \
					% (i, matches[4], matches[5], int(matches[0]) * 60 + int(matches[1]), int(matches[2]), int(matches[3])))
				continue
			matches = matches[0]
			f_cue.write("  TRACK %02d AUDIO\n    PERFORMER %s\n    TITLE %s\n    INDEX 01 %02d:%02d:%02d\n" \
				% (i, matches[3], matches[4], int(matches[0]), int(matches[1]), int(matches[2])))
		if errors > 0:
			print("completed with %d errors, pls fix cuesheet manually" % errors)
