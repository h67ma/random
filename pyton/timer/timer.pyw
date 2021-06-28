from threading import Thread, Event
from pystray import MenuItem, Icon, Menu
from PIL import Image, ImageDraw
from datetime import datetime


# add some tabs at the end in case it doesn't line up in status
TIMERS_DATA = [
	(5*60, "Look away"),
	(3*60*60, "Stand up")
]


def seconds_to_hh_mm_ss(seconds: int) -> str:
	out_h = int(seconds / 3600)
	out_m = int((seconds % 3600) / 60)
	out_s = int(seconds % 60)
	return "%d:%02d:%02d" % (out_h, out_m, out_s)


class PerpetualTimer(Thread):
	def __init__(self, duration: int, func, name: str):
		Thread.__init__(self)
		self.stopped = Event()
		self.duration = duration
		self.func = func
		self.name = name # sorry, you just get a single arg
		self.start_time = datetime.now()

	def run(self):
		while not self.stopped.wait(self.duration):
			self.func(self.name)
			self.start_time = datetime.now()

	def cancel(self):
		self.stopped.set()

	def get_remaining_seconds(self) -> int:
		return self.duration - (datetime.now() - self.start_time).seconds


timers = []

def timers_status():
	status_str = ""
	for timer in timers:
		status_str += "%s:\t%s\n" % (timer.name, seconds_to_hh_mm_ss(timer.get_remaining_seconds()))
	icon.notify(status_str, title="Upcoming timers")


def quit_window():
	for timer in timers:
		timer.cancel()
	icon.stop()


#image = Image.open("eyeball.png")

image = Image.new("RGB", (16, 16), color = "black")
draw = ImageDraw.Draw(image)
draw.line([(7, 1), (7, 14)], width=4, fill="green")
draw.line([(1, 2), (14, 2)], width=4, fill="green")

menu = Menu(
	MenuItem("Timers status", timers_status, default=True),
	MenuItem("Quit", quit_window)
)

icon = Icon("Simple Timer", image, "Simple Timer", menu)

for timer_data in TIMERS_DATA:
	timer = PerpetualTimer(timer_data[0], icon.notify, timer_data[1])
	timers.append(timer)
	timer.start()

icon.run()
