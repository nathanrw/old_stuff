#zoomzoom
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
    def __init__(self, xy, zoompercent):
        self.width = xy[0]
        self.height = xy[1]
        self.zoompercent = zoompercent
        self.centerpoint = (xy[0]/2,xy[1]/2)
    def _move(self,xy):
        self.centerpoint = (self.centerpoint[0]+xy[0],
                            self.centerpoint[1]+xy[1])
        print self.center
    def _zoom(self,sign):
        if self.zoompercent > 2 and self.zoompercent < 200:
            if sign == -1:
                self.zoompercent -= 2
            elif sign == 1:
                self.zoompercent += 2

            self.centerpoint = ((self.centerpoint[0]/100*self.zoompercent),(self.centerpoint[1]/100*self.zoompercent))
    
def main():
    pygame.init()

    SCREENRECT = (400,400)
    screen = pygame.display.set_mode(SCREENRECT, DOUBLEBUF)

    view = View(SCREENRECT, 100)
    
    #Import The Image
    theimage = ImportImg("Bal-map4.jpg", "")

    while 1:

        for event in pygame.event.get():
            if event.type == QUIT   \
               or (event.type == KEYDOWN and    \
                   event.key == K_ESCAPE):
                pygame.quit()
                return
            if event.type == KEYDOWN:
                if event.key == K_s:
                    if (view.centerpoint[1] + (view.height/2)) < ((theimage.get_height()/100)*view.zoompercent):
                        view._move((0,5))
                if event.key == K_d:
                    if (view.centerpoint[0] + (view.width/2)) < ((theimage.get_width()/100)*view.zoompercent):
                        view._move((5,0))
                if event.key == K_a:
                    if (view.centerpoint[0] + (view.width/2)) < ((theimage.get_width()/100)*view.zoompercent):
                        view._move((-5,0))
                if event.key == K_w:
                    if (view.centerpoint[1] + (view.height/2)) < ((theimage.get_height()/100)*view.zoompercent):
                        view._move((0,-5))
                if event.key == K_t:
                    view._zoom(1)
                if event.key == K_g:
                    view._zoom(-1)

        zoomed = pygame.transform.scale(theimage,(((theimage.get_width()/100)*view.zoompercent),(theimage.get_height()/100) * view.zoompercent))

        dx = view.centerpoint[0] - (view.width/2)
        dy = view.centerpoint[1] - (view.height/2)
        
        thing = pygame.transform.chop(zoomed,(dx,dy,view.width,view.height))
        screen.blit(thing,(0,0))
        pygame.display.update()

if __name__ == "__main__": main()
