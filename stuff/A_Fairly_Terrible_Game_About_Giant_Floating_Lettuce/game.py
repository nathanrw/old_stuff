import objects
import pygame
import maths2D
import pickle
from pygame.locals import *

class Game():

    def __init__(self):

        pygame.init()

        self.screen = pygame.display.set_mode((1024,768))
        self.screencentre = (self.screen.get_width()/2, self.screen.get_height()/2)
        pygame.display.set_caption("Lettuce In Space")
        
        self.bodies = []
        self.lettuce = []

        self.clock = pygame.time.Clock()

        self.fps = 30

        self.shadowMaskSurface = pygame.Surface(self.screen.get_rect().size)
        self.shadowMaskSurface.set_colorkey((255,255,255))
        self.shadowMask = pygame.mask.from_surface(self.shadowMaskSurface)

        self.loadLevel()
    
    def loadLevel(self):
        self.bodies = pickle.load(open("level.txt", "r"))
        self.sun = self.bodies[0]

        self.seeds = 10

        self.score = 0

    def update(self):

        for body in self.bodies:
            body.update()
            try:
                if self.shadowMask.get_at(maths2D.add2D(body.getPosition(), self.screencentre)):
                    body.inshadow = 1
                else:
                    body.inshadow = 0
            except:
                body.inshadow = 1

        for A in self.bodies:
            for B in self.bodies:
                if A == B: continue
                A.fall(B)
                if A.collide(B):
                    if isinstance(A, objects.Lettuce):
                        self.score += A.getMass()**1.1
                    if isinstance(B, objects.Lettuce):
                        self.score += B.getMass()**1.1

        if self.seeds == 0 and len(self.lettuce) == 0: return 0

        return 1

    def getInput(self):

        for e in pygame.event.get():

            if e.type == QUIT:
                return 0

            elif e.type == KEYDOWN:

                if e.key == K_ESCAPE:
                    return 0

                #elif e.key == K_y:
                #
                #    pickle.dump(self.bodies, open("level.txt", "w"))

            elif e.type == MOUSEBUTTONDOWN:

                #if e.button == 3:
                #    pos = maths2D.sub2D(pygame.mouse.get_pos(), self.screencentre)
                #    self.spawnAsteroid(pos, random.randrange(6, 20))

                if e.button == 1:
                    if self.seeds > 0:
                        pos = maths2D.sub2D(pygame.mouse.get_pos(), self.screencentre)
                        self.spawnLettuce(pos, 7)
                        self.seeds -= 1

        return 1

    def draw(self):

        self.screen.fill((0,0,0))

        for body in self.bodies:
            body.draw(self.screen)

        self.shadowMaskSurface.fill((255,255,255))

        for body in self.bodies:
            if body != self.sun:
                shadow = body.calculateShadow(self.screen.get_rect())
                pygame.draw.polygon(self.shadowMaskSurface, (0,0,0), shadow)

        self.screen.blit(self.shadowMaskSurface, (0,0))
        self.shadowMask = pygame.mask.from_surface(self.shadowMaskSurface)

        self.drawText()
        pygame.display.update()

    def mainLoop(self):
        while 1:
            if not self.getInput():
                pygame.display.quit()
                return
            if not self.update():
                break
            self.draw()
            self.clock.tick(self.fps)

        self.screen.fill((0,0,0))
        font = pygame.font.Font(None, 48)
        text = "Score: " + str(self.score)
        self.screen.blit(font.render(text, 1, (255,255,255)), (10,10))
        pygame.display.update()
        pygame.time.wait(2000)
        pygame.display.quit()

    def drawText(self):
        font = pygame.font.Font(None, 24)
        
        
        txt_col = (255,255,255)
        fps_str = "FPS: " + str(int(self.clock.get_fps()))
        self.screen.blit(font.render(fps_str,1,txt_col), (10,10))
        seeds_str = "Lettuce Seeds: " + str(self.seeds)
        self.screen.blit(font.render(seeds_str,1,txt_col), (10,25))
        score_str = "Score: " + str(int(self.score))
        self.screen.blit(font.render(score_str,1,txt_col), (10,40))
    
    #***************************************************************************

    def spawnAsteroid(self, position, radius):
        asteroid = objects.Asteroid(position, (0,0), 10000, radius, self.bodies)
        v = asteroid.calculateOrbitalVelocity(self.sun)
        asteroid.setVelocity(v)

    def spawnLettuce(self, position, radius):
        lettuce = objects.Lettuce(position, (0,0), 10, radius, self.bodies, self.lettuce)
        v = lettuce.calculateOrbitalVelocity(self.sun)
        lettuce.setVelocity(v)
