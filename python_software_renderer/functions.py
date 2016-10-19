#====================================================
#functions.py (graphics.py might be more accurate)
#This is the main graphics file.
#====================================================

#====================================================
#Definitely needs sorting out.
#====================================================

#====================================================
#Pygame and the maths, as well as copy.
#====================================================
import pygame; from pygame.locals import *
from math import *
from vector_maths import *
from copy import copy

#====================================================
#The rest of the graphics.
#====================================================
from prepare_polygons import prepare_polygon_3D
from rotations import rotate_3D, rotate_point_about_camera
from projection import project_polygon, project_point
from filler import filler
from lighting import illuminate
from entities import Polygon, Light

class camera():
    #====================================================
    #"Are you still there?"
    #====================================================
    def __init__(self, window, pos, angle):
        self.position = pos
        self.angle = angle
        self.field_of_view = [0,0,0]
        self.dist = window[0]/2
        self.size = window
    def move(self,pos):
        #====================================================
        #Move the camera by the specified vector.
        #====================================================
        self.position = [self.position[0] + pos[0],self.position[1] + pos[1],self.position[2] + pos[2]]
    def look(self,angle):
        #====================================================
        #Change the angle to the one specified.
        #====================================================
        self.angle = [angle[0],angle[1],angle[2]]
        
def render(polylist, lights, camera, surface):
    
    #====================================================
    #Undraw everything
    #====================================================
    surface.fill((50,50,50))
    
    #====================================================
    # Make camera the origin and rotate everything about it
    # by the camera's rotation. Make life easy. Illuminate
    # the polygon.
    #====================================================
    renderlist = polylist
    for polygon in renderlist:
        
        polygon.shown = "yes"
        #====================================================
        #Light Polygon
        #====================================================
        polygon.colourmod = [0,0,0]
        for light in lights:
            illuminate(polygon, light)
        
        #====================================================
        #Rotate the polgon about the camera
        #====================================================
        output_points = []
        for point in polygon.points:
            output_points.append(rotate_point_about_camera(point,camera.position,camera.angle))
        
        polygon.points = output_points
        polygon.reaverage()
        
        #====================================================
        #For textured polygons, update P, M and N
        #====================================================
        if polygon.texture is not None:
            #====================================================
            #P
            #====================================================
            output_P = rotate_point_about_camera(polygon.P,camera.position,camera.angle)
            
            #====================================================
            #M
            #====================================================
            output_M = add_3D(polygon.M,polygon.P)
            output_M = rotate_point_about_camera(output_M,camera.position,camera.angle)
            output_M = minus_3D(output_M,output_P)
            
            #====================================================
            #N
            #====================================================
            output_N = add_3D(polygon.N,polygon.P)
            output_N = rotate_point_about_camera(output_N,camera.position,camera.angle)
            output_N = minus_3D(output_N,output_P)
            
            #====================================================
            #Update
            #====================================================
            polygon.P = output_P
            polygon.M = output_M
            polygon.N = output_N
    
        #====================================================
        #Prepare the polygons for projection.
        #====================================================
        prepare_polygon_3D(camera,polygon)
    
        #====================================================
        #Project the polygon.
        #====================================================
        if polygon.shown == "yes":
            project_polygon(polygon, camera.size, camera.dist)

    #====================================================
    #Draw
    #====================================================
    filler(renderlist, camera, surface)
    
    #====================================================
    #Join the dots.
    #====================================================
    #for poly in polygons:
        #pygame.draw.lines(surface,(0,0,0),1,poly.points,3)
