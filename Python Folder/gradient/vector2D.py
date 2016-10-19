#*******************************************************************************
#
#
#
#*******************************************************************************

from math import hypot, sin, cos, acos

#*******************************************************************************
# Vector2D - a 2D vector object.
#*******************************************************************************
class Vector2D(object):
    __slots__ = ['x', 'y']

    def __init__(self,x,y=None):
        if y == None:
            self.x = float(x[0])
            self.y = float(x[1])
        else:
            self.x = float(x)
            self.y = float(y)

    def __len__(self):
        return 2

    def __getitem__(self,index):
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        else:
            print "Index out of bounds."

    def __setitem__(self,index,value):
        if index == 0:
            self.x = value
        elif index == 1:
            self.y = value
        else:
            print "Index out of bounds."

    def __getstate__(self):
        return [self.x,self.y]

    def __repr__(self):
        return "Vector2D<"+ str((self.x,self.y))+">"

    def __neg__(self):
        return Vector2D(-self.x,-self.y)

    def __add__(self,b):
        if isinstance(b,Vector2D):
            return Vector2D(self.x+b.x,self.y+b.y)
        else:
            return Vector2D(self.x+b,self.y+b)

    def __sub__(self,b):
        if isinstance(b,Vector2D):
            return Vector2D(self.x-b.x,self.y-b.y)
        else:
            return Vector2D(self.x-b,self.y-b)

    def __mod__(self,b):
        if isinstance(b,Vector2D):
            pass
        else:
            print "Cross product failed"

    def __div__(self,b):
        return Vector2D(self.x/b,self.y/b)

    def __mul__(self,b):
        return Vector2D(self.x*b,self.y*b)

    def magnitude(self):
        return hypot(self.x,self.y)

    def unit(self):
        m = self.magnitude()
        return Vector2D(self.x/m,self.y/m)

    def normal(self):
        return Vector2D(self.y, self.x)

    def rotate(self, angle, origin=(0,0)):
        sinval = sin(angle)
        cosval = cos(angle)
        A = self.x-origin[0]
        B = self.y-origin[1]
        return Vector2D(A*cosval - B*sinval + origin[0],A*sinval + B*cosval + origin[1])

    def dotProduct(self, v):
        return self.x*v.x + self.y*v.y
    
    def angleBetween(self, v):
        return acos(self.cosineBetween(v))
    
    def cosineBetween(self, v):
        return self.dotProduct(v)/(self.magnitude()*v.magnitude)

    def toTuple(self):
        return (self.x, self.y)