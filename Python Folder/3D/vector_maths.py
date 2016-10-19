#Vector Maths
from math import sqrt

def dot_product_3D(a,b):
    return a[0]*b[0] + a[1]*b[1] + a[2]*b[2]
def cross_product_3D(a,b):
    return[a[1]*b[2] - a[2]*b[1],
           a[2]*b[0] - a[0]*b[2],
           a[0]*b[1] - a[1]*b[0]]
def add_3D(a,b):
    return [a[0]+b[0],
            a[1]+b[1],
            a[2]+b[2]]
def minus_3D(a,b):
    return [a[0]-b[0],
            a[1]-b[1],
            a[2]-b[2]]
def mag_3D(a):
    return sqrt(a[0]**2 + a[1]**2 + a[2]**2)

def mul_scalar_3D(a, scalar):
    return [a[0]*scalar,a[1]*scalar,a[2]*scalar]

def int_3D(a):
    return [int(a[0]),int(a[1]),int(a[2])]

def dot_product_2D(a,b):
    return a[0]*b[0] + a[1]*b[1]

def add_2D(a,b):
    return [a[0]+b[0],
            a[1]+b[1]]

def minus_2D(a,b):
    return [a[0]-b[0],
            a[1]-b[1]]
