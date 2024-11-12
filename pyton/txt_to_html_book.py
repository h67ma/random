import os
import argparse
from pathlib import Path
from html import escape


def txt_to_basic_html(in_filename: str, out_filename: str, title: str, no_separators: bool):
	with open(in_filename, "r") as in_f, open(out_filename, "w") as out_f:
		out_f.write("<html>\n")

		if title is not None:
			out_f.write("<head>\n<title>%s</title>\n</head>\n" % title)

		out_f.write("<body>\n")

		sep = False
		for line in in_f:
			line = line.strip()
			
			if line == "":
				if not no_separators and not sep:
					out_f.write("<hr/>\n")
					sep = True
				continue

			sep = False
			out_f.write("<p>%s</p>\n" % escape(line))

		out_f.write("</body>\n</html>\n")


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Transform unformatted txt file to a basic html page with each line as a paragraph. Useful for ebook readers.")
	parser.add_argument("-i", "--input", action="store", required=True, type=str, help=("Input file"))
	parser.add_argument("-o", "--output", action="store", type=str, help=("Output file"))
	parser.add_argument("-t", "--title", action="store", type=str, help=("Title"))
	parser.add_argument("--nosep", action="store_true", help=("Do not insert <hr/> in place of multiple newlines"))
	args = parser.parse_args()

	if args.output is None:
		in_path = Path(args.input)
		output = os.path.join(in_path.parent, in_path.stem + ".html")
	else:
		output = args.output
	
	txt_to_basic_html(args.input, output, args.title, args.nosep)
