from planet import *

class Rover:
	
	def __init__(self, row, col, current_elevation, planet):
		"""
		Initialises the rover
		"""
		self.row = row
		self.col = col
		self.current_elevation = current_elevation
		self.battery = 100
		self.planet = planet
		self.scan_row_scope = 2
		self.scan_col_scope = 2
	
	def move(self, direction, cycles):
		"""
		Moves the rover on the planet
		"""
		try:
			if int(cycles) <= 0:
				return
		except:
			return

		if direction == "N":
			self.move_north(cycles)
		elif direction == "S":
			self.move_south(cycles)
		elif direction == "E":
			self.move_east(cycles)
		elif direction == "W":
			self.move_west(cycles)

		if not self.planet.tiles[self.row][self.col].discovered:
			self.planet.tiles[self.row][self.col].discovered = True
			self.planet.ratio += 1

	def move_west(self, cycles):
		for i in range(1, cycles + 1):
			new_col = self.planet.recalculation(self.col - 1, self.planet.width)
			current_tile = self.planet.tiles[self.row][self.col]
			new_tile = self.planet.tiles[self.row][new_col]
			# print("current: {0} {1}, access: {2} {3}".format(self.row, self.col, self.row, new_col))
			result, new_elevation = self.planet.check(current_tile, new_tile)
			if result:
				current_tile.set_occupant(None)
				new_tile.set_occupant(self)
				self.col = new_col
				self.current_elevation = new_tile.current_elevation

				if new_tile.is_shaded():
					self.battery -= 1
					if self.battery < 0:
						break

	def move_east(self, cycles):
		for i in range(1, cycles + 1):
			new_col = self.planet.recalculation(self.col + 1, self.planet.width)
			current_tile = self.planet.tiles[self.row][self.col]
			new_tile = self.planet.tiles[self.row][new_col]
			# print("current: {0} {1}, access: {2} {3}".format(self.row, self.col, self.row, new_col))
			result, new_elevation = self.planet.check(current_tile, new_tile)
			if result:
				current_tile.set_occupant(None)
				new_tile.set_occupant(self)
				self.col = new_col
				self.current_elevation = new_tile.current_elevation

				if new_tile.is_shaded():
					self.battery -= 1
					if self.battery < 0:
						break

	def move_south(self, cycles):
		for i in range(1, cycles + 1):
			new_row = self.planet.recalculation(self.row + 1, self.planet.height)
			current_tile = self.planet.tiles[self.row][self.col]
			new_tile = self.planet.tiles[new_row][self.col]
			# print("current: {0} {1}, access: {2} {3}".format(self.row, self.col, new_row, self.col))
			result, new_elevation = self.planet.check(current_tile, new_tile)
			if result:
				current_tile.set_occupant(None)
				new_tile.set_occupant(self)
				self.row = new_row
				self.current_elevation = new_tile.current_elevation

				if new_tile.is_shaded():
					self.battery -= 1
					if self.battery < 0:
						break

	def move_north(self, cycles):
		for i in range(1, cycles + 1):
			new_row = self.planet.recalculation(self.row - 1, self.planet.height)
			current_tile = self.planet.tiles[self.row][self.col]
			new_tile = self.planet.tiles[new_row][self.col]
			# print("current: {0} {1}, access: {2} {3}".format(self.row, self.col, new_row, self.col))
			result, new_elevation = self.planet.check(current_tile, new_tile)
			if result:
				current_tile.set_occupant(None)
				new_tile.set_occupant(self)
				self.row = new_row
				self.current_elevation = new_tile.current_elevation

				if new_tile.is_shaded():
					self.battery -= 1
					if self.battery < 0:
						break

	def wait(self, cycles):
		"""
		The rover will wait for the specified cycles
		"""
		self.battery += int(cycles)
		if self.battery >= 100:
			self.battery = 100

	def scan(self, mode):
		if mode == "shade":
			print( )
			self.scan_shade()
			print( )
		elif mode == "elevation":
			print( )
			self.scan_elevation()
			print( )
		else:
			print( )
			print("Cannot perform this command")
			print( )
		self.planet.update_ratio(self.row, self.col)

	def scan_shade(self):
		for i in range(-1 * self.scan_row_scope, self.scan_row_scope + 1):
			line = "|"
			for j in range(-1 * self.scan_col_scope, self.scan_col_scope + 1):
				row = self.planet.recalculation(self.row + i, self.planet.height)
				col = self.planet.recalculation(self.col + j, self.planet.width)
				# print(row, col)
				if i == 0 and j == 0:
					line += "H|"
				elif self.planet.tiles[row][col].is_shaded():
					line += "#|"
				else:
					line += " |"
			print(line)

	def scan_elevation(self):
		elevation = self.current_elevation
		for i in range(-1 * self.scan_row_scope, self.scan_row_scope + 1):
			line = "|"
			for j in range(-1 * self.scan_col_scope, self.scan_col_scope + 1):
				row = self.planet.recalculation(self.row + i, self.planet.height)
				col = self.planet.recalculation(self.col + j, self.planet.width)

				if i == 0 and j == 0:
					line += "H|"
				else:
					rover_type = len(elevation)
					tile_type = len(self.planet.tiles[row][col].elevation())
					tile = self.planet.tiles[row][col].elevation()
					if tile_type == 2 and rover_type == 2:  # current slop vs slop
						if elevation[1] > tile[0]:
							line += "-|"
						elif elevation[0] < tile[1]:  # plain lower elevation
							line += "+|"
						else:
							line += " |"
					elif tile_type == 1 and rover_type == 1:  # current plain vs plain
						if elevation[0] == tile[0]:
							line += " |"
						elif elevation[0] > tile[0]:
							line += "-|"
						else:
							line += "+|"
					elif tile_type == 1 and rover_type == 2:  # current slop vs plain
						if elevation[1] > tile[0]:
							line += "-|"
						elif elevation[0] < tile[0]:
							line += "+|"
						else:
							line += " |"
					elif tile_type == 2 and rover_type == 1:  # current plain vs slop
						# if row == 1 and col == 0:
						# 	print("AAA")
						if elevation[0] == tile[0]:  # elevation equals to highest slop
							line += "\|"
						elif elevation[0] == tile[1]:  # elevation equals to lowest slop
							line += "/|"
						elif elevation[0] < tile[1]:  # elevation lower than lowest slop
							line += "+|"
						else:
							line += "-|"
			print(line)
