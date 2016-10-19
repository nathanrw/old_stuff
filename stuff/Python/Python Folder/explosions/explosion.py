#
# scriptedfun.com
#
# Screencast #1
# Barebones Pygame Application
#

import pygame, os
from pygame.locals import *

SCREENRECT = Rect(0, 0, 640, 480)

def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', fullname
        raise SystemExit, message
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

class smoke(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image("smoke.bmp", -1)

    def update(self):
        return
        
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
