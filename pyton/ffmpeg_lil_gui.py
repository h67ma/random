import os
import threading
import subprocess
from tkinter import Tk, StringVar, IntVar, Text, filedialog, N, E, W, S, CENTER, LEFT, RIGHT, INSERT, WORD, END
from tkinter.ttk import Frame, LabelFrame, Label, Button, Checkbutton, Entry, Radiobutton, Scrollbar
from tkinterdnd2 import TkinterDnD, DND_FILES

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

root = TkinterDnD.Tk()
root.title("lil ffmpeg helper")

# data
in_txt = StringVar()
out_txt = StringVar()

def strip_mustache(string):
	if string[0] == "{" and string[-1] == "}":
		return string[1:-1]
	return string

def drop_in(event):
	in_txt.set(strip_mustache(event.data))

def drop_out(event):
	out_txt.set(strip_mustache(event.data))

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
f = Frame()

f.columnconfigure(0, pad=10)
f.columnconfigure(1, pad=10)
f.columnconfigure(2, pad=10)

f.rowconfigure(0, pad=10)
f.rowconfigure(1, pad=10)
f.rowconfigure(2, pad=10)
f.rowconfigure(3, pad=10)
f.rowconfigure(4, pad=10)
f.rowconfigure(5, pad=10)

# IO groupbox
in_out_frame = LabelFrame(f, text="IO")
in_out_frame.grid(row=0, columnspan=3, sticky=N+E+W+S)

inside_in_out = Frame(in_out_frame)

inside_in_out.columnconfigure(0, pad=10)
inside_in_out.columnconfigure(1, pad=10)
inside_in_out.columnconfigure(2, pad=10)

inside_in_out.rowconfigure(0, pad=10)
inside_in_out.rowconfigure(1, pad=10)
inside_in_out.rowconfigure(2, pad=10)

Label(inside_in_out, text="In:").grid(row=0, column=0, sticky=W)

in_lbl_f = Entry(inside_in_out, width=60, textvariable=in_txt)
in_lbl_f.drop_target_register(DND_FILES)
in_lbl_f.dnd_bind("<<Drop>>", drop_in)
in_lbl_f.grid(row=0, column=1, sticky=N+E+W+S)

select_in_btn = Button(inside_in_out, text="Select")
select_in_btn.grid(row=0, column=2, sticky=N+E+W+S)

Label(inside_in_out, text="Out:").grid(row=1, column=0, sticky=W)

out_lbl_f = Entry(inside_in_out, width=60, textvariable=out_txt)
out_lbl_f.drop_target_register(DND_FILES)
out_lbl_f.dnd_bind("<<Drop>>", drop_out)
out_lbl_f.grid(row=1, column=1, sticky=N+E+W+S)

select_out_btn = Button(inside_in_out, text="Select")
select_out_btn.grid(row=1, column=2, sticky=N+E+W+S)

Label(inside_in_out, text="Note: urls (blobs) also work").grid(row=2, column=0, columnspan=3, sticky=N+E+W+S)

inside_in_out.pack(expand=True, fill="both")

# trim image groupbox
trim_video_frame = LabelFrame(f, text="Trim image")
trim_video_frame.grid(row=1, column=0, sticky=N+E+W+S, padx=(0, 10))

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
trim_time_frame = LabelFrame(f, text="Trim time")
trim_time_frame.grid(row=1, column=1, columnspan=2, sticky=N+E+W+S)

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
output_video_frame = LabelFrame(f, text="Video output")
output_video_frame.grid(row=2, column=0, sticky=N+E+W+S, padx=(0, 10))

inside_video_output = Frame(output_video_frame)

Radiobutton(inside_video_output, text="Default", variable=video_output, value=0).pack(expand=True, fill="both")
Radiobutton(inside_video_output, text="Disabled", variable=video_output, value=1).pack(expand=True, fill="both")
Radiobutton(inside_video_output, text="Copy", variable=video_output, value=2).pack(expand=True, fill="both")

inside_video_output.pack()

# audio output
output_audio_frame = LabelFrame(f, text="Audio output")
output_audio_frame.grid(row=2, column=1, sticky=N+E+W+S, padx=(0, 10))

inside_audio_output = Frame(output_audio_frame)

