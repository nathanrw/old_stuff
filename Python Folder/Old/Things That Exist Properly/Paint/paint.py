#The Amazing Paint Program

#Import

import pygame
from pygame.locals import *
pygame.font.init()

#Define Main

def load():
    try: #Incase you typo.
        image = pygame.image.load(raw_input("ENTER FILENAME: "))
    except: #Tells you your loading failed.
        lol = (pygame.Surface((200,200))).convert()
        font1 = pygame.font.Font(None, 36)
        loadfailed = font1.render("Load Failed.", 1, (250, 250, 250))
        msgpos = (100 - (loadfailed.get_width()/2)), 75
        lol.blit(loadfailed, msgpos)
        return lol
    image = image.convert()
    return image

def main():

    # Make the screen
    width = int(input("WIDTH:"))
    height = int(input("HEIGHT:"))
    screen = pygame.display.set_mode((width,height), DOUBLEBUF)
    screen.fill((255,255,255))

    # Control things
    running = 1
    drawing = 0

    # Start the clock
    clock = pygame.time.Clock()

    # Make the dot brush
    dot = pygame.Surface((1,1))
    dot.fill((0,0,0))

    # For lines
    oldpos = pygame.mouse.get_pos()

    # Black lines default
    linecol = (0,0,0)

    while running == 1:

        clock.tick(40) #FPS
        mpos = pygame.mouse.get_pos() #For lines + drawing
        mousepressed = pygame.mouse.get_pressed() # Controls drawing

        if mousepressed[0] == 1: #LMB
                drawing = 1
        if mousepressed[2] == 1: #RMB
                drawing = 2
        
        for event in pygame.event.get(): #The innards
            if event.type == QUIT:
                running = 0
                
            elif event.type == MOUSEBUTTONUP: #Stop drawing, fool!
                drawing = 0

            if event.type == KEYDOWN:
                if event.key == K_c: # Save
                    pygame.image.save(screen, raw_input("ENTER FILENAME: ")+".bmp")
                elif event.key == K_k: # Clear
                    screen.fill((255,255,255))
                elif event.key == K_q: # Red
                    linecol = (255,0,0)
                elif event.key == K_w: # Green
                    linecol = (0,255,0)
                elif event.key == K_e: # Blue
                    linecol = (0,0,255)
                elif event.key == K_r: # Light Blue
                    linecol = (0,255,255)
                elif event.key == K_t: # Yellow
                    linecol = (255,255,0)
                elif event.key == K_y: # Black
                    linecol = (0,0,0)
                    
                elif event.key == K_l: # Load
                    image = load()
                    size = [image.get_width(), image.get_height()]
                    pygame.display.quit
                    screen = pygame.display.set_mode(size, DOUBLEBUF)
                    screen.blit(image,(0,0))

                dot.fill(linecol) # Makes dot the right colour

        # If the LMB is down, draw a line from the old mouse position to
        # the new one.
        if drawing == 1: 
            #screen.blit(dot,mpos)
            #screen.blit(dot,(((mpos[0]+oldpos[0])/2),((mpos[1]+oldpos[1])/2)))
            pygame.draw.line(screen, linecol, oldpos, mpos)

        # If RMB is down, draw a dot at the mpos and a dot half way
        # between new and old mouse positions.
        if drawing == 2: 
            screen.blit(dot,(((mpos[0]+oldpos[0])/2),((mpos[1]+oldpos[1])/2)))

        pygame.display.flip() # Flip the display surface.
        oldpos = mpos # Update the old position

    print "Have a nice day"
    pygame.display.quit() # Get rid of the window

# The manual. Looks cool.
print """
NATHAN PAINT"""
print """
KEYS:
Q    |    RED
W    |    GREEN
E    |    BLUE
R    |    LIGHT BLUE
T    |    YELLOW
Y    |    BLACK

C    |    SAVE - ENTER FILENAME INTO CONSOLE, ANYTHING YOU WANT THAT IS .BMP
K    |    CLEAR - FILL SCREEN WHITE
L    |    LOAD - LOADS A PREVIOUS IMAGE

I    |    SET UNDO POINT
U    |    UNDO

LEFT MOUSE BUTTON    |    LINE
RIGHT MOUSE BUTTON   |    DOT
"""
main() # Tally ho, what what!
