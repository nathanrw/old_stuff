import pygame; from pygame.locals import *
import math; from math import *

def prepare_polygons_3D(camera,polygons):
    """Get rid of polygons that are not needed, and prepare the
       rest for projection."""

    remaining_polygons = []
    for polygon in polygons:
        # If failed gets set to 1, the polygon is not returned for
        # projection.
        failed = 0

        #Backface Culling

        # Point 1 - Point 2
        p1_p2 = (polygon.points[0][0]-polygon.points[1][0],
                 polygon.points[0][1]-polygon.points[1][1],
                 polygon.points[0][2]-polygon.points[1][2])

        # Point 3 - Point 2
        p3_p2 = (polygon.points[2][0]-polygon.points[1][0],
                 polygon.points[2][1]-polygon.points[1][1],
                 polygon.points[2][2]-polygon.points[1][2])

        # Normal to the polygon.
        normal = (p1_p2[1]*p3_p2[2] - p1_p2[2]*p3_p2[1],
                  p1_p2[2]*p3_p2[0] - p1_p2[0]*p3_p2[2],
                  p1_p2[0]*p3_p2[1] - p1_p2[1]*p3_p2[0])

        # Plane's constant.
        k = normal[0]*polygon.points[0][0] + \
            normal[1]*polygon.points[0][1] + \
            normal[2]*polygon.points[0][2]

        # Substitute the camera into the plane equation to
        # see which side of the polygon we're on.
        if k > 0:
            failed = 1

        # Kill polygons we can't see.

        #etc

        # Clip to Z axis.
            #For now this kills anything that dares to cross.
        
        for point in polygon.points:
            if point[2] < 0:
                failed = 1
        
        #Finish
        if failed == 0:remaining_polygons.append(polygon)
        
    return remaining_polygons

def prepare_polygons_2D(camera, polygons):
    pass
