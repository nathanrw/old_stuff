#The Amazing Grid Thing Simulator
#Made by Nathan.

#Import necessities.
import pygame
import random
from random import *
from pygame.locals import *

#Classes for the squares moving around.
import dots
from dots import *

#States the obvious, obviously
print "IT'S ON!"

#Gridmaking function.
def makegrid(tilesize,bgx,bgy):

    #Set up the surfaces
    bg = pygame.Surface((bgx,bgy))
    tile = pygame.Surface((tilesize,tilesize))
    tilein = pygame.Surface((tilesize-2,tilesize-2))

    #Fill the surfaces and make a tile
    tilein.fill((200,200,200))
    tile.fill((60,60,60))
    tile.blit(tilein, (1,1))

    #Calculate the number of tiles
    tilesx = bgx/tilesize
    tilesy = bgy/tilesize

    #Nested loop constructs a grid with tilesy rows and tilesx columns.
    countery = tilesy
    while countery > 0:
        countery -= 1
        counterx = tilesx
        while counterx > 0:
            counterx -= 1
            bg.blit(tile,(tilesize*counterx,tilesize*countery))

    #Returns the completed grid.
    return bg

#Main Function
def main(bgx, bgy, tilesize):

    pygame.font.init()

    #Calculate the number of tiles.
    tilesx = bgx/tilesize
    tilesy = bgy/tilesize
    numtiles = tilesx*tilesy

    #Make the clock object
    clock = pygame.time.Clock()

    #Make the display
    screen = pygame.display.set_mode((bgx+40,bgy+100), DOUBLEBUF)
    screen.fill((120,120,120))

    #Make the background and grid.
    grid = makegrid(tilesize, bgx, bgy)
    background = grid.convert()

    #Tracking variables et cetera.
    running = 1
    deaths = 0
    squares_alive = 0
    reapers_alive = 0
    FPS = 0
    Time = 0.0
    Timer = 0.0
    minutes = 0
    measure = "s"

    #Sprite Groups
    dot_sprite = pygame.sprite.RenderClear()
    reaper_sprite = pygame.sprite.RenderClear()

    #Main loop
    while running == 1:

        #Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = 0

        #Add squares randomly until 45.
        if randrange(0,10,1) == 1 and len(dot_sprite)<45:
            dot_sprite.add(dot(tilesize))

        #Keep reapers at 5
        if len(reaper_sprite) < 5:
            reaper_sprite.add(reaper(tilesize))

        #Clear Sprites
        dot_sprite.clear(screen,background)
        reaper_sprite.clear(screen,background)

        #Update Sprites
        dot_sprite.update()
        reaper_sprite.update()

        #Reaping
        for kill in pygame.sprite.groupcollide(reaper_sprite,dot_sprite,0,1):
            deaths += 1

        #Follow The Reaper. Or Rather, LEG IT!
        for a in dot_sprite:
            for b in reaper_sprite:
                
                #X Movement Of Squares
                if b.tile[0] <= a.tile[0]+4 and b.tile[0] > a.tile[0]:
                    a.xmove = -1
                elif b.tile[0] >= a.tile[0]-4 and b.tile[0] < a.tile[0]:
                    a.xmove = 1
                    
                #Y Movement Of Squares
                if b.tile[1] <= a.tile[1]+4 and b.tile[1] > a.tile[1]:
                    a.ymove = -1
                elif b.tile[1] >= a.tile[1]-4 and b.tile[1] < a.tile[1]:
                    a.ymove = 1

        squares_alive = len(dot_sprite)
        reapers_alive = len(reaper_sprite)

        SquaresAlive = "Squares Alive: " + str(squares_alive)
        ReapersAlive = "Reapers Alive: " + str(reapers_alive)
        Deaths = "Reaper Killcount: " + str(deaths)
        FrameRate = "FPS: " + str(int(FPS))
        TimeText = "Time (" + measure +"): " + str(Timer)

        fontsize = 22
        font = pygame.font.Font(None, fontsize)
	
        SquaresAliveText = font.render(SquaresAlive, 1, (230, 230, 230))
        ReapersAliveText = font.render(ReapersAlive, 1, (230, 230, 230))
        KillCountText = font.render(Deaths, 1, (230, 230, 230))
        FPSText = font.render(FrameRate, 1, (230, 230, 230))
        TimeText = font.render(TimeText, 1, (230, 230, 230))

        #Make the screen grey and put the blank grid back.
        screen.fill((120,120,120))
        screen.blit(background,(20,20))

        Text3Y = 600 + fontsize*3 + 4
        Text2Y = 600 + fontsize*2 + 4
        Text1Y = 600 + fontsize*1 + 4

        #Draw Text.

        screen.blit(SquaresAliveText, (22,Text1Y))
        screen.blit(KillCountText, (22,Text2Y))
        screen.blit(ReapersAliveText,(22,Text3Y))
        
        screen.blit(FPSText,(220,Text1Y))
        screen.blit(TimeText,(220,Text2Y))

        #Draw Sprites
        dot_sprite.draw(screen)
        reaper_sprite.draw(screen)
        
        #Flip the display
        pygame.display.flip()

        #Set FPS limit.
        clock.tick(20)

        FPS = clock.get_fps()
        Time = clock.get_time() + Time
        if minutes == 0:
            Timer = int(Time/1000)
            if Timer >= 60:
                minutes = 1
                measure = "m"
        elif minutes == 1:
            Timer = int((Time/1000)/60)

    #Gets rid of the window.
    pygame.display.quit()

    #States the obvious, in case you didn't notice the window disappear.
    print "IT'S OFF"
    #Dead Squares.
    print "Bodycount: ", deaths
    print "Reapers: ", reapers_alive
    print "Squares Alive: ", squares_alive

#Calls the main function and gives it the window size and the tile size.
main(800, 600, 20)
            
            
