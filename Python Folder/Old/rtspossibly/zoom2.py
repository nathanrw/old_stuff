#zoomzoom2
import pygame, os
from pygame.locals import *

def ImportImg(name, folder, colorkey=None):
    ULTRApath = os.path.join(folder, name)
    print ULTRApath
    try:
        image = pygame.image.load(ULTRApath)
    except pygame.error, message:
        print 'Cannot load image'
        raise SystemExit, message
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image

class View():
    
    def __init__(self, x, y):
        self.rect = pygame.Rect(0,0,x,y)
        self.zoom = 100
        
    def bounds(self, bottom, right):
        self.bottom = bottom
        self.right = right
        
    def check(self):
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > self.bottom:
            self.rect.bottom = self.bottom
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self.right:
            self.rect.right = self.right
            
    def _move_one(self, magnitude, direction):
        if direction == "up":
            self.rect = self.rect.move(0,-magnitude)
        elif direction == "down":
            self.rect = self.rect.move(0,magnitude)
        elif direction == "left":
            self.rect = self.rect.move(-magnitude,0)
        elif direction == "right":
            self.rect = self.rect.move(magnitude,0)

    def _zoom(self,sign):
        width = 10 * sign
        height = 10 * sign

        if (self.zoom + 10*sign) > -100 and (self.zoom + 10*sign) < 300:
            self.rect = self.rect.inflate(width,height)
            self.zoom += 10*sign

def getslice(source, rect):
    rect = Rect(rect)
    Image = pygame.Surface(rect.size).convert()
    Image.blit(source,(0,0),rect)
    return Image

def main():
    pygame.init()
    SCREENRECT = (1024,768)
    DISPLAYRECT = SCREENRECT
    screen = pygame.display.set_mode(SCREENRECT, DOUBLEBUF)
    view = View(DISPLAYRECT[0], DISPLAYRECT[1])
    theimage = ImportImg("bill.jpg","")
    view.bounds(theimage.get_height(),theimage.get_width())

    while 1:
        for event in pygame.event.get():
            if event.type == QUIT   \
               or (event.type == KEYDOWN and    \
                   event.key == K_ESCAPE):
                pygame.quit()
                return
            if event.type == KEYDOWN:
                if event.key == K_w:
                    view._move_one(25, "up")
                elif event.key == K_a:
                    view._move_one(25, "left")
                elif event.key == K_d:
                    view._move_one(25, "right")
                elif event.key == K_s:
                    view._move_one(25, "down")
                elif event.key == K_k:
                    view._zoom(1)
                elif event.key == K_l:
                    view._zoom(-1)

        output_image = getslice(theimage, (view.rect.left,view.rect.top,view.rect.width,view.rect.height))
        output_image = pygame.transform.scale(output_image, DISPLAYRECT)
        screen.blit(output_image,(0,0))
        pygame.display.update()

if __name__ == "__main__": main()
