from planet import Planet
from rover import *
import traceback


def load_level(filename):
	"""
	Loads the level and returns an object of your choosing
	"""
	result = True
	# planet = Planet("", 0, 0)
	# rover = Rover(0, 0, 0, planet)
	with open(filename) as fp:
		lines = fp.readlines()
		# first line should be "[planet]"
		if not lines[0].strip() == "[planet]":
			return False, None

		# extract name
		try:
			if not lines[1].split(",")[0] == "name" or not lines[2].split(",")[0] == "width" or not lines[3].split(",")[0] == "height" or not lines[4].split(",")[0] == "rover":
				return False, None

			planet_name = lines[1].strip().split(",")[1]
			width = int(lines[2].strip().split(",")[1])
			height = int(lines[3].strip().split(",")[1])
			rover_col = int(lines[4].strip().split(",")[1])
			rover_row = int(lines[4].strip().split(",")[2])

			if width < 5 or height < 5 or width < rover_col or height < rover_row or rover_row < 0 or rover_col < 0:
				return False, None

			planet = Planet(planet_name, width, height)

			for i in range(7, len(lines)):
				row = int((i - 7) / width)
				col = int((i - 7) % width)

				planet.tiles[row][col].type = lines[i].strip().split(",")[0]
				planet.tiles[row][col].current_elevation = []
				for e in lines[i].strip().split(",")[1:]:
					planet.tiles[row][col].current_elevation.append(int(e))

			rover = Rover(rover_row, rover_col, planet.tiles[rover_row][rover_col].current_elevation, planet)
			rover.planet.tiles[rover.row][rover.col].discovered = True
			rover.planet.ratio += 1

		except Exception as e:
			traceback.print_exc()
			return False, None

	return result, rover
