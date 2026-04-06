#PHYSICS_T: testing file for physics

from physics import Workspace, Object, Property

o = Object().create("point")
w = Workspace()

print("Creating objects:")
if o:
	print("Success,",o)
else:
	print("Failed")
	exit()
print("Creating workspace:")
if w:
	print("Success,",w)
else:
	print("Failed")
	exit()
print("Setting properties:")
t=[w,o,o,o,o,o,w];v=[1,1,(0,0,0),(0,0,0),.1,.1,.1] #wow!!!!!!!
for i,prop in enumerate(Property):
	s=t[i].setProperty(prop, v[i])
	if s:
		print(str(prop)+": Success")
	else:
		print(str(prop)+": Failed")
