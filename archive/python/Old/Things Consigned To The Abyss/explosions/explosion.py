import pygame, os
from pygame.locals import *

SCREENRECT = Rect(0, 0, 640, 480)

def ImportPNG(name):
    ULTRApath = os.path.join('data', name)
    print ULTRApath
    try:
        image = pygame.image.load(ULTRApath)
    except pygame.error, message:
        print 'Cannot load image'
        raise SystemExit, message
    image = image.convert_alpha()
    return image

def ImportImages(name, numimages, colorkey=None):
    Images = []
    counter = 0
    while counter <= numimages:
        fullname = name + "_" + str(counter) + ".png"
        if colorkey is None or colorkey is -1:
            try:
                Images.append(ImportImg(fullname, colorkey))
            except:
                print"Error"
                return Images
        elif colorkey is 1:
            try:
                Images.append(ImportPNG(fullname))
            except:
                print "Error"
                return Images
            
        counter += 1

    return Images
        
def main():
    pygame.init()

    screen = pygame.display.set_mode(SCREENRECT.size)

    # make background
    background = pygame.Surface(SCREENRECT.size).convert()
    background.fill((0, 0, 255))
    lol = smoke()
    lolsprite = pygame.sprite.RenderClear(lol)
    lolsprite.draw(background)
    screen.blit(background, (0, 0))
    pygame.display.update()

    # keep track of sprites
    all = pygame.sprite.RenderUpdates()

    # keep track of time
    clock = pygame.time.Clock()

    # game loop
    while 1:

        # get input
        for event in pygame.event.get():
            if event.type == QUIT   \
               or (event.type == KEYDOWN and    \
                   event.key == K_ESCAPE):
                return

        # clear sprites
        all.clear(screen, background)

        # update sprites
        all.update()

        # redraw sprites
        dirty = all.draw(screen)
        pygame.display.update(dirty)

        # maintain frame rate
        clock.tick(60)

if __name__ == '__main__': main()
