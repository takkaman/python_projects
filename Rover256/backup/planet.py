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

	# def update_ratio(self):
	# 	self.ratio += 1

	def scan_shade(self, x, y):
		# shades = [[0 for i in range(5)] for i in range(5)]
		for i in range(-2, 3):
			line = "|"
			for j in range(-2, 3):
				row = self.cycle(x + i, self.height)
				col = self.cycle(y + j, self.width)

				if i == 0 and j == 0:
					line += "H|"
				elif self.tiles[row][col].is_shaded():
					line += "#|"
				else:
					line += " |"
			print(line)

	def scan_elevation(self, x, y, rov_elv):
		# shades = [[0 for i in range(5)] for i in range(5)]
		elv = rov_elv
		# print(elv)
		for i in range(-2, 3):
			line = "|"
			for j in range(-2, 3):
				row = self.cycle(x + i, self.height)
				col = self.cycle(y + j, self.width)

				if i == 0 and j == 0:
					line += "H|"
				else:
					# if row == 1 and col == 0:
					# 	print(len(self.tiles[row][col].elevation()))
					# 	print(len(self.tiles[row][col].elevation()), len(elv))
					if len(self.tiles[row][col].elevation()) == 2 and len(elv) == 1:  # current plain vs slop
						# if row == 1 and col == 0:
						# 	print("AAA")
						if elv[0] == self.tiles[row][col].elevation()[0]:  # elevation equals to highest slop
							line += "\|"
						elif elv[0] == self.tiles[row][col].elevation()[1]:  # elevation equals to lowest slop
							line += "/|"
						elif elv[0] < self.tiles[row][col].elevation()[1]:  # elevation lower than lowest slop
							line += "+|"
						else:
							line += "-|"
					elif len(self.tiles[row][col].elevation()) == 1 and len(elv) == 1:  # current plain vs plain
						if elv[0] == self.tiles[row][col].elevation()[0]:
							line += " |"
						elif elv[0] > self.tiles[row][col].elevation()[0]:
							line += "-|"
						else:
							line += "+|"
					elif len(self.tiles[row][col].elevation()) == 1 and len(elv) == 2:  # current slop vs plain
						if elv[1] > self.tiles[row][col].elevation()[0]:
							line += "-|"
						elif elv[0] < self.tiles[row][col].elevation()[0]:
							line += "+|"
						else:
							line += " |"
					elif len(self.tiles[row][col].elevation()) == 2 and len(elv) == 2:  # current slop vs slop
						if elv[1] > self.tiles[row][col].elevation()[0]:
							line += "-|"
						elif elv[0] < self.tiles[row][col].elevation()[1]:  # plain lower elevation
							line += "+|"
						else:
							line += " |"
			print(line)

	def explore(self, direct, cycles, rov):
		# print("Attempt move the rover {0} by {1} tiles".format(direct, cycles))
		if direct == "N":
			for i in range(1, cycles + 1):
				new_row = self.cycle(rov.x - 1, self.height)
				current_tile = self.tiles[rov.x][rov.y]
				new_tile = self.tiles[new_row][rov.y]
				print("current: {0} {1}, access: {2} {3}".format(rov.x, rov.y, new_row, rov.y))
				result, new_elv = self.accessable(current_tile, new_tile)
				if result:
					current_tile.set_occupant(None)
					new_tile.set_occupant(rov)
					rov.x = new_row
					rov.elv = new_tile.elv
					# if not new_tile.explored:
					# new_tile.explored = True
					tmp_x = self.cycle(rov.x+2, self.height)
					for j in range(-2,3):
						tmp_y = self.cycle(tmp_y+j, self.width)
						if not self.tiles[tmp_x][tmp_y].explored:
							self.tiles[tmp_x][tmp_y].explored = True
							self.ratio += 1

						# self.ratio += 1

					if new_tile.is_shaded():
						rov.battery -= 1
						if rov.battery == 0:
							return rov
				else:
					return rov
			return rov
		if direct == "S":
			for i in range(1, cycles + 1):
				new_row = self.cycle(rov.x + 1, self.height)
				current_tile = self.tiles[rov.x][rov.y]
				new_tile = self.tiles[new_row][rov.y]
				print("current: {0} {1}, access: {2} {3}".format(rov.x, rov.y, new_row, rov.y))
				result, new_elv = self.accessable(current_tile, new_tile)
				if result:
					current_tile.set_occupant(None)
					new_tile.set_occupant(rov)
					rov.x = new_row
					rov.elv = new_tile.elv
					# if not new_tile.explored:
					# 	new_tile.explored = True
					tmp_x = self.cycle(rov.x-2, self.height)
					for j in range(-2,3):
						tmp_y = self.cycle(tmp_y+j, self.width)
						if not self.tiles[tmp_x][tmp_y].explored:
							self.tiles[tmp_x][tmp_y].explored = True
							self.ratio += 1

					if new_tile.is_shaded():
						rov.battery -= 1
						if rov.battery == 0:
							return rov
				else:
					return rov
			return rov
		if direct == "E":
			for i in range(1, cycles + 1):
				new_col = self.cycle(rov.y + 1, self.width)
				current_tile = self.tiles[rov.x][rov.y]
				new_tile = self.tiles[rov.x][new_col]
				print("current: {0} {1}, access: {2} {3}".format(rov.x, rov.y, rov.x, new_col))
				result, new_elv = self.accessable(current_tile, new_tile)
				if result:
					current_tile.set_occupant(None)
					new_tile.set_occupant(rov)
					rov.y = new_col
					rov.elv = new_tile.elv
					# if not new_tile.explored:
					# 	new_tile.explored = True
					tmp_y = self.cycle(rov.y+2, self.width)
					for j in range(-2,3):
						tmp_x = self.cycle(tmp_x+j, self.height)
						if not self.tiles[tmp_x][tmp_y].explored:
							self.tiles[tmp_x][tmp_y].explored = True
							self.ratio += 1

					if new_tile.is_shaded():
						rov.battery -= 1
						if rov.battery == 0:
							return rov
				else:
					return rov
			return rov
		if direct == "W":
			for i in range(1, cycles + 1):
				new_col = self.cycle(rov.y - 1, self.width)
				current_tile = self.tiles[rov.x][rov.y]
				new_tile = self.tiles[rov.x][new_col]
				print("current: {0} {1}, access: {2} {3}".format(rov.x, rov.y, rov.x, new_col))
				result, new_elv = self.accessable(current_tile, new_tile)
				if result:
					current_tile.set_occupant(None)
					new_tile.set_occupant(rov)
					rov.y = new_col
					rov.elv = new_tile.elv
					# if not new_tile.explored:
					# 	new_tile.explored = True
					tmp_y = self.cycle(rov.y-2, self.width)
					for j in range(-2,3):
						tmp_x = self.cycle(tmp_x+j, self.height)
						if not self.tiles[tmp_x][tmp_y].explored:
							self.tiles[tmp_x][tmp_y].explored = True
							self.ratio += 1

					if new_tile.is_shaded():
						rov.battery -= 1
						if rov.battery == 0:
							return rov
				else:
					return rov
			return rov

	def accessable(self, current_tile, new_tile):
		curr_elv = current_tile.elevation()
		new_elv = new_tile.elevation()
		if len(curr_elv) == 1 and len(new_elv) == 1:
			if curr_elv[0] == new_elv[0]:
				return True, new_elv[0]
			else:
				return False, None
		elif len(curr_elv) == 2 and len(new_elv) == 1:
			if curr_elv[0] == new_elv[0] or curr_elv[1] == new_elv[0]:
				return True, new_elv[0]
			else:
				return False, None
		elif len(curr_elv) == 1 and len(new_elv) == 2:
			if curr_elv[0] == new_elv[0]:  # down slop
				return True, new_elv[1]
			elif curr_elv[0] == new_elv[1]:  # up slop
				return True, new_elv[0]
			else:
				return False, None
		else:
			return False, None  # assume no consecutive slops

	def cycle(self, val, bound):
		if val >= bound:
			return val - bound
		elif val < 0:
			return val + bound
		else:
			return val





