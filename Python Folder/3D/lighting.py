from math import sqrt
from vector_maths import *

def illuminate(polygon, light):
    points = polygon.points
    
    #Get centre point
    centre_point = minus_3D(polygon.average,light.position)

    #Get normal to plane of polygon
    p1_p2 = minus_3D(points[0],points[1])
    p3_p2 = minus_3D(points[2],points[1])
    normal = cross_product_3D(p1_p2,p3_p2)

    #Light to centre
    ray = minus_3D([0,0,0],centre_point)

    #Magnitudes
    normal_inv_m =  1.0/mag_3D(normal)
    ray_inv_m =     1.0/mag_3D(ray)

    #Unit vectors
    normal_unit = mul_scalar_3D(normal,normal_inv_m)
    ray_unit = mul_scalar_3D(ray,ray_inv_m)

    #Cosine of the angle between the two vectors.
    cosofangle = dot_product_3D(normal_unit,ray_unit)

    if cosofangle < 0:
        cosofangle = 0

    #Colour is angle to light * brightness of light, so:

    byte_fraction = 255 * cosofangle
    colmod = int_3D(mul_scalar_3D(light.luminosity,byte_fraction))
    polygon.colourmod = add_3D(polygon.colourmod,colmod)
