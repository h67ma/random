from PIL import Image
import argparse
from enum import Enum
import os
import shutil


def apply_alpha_to_img(out_comb_dir, in_mask_dir, in_opaque_dir):
	if not os.path.isdir(in_mask_dir):
		print("Input dir invalid (mask)")
		return

	if not os.path.isdir(in_opaque_dir):
		print("Input dir invalid (opaque)")
		return

	os.makedirs(out_comb_dir, exist_ok=True)

	for in_opaque_name in os.listdir(in_opaque_dir):
		in_opaque_path = os.path.join(in_opaque_dir, in_opaque_name)
		if not os.path.isfile(in_opaque_path):
			continue

		print("Processing", in_opaque_path)

		out_comb_path = os.path.join(out_comb_dir, in_opaque_name)
		if os.path.isfile(out_comb_path):
			print("Output image already exists, not overwriting")
			continue

		in_mask_path = os.path.join(in_mask_dir, in_opaque_name)
		if not os.path.isfile(in_mask_path):
			print("Mask image missing, only copying to combdir")
			shutil.copy(in_opaque_path, out_comb_path)
			continue

		in_opaque_img = Image.open(in_opaque_path, "r")
		in_mask_img = Image.open(in_mask_path, "r")

		if in_opaque_img.size != in_mask_img.size:
			print("Opaque and mask have different dimensions, skipping")
			continue

		if in_mask_img.mode != "L":
			# convert to grayscale
			in_mask_img = in_mask_img.convert("L")

		in_opaque_img.putalpha(in_mask_img)
		in_opaque_img.save(out_comb_path)


def extract_alpha_layer(in_comb_dir, out_mask_dir, out_opaque_dir):
	if not os.path.isdir(in_comb_dir):
		print("Input dir invalid (combined)")
		return

	os.makedirs(out_mask_dir, exist_ok=True)
	os.makedirs(out_opaque_dir, exist_ok=True)

	for in_comb_name in os.listdir(in_comb_dir):
		in_comb_path = os.path.join(in_comb_dir, in_comb_name)

		if not os.path.isfile(in_comb_path):
			continue

		print("Processing", in_comb_path)

		out_mask_path = os.path.join(out_mask_dir, in_comb_name)
		out_opaque_path = os.path.join(out_opaque_dir, in_comb_name)

		if os.path.isfile(out_mask_path) or os.path.isfile(out_opaque_path):
			print("Output image(s) already exists, not overwriting")
			continue

		in_comb_img = Image.open(in_comb_path, "r")

		if in_comb_img.mode != "RGBA":
			print("Not a transparent image, only copying to opaquedir")
			shutil.copy(in_comb_path, out_opaque_path)
			continue

		# save alpha channel
		out_mask_img = in_comb_img.getchannel("A")
		out_mask_img.save(out_mask_path)

		out_opaque_img = Image.new("RGB", in_comb_img.size, (0, 0, 0)) # black background
		out_opaque_img.paste(in_comb_img, (0, 0), in_comb_img)
		out_opaque_img.save(out_opaque_path)


# TODO? possible improvements:
# * selectable background color for opaque imgs
# * overwrite existing files flag
if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Batch extract alpha masks and opaque images from images with transparency. Images without alpha channel present will be only copied to opaquedir.")
	parser.add_argument("-c", "--combdir", action="store", required=True, type=str, help=("Original/combined images dir"))
	parser.add_argument("-m", "--maskdir", action="store", required=True, type=str, help=("Mask images dir"))
	parser.add_argument("-o", "--opaquedir", action="store", required=True, type=str, help=("Opaque images dir"))
	parser.add_argument("-r", "--reverse", action="store_true", help=("Instead of splitting, combine masks and opaque images into transparent ones. Images without a matching image with the same dimensions and name in maskdir will only be copied to combdir. All directories switch their direction (input/output)"))
	args = parser.parse_args()

	if args.reverse:
		apply_alpha_to_img(args.combdir, args.maskdir, args.opaquedir)
	else:
		extract_alpha_layer(args.combdir, args.maskdir, args.opaquedir)
