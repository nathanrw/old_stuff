from math import *

m_x = 200
m_y = -200
s_x = 100
s_y = 60

i = float(s_x - m_x)
j = float(s_y - m_y)

try:
    angle = degrees(atan(j/i))
except:
    angle = 0

print angle

def RotPoint( point, axis, ang):
    #Function to generate a new centre. This is stolen from a person called altern.
    x = point[0] - axis[0]
    y = point[1] - axis[1]
    radius = sqrt(x*x + y*y)
    RAng = radians(ang)

    h = axis[0] + ( radius * cos(RAng) )
    v = axis[1] + ( radius * sin(RAng) )

    newpos = (h,v)
    return newpos

newpos = RotPoint( (20,20), (10,10), 45)
print newpos
