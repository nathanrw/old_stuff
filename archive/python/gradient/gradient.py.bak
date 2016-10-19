import pygame
from pygame.locals import *

def transparencyGradient(w, h, rgba):
    
    r, g, b, a = rgba
    
    surf = pygame.Surface((w, h), SRCALPHA)
    
    # The whole thing will be transparent, so there is no
    # need to do anything.
    if rgba[3] == 0:
        return surf
    
    pixels = pygame.PixelArray(surf)
    
    x = 0
    y = 0
    
    # Amount to change a by each time y is incremented.
    da = -a/float(h)
    
    while y < h:
        
        while x < w:
            
            pixels[x][y] = (r, g, b, int(a))
            
            x += 1
        
        x = 0
        y += 1
        
        a += da
    
    return surf

def main():
    
    pygame.init()
    
    screen = pygame.display.set_mode((800,600))
    
    surf = transparencyGradient(100,20,(0,0,0,255))
    
    screen.fill((255,255,255))
    
    screen.blit(surf, (10,10))
    
    pygame.display.update()
    
    pygame.time.wait(2000)
    
if __name__ == '__main__':
    main()