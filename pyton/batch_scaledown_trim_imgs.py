from PIL import Image
import argparse
import os

ACCEPTABLE_RESOLUTIONS = [
	(3840, 2160),
	(2560, 1440),
	(1920, 1080)
]

W_H = 16/9
H_W = 9/16

def best_trim(im):
	"""Returns resized image on success, None on error"""
	w = im.width
	h = im.height
	selected_res = None
	trim_box = None
	if w/h > W_H:
		# image is wider than it should be - we'll scale to the greatest acceptable height
		for res in ACCEPTABLE_RESOLUTIONS:
			if res[1] <= h:
				selected_res = res
				break
		if selected_res is None:
			return None

		in_ratio_w = W_H * h
		w_padding = (w - in_ratio_w)/2
		trim_box = (w_padding, 0, w - w_padding, h)
	else:
		# image is higher than it should be - we'll scale to the greatest acceptable width
		for res in ACCEPTABLE_RESOLUTIONS:
			if res[0] <= w:
				selected_res = res
				break
		if selected_res is None:
			return None

		in_ratio_h = H_W * w
		h_padding = (h - in_ratio_h)/2
		trim_box = (0, h_padding, w, h - h_padding)

	return im.resize(selected_res, box=trim_box)


parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", action="store", required=True, type=str, help=("Input dir"))
parser.add_argument("-o", "--output", action="store", required=True, type=str, help=("Output dir"))
parser.description = "Batch scale down images to the best predefined resolution and trim excess (centered). For best effect, ratios of the original images should be close to the desired ratio."
args = parser.parse_args()

os.makedirs(args.output, exist_ok=True)

for filename in os.listdir(args.input):
	path = os.path.join(args.input, filename)
	try:
		with Image.open(path) as im:
			print("Processing", filename)
			trimmed = best_trim(im)
			if trimmed is not None:
				trimmed.save(os.path.join(args.output, filename))
			else:
				print(filename, "is too smol")
	except:
		print("Skipping", filename)
