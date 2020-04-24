from PIL import Image
import sys
import json

def crop(base_dir, in_filename):
	with open("%s\\%s.json" % (base_dir, in_filename), "r", encoding="utf-8-sig") as f:
		# use json from Adobe Animate
		symbols = json.load(f)
		with Image.open("%s\\%s.png" % (base_dir, in_filename)) as orig_image:
			for symbol, symbol_data in symbols["frames"].items():
				x = symbol_data["frame"]["x"]
				y = symbol_data["frame"]["y"]
				w = symbol_data["frame"]["w"]
				h = symbol_data["frame"]["h"]

				if w > 0 and h > 0:
					try:
						cropped = orig_image.crop((x, y, x + w, y + h))
						cropped.save("%s\\trim\\%s.png" % (base_dir, symbol))
					except SystemError:
						print("region outside image - x=%d y=%d x+w=%d y+h=%d" % (x, y, x + w, y + h))
				else:
					print("skipping image with w=0 or h=0 - " + symbol)

if len(sys.argv) < 3:
	print("too few arguments")
	exit()

crop(sys.argv[1], sys.argv[2])
