import os
import re
import sys
import glob
import subprocess
import shutil

def docx_to_md(pandoc_bin, media_dir, in_file, out_file):
	subprocess.call([pandoc_bin, in_file, "--from", "docx", "--to", "gfm+pipe_tables+lists_without_preceding_blankline+task_lists", \
		"--extract-media=" + media_dir, "--wrap=none", "--preserve-tabs", "--atx-headers", "-o", out_file])

def process_and_split_md(base_dir, in_md):
	with open(in_md, "r", encoding="utf-8") as file:
		in_content = file.read()

		# page name, date, time
		meta = re.findall(r"([^\n]+)\n\n(\d{2} [a-zA-Z]+ \d{4})\n\n(\d{2}:\d{2})", in_content)

		# page content
		pages = re.split(r"[^\n]+\n\n\d{2} [a-zA-Z]+ \d{4}\n\n\d{2}:\d{2}\n\n", in_content)
		del pages[0] # empty match, because nothing before first title

		if len(meta) != len(pages):
			print("a horrible chill goes down your spine... len(meta) = %d, len(pages) = %d" % (len(meta), len(pages)))
		else:
			for i in range(len(meta)):
				nice_filename = "%s/%s.md" % (base_dir, re.sub(r"[^a-zA-Z0-9_\- ]", "", meta[i][0]).lower())

				# fix weird bullet lists
				# remove newlines before bullet list items (levels 1, 2, 3)
				# remove nbsp bs at the end of each section and nbsp in general
				nice_content = pages[i] \
                    .replace("  - > ", "* ") \
                    .replace("    ", "\t") \
					.replace("\n* ", "* ") \
					.replace("\t\n\t* ", "\t* ") \
					.replace("\t\t\n\t\t* ", "\t\t* ") \
					.replace("\n\n\u00A0\n\n\u00A0", "") \
					.replace("\u00A0", "")

				# fix image paths (add slash at the beginning)
				nice_content = re.sub(r"!\[([^\]]*)\]\((media\/[^\)]+)\)", r"![\1](/\2)", nice_content)

				with open(nice_filename, "w", encoding="utf-8") as file:
					# add title and creation time at the top
					file.write("# %s\n\nCreated %s %s\n- - -\n%s" % (meta[i][0], meta[i][1], meta[i][2], nice_content))

if len(sys.argv) < 3:
	print("too few arguments")
	print("arg1 = path to pandoc binary")
	print("arg2 = path to dir containing dirs (notebooks) with .docx files (sections)")
	exit()

pandoc_bin = sys.argv[1]
root_path = sys.argv[2]
tmp_md = root_path + "/tmp.md"

for notebook in os.listdir(root_path):
	if os.path.isdir("%s/%s" % (root_path, notebook)):
		for section_docx in glob.glob("%s/%s/*.docx" % (root_path, notebook)):
			section_dirname = section_docx[:-5]
			section_name = re.split(r"[\\/]", section_dirname)[-1]
			os.mkdir(section_dirname)
			docx_to_md(pandoc_bin, "media/" + section_name, section_docx, tmp_md)
			process_and_split_md(section_dirname, tmp_md)

os.remove(tmp_md)

# move the media dir to target dir
shutil.move("media", root_path + "/media")
