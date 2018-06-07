from terrian import *


class Planet:
	def __init__(self, name, width, height):
		"""
		Initialise the planet object
		"""
		self.name = name
		self.width = width
		self.height = height
		self.tiles = [[Tile() for i in range(width)] for i in range(height)]
		self.ratio = 0

	def check(self, current_tile, new_tile):
		curr_elevation = current_tile.elevation()
		new_elevation = new_tile.elevation()
		if len(curr_elevation) == 1 and len(new_elevation) == 1:
			if curr_elevation[0] == new_elevation[0]:
				return True, new_elevation[0]
			else:
				return False, None
		elif len(curr_elevation) == 2 and len(new_elevation) == 1:
			if curr_elevation[0] == new_elevation[0] or curr_elevation[1] == new_elevation[0]:
				return True, new_elevation[0]
			else:
				return False, None
		elif len(curr_elevation) == 1 and len(new_elevation) == 2:
			if curr_elevation[0] == new_elevation[0]:  # down slop
				return True, new_elevation[1]
			elif curr_elevation[0] == new_elevation[1]:  # up slop
				return True, new_elevation[0]
			else:
				return False, None
		else:
			return False, None  # assume no consecutive slops

	def recalculation(self, val, bound):
		if val >= bound:
			return val - bound
		elif val < 0:
			return val + bound
		else:
			return val

	def update_ratio(self, row, col):
		for i in range(-2, 3):
			for j in range(-2, 3):
				tmp_row = self.recalculation(row + i, self.height)
				tmp_col = self.recalculation(col + j, self.width)
				if not self.tiles[tmp_row][tmp_col].discovered:
					self.tiles[tmp_row][tmp_col].discovered = True
					self.ratio += 1




