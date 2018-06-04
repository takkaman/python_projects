
class Tile:

	def __init__(self, *args):
		"""
		Initialises the terrain tile and attributes
		"""
		self.type = ""
		self.current_elevation = []
		for arg in args:
			self.current_elevation.append(int(arg))
		self.occupant = None
		self.discovered = False

	def elevation(self):
		"""
		Returns an list value of the elevation number
		of the terrain object
		"""
		return self.current_elevation
	
	def is_shaded(self):
		"""
		Returns True if the terrain tile is shaded, otherwise False
		"""
		if self.type == "shaded":
			return True
		else:
			return False
	
	def set_occupant(self, obj):
		"""
		Sets the occupant on the terrain tile
		"""
		self.occupant = obj
	
	def get_occupant(self):
		"""
		Gets the entity on the terrain tile
		If nothing is on this tile, it should return None
		"""
		return self.occupant

