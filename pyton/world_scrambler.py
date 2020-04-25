import sys

def find_matches(letters, desired):
	"""
	checks if desired words can be made with letters that you have laying around
	:type letters: string with letters that you have. Multiple letter occurences matter. Spaces will be ignored
	:type desired: string with words that you want to make. Spaces will be ignored.
	"""
	letters = list(letters.replace(" ", "").lower())
	desired = list(desired.replace(" ", "").lower())

	for letter in desired:
		if letter in letters:
			letters.remove(letter)
		else:
			return False

	return True

if len(sys.argv) < 3:
	print("too few arguments")
	print("arg1 = letters that you have")
	print("arg2 = words that you want to make")
	exit()

if find_matches(sys.argv[1], sys.argv[2]):
	print("possible match")
else:
	print("impossible match")
