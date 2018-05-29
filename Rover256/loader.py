from planet import Planet
from rover import *
import traceback


def load_level(filename):
	"""
	Loads the level and returns an object of your choosing
	"""
	result = True
	pt = Planet("dummy", 0, 0)
	rov = Rover(0, 0, 0)
	with open(filename) as fp:
		lines = fp.readlines()
		# first line should be "[planet]"
		if not lines[0].strip() == "[planet]":
			return False, None, None

		# extract name
		try:
			if not lines[1].split(",")[0] == "name": return False, None, None
			if not lines[2].split(",")[0] == "width": return False, None, None
			if not lines[3].split(",")[0] == "height": return False, None, None
			if not lines[4].split(",")[0] == "rover": return False, None, None

			planet_name = lines[1].strip().split(",")[1]
			width = int(lines[2].strip().split(",")[1])
			height = int(lines[3].strip().split(",")[1])
			rov_x = int(lines[4].strip().split(",")[1])
			rov_y = int(lines[4].strip().split(",")[2])

			"""
			There is exactly 4 fields specified under the planet section and the number of tiles match the dimensions of the planet.
			The rover’s coordinates specified are greater than or equal to 0.
			The rover’s coordinates must be within the bounds of the planet’s dimensions.
			Both width and height values need to be greater than or equal to 5.
			highest elevation is strictly greater than lowest elevation for a tile.
			"""
			if width < 5 or height < 5: return False, None, None

			if len(lines) != width * height + 7: return False, None, None
			if width < rov_x or height < rov_y or rov_x < 0 or rov_y < 0: return False, None, None

			pt = Planet(planet_name, width, height)
			rov = Rover(rov_x, rov_y, 0)
			for i in range(7, 37):
				row = int((i - 7) / width)
				col = int((i - 7) % width)
				# print(lines[i].strip().split(","))
				pt.tiles[row][col].type = lines[i].strip().split(",")[0]
				pt.tiles[row][col].elv = lines[i].strip().split(",")[1:]

		except Exception as e:
			traceback.print_exc()
			return False, None, None

	return result, pt, rov
