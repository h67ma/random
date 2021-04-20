import os
import threading
import subprocess
import sys
from tkinter import Tk, StringVar, IntVar, filedialog, N, E, W, S, CENTER, INSERT, WORD, END, DISABLED, NORMAL
from tkinter.ttk import Frame, LabelFrame, Label, Button, Checkbutton, Entry, Radiobutton
from tkinterdnd2 import TkinterDnD, DND_FILES
from tkinter.scrolledtext import ScrolledText
from functools import partial

if len(sys.argv) < 2:
	print("arg1 = path to default dir")
	exit()

default_dir = sys.argv[1]

def float_get_after_decimal(val):
	return int(str(val - int(val))[2:]) # this is so bad, but it works

def hmsms_to_sms(h, m, s, ms):
	ms = float("0.%s" % str(ms)) # again, this is soo bad
	return ms + s + m*60 + h*3600

def sms_to_hmsms(s):
	out_h = int(s / 3600)
	out_m = int((s % 3600) / 60)
	out_s = int(s % 60)
	return out_h, out_m, out_s


def strip_mustache(string):
	if string[0] == "{" and string[-1] == "}":
		return string[1:-1]
	return string


def drop_in1(event):
	in_txt1.set(strip_mustache(event.data))


def drop_in2(event):
	in_txt2.set(strip_mustache(event.data))


def drop_out(event):
	out_txt.set(strip_mustache(event.data))


root = TkinterDnD.Tk()
root.title("lil ffmpeg helper")

# data
in_txt1 = StringVar()
in_txt2 = StringVar()
out_txt = StringVar()

trim_video = IntVar(value=0)
x_txt = IntVar(value=0)
y_txt = IntVar(value=0)
w_txt = IntVar(value=0)
h_txt = IntVar(value=0)

trim_time = IntVar(value=0)
start_h = IntVar(value=0)
start_m = IntVar(value=0)
start_s = IntVar(value=0)
start_ms = IntVar(value=0)
end_h = IntVar(value=0)
end_m = IntVar(value=0)
end_s = IntVar(value=0)
end_ms = IntVar(value=0)

video_output = IntVar(value=0)
audio_output = IntVar(value=0)
gif = IntVar(value=0)
strict2 = IntVar(value=0)
open_after_done = IntVar(value=1)

command = ""

# top layout
root.columnconfigure(0, pad=10)
root.columnconfigure(1, pad=10)
root.columnconfigure(2, pad=10)
root.columnconfigure(3, pad=10, weight=1)

root.rowconfigure(0, pad=10)
root.rowconfigure(1, pad=10)
root.rowconfigure(2, pad=10)
root.rowconfigure(3, pad=10, weight=1)
root.rowconfigure(4, pad=10)

# IO groupbox
in_out_frame = LabelFrame(root, text="IO")

in_out_frame.columnconfigure(0, pad=10)
in_out_frame.columnconfigure(1, pad=10, weight=1)
in_out_frame.columnconfigure(2, pad=10)

in_out_frame.rowconfigure(0, pad=10)
in_out_frame.rowconfigure(1, pad=10)
in_out_frame.rowconfigure(2, pad=10)
in_out_frame.rowconfigure(3, pad=10)

Label(in_out_frame, text="In 1:").grid(row=0, column=0, sticky=W)

in_lbl_f1 = Entry(in_out_frame, width=60, textvariable=in_txt1)
in_lbl_f1.drop_target_register(DND_FILES)
in_lbl_f1.dnd_bind("<<Drop>>", drop_in1)
in_lbl_f1.grid(row=0, column=1, sticky=N+E+W+S)

select_in_btn1 = Button(in_out_frame, text="Select")
select_in_btn1.grid(row=0, column=2, sticky=N+E+W+S, padx=3)

Label(in_out_frame, text="In 2:").grid(row=1, column=0, sticky=W)

in_lbl_f2 = Entry(in_out_frame, width=60, textvariable=in_txt2)
in_lbl_f2.drop_target_register(DND_FILES)
in_lbl_f2.dnd_bind("<<Drop>>", drop_in2)
in_lbl_f2.grid(row=1, column=1, sticky=N+E+W+S)

select_in_btn2 = Button(in_out_frame, text="Select")
select_in_btn2.grid(row=1, column=2, sticky=N+E+W+S, padx=3)

Label(in_out_frame, text="Out:").grid(row=2, column=0, sticky=W)

