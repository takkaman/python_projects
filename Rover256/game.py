import os
from loader import *
import traceback
# import planet
# import rover
# import tile


def quit():
	"""
	Will quit the program
	"""
	exit()


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
	if not os.path.exists(filepath):
		print("Level file could not be found")
	else:
		result, pt, rov = load_level(filepath)
		if not result:
			print("Unable to load level file")
		else:
			# print(pt.tiles[1][2].type)
			# print(rov.elv)
			while True:
				action = input("Please select the action for rover: SCAN, MOVE, STATS, WAIT, FINISH:\n")
				if action == "FINISH":
					print("You explored {0} % of {1}".format(pt.ratio, pt.name))
					break
				if action == "STATS":
					print("Explored: {0}%".format(pt.ratio))
					print("Battery: {0}/100".format(rov.battery))
					continue
				if "MOVE" in action:
					try:
						direct = action.strip().split(" ")[1]
						cycles = int(action.strip().split(" ")[2])
						if not direct == "N" and not direct == "E" and not direct == "S" and not direct == "W": continue
						if cycles <= 0: continue
						rov = pt.explore(direct, cycles, rov)
						print("New pos: {0} {1}, elevation: {2}, battery: {3}".format(rov.x, rov.y, rov.elv, rov.battery))
					except:
						traceback.print_exc()
						pass
				if "SCAN" in action:
					try:
						mode = action.strip().split(" ")[1]
						if mode == "shade":
							pt.scan_shade(rov.x, rov.y)
						elif mode == "elevation":
							pt.scan_elevation(rov.x, rov.y, rov.elv)
						else:
							print("Cannot perform this command")
					except:
						traceback.print_exc()
				if "WAIT" in action:
					try:
						cycles = action.strip().split(" ")[1]
						if not pt.tiles[rov.x][rov.y].is_shaded():
							rov.wait(cycles)
					except:
						traceback.print_exc()
						pass


def menu():
	"""
	Start the menu component of the game
	"""
	select = input("Please select the item: QUIT, START, HELP:\n")
	if "START" in select:
		try:
			filepath = select.split(' ')[1]
			# print(filepath)
			menu_start_game(filepath)
		except:
			traceback.print_exc()
			print("Unable to load level file")
	elif select == "HELP":
		menu_help()
	elif select == "QUIT":
		quit()

if __name__ == '__main__':
	menu()
