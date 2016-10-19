import pygame
from pygame.locals import *

SCREENRECT = Rect(0, 0, 800, 320)

def main():
    pygame.init()

    screen = pygame.display.set_mode(SCREENRECT.size, DOUBLEBUF)

    # make background
    background = pygame.Surface(SCREENRECT.size).convert()
    background.fill((0, 0, 255))
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
                pygame.display.quit()
                return

        # clear sprites
        all.clear(screen, background)

        #Game Logic

        # update sprites
        all.update()

        # redraw sprites
        dirty = all.draw(screen)
        pygame.display.update(dirty)

        # maintain frame rate
        clock.tick(40)

if __name__ == '__main__': main()