out_lbl_f = Entry(in_out_frame, width=60, textvariable=out_txt)
out_lbl_f.drop_target_register(DND_FILES)
out_lbl_f.dnd_bind("<<Drop>>", drop_out)
out_lbl_f.grid(row=2, column=1, sticky=N+E+W+S)

select_out_btn = Button(in_out_frame, text="Select")
select_out_btn.grid(row=2, column=2, sticky=N+E+W+S, padx=3)

Label(in_out_frame, text="Default output dir: " + default_dir).grid(row=3, column=0, columnspan=3, sticky=N+E+W+S)

in_out_frame.grid(row=0, column=0, columnspan=4, sticky=N+E+W+S, padx=5)

# trim image groupbox
trim_video_frame = LabelFrame(root, text="Trim image")
trim_video_frame.grid(row=1, column=0, sticky=N+E+W+S, padx=5)

inside_trim_video = Frame(trim_video_frame)

inside_trim_video.columnconfigure(0, pad=10)
inside_trim_video.columnconfigure(1, pad=10)
inside_trim_video.columnconfigure(2, pad=10)
inside_trim_video.columnconfigure(3, pad=10)

inside_trim_video.rowconfigure(0, pad=10)
inside_trim_video.rowconfigure(1, pad=10)
inside_trim_video.rowconfigure(2, pad=10)

enable_video_trim = Checkbutton(inside_trim_video, text="Enable", variable=trim_video)
enable_video_trim.grid(row=0, columnspan=4)

Label(inside_trim_video, text="x").grid(row=1, column=0)
Entry(inside_trim_video, textvariable=x_txt, width=6, justify=CENTER).grid(row=1, column=1, sticky=N+E+W+S)

Label(inside_trim_video, text="y").grid(row=1, column=2)
Entry(inside_trim_video, textvariable=y_txt, width=6, justify=CENTER).grid(row=1, column=3, sticky=N+E+W+S)

Label(inside_trim_video, text="w").grid(row=2, column=0)
Entry(inside_trim_video, textvariable=w_txt, width=6, justify=CENTER).grid(row=2, column=1, sticky=N+E+W+S)

Label(inside_trim_video, text="h").grid(row=2, column=2)
Entry(inside_trim_video, textvariable=h_txt, width=6, justify=CENTER).grid(row=2, column=3, sticky=N+E+W+S)

inside_trim_video.pack()

# trim time groupbox
trim_time_frame = LabelFrame(root, text="Trim time")
trim_time_frame.grid(row=1, column=1, columnspan=2, sticky=N+E+W+S, padx=(0, 5))

inside_trim_time = Frame(trim_time_frame)

inside_trim_time.columnconfigure(0, pad=10)
inside_trim_time.columnconfigure(1, pad=10)
inside_trim_time.columnconfigure(2, pad=10)
inside_trim_time.columnconfigure(3, pad=10)
inside_trim_time.columnconfigure(4, pad=10)
inside_trim_time.columnconfigure(5, pad=10)
inside_trim_time.columnconfigure(6, pad=10)
inside_trim_time.columnconfigure(7, pad=10)

inside_trim_time.rowconfigure(0, pad=10)
inside_trim_time.rowconfigure(1, pad=10)
inside_trim_time.rowconfigure(2, pad=10)
inside_trim_time.rowconfigure(3, pad=10)

enable_time_trim = Checkbutton(inside_trim_time, text="Enable", variable=trim_time)
enable_time_trim.grid(row=0, columnspan=8)

Label(inside_trim_time, text="h").grid(row=1, column=1)
Label(inside_trim_time, text="m").grid(row=1, column=3)
Label(inside_trim_time, text="s").grid(row=1, column=5)
Label(inside_trim_time, text="ms").grid(row=1, column=7)

Label(inside_trim_time, text="Start").grid(row=2, column=0, sticky=W)
Entry(inside_trim_time, textvariable=start_h, width=3, justify=CENTER).grid(row=2, column=1, sticky=N+E+W+S)
Label(inside_trim_time, text=":").grid(row=2, column=2)
Entry(inside_trim_time, textvariable=start_m, width=3, justify=CENTER).grid(row=2, column=3, sticky=N+E+W+S)
Label(inside_trim_time, text=":").grid(row=2, column=4)
Entry(inside_trim_time, textvariable=start_s, width=3, justify=CENTER).grid(row=2, column=5, sticky=N+E+W+S)
Label(inside_trim_time, text=".").grid(row=2, column=6)
Entry(inside_trim_time, textvariable=start_ms, width=6, justify=CENTER).grid(row=2, column=7, sticky=N+E+W+S)

