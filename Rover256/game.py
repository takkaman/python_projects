def quit():
	"""
	Will quit the program
	"""
	pass


def menu_help():
	"""
	Displays the help menu of the game
	"""
	msg = """START <level file> - Starts the game with a provided file.
QUIT - Quits the game
HELP - Shows this message"""
	print(msg)


def menu_start_game(filepath):
	"""
	Will start the game with the given file path
	"""
	pass


def menu():
	"""
	Start the menu component of the game
	"""
	select = input("Please select the item: QUIT, START, HELP:\n")
	if "START" in select:
		filepath = select.split(' ')[1]
		# print(filepath)
		menu_start_game(filepath)
	elif select == "HELP":
		menu_help()
	elif select == "QUIT":
		quit()

if __name__ == '__main__':
	menu()
