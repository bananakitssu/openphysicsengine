### LIBRARIES ###
from enum import Enum
from time import sleep
from math import floor as mfloor

### GLOBALS ###

FPS = 30
TICK = 0

### HELPERS ###

class Property(Enum):
	Gravity = "gravity"
	Mass = "mass"
	Position = "position"
	Velocity = "velocity"
	Restitution = "restitution"

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
	
class ObjectType(Enum):
	Point = "point"
	Floor = "floor"
	
	@staticmethod
	def from_string(name: str):
		if not isinstance(name, str):
			raise TypeError(f"Expected str, got {type(name).__name__}")
		try:
			return ObjectType(name.lower())
		except ValueError:
			raise ValueError(f"Unknown type: {name}")

def objt(name: str) -> ObjectType:
	return ObjectType.from_string(name)

class Workspace:

	def __init__(self):
		self.Gravity = 0.5
		self.Objects = {}
		self.GravityDirection = (0, -1, 0)
		self.Floor = None

	def addObject(self, obj):
		if obj.Type == "Floor": self.Floor = obj
		else:
			uuid = len(self.Objects) + 1
			self.Objects[uuid] = obj
			obj.uuid = uuid
			obj.workspace = self
			return uuid

	def addObjects(self, *objs):
		for obj in objs:
			addObject(obj)

	def getObject(self, uuid):
		return self.Objects[uuid]

	def getAllObjects(self):
		return self.Objects
		
	def getGlobalTime(self):
		return mfloor(TICK/FPS*100)/100
	
	def getFloor(self):
		return self.Floor

	def setProperty(self, property: Property, value):
		if property == Property.Gravity:
			if type(value).__name__ == "int":
				self.Gravity = value
				return True, f"Set gravity to {value}"
		else:return(False,None)
		
	def getProperty(self, property: Property):
		if property == Property.Gravity: return True, self.Gravity
		else:return(False,None)

class Object:
	def __init__(self):
		self.Mass = 0
		self.Restitution = 0
		self.Position = [0, 0, 0]
		self.Velocity = [0, 0, 0]
		self.workspace = None
		self.uuid = None
		self.Type = None
		self._listeners = {}
		
	def create(self, type: ObjectType):
		type = str(type)
		if type == "Point":
			self.Mass = 5
			self.Position = [0, 0, 0]
			self.Velocity = [0, 0, 0]
			self.Restitution
		elif type == "Floor":
			self.Mass = 0
			self.Position = [0, 0, 0]
			self.Velocity = [0, 0, 0]
			def reset(*args):
				self.Mass = 0
				self.Velocity = [0, 0, 0]
			self.propertyChanged(Property.Velocity, reset)
		self.Type = type
		return self

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
		
		if self.Type == "Point":
			floor = self.workspace.getFloor()
			if floor:
				if self.Position[1] <= floor.Position[1]:
					self.Position[1] = floor.Position[1]
					self.Velocity[1] = self.Velocity[1]*-self.Restitution
					
	def setProperty(self, property: Property, value):
		success = False

		if property == Property.Position and isinstance(value, tuple):
			self.Position = list(value)
			success = True
	
		elif property == Property.Velocity and isinstance(value, tuple):
			self.Velocity = list(value)
			success = True
	
		elif property == Property.Mass and isinstance(value, int):
			self.Mass = value
			success = True
		
		elif property == Property.Restitution and isinstance(value, float):
			self.Restitution = value
			success = True
	
		if success:
			if hasattr(self, "_listeners") and property in self._listeners:
				for callback in self._listeners[property]:
					callback(value)
	
			return True, f"Set {property} to {value}"
	
		return False, None
	
	def getProperty(self, property: Property):
		if property == Property.Position: return True, self.Position
		elif property == Property.Velocity: return True, self.Velocity
		elif property == Property.Mass: return True, self.Mass
		elif property == Property.Restitution: return True, self.Restitution
		else:return(False,None)
	
	def propertyChanged(self, property: Property, callback):
		if property not in self._listeners:
			self._listeners[property] = []
		self._listeners[property].append(callback)



### MAIN ###




# Startup
work = Workspace()
floor = Object().create("Floor")
point = Object().create("Point")
point.setProperty(Property.Restitution, 0.95)
floor.setProperty(Property.Position, (0, -20, 0))
work.addObject(point)
work.addObject(floor)

# Functions / Helpers
def stepAll():
	for obj in work.getAllObjects().values():
		obj.step()

# Main loop
def main():
	global TICK
	while True:
		sleep(1 / FPS)
		stepAll()
		print(f"At tick {TICK} and time {work.getGlobalTime()}")
		for obj in work.getAllObjects().values():
			print(f"--- Object #{obj.uuid} ---")
			print(f"Position: {obj.getProperty(Property.Position)[1]}")
			print(f"Velocity: {obj.getProperty(Property.Velocity)[1]}")
			print(f"Mass: {obj.getProperty(Property.Mass)[1]}")
		
		TICK += 1

# Start program

main()
