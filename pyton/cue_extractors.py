import re

def extract_mm_ss(line):
	matches = re.findall(r"^\[(\d+):(\d+)\]", line)
	if len(matches) != 1:
		return None
	matches = matches[0]
	mm = int(matches[0])
	ss = int(matches[1])
	return (mm, ss, 0)


def extract_hh_mm_ss(line):
	matches = re.findall(r"^\[(\d+):(\d+):(\d+)\]", line)
	if len(matches) != 1:
		return None
	matches = matches[0]
	mm = int(matches[0]) * 60 + int(matches[1])
	ss = int(matches[2])
	return (mm, ss, 0)


def extract_mm_ss_ms(line):
	matches = re.findall(r"^\[(\d+):(\d+)\.(\d+)\]", line)
	if len(matches) != 1:
		return None
	matches = matches[0]
	mm = int(matches[0])
	ss = int(matches[1])
	ms = int(matches[2])
	return (mm, ss, ms)


def extract_hh_mm_ss_ms(line):
	matches = re.findall(r"^\[(\d+):(\d+):(\d+)\.(\d+)\]", line)
	if len(matches) != 1:
		return None
	matches = matches[0]
	mm = int(matches[0]) * 60 + int(matches[1])
	ss = int(matches[2])
	ms = int(matches[3])
	return (mm, ss, ms)


def extract_title_artist(line):
	matches = re.findall(r"^\[[^\]]+\]([^-]+) - (.+)$", line)
	if len(matches) != 1:
		return None
	matches = matches[0]
	artist_line = "\n    PERFORMER %s" % matches[0].strip() # strip - discard space at the beginning
	title = matches[1]
	return (artist_line, title)


def extract_title(line):
	matches = re.findall(r"^\[[^\]]+\](.+)$", line)
	if len(matches) != 1:
		return None
	line = ""
	title = matches[0] # so it turns out that when group cnt==1 then it's different :() thanks python
	title = title.strip() # strip - discard space at the beginning
	return ("", title)