Label(inside_trim_time, text="End").grid(row=3, column=0, sticky=W)
Entry(inside_trim_time, textvariable=end_h, width=3, justify=CENTER).grid(row=3, column=1, sticky=N+E+W+S)
Label(inside_trim_time, text=":").grid(row=3, column=2)
Entry(inside_trim_time, textvariable=end_m, width=3, justify=CENTER).grid(row=3, column=3, sticky=N+E+W+S)
Label(inside_trim_time, text=":").grid(row=3, column=4)
Entry(inside_trim_time, textvariable=end_s, width=3, justify=CENTER).grid(row=3, column=5, sticky=N+E+W+S)
Label(inside_trim_time, text=".").grid(row=3, column=6)
Entry(inside_trim_time, textvariable=end_ms, width=6, justify=CENTER).grid(row=3, column=7, sticky=N+E+W+S)

inside_trim_time.pack()

# video output
output_video_frame = LabelFrame(root, text="Video output")
output_video_frame.grid(row=2, column=0, sticky=N+E+W+S, padx=5)

inside_video_output = Frame(output_video_frame)

Radiobutton(inside_video_output, text="Default", variable=video_output, value=0).pack(expand=True, fill="both")
Radiobutton(inside_video_output, text="Disabled", variable=video_output, value=1).pack(expand=True, fill="both")
Radiobutton(inside_video_output, text="Copy", variable=video_output, value=2).pack(expand=True, fill="both")

inside_video_output.pack()

# audio output
output_audio_frame = LabelFrame(root, text="Audio output")
output_audio_frame.grid(row=2, column=1, sticky=N+E+W+S, padx=(0, 5))

inside_audio_output = Frame(output_audio_frame)

Radiobutton(inside_audio_output, text="Default", variable=audio_output, value=0).pack(expand=True, fill="both")
Radiobutton(inside_audio_output, text="Disabled", variable=audio_output, value=1).pack(expand=True, fill="both")
Radiobutton(inside_audio_output, text="Copy", variable=audio_output, value=2).pack(expand=True, fill="both")

inside_audio_output.pack()

# extra options groupbox
output_options_frame = LabelFrame(root, text="Extra options")
output_options_frame.grid(row=2, column=2, sticky=N+E+W+S, padx=(0, 5))

inside_output_options = Frame(output_options_frame)

gif_checkbox = Checkbutton(inside_output_options, text="gif", variable=gif)
gif_checkbox.pack(expand=True, fill="both")

strict2_checkbox = Checkbutton(inside_output_options, text="-strict -2", variable=strict2)
strict2_checkbox.pack(expand=True, fill="both")

inside_output_options.pack()

# commandline groupbox
status_frame = LabelFrame(root, text="Command line")

command_box = ScrolledText(status_frame, wrap=WORD, height=10, width=60)
command_box.pack(expand=True, fill="both", padx=5, pady=5)

status_frame.grid(row=3, column=0, columnspan=3, sticky=N+E+W+S, padx=5)

# run btn and open output checkbox
run_btn = Button(root, text="Run")
run_btn.grid(row=4, column=0, columnspan=2, sticky=N+E+W+S, padx=5, pady=(0, 5))

open_after_checkbox = Checkbutton(root, text="Open output after done", variable=open_after_done)
open_after_checkbox.grid(row=4, column=2, padx=(0, 5), pady=(0, 5))

# log groupbox
log_frame = LabelFrame(root, text="Log")

log_box = ScrolledText(log_frame, state=DISABLED, wrap=WORD, width=80)
log_box.pack(expand=True, fill="both", padx=5, pady=5)

log_frame.grid(row=1, column=3, rowspan=4, sticky=N+E+W+S, padx=5, pady=(0, 5))


def update_status(new_status):
	append_log_text("> %s\n" % new_status)


def set_command_text(new_text):
	command_box.delete("1.0", END)
	command_box.insert(INSERT, new_text)


def append_log_text(new_line):
	log_box.configure(state=NORMAL) # cringe
	log_box.insert(END, new_line)
	log_box.configure(state=DISABLED) # cringe 2
	log_box.yview(END) # scroll to bottom


