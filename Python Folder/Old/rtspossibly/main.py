#main.py - main file
import pygame, os, math
from pygame.locals import *

#Sorting functions

#Bubble sorrting function => Not that good.
#Goes along the list and compare everything, swapping if needed.
#Eventually, it's in order.
def bubblesort(data):
    n = 1;rmr = 1
    while rmr == 1:
        ptr = 0;ctr = 0;rmr = 0
        while ctr < len(data)-n:
            if data[ptr+1] < data[ptr]:
                data[ptr], data[ptr+1] = swap(data[ptr], data[ptr+1]);rmr = 1
            ctr += 1;ptr+=1
        n += 1
    return data

#Gets rid of recurring pieces of data.
#Useful for keeping the sprites in order.
def cullrecurring(data):
    Z = [];check = 1
    for x in data:
        check = 1
        for y in Z:
            if x == y:
                check = 0
        if check == 1: Z.append(x)
    return Z

#Swaps two values. Thinking about it, this is useless.
def swap(x,y):xo = x;x = y;y = xo;return x, y

#Endeth Sorters.

#T'importer
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

#Intelligent Falling > Gravitation
global gravity
gravity = -0.1

#Will load all data files. Hahar.
def LoadAllResources(resources):
    return resources

#Thine holy camera of antioch
class View():
    
    def __init__(self, x, y):
        self.rect = pygame.Rect(0,0,x,y)
        self.zoom = 100
        self.z = 100
        
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

    #Changes the height of the camera.
    def _zoom(self,sign):
        width = 10 * sign
        height = 10 * sign
        self.z += 5 * sign
        if (self.zoom + 10*sign) > -100 and (self.zoom + 10*sign) < 300:
            self.rect = self.rect.inflate(width,height)
            self.zoom += 10*sign

    #Checks the sprites to see which should be drawn.
    def spritecheck(self,spritegroup):
        #Gets the sprites to be drawn
        allsprites = spritegroup
        remaining = pygame.sprite.OrderedUpdates()
        for sprite in allsprites:
            if sprite.x < self.rect.right \
               and sprite.x+sprite.image.get_width() > self.rect.left \
               and sprite.y > self.rect.top \
               and sprite.y+sprite.image.get_height() < self.rect.bottom \
               and sprite.z + sprite.depth < self.z:
                remaining.add(sprite)

        #Orders the sprites.
        Z = []
        for sprite in remaining: Z.append(sprite.z)
        
        Z = bubblesort(cullrecurring(Z))
        old = pygame.sprite.OrderedUpdates()
        for sprite in remaining:
            old.add(sprite)
            
        remaining.empty()
        for x in Z:
            for sprite in old:
                if sprite.z == x:remaining.add(sprite)
        
        return remaining

#Unit class
class Unit(pygame.sprite.Sprite):
#class Unit():
    def __init__(self, stats, state, depth):
        pygame.sprite.Sprite.__init__(self)

        self.hp = stats[3][0]
        self.attack = stats[3][1]
        self.maxspeed = stats[3][2]
        self.armour = stats[3][3]

        self.xvel = state[0][0][0]
        self.yvel = state[0][0][1]
        self.zvel = state[0][0][2]
        self.x = state[0][1][0]
        self.y = state[0][1][1]
        self.z = state[0][1][2]
        
        self.depth = depth
        self.height = 0
        self.width = 0

        #Idle = anims[0] Move = anims[1] Attack = anims[2] Death = anims[3]

        self.anims = stats[0]
        self.current_anim = self.anims[0]
        self.image = self.current_anim[0]
        
        self.rect = self.image.get_rect()
        
        self.counter = 0
        self.limitcounter = 0

        self.updatecube()
        self.angle = 45

        self.player = 0

    def update(self):
        self.x += self.xvel
        self.y += self.yvel
        self.z += self.zvel
        
        if self.z < 0:
            self.z = 0
            self.zvel = 0
        if self.z > 0:self.zvel += gravity
        
        self.updatecube()
        
        self.angle = self.checkangle()
        
        self.image = pygame.transform.rotate(self.current_anim[self.counter],self.angle)

    def checkangle(self):

        if self.xvel > 0 and self.yvel < 0:
            self.angle = math.degrees(math.atan(self.xvel/self.yvel))
        elif self.xvel > 0 and self.yvel > 0:
            self.angle = -90 + math.degrees(math.atan(self.xvel/-self.yvel))
        elif self.xvel < 0 and self.yvel < 0:
            self.angle = math.degrees(math.atan(-self.xvel/-self.yvel))
        elif self.xvel < 0 and self.yvel > 0:
            self.angle = 90 + math.degrees(math.atan(-self.xvel/self.yvel))
        elif self.xvel == 0 and self.yvel > 0:
            self.angle = 180
        elif self.xvel == 0 and self.yvel < 0:
            self.angle = 0
        elif self.xvel > 0 and self.yvel == 0:
            self.angle = -90
        elif self.xvel < 0 and self.yvel == 0:
            self.angle = 90

        return self.angle

    def updatecube(self):
        self.cube = (self.rect.width,self.rect.height,self.depth)

    def changevel(self,x,y,z):
        self.xvel += x
        self.yvel += y
        self.zvel += z

