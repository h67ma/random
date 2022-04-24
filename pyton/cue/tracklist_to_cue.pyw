import os
from tkinter import StringVar, N, E, W, S, WORD, LEFT, RIGHT, Text, filedialog, END, INSERT
from tkinter.ttk import Frame, LabelFrame, Label, Entry, Scrollbar, Button
from tkinterdnd2 import TkinterDnD, DND_FILES
from cue_extractors import line_extractors


root = TkinterDnD.Tk()
root.title("tracklist to cue")

# data
in_track_name_txt = StringVar()


def update_status(new_status):
	status_lbl.configure(text=new_status)


def update_out_cue(new_text):
	out_cue_box.delete("1.0", END)
	out_cue_box.insert(INSERT, new_text)


def select_output_file():
	filename = filedialog.askopenfilename(title = "Select a file",
										filetypes = [("all files", "*.*")])
	if filename == "":
		update_status("Invalid file")
		return
	in_track_name_txt.set(value=filename)
	update_status("Rdy")


def strip_mustache(string):
	if string[0] == "{" and string[-1] == "}":
		return string[1:-1]
	return string


def drop_file(event):
	in_track_name_txt.set(strip_mustache(event.data))


def translate_to_cue():
	tracklist = in_tracklist_box.get("1.0", END).replace('\u200b', '').split('\n') # \u2000b appears when copying timestamp links from yt
	track_name = os.path.basename(in_track_name_txt.get())

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

		found = False
		for extractor in line_extractors:
			result = extractor(line)
			if result is not None:
				mm = result[0]
				ss = result[1]
				ms = result[2]
				artist = result[3]
				artist_line = "\n    PERFORMER " + artist if artist != "" else ""
				title = result[4]
				found = True
				break

		if not found:
			print("Can't find timestamp in track %d: %s" % (i, line))
			cue += "  TRACK %02d AUDIO\n    PERFORMER FIXME\n    TITLE FIXME\n    INDEX 01 00:00:00\n" % i
			errors += 1
			continue

		cue += "  TRACK %02d AUDIO%s\n    TITLE %s\n    INDEX 01 %02d:%02d:%02d\n" % (i, artist_line, title, mm, ss, ms)
	if errors > 0:
		update_status("Completed with %d errors (see console), pls fix cuesheet manually" % errors)
	else:
		update_status("All tracks parsed successfully")
	update_out_cue(cue)


def save():
	cue_filename = "".join(in_track_name_txt.get().split('.')[:-1]) + ".cue" # strip file extension, replace with cue
	if cue_filename == ".cue":
		update_status("Invalid file")
		return

	to_write = out_cue_box.get("1.0", END)

	with open(cue_filename, "w", encoding="utf-8-sig") as f_cue:
		f_cue.write(to_write)

	update_status("Saved to %s" % cue_filename)


# top layout
#f = Frame()
root.columnconfigure(0, pad=10, weight=1)
root.columnconfigure(1, pad=10, weight=1)

root.rowconfigure(0, pad=10)
root.rowconfigure(1, pad=10, weight=1)
root.rowconfigure(2, pad=10)

# track name groupbox
cue_filename_frame = LabelFrame(root, text="Track filename")
cue_filename_frame.columnconfigure(0, pad=10, weight=1)
cue_filename_frame.columnconfigure(1, pad=10)
cue_filename_frame.rowconfigure(0, pad=10)

out_cue_f = Entry(cue_filename_frame, textvariable=in_track_name_txt)
out_cue_f.drop_target_register(DND_FILES)
out_cue_f.dnd_bind("<<Drop>>", drop_file)
out_cue_f.grid(row=0, column=0, sticky=N+E+W+S, padx=5)

select_in_btn = Button(cue_filename_frame, text="Select")
select_in_btn.grid(row=0, column=1, sticky=N+E+W+S, padx=(0, 5))

cue_filename_frame.grid(row=0, column=0, columnspan=2, sticky=N+E+W+S, padx=5)

