import sys
import re
from tkinter import StringVar, N, E, W, S, WORD, LEFT, RIGHT, Text, filedialog, END, INSERT
from tkinter.ttk import Frame, LabelFrame, Label, Entry, Scrollbar, Button
from tkinterdnd2 import TkinterDnD, DND_FILES
from cue_extractors import extract_hh_mm_ss_ms, extract_mm_ss_ms, extract_mm_ss, extract_hh_mm_ss, extract_title, extract_title_artist


root = TkinterDnD.Tk()
root.title("tracklist to cue")

# data
in_track_name_txt = StringVar()
out_cue_path_txt = StringVar()


def update_status(new_status):
	status_lbl.configure(text=new_status)


def update_out_cue(new_text):
	out_cue_box.delete("1.0", END)
	out_cue_box.insert(INSERT, new_text)


def select_output_file():
	filename = filedialog.asksaveasfilename(title = "Create a file",
											filetypes = [("all files", "*.*")])
	if filename == "":
		update_status("Invalid file")
		return
	out_cue_path_txt.set(value=filename)
	update_status("Rdy")


def strip_mustache(string):
	if string[0] == "{" and string[-1] == "}":
		return string[1:-1]
	return string


def drop_file(event):
	out_cue_path_txt.set(strip_mustache(event.data))


def translate_to_cue():
	time_extractors = [extract_mm_ss, extract_hh_mm_ss, extract_hh_mm_ss_ms, extract_mm_ss_ms]
	title_extractors = [extract_title_artist, extract_title]
	tracklist = in_tracklist_box.get("1.0", END).split('\n')
	track_name = in_track_name_txt.get()

	if tracklist == ['', '']:
		update_status("Empty tracklist")
		return

	if track_name == "":
		update_status("Empty track name")
		return

	cue = ""
	cue += "FILE \"%s\" WAVE\n" % track_name
	i = 0
	errors = 0
	for line in tracklist:
		line = line.strip()
		if line == "":
			continue
		i += 1

		time_found = False
		for extractor in time_extractors:
			result = extractor(line)
			if result is not None:
				mm = result[0]
				ss = result[1]
				ms = result[2]
				time_found = True
				break

		if not time_found:
			print("Can't find timestamp in track %d: %s" % (i, line))
			cue += "  TRACK %02d AUDIO\n    PERFORMER FIXME\n    TITLE FIXME\n    INDEX 01 00:00:00\n" % i
			errors += 1
			continue

		title_found = False
		for extractor in title_extractors:
			result = extractor(line)
			if result is not None:
				artist_line = result[0]
				title = result[1]
				title_found = True
				break

		if not title_found:
			print("Can't find track %d info: %s" % (i, line))
			cue += "  TRACK %02d AUDIO\n    PERFORMER FIXME\n    TITLE FIXME\n    INDEX 01 %02d:%02d:%02d\n" % (i, mm, ss, ms)
			errors += 1
			continue

		cue += "  TRACK %02d AUDIO%s\n    TITLE %s\n    INDEX 01 %02d:%02d:%02d\n" % (i, artist_line, title, mm, ss, ms)
	if errors > 0:
		update_status("Completed with %d errors (see console), pls fix cuesheet manually" % errors)
	else:
		update_status("All tracks parsed successfully")
	update_out_cue(cue)


def save():
	cue_filename = out_cue_path_txt.get()
	if cue_filename == "":
		update_status("Invalid file")
		return

	to_write = out_cue_box.get("1.0", END)

	with open(cue_filename, "w") as f_cue:
		f_cue.write(to_write)

	update_status("Saved to %s" % cue_filename)


# top layout
f = Frame()

f.columnconfigure(0, pad=10)
f.columnconfigure(1, pad=10)

# in

in_frame = LabelFrame(f, text="Input")

# track name groupbox
relative_track_in_frame = LabelFrame(in_frame, text="Relative track filename")
in_track_name = Entry(relative_track_in_frame, width=80, textvariable=in_track_name_txt)
in_track_name.pack(fill="both", padx=5, pady=5)
relative_track_in_frame.pack(fill="both", padx=5)

# in tracklist groupbox
tracklist_in_frame = LabelFrame(in_frame, text="Tracklist")

in_tracklist_box = Text(tracklist_in_frame, wrap=WORD, height=50, width=60)
in_tracklist_box_scroll = Scrollbar(tracklist_in_frame, orient="vertical", command=in_tracklist_box.yview)
in_tracklist_box.configure(yscrollcommand=in_tracklist_box_scroll.set)
in_tracklist_box_scroll.pack(side=RIGHT, expand=True, fill="both", padx=(0, 5), pady=5)
in_tracklist_box.pack(side=LEFT, expand=True, fill="both", padx=(5, 0), pady=5)
tracklist_in_frame.pack(fill="both", padx=5)

# supported formats groupbox
supported_formats_frame = LabelFrame(in_frame, text="Supported formats")
Label(supported_formats_frame, text="[mm:ss.ms]Artist - Title\n[mm:ss.ms]Title\n[hh:mm:ss.ms]Artist - Title\n[hh:mm:ss.ms]Title").pack(expand=True, fill="both", padx=5, pady=(0, 5))
supported_formats_frame.pack(expand=True, fill="both", padx=5, pady=(0, 5))

in_frame.grid(row=0, column=0, sticky=N+E+W+S, padx=(0, 10))

# out

out_frame = LabelFrame(f, text="Output")

# output cue filename groupbox
cue_filename_frame = LabelFrame(out_frame, text="cue output path")

out_cue_f = Entry(cue_filename_frame, width=67, textvariable=out_cue_path_txt)
out_cue_f.drop_target_register(DND_FILES)
out_cue_f.dnd_bind("<<Drop>>", drop_file)
out_cue_f.grid(row=0, column=0, padx=5, pady=5)

select_in_btn = Button(cue_filename_frame, text="Select")
select_in_btn.grid(row=0, column=1)

cue_filename_frame.pack(expand=False, fill="both", padx=5)

# out cue groupbox
cue_out_frame = LabelFrame(out_frame, text="cue tracklist")

out_cue_box = Text(cue_out_frame, wrap=WORD, height=50, width=60)
out_cue_box_scroll = Scrollbar(cue_out_frame, orient="vertical", command=out_cue_box.yview)
out_cue_box.configure(yscrollcommand=out_cue_box_scroll.set)
out_cue_box_scroll.pack(side=RIGHT, expand=True, fill="both", padx=(0, 5), pady=5)
out_cue_box.pack(side=LEFT, expand=True, fill="both", padx=(5, 0), pady=5)
cue_out_frame.pack(expand=False, fill="both", padx=5)

translate_btn = Button(out_frame, text="Translate")
translate_btn.pack(expand=True, fill="both", pady=(5, 0), padx=5)

save_btn = Button(out_frame, text="Save")
save_btn.pack(expand=True, fill="both", pady=(5, 0), padx=5)

status_lbl = Label(out_frame, text="Rdy")
status_lbl.pack(expand=False, fill="both", pady=5, padx=5)

out_frame.grid(row=0, column=1, sticky=N+E+W+S)

f.pack(padx=5, pady=5)

# callbacks

select_in_btn.configure(command=select_output_file)
translate_btn.configure(command=translate_to_cue)
save_btn.configure(command=save)


root.resizable(0, 0) # prevent changing window size
root.mainloop()