#Some Nice Functions

def getslice(source, rect):
    rect = Rect(rect)
    Image = pygame.Surface(rect.size).convert()
    Image.blit(source,(0,0),rect)
    return Image

def draw_the_sprites(drawsprites, output_image):
    for sprite in drawsprites:
        scaling = sprite.z
        width = sprite.image.get_width() + int((sprite.image.get_width()*scaling)/10)
        height = sprite.image.get_height() + int((sprite.image.get_height()*scaling)/10)
        output_image.blit(pygame.transform.scale(sprite.image,(width,height)),(sprite.x-(width/2),sprite.y-(height/2)))
    return output_image

#Here endeth nice functions and starteth main.

def main():
    pygame.init()

    clock = pygame.time.Clock()
    
    SCREENRECT = (500,500)
    DISPLAYRECT = (SCREENRECT[0],SCREENRECT[1]-60)
    
    screen = pygame.display.set_mode(SCREENRECT, DOUBLEBUF)
    view = View(DISPLAYRECT[0], DISPLAYRECT[1])
    
    global theimage
    theimage = ImportImg("map.png","")
    themap = (theimage.get_width(),theimage.get_height())
    view.bounds(theimage.get_height(),theimage.get_width())

    allsprites = pygame.sprite.RenderClear()
    drawsprites = pygame.sprite.OrderedUpdates()

    #EXAMPLE: unit = [[anim1],[anim2],[anim3],[anim4]],[type],[id],[hp,attack,maxspeed,armour]]
    #EXAMPLE: state = [[[xvel,yvel,zvel],[x,y,z]],[player]]
    
    wizard = [[[ImportImg("unit.bmp","",-1)],[ImportImg("unit.bmp","")],[ImportImg("unit.bmp","")],[ImportImg("unit.bmp","")]],["wizard"],[00],[20,2,2,2]]
    #Ist Krieg.
    
    allsprites.add(Unit(wizard,
     [[[0,2,4],[200,200,0]],0],3))

    output_image = pygame.Surface((theimage.get_width(),theimage.get_height()))
    output_image.blit(theimage,(0,0))

    while 1:
        
        #Handle Input
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

        #Reset the output image.
        output_image = pygame.Surface((theimage.get_width(),theimage.get_height()))
        output_image.blit(theimage,(0,0))

        #Sort the sprites.
        if allsprites is not None:
            allsprites.update()
            drawsprites = view.spritecheck(allsprites)

        #Visible area.
        visible = (view.rect.left,view.rect.top,view.rect.width,view.rect.height)

        #Draw the sprites.
        output_image = draw_the_sprites(drawsprites,output_image)

        #Ready the output.
        output_image = getslice(output_image, visible)
        output_image = pygame.transform.scale(output_image, DISPLAYRECT)

        #Blit to screen + Display.
        screen.blit(output_image,(0,0))
        pygame.display.update()

        #Maintain FPS.
        clock.tick(35)

if __name__ == "__main__": main()
