from tile import *

class Planet:
	def __init__(self, name, width, height):
		"""
		Initialise the planet object
		"""
		self.name = name
		self.width = width
		self.height = height
		self.tiles = [[Tile("plain") for i in range(width)] for i in range(height)]
		self.ratio = 0

	def update_ratio(self):
		self.ratio += 1

	def scan_shade(self, x, y):
		# shades = [[0 for i in range(5)] for i in range(5)]
		for i in range(-2, 3):
			line = "|"
			for j in range(-2, 3):
				row = x + i
				if row < 0:
					row += self.height
				elif row >= self.height:
					row -= self.height

				col = y + j
				if col < 0:
					col += self.width
				elif col >= self.width:
					col -= self.width
				# print(row, col)

				if i == 0 and j == 0:
					line += "H|"
				elif self.tiles[row][col].is_shaded():
					line += "#|"
				else:
					line += " |"
			print(line)

	def scan_elevation(self, x, y):
		pass

