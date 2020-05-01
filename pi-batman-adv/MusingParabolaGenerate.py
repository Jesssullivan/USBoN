# quickly generate parabolic dish for Tx / Rx hardware
# just a bunch of ideas mostly from https://forum.freecadweb.org/viewtopic.php?t=4430

import Part, math

# musings derived from:
# comments from forum are kept.

# ? may need to sc. mm --> cm?
tu = FreeCAD.Units.parseQuantity
def mm(value):
    return tu('{} mm'.format(value))
# unit mm may not be worth it here...?
rs = mm(1.9)
thicken = -(rs / mm(15))  # ~shell thickness

# defer to scale during fitting / fillet elsewhere for now...  :(
m=App.Matrix()
m.rotateY(math.radians(-90))
# create a parabola with the symmetry axis (0,0,1)
parabola=Part.Parabola()
parabola.transform(m)

# get only the right part of the curve
edge=parabola.toShape(0,rs)

# add a line to the parabola to get a closed revolution body
pt=parabola.value(rs)
line=Part.makeLine(pt,App.Vector(0,0,pt.z))
wire=Part.Wire([edge,line])
shell=wire.revolve(App.Vector(0,0,0),App.Vector(0,0,1),360)

# make a solid
solid=Part.Solid(shell)

# apply a thickness, solid.Faces[1] is the plane that gets removed therefore
thick=solid.makeThickness([solid.Faces[1]],thicken,0.001) # a thickness of -1
Part.show(thick)

Gui.SendMsgToActiveView("ViewFit")

"""
# fit to view- parabola is "chopped" by value rs, and is significantly reduced
# in size compared to Part.parabola() without set extents from toShape()
Gui.SendMsgToActiveView("ViewFit")

# Remove Part in default env:
App.getDocument("Unnamed1").removeObject("Shape")
"""
