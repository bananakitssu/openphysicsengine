### LIBRARIES ###
from enum import Enum
from time import sleep

### GLOBALS ###

FPS = 30
TICK = 0

### HELPERS ###

class Property(Enum):
	Gravity = "gravity"
	Mass = "mass"
	Position = "position"
	Velocity = "velocity"

	@staticmethod
	def from_string(name: str):
		if not isinstance(name, str):
			raise TypeError(f"Expected str, got {type(name).__name__}")
		try:
			return Property(name.lower())
		except ValueError:
			raise ValueError(f"Unknown property: {name}")

def prop(name: str) -> Property:
	return Property.from_string(name)

class Workspace:

	def __init__(self):
		self.Gravity = 0.5
		self.Objects = {}
		self.GravityDirection = (0, -1, 0)

	def addObject(self, obj):
		uuid = len(self.Objects) + 1
		self.Objects[uuid] = obj
		obj.uuid = uuid
		obj.workspace = self
		return uuid

	def getObject(self, uuid):
		return self.Objects[uuid+1]

	def getAllObjects(self):
		return self.Objects
		
	def getGlobalTime(self):
		return TICK / FPS

	def setProperty(self, property: Property, value):
		if property == Property.Gravity:
			if type(value).__name__ == "int":
				self.Gravity = value
				return True, f"Set gravity to {value}"
				
class Object:

	def __init__(self):
		self.Mass = 5
		self.Position = [0, 0, 0]
		self.Velocity = [0, 0, 0]
		self.workspace = None
		self.uuid = None

	def step(self):
		gx, gy, gz = self.workspace.GravityDirection
		g = self.workspace.Gravity

		ax, ay, az = gx * g, gy * g, gz * g

		self.Velocity[0] += ax
		self.Velocity[1] += ay
		self.Velocity[2] += az

		self.Position[0] += self.Velocity[0]
		self.Position[1] += self.Velocity[1]
		self.Position[2] += self.Velocity[2]
	
	def setProperty(self, property: Property, value):
		if property == Property.Position:
			if type(value).__name__ == "tuple":
				self.Position = value
				return True, f"Set position to {value}"
		if property == Property.Velocity:
			if type(value).__name__ == "tuple":
				self.Velocity = value
				return True, f"Set velocity to {value}"
		if property == Property.Mass:
			if type(value).__name__ == "int":
				self.Mass = value
				return True, f"Set mass to {value}"




### MAIN ###




# Startup
work = Workspace()
work.addObject(Object())

# Functions / Helpers
def stepAll():
	for obj in work.getAllObjects().values():
		obj.step()

# Main loop
def main():
	while True:
		sleep(1 / FPS)
		stepAll()
		for obj in work.getAllObjects().values():
			print(f"--- Object #{obj.uuid} ---")
			print(f"Position: {obj.Position}")
		
		TICK += 1

# Start program

main()
