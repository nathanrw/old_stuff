import maths3D

a = maths3D.Vector3D(1,3,7)
b = maths3D.Vector3D(4,5,6)

print a
print b
print "Testing operators:"
print
print a + b
print a * b
print a % b
print a * 6
print "Testing magnitude:"
print
print a.mag()
print "Testing unit vector:"
print
print a.unit()
print a.unit().mag()
