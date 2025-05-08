import argparse


# note that a single xstack filter could also be used instead, but it would be more messy
parser = argparse.ArgumentParser(description="A primitive tool for generating complex filter in the shape of a grid, just like the tile filter but with multiple inputs")
parser.add_argument("-x", "--width", action="store", required=True, type=int, help=("Grid width"))
parser.add_argument("-y", "--height", action="store", required=True, type=int, help=("Grid height"))
args = parser.parse_args()

filter = ""
for y in range(args.height):
	for x in range(args.width):
		stream_id = (y * args.width) + x
		filter += "[0:v:%d]" % stream_id
	filter += "hstack=inputs=%d[r%d];" % (args.width, y)

for y in range(args.height):
	filter += "[r%d]" % y
filter += "vstack=inputs=%d[out]" % args.height

print(filter)
