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
	print("START <level file> - Starts the game with a provided file.\n"+"QUIT - Quits the game.\n"+"HELP - Shows this message.")


def menu_start_game(filepath):
	"""
	Will start the game with the given file path
	"""
	result, rover = load_level(filepath)
	if not result:
		print("Unable to load level file")
	else:
		while True:
			action = input("Please choose: SCAN, MOVE, STATS, WAIT, FINISH:\n")
			if "SCAN" in action:
				try:
					mode = action.strip().split(" ")[1]
					rover.scan(mode)
				except:
					traceback.print_exc()
			if "MOVE" in action:
				direct = action.strip().split(" ")[1]
				cycles = int(action.strip().split(" ")[2])
				rover.move(direct, cycles)

			if action == "STATS":
				discover_result = float(rover.planet.ratio * 100 / (rover.planet.width * rover.planet.height))
				print("Explored: %.3f%%" % discover_result)
				print("Battery: %d/100" % rover.battery)
				continue
			if "WAIT" in action:
				try:
					cycles = action.strip().split(" ")[1]
					if not rover.planet.tiles[rover.row][rover.col].is_shaded():
						rover.wait(cycles)
				except:
					traceback.print_exc()
					pass
			if action == "FINISH":
				discover_result = float(rover.planet.ratio * 100 / (rover.planet.width * rover.planet.height))
				print("You explored %.3f%% of %s" % (discover_result, rover.planet.name))
				break


def menu():
	"""
	Start the menu component of the game
	"""
	choice = input("Please choose: QUIT, START, HELP:\n")
	if "START" in choice:
		try:
			filepath = choice.split(' ')[1]
			if not os.path.exists(filepath):
				print("Level file could not be found")
				return
			menu_start_game(filepath)
		except:
			traceback.print_exc()
			print("Unable to load level file")
	elif choice == "QUIT":
		quit()
	elif choice == "HELP":
		menu_help()

if __name__ == '__main__':
	menu()
