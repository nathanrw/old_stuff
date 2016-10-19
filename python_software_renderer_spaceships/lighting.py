from math import sqrt
from vector_maths import *
def illuminate(polygon, light):
    
    #Get centre point
    centre_point = [0,0,0]
    for point in polygon.points:
        centre_point[0] += point[0]
        centre_point[1] += point[1]
        centre_point[2] += point[2]
    centre_point[0] = centre_point[0]/len(polygon.points) - light.position[0]
    centre_point[1] = centre_point[1]/len(polygon.points) - light.position[1]
    centre_point[2] = centre_point[2]/len(polygon.points) - light.position[2]

    #Get normal.

    #Point 1 - Point 2
    p1_p2 = (polygon.points[0][0]-polygon.points[1][0],
             polygon.points[0][1]-polygon.points[1][1],
             polygon.points[0][2]-polygon.points[1][2])

    #Point 3 - Point 2
    p3_p2 = (polygon.points[2][0]-polygon.points[1][0],
             polygon.points[2][1]-polygon.points[1][1],
             polygon.points[2][2]-polygon.points[1][2])

    #Normal to the polygon.
    normal = (p1_p2[1]*p3_p2[2] - p1_p2[2]*p3_p2[1],
              p1_p2[2]*p3_p2[0] - p1_p2[0]*p3_p2[2],
              p1_p2[0]*p3_p2[1] - p1_p2[1]*p3_p2[0])

    #Light to centre
    ray = [-centre_point[0],
           -centre_point[1],
           -centre_point[2]]

    #Magnitudes
    normal_m =  sqrt(normal[0]*normal[0] + \
                     normal[1]*normal[1] + \
                     normal[2]*normal[2])

    ray_m =     sqrt(ray[0]*ray[0] + \
                     ray[1]*ray[1] + \
                     ray[2]*ray[2])

    #Unit vectors
    normal_unit =   [normal[0]/normal_m,
                     normal[1]/normal_m,
                     normal[2]/normal_m]

    ray_unit =      [ray[0]/ray_m,
                     ray[1]/ray_m,
                     ray[2]/ray_m]

    #Cosine of angle between the two
    #vectors.
    cosofangle = normal_unit[0]*ray_unit[0] + \
                 normal_unit[1]*ray_unit[1] + \
                 normal_unit[2]*ray_unit[2]

    #Positive.
    if cosofangle < 0:
        cosofangle = 0

    #RGB colour modifier
    colmod = ((int(255 * cosofangle * light.luminosity)),
              (int(255 * cosofangle * light.luminosity)),
              (int(255 * cosofangle * light.luminosity)))

    polygon.colourmod = colmod
