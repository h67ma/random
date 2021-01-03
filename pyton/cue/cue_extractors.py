import re

def extract_mm_ss(line):
	matches = re.findall(r"^\[?(\d+):(\d+)\]?\s*([^-]+ - )?(.+)?$", line)
	if len(matches) != 1:
		return None
	matches = matches[0]
	mm = int(matches[0])
	ss = int(matches[1])
	artist = matches[2][:-3].strip() # trim " - " at the end
	title = matches[3].strip()
	return (mm, ss, 0, artist, title)


def extract_hh_mm_ss(line):
	matches = re.findall(r"^\[?(\d+):(\d+):(\d+)\]?\s*([^-]+ - )?(.+)?$", line)
	if len(matches) != 1:
		return None
	matches = matches[0]
	mm = int(matches[0]) * 60 + int(matches[1])
	ss = int(matches[2])
	artist = matches[3][:-3].strip() # trim " - " at the end
	title = matches[4].strip()
	return (mm, ss, 0, artist, title)


def extract_mm_ss_ms(line):
	matches = re.findall(r"^\[?(\d+):(\d+)\.(\d+)\]?\s*([^-]+ - )?(.+)?$", line)
	if len(matches) != 1:
		return None
	matches = matches[0]
	mm = int(matches[0])
	ss = int(matches[1])
	ms = int(matches[2])
	artist = matches[3][:-3].strip() # trim " - " at the end
	title = matches[4].strip()
	return (mm, ss, ms, artist, title)


def extract_hh_mm_ss_ms(line):
	matches = re.findall(r"^\[?(\d+):(\d+):(\d+)\.(\d+)\]?\s*([^-]+ - )?(.+)?$", line)
	if len(matches) != 1:
		return None
	matches = matches[0]
	mm = int(matches[0]) * 60 + int(matches[1])
	ss = int(matches[2])
	ms = int(matches[3])
	artist = matches[4][:-3].strip() # trim " - " at the end
	title = matches[5].strip()
	return (mm, ss, ms, artist, title)


line_extractors = [extract_hh_mm_ss_ms, extract_mm_ss_ms, extract_hh_mm_ss, extract_mm_ss]