# in tracklist groupbox
tracklist_in_frame = LabelFrame(root, text="Tracklist")
tracklist_in_frame.columnconfigure(0, weight=1)
tracklist_in_frame.rowconfigure(0, weight=1)

in_tracklist_box = Text(tracklist_in_frame, wrap=WORD, height=50, width=60)
in_tracklist_box_scroll = Scrollbar(tracklist_in_frame, orient="vertical", command=in_tracklist_box.yview)
in_tracklist_box.configure(yscrollcommand=in_tracklist_box_scroll.set)
in_tracklist_box_scroll.grid(row=0, column=1, sticky=N+E+W+S, padx=(0, 5), pady=(0, 5))
in_tracklist_box.grid(row=0, column=0, sticky=N+E+W+S, padx=(5, 0), pady=(0, 5))
tracklist_in_frame.grid(row=1, column=0, sticky=N+E+W+S, padx=5)

# supported formats groupboxex
help_frame = Frame(root)

help_frame.columnconfigure(0, weight=1)
help_frame.columnconfigure(1, weight=1)
help_frame.columnconfigure(2, weight=1)

help_frame.rowconfigure(0, weight=1)

supported_formats_frame = LabelFrame(help_frame, text="Supported time formats")
Label(supported_formats_frame, text="[hh:mm:ss.ms]\n[hh:mm:ss]\n[mm:ss.ms]\n[mm:ss]").pack(expand=True, fill="both", padx=5, pady=(0, 5))
supported_formats_frame.grid(row=0, column=0, sticky=N+E+W+S, padx=5)

supported_formats_frame = LabelFrame(help_frame, text="Supported artist/title formats")
Label(supported_formats_frame, text="Title\nArtist - Title").pack(expand=True, fill="both", padx=5, pady=(0, 5))
supported_formats_frame.grid(row=0, column=1, sticky=N+E+W+S)

supported_formats_frame = LabelFrame(help_frame, text="Examples")
Label(supported_formats_frame, text="[12:34:56.78]Title\n[12:34:56] Artist - Title\n34:56 Title\n34:56.789 Title - Artist").pack(expand=True, fill="both", padx=5, pady=(0, 5))
supported_formats_frame.grid(row=0, column=2, sticky=N+E+W+S, padx=5)

help_frame.grid(row=2, column=0, sticky=N+E+W+S, pady=(0, 5))

# out cue groupbox
cue_out_frame = LabelFrame(root, text="cue tracklist")
cue_out_frame.columnconfigure(0, weight=1)
cue_out_frame.rowconfigure(0, weight=1)

out_cue_box = Text(cue_out_frame, wrap=WORD, height=50, width=60)
out_cue_box_scroll = Scrollbar(cue_out_frame, orient="vertical", command=out_cue_box.yview)
out_cue_box.configure(yscrollcommand=out_cue_box_scroll.set)
out_cue_box_scroll.grid(row=0, column=1, sticky=N+E+W+S, padx=(0, 5), pady=(0, 5))
out_cue_box.grid(row=0, column=0, sticky=N+E+W+S, padx=(5, 0), pady=(0, 5))
cue_out_frame.grid(row=1, column=1, sticky=N+E+W+S, padx=(0, 5))

btn_box = Frame(root)
btn_box.columnconfigure(0, pad=10, weight=1)
btn_box.columnconfigure(1, pad=10, weight=1)

btn_box.rowconfigure(0, pad=10)
btn_box.rowconfigure(0, pad=10)

translate_btn = Button(btn_box, text="Translate")
translate_btn.grid(row=0, column=0, sticky=N+E+W+S)

save_btn = Button(btn_box, text="Save")
save_btn.grid(row=0, column=1, sticky=N+E+W+S)

status_lbl = Label(btn_box, text="Rdy", wraplength=480)
status_lbl.grid(row=1, column=0, columnspan=2, sticky=N+E+W+S)

btn_box.grid(row=2, column=1, sticky=N+E+W+S, padx=(0, 5), pady=5)

# callbacks

select_in_btn.configure(command=select_output_file)
translate_btn.configure(command=translate_to_cue)
save_btn.configure(command=save)

root.mainloop()