def select_input_file(in_txt_control):
	filename = filedialog.askopenfilename(title = "Select a file", filetypes = [("all files", "*.*")])
	if filename == "":
		update_status("Invalid file")
		return
	in_txt_control.set(value=filename)

	update_status("Autodetecting input properties...")
	vid_data = os.popen("ffprobe -v error -select_streams v:0 -show_entries stream=width,height,duration -of csv=s=,:p=0 \"%s\"" % filename)
	vid_data = vid_data.read().split(',')
	w_txt.set(vid_data[0])
	h_txt.set(vid_data[1])
	duration_s = float(vid_data[2])
	duration_ms = float_get_after_decimal(duration_s)
	duration_h, duration_m, duration_s = sms_to_hmsms(duration_s)

	end_h.set(duration_h)
	end_m.set(duration_m)
	end_s.set(duration_s)
	end_ms.set(duration_ms)
	update_command()
	update_status("Rdy")


def select_output_file():
	filename = filedialog.asksaveasfilename(title = "Create a file",
											filetypes = [("all files", "*.*")])
	if filename == "":
		update_status("Invalid file")
		return
	out_txt.set(value=filename)
	update_command()
	update_status("Rdy")


def run_ffmpeg_thread(command):
	try:
		p = subprocess.Popen(command, stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
	except FileNotFoundError as ex:
		append_log_text(ex)
		append_log_text('\n')
		update_status("Error running ffmpeg, check commandline")
		return

	while True:
		retcode = p.poll() # returns None while subprocess is running

		outs, errs = p.communicate()

		append_log_text(outs)
		append_log_text(errs)

		if retcode is not None:
			break

	if retcode == 0:
		update_status("Success")
		if open_after_done.get() == 1:
			retcode = subprocess.call("\"%s\"" % get_output_filename(), shell=True)
			if retcode != 0:
				update_status("Can't open output")
	else:
		update_status("ffmpeg finished with errors")


def update_command():
	command = "ffmpeg" # it's a start

	# input file(s)
	in_filename1 = in_txt1.get()
	in_filename2 = in_txt2.get()

	if in_filename1 != "":
		command += " -i \"%s\"" % in_filename1

	if in_filename2 != "":
		command += " -i \"%s\"" % in_filename2

	# overwrite without asking
	command += " -y"

	# trim image
	if trim_video.get() == 1:
		command += " -filter:v crop=%s:%s:%s:%s" % (w_txt.get(), h_txt.get(), x_txt.get(), y_txt.get())

	# trim time
	if trim_time.get() == 1:
		start_only_sms = hmsms_to_sms(start_h.get(), start_m.get(), start_s.get(), start_ms.get())
		end_only_sms = hmsms_to_sms(end_h.get(), end_m.get(), end_s.get(), end_ms.get())
		tt_only_sms = end_only_sms - start_only_sms
		start_ms.get()
		command += " -ss %f -t %f" % (start_only_sms, tt_only_sms)

	# video output
	if video_output.get() == 1:
		command += " -vn"
	elif video_output.get() == 2:
		command += " -vcodec copy"

	# audio output
	if audio_output.get() == 1:
		command += " -an"
	elif audio_output.get() == 2:
		command += " -acodec copy"

	# jiff
	if gif.get() == 1:
		command += " -gifflags +transdiff"

	# some random flag that fixes random problems
	if strict2.get() == 1:
		command += " -strict -2"

	# finally, output filename
	command += " \"%s\"" % get_output_filename()

	set_command_text(command)


def get_output_filename():
	target_file = out_txt.get()

	if "/" not in target_file and "\\" not in target_file:
		# only filename - append default dir
		target_file = os.path.join(default_dir, target_file)

	return target_file


def run():
	update_status("Running ffmpeg, pls wait...")
	command = command_box.get("1.0", END)
	threading.Thread(target=run_ffmpeg_thread, args=(command,)).start()


# callbacks

select_in_btn1.configure(command=partial(select_input_file, in_txt1))
select_in_btn2.configure(command=partial(select_input_file, in_txt2))
select_out_btn.configure(command=select_output_file)

update_command_on_change_controls = [
	enable_video_trim,
	enable_time_trim,
	gif_checkbox,
	strict2_checkbox
]

for control in update_command_on_change_controls:
	control.configure(command=update_command)

update_command_on_text_change_controls = [
	in_txt1,
	in_txt2,
	out_txt,
	x_txt,
	y_txt,
	w_txt,
	h_txt,
	start_h,
	start_m,
	start_s,
	start_ms,
	end_h,
	end_m,
	end_s,
	end_ms,
	video_output,
	audio_output
]

for control in update_command_on_text_change_controls:
	control.trace("w", lambda *a: update_command())

run_btn.configure(command=run)

Tk.report_callback_exception = lambda *args: update_status("invalid input") # cringe

set_command_text("ffmpeg")

# run
root.mainloop()
