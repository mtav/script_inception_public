from __future__ import division # allows floating point division from integers

import Part
from FreeCAD import Base

from math import sqrt, pi, sin, cos, asin
from numpy import array

doc = FreeCAD.activeDocument()

cylinder = Part.makeCylinder(3,10,Base.Vector(0,0,0),Base.Vector(1,0,0))
sphere = Part.makeSphere(5,Base.Vector(5,0,0))
diff = cylinder.cut(sphere)

obj = doc.addObject("Part::Feature", 'boolean-test')
obj.Shape = diff

doc.recompute()

FreeCAD.Console.PrintMessage("DONE\n")
