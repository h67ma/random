import sys
from googletrans import Translator, LANGCODES
import xml.etree.ElementTree as ET
from httpx import Timeout
import time

def translate_xml(node):
	children = list(node)
	if node.text is None or len(children) > 0:
		for child in children:
			translate_xml(child)
	else:
		in_text = node.text.strip()
		while True: # sometimes the translation randomly fails
			try:
				translated = translator.translate(in_text, srt=in_lang, dest=out_lang)
				node.text = translated.text
				break
			except Exception as ex:
				print(ex)
				print("can't translate:", in_text)
				print("retrying...")
				time.sleep(5)


if len(sys.argv) < 5:
	print("args:\n* input xml filename\n* output xml filename\n* input language code \n* output language code\nlanguage codes:")
	print(LANGCODES)
	exit()

in_filename = sys.argv[1]
out_filename = sys.argv[2]
in_lang = sys.argv[3]
out_lang = sys.argv[4]

translator = Translator(raise_exception=True, timeout=Timeout(10.0))

tree = ET.parse(in_filename)
root = tree.getroot()
translate_xml(root)

tree.write(open(out_filename, "w", encoding="UTF-8"), encoding="unicode")
