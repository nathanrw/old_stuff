#3D Spaceship Thing

#Import Libraries
import os, sys
import pygame; from pygame.locals import *

#Import additional files
from functions import *
from get_input import *
from entities import *

#Get external resources
import resources

#For speed, import psyco.
try:
    import psyco
    psyco.full()
except: 
    print "Failed to import Psyco"

def main():

    #Start pygame.
    pygame.init()

    #Some pre written display sizes.
    RES_1 = (200,150)
    RES_2 = (240,150)
    RES_3 = (800,600)
    RES_4 = (1280,800)
    RES_5 = (1680,1050)
    
    #Set the size of the display, whether or not the display is fullscreen,
    #whether or not the windowsize will be inflated and the factor by which
    #the window is inflated.
    WINDOWSIZE = RES_4
    ISFULLSCREEN = 0
    TINYWINDOW = 0
    FACTOR = 3.2
    
    #Set the framerate, whether or not statistics such as the camera position
    #are shown, and whether or not the framerate is shown.
    FRAMERATE = 30
    STATS = 0
    FPS = 1

    #Create lists for collected entities and lights.
    ENTITIES = []
    LIGHTS = []
    
    #Groups for different types of entity
    
    ##Group for ships. May need to be split.
    SHIPS = []
    TURRETS = []
    
    ##Group for scenery - anything that doesn't need to _do_
    ##anything.
    SCENERY = []
    
    ##Group for effects. These will not be illuminated - 
    ##they will typically light sources themselves.
    EFFECTS = []
    
    ##Group for projectiles. A misnomer in that this includes lasers
    ##and things.
    PROJECTILES = []
    
    #Groups for different types of lights
    
    ##Impermanent lights - for explosions, lasers, etc.
    TEMP_LIGHTS = []
    
    #Permanent light sources - for suns, or anything that doesn't
    #need to move or disappear.
    PERM_LIGHTS = []

    #If a really low resolution is not being inflated to fill the window,
    #windowsize is used for the size of the screen.
    if not TINYWINDOW:
        if ISFULLSCREEN:
            screen = pygame.display.set_mode(WINDOWSIZE, DOUBLEBUF | HWSURFACE | FULLSCREEN)
        else:
            screen = pygame.display.set_mode(WINDOWSIZE, DOUBLEBUF)
            
    #If this is not so, WINDOWSIZE is multiplied by FACTOR and then used
    #as the size of the screen.
    elif TINYWINDOW:
        if ISFULLSCREEN:
            NEWWINDOWSIZE = (WINDOWSIZE[0]*FACTOR,WINDOWSIZE[1]*FACTOR)
            screen = pygame.display.set_mode(NEWWINDOWSIZE, DOUBLEBUF | HWSURFACE | FULLSCREEN)
        else:
            NEWWINDOWSIZE = (WINDOWSIZE[0]*FACTOR,WINDOWSIZE[1]*FACTOR)
            screen = pygame.display.set_mode(NEWWINDOWSIZE, DOUBLEBUF)

    #Window is titled.
    pygame.display.set_caption("3D Spaceships Thing")

    CLOCK = pygame.time.Clock()

    #Initial position and angle of the camera.
    POS = [0,-2000,0]
    ANGLE = [-90,0,0]
    
    #Create the camera, the surface drawn to from the camera, and the
    #font used for statistics.
    CAMERA_ONE = camera(WINDOWSIZE, POS, ANGLE)
    SURFACE_ONE = pygame.Surface((WINDOWSIZE))
    FONT = pygame.font.Font(None, 18)
    
    ###
    
    SHIPS.append(Ship(50,[0,0,0],[-20,0,0],[0,0,0]))
    for ship in SHIPS:
        TURRETS += ship.turrets
    PERM_LIGHTS.append(Light([-3000,-3000,-3000],3))
    
    ###
    
    #Main loop starts here.
    while 1:
        #Input from keyboard.
        if accept_input(pygame.event.get(), CAMERA_ONE) == "quit":
            pygame.quit()
            return
        
        #Update Entities
        
        for ship in SHIPS:
            ship.update()
        for turret in TURRETS:
            p = turret.update()
            if p != 0:
                PROJECTILES += p
        for n, projectile in enumerate(PROJECTILES):
            projectile.update()
            if projectile.state == "dead":
                del PROJECTILES[n]
        for n, effect in enumerate(EFFECTS):
            effect.update()
            if effect.state == "dead":
                del EFFECTS[n]
        
        #Update Lights
        for light in TEMP_LIGHTS:
            light.update()

        #Combine different lights and entities into ENTITIES
        #and LIGHTS for drawing.
        ENTITIES = SHIPS + SCENERY + EFFECTS + TURRETS + PROJECTILES
        LIGHTS = TEMP_LIGHTS + PERM_LIGHTS

        #Get polygons from entities in order to draw them.
        POLYGONS = []
        
        for ENTITY in ENTITIES:
            for polygon in ENTITY.return_polygons():
                POLYGONS.append(polygon)
        
        #Draw everything.
        render(POLYGONS,LIGHTS,CAMERA_ONE,SURFACE_ONE)
        
        #Blit SURFACE_ONE to the screen.
        if not TINYWINDOW:
            screen.blit(SURFACE_ONE, (0,0))
        else:
            screen.blit(pygame.transform.scale(SURFACE_ONE,NEWWINDOWSIZE),(0,0))
            
        #Blit text to the screen
        if FPS:
            screen.blit(FONT.render("FPS: " + str(int(CLOCK.get_fps())),1,(250,250,250)),(5,5))

        if STATS:
            screen.blit(FONT.render("Camera Position: " + str(CAMERA_ONE.position),1,(250,250,250)),(5,30))
            screen.blit(FONT.render("Camera Rotation: " + str(CAMERA_ONE.angle),1,(250,250,250)),(5,55))
            screen.blit(FONT.render("WASD to move, IJKL to rotate about x and y,",1,(250,250,250)),(5,80))
            screen.blit(FONT.render("and OP to rotate about z.",1,(250,250,250)),(5,105))
        
        #Show
        pygame.display.flip()
        
        #Maintain framerate.
        CLOCK.tick(FRAMERATE)

if __name__ == "__main__": main()