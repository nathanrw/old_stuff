import pygame
from vec2d import vec2d

class Widget():
    
    def __init__(self):
        self.children = []
        self.parent = None
        self.position = vec2d(0,0)
        self.surface = None
        self.dirty = 1
        self.hasfocus = 0
    
    def handlePygameEvent(self, event):
        
        if len(self.children) != 0:
            childevent = pygame.event.Event(event.type, event.dict)
            if hasattr(childevent, "pos"):
                childevent.pos = vec2d(event.pos) - self.position
            for child in self.children:
                child.handlePygameEvent(childevent)
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.handleMouseButtonDown(event.button, event.pos)
        
        elif event.type == pygame.MOUSEBUTTONUP:
            self.handleMouseButtonUp(event.button, event.pos)
        
        elif event.type == pygame.MOUSEMOTION:
            self.handleMouseMotion(event.rel, event.pos)
        
        elif event.type == pygame.KEYDOWN:
            self.handleKeyDown(event.key, event.unicode)
            
        elif event.type == pygame.KEYUP:
            self.handleKeyUp(event.key)
    
    def handleMouseButtonDown(self, button, pos):
        pass
    
    def handleMouseButtonUp(self, button, pos):
        if self.mouseover: self.hasfocus = 1
        else: self.hasfocus = 0
    
    def handleMouseMotion(self, rel, pos):
        self.mouseover = self.rect.collidepoint(*pos)
    
    def handleKeyDown(self, key, unicode):
        pass
    
    def handleKeyUp(self, key):
        pass
    
    def loseFocus(self):
        self.hasfocus = 0
    
    def add(self, child):
        self.children.append(child)
        child.parent = self
    
    def remove(self, child):
        self.children.remove(child)
        child.parent = None
    
    def destroy(self):
        self.parent.remove(self)
    
    def get_rect(self):
        rect = self.surface.get_rect()
        rect.topleft = self.position
        return rect
    
    def render(self):
        pass
    
    def update(self):
        pass
    
    def draw(self, surface, origin=vec2d(0,0)):
        self.render()
        surface.blit(self.surface, origin+self.position)
        for child in self.children:
            child.draw(surface, origin+self.position)
    
    rect = property(fget=get_rect)

class BorderedRectangle():
    
    def __init__(self, topleft, top, topright, right, bottomright, bottom, 
                 bottomleft, left, middle):
        
        self.topleft = topleft
        self.top = top
        self.topright = topright
        self.right = right
        self.bottomright = bottomright
        self.bottom = bottom
        self.bottomleft = bottomleft
        self.left = left
        self.middle = middle
    
    def render(self, width, height):
        
        self.width = width
        self.height = height
        
        self.surface = pygame.Surface((width,height))
        
        self.surface.blit(self.topleft, (0,0))
        self.surface.blit(self.topright,(self.width-self.topright.get_width(),0))
        self.surface.blit(self.bottomright,(self.width-self.bottomright.get_width(),self.height-self.bottomright.get_height()))
        self.surface.blit(self.bottomleft,(0,self.height-self.bottomleft.get_height()))
        
        self.draw_left()
        self.draw_right()
        self.draw_top()
        self.draw_bottom()
        self.draw_middle()
        
        return self.surface
    
    def draw_left(self):

        x = 0
        y = self.topleft.get_height()
        
        w = self.left.get_width()
        h = self.height-self.topleft.get_height()-self.bottomleft.get_height()

        pos = (x,y)
        size = (w,h)
        
        self.tile(self.left, self.surface, pygame.Rect(pos,size))
        
    def draw_right(self):

        x = self.width - self.right.get_width()
        y = self.topright.get_height()
        
        w = self.right.get_width()
        h = self.height-self.topright.get_height()-self.bottomright.get_height()

        pos = (x,y)
        size = (w,h)
        
        self.tile(self.right, self.surface, pygame.Rect(pos,size))
        
    def draw_top(self):
        
        x = self.topleft.get_width()
        y = 0
        
        w = self.width - self.topright.get_width() - self.topleft.get_width()
        h = self.top.get_height()

        pos = (x,y)
        size = (w,h)
        
        self.tile(self.top, self.surface, pygame.Rect(pos,size))
        
    def draw_bottom(self):
        
        x = self.bottomleft.get_width()
        y = self.height-self.bottom.get_height()
        
        w = self.width - self.bottomright.get_width() - self.bottomleft.get_width()
        h = self.bottom.get_height()

        pos = (x,y)
        size = (w,h)
        
        self.tile(self.bottom, self.surface, pygame.Rect(pos,size))
        
    def draw_middle(self):
        x = self.topleft.get_width()
        y = self.topleft.get_height()
        
        w = self.width - self.right.get_width() - self.left.get_width()
        h = self.height - self.top.get_height() - self.bottom.get_height()

        pos = (x,y)
        size = (w,h)
        
        self.tile(self.middle, self.surface, pygame.Rect(pos,size))
        
    def tile(self, image, dest, rect):
        
        x_step = image.get_width()
        y_step = image.get_height()
        
        x = 0
        
        while x < rect.w:
            y=0
            while y < rect.h:
                dest.blit(image, (x+rect.x,y+rect.y))
                y += y_step
            x += x_step

class TextRect():
    
    def render():
        pass

class Panel(Widget):
    
    def __init__(self, width, height, borderedRectangle):
        Widget.__init__(self)
        self.width = width
        self.height = height
        self.borderedRectangle = borderedRectangle
        self.sourceImage = self.borderedRectangle.render(self.width,self.height)
        self.surface.blit(self.sourceImage,(0,0))
        
    def render(self):
        if self.dirty:
            self.surface.blit(self.sourceImage,(0,0))
            self.dirty = 0

class TextBox(Widget):
    
    def __init__(self, font, width, height, borderedRectangle):
        
        Widget.__init__(self)
        
        self.width = width
        self.height = height
        
        self.borderedRectangle = borderedRectangle
        
        self.font = font
        
        self.text = ""
        self.textColour = (255,255,255)
        self.antialias = 1
        
        self.backimage = self.borderedRectangle.render(self.width,self.height)
        
        self.surface = pygame.Surface((self.width,self.height),pygame.SRCALPHA)
        self.surface.blit(self.backimage,(0,0))
        
        self.keybuffer = []
        
        self.cursor = 0
        
        self.multiline = 1
    
    def handleKeyDown(self, key, unicode):
        if self.hasfocus:
            if unicode == "":
                pass
            else:
                self.keybuffer += unicode
    
    def handleKeyUp(self, key):
        pass
    
    def update(self):
        for key in self.keybuffer:
            if ord(key) == 8:
                if self.cursor != 0:
                    self.text = self.text[:self.cursor-1]+self.text[self.cursor:]
                    self.cursor -= 1
            elif ord(key) == 127:
                if self.cursor < len(self.text)-1:
                    self.text = self.text[:self.cursor]+self.text[self.cursor+1:]
                    self.cursor -= 1
            elif (not self.multiline) and ord(key) == 13:
                self.loseFocus()
            else:
                self.text = self.text[:self.cursor]+key+self.text[self.cursor:]
                self.cursor += 1
                
            self.keybuffer = self.keybuffer[1:]
            self.dirty = 1
        
    def render(self):
        if self.dirty:
            self.surface = pygame.Surface((self.width,self.height),pygame.SRCALPHA)
            self.surface.blit(self.backimage,(0,0))
            text = self.font.render(self.text,self.antialias,self.textColour)
            rect = text.get_rect()
            rect.center = self.surface.get_rect().center
            self.surface.blit(text,rect)
            self.dirty = 0

def main():
    
    pygame.init()
    screen = pygame.display.set_mode((800,600))
    
    widgets = []
    
    font = pygame.font.Font(None, 14)
    
    
    tl= pygame.image.load("thin_topleft.png").convert_alpha()
    t=  pygame.image.load("thin_top.png").convert_alpha()
    tr= pygame.image.load("thin_topright.png").convert_alpha()
    r=  pygame.image.load("thin_right.png").convert_alpha()
    br= pygame.image.load("thin_bottomright.png").convert_alpha()
    b=  pygame.image.load("thin_bottom.png").convert_alpha()
    bl= pygame.image.load("thin_bottomleft.png").convert_alpha()
    l=  pygame.image.load("thin_left.png").convert_alpha()
    m=  pygame.image.load("thin_middle.png").convert_alpha()
    
    r = BorderedRectangle(tl,t,tr,r,br,b,bl,l,m)
    
    widgets.append(TextBox(font,150,25,r))
    
    while 1:
        
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                return
            for widget in widgets:
                widget.handlePygameEvent(e)
        screen.fill((0,0,0))
        for widget in widgets:
            widget.update()
            widget.draw(screen)
        pygame.display.update()

if __name__ == '__main__':
    main()