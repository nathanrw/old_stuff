import pygame; from pygame.locals import *
import math; from math import *

def prepare_polygon_3D(camera,polygon):
    #=============================================
    #Get rid of unneeded polygons
    #=============================================
    
    #=============================================
    #Requires that the camera's position be the
    #origin and the camera's rotation be 0. In
    #other words, rotate_point_about_camera must be
    #used on everything first.
    #=============================================

    #=============================================
    # If failed gets set to 1, the polygon is not returned for
    # projection.
    #=============================================
    failed = 0

    #=============================================
    # Backface Culling.
    #
    # Point 1 - Point 2
    #=============================================
    p1_p2 = (polygon.points[0][0]-polygon.points[1][0],
             polygon.points[0][1]-polygon.points[1][1],
             polygon.points[0][2]-polygon.points[1][2])

    #=============================================
    # Point 3 - Point 2
    #=============================================
    p3_p2 = (polygon.points[2][0]-polygon.points[1][0],
             polygon.points[2][1]-polygon.points[1][1],
             polygon.points[2][2]-polygon.points[1][2])

    #=============================================
    # Normal to the polygon.
    #=============================================
    normal = (p1_p2[1]*p3_p2[2] - p1_p2[2]*p3_p2[1],
              p1_p2[2]*p3_p2[0] - p1_p2[0]*p3_p2[2],
              p1_p2[0]*p3_p2[1] - p1_p2[1]*p3_p2[0])

    #=============================================
    # Plane's constant.
    #=============================================
    k = normal[0]*polygon.points[0][0] + \
        normal[1]*polygon.points[0][1] + \
        normal[2]*polygon.points[0][2]
    
    #=============================================
    # Substitute the camera into the plane equation to
    # see which side of the polygon we're on.
    #=============================================
    if k > 0:
        failed = 1
    
    #=============================================
    # Clip to Z axis. Well...
    #=============================================
    for point in polygon.points:
        if point[2] < 0:
            failed = 1
            
    if failed == 1:
        polygon.shown = "no"