Radiobutton(inside_audio_output, text="Default", variable=audio_output, value=0).pack(expand=True, fill="both")
Radiobutton(inside_audio_output, text="Disabled", variable=audio_output, value=1).pack(expand=True, fill="both")
Radiobutton(inside_audio_output, text="Copy", variable=audio_output, value=2).pack(expand=True, fill="both")

inside_audio_output.pack()

# extra options groupbox
output_options_frame = LabelFrame(f, text="Extra options")
output_options_frame.grid(row=2, column=2, sticky=N+E+W+S)

inside_output_options = Frame(output_options_frame)

gif_checkbox = Checkbutton(inside_output_options, text="gif", variable=gif)
gif_checkbox.pack(expand=True, fill="both")

strict2_checkbox = Checkbutton(inside_output_options, text="-strict -2", variable=strict2)
strict2_checkbox.pack(expand=True, fill="both")

inside_output_options.pack()

# commandline groupbox
status_frame = LabelFrame(f, text="Command line")
status_frame.grid(row=3, column=0, columnspan=3, sticky=N+E+W+S)

inside_status = Frame(status_frame)

command_box = Text(inside_status, wrap=WORD, height=6, width=60)
commandbox_scroll = Scrollbar(inside_status, orient="vertical", command=command_box.yview)
command_box.configure(yscrollcommand=commandbox_scroll.set)
commandbox_scroll.pack(side=RIGHT, expand=True, fill="both")
command_box.pack(side=LEFT, expand=True, fill="both")

inside_status.pack(expand=True, fill="both")

# run btn and open output checkbox
run_btn = Button(f, text="Run")
run_btn.grid(row=4, column=0, columnspan=2, sticky=N+E+W+S)

open_after_checkbox = Checkbutton(f, text="Open output after done", variable=open_after_done)
open_after_checkbox.grid(row=4, column=2)

# status lbl
status_lbl = Label(f, text="Rdy")
status_lbl.grid(row=5, column=0, columnspan=3, sticky=N+E+W+S)


f.pack(padx=10, pady=5)


def update_status(new_status):
	status_lbl.configure(text=new_status)


def set_command_text(new_text):
	command_box.delete("1.0", END)
	command_box.insert(INSERT, new_text)


def select_input_file():
	filename = filedialog.askopenfilename(title = "Select a file", filetypes = [("all files", "*.*")])
	if filename == "":
		update_status("Invalid file")
		return
	in_txt.set(value=filename)

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
	result = os.system(command)
	if result == 0:
		update_status("Success")
	else:
		update_status("ffmpeg finished with errors, check console")
	if open_after_done.get() == 1:
		subprocess.call("\"%s\"" % out_txt.get(), shell=True)


def update_command():
	# input filename, overwrite without asking
	command = "ffmpeg -i \"%s\" -y" % in_txt.get()

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

	if strict2.get() == 1:
		command += " -strict -2"

	# finally, output filename
	command += " \"%s\"" % out_txt.get()
	set_command_text(command)


def run():
	update_status("Running ffmpeg, pls wait...")
	command = command_box.get("1.0", END)
	threading.Thread(target=run_ffmpeg_thread, args=(command,)).start()


# callbacks
select_in_btn.configure(command=select_input_file)
select_out_btn.configure(command=select_output_file)

enable_video_trim.configure(command=update_command)
in_txt.trace("w", lambda *a: update_command())
out_txt.trace("w", lambda *a: update_command())

x_txt.trace("w", lambda *a: update_command())
y_txt.trace("w", lambda *a: update_command())
w_txt.trace("w", lambda *a: update_command())
h_txt.trace("w", lambda *a: update_command())

enable_time_trim.configure(command=update_command)
start_h.trace("w", lambda *a: update_command())
start_m.trace("w", lambda *a: update_command())
start_s.trace("w", lambda *a: update_command())
start_ms.trace("w", lambda *a: update_command())
end_h.trace("w", lambda *a: update_command())
end_m.trace("w", lambda *a: update_command())
end_s.trace("w", lambda *a: update_command())
end_ms.trace("w", lambda *a: update_command())

video_output.trace("w", lambda *a: update_command())
audio_output.trace("w", lambda *a: update_command())
gif_checkbox.configure(command=update_command)
strict2_checkbox.configure(command=update_command)

run_btn.configure(command=run)

Tk.report_callback_exception = lambda *args: update_status("invalid input") # cringe
root.resizable(0, 0) # prevent changing window size
root.mainloop()
