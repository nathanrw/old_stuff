""" carGE.py 
    extend SuperSprite to add keyboard input
"""

import pygame, gameEngine

class Car(gameEngine.SuperSprite):
    def __init__(self, scene):
        gameEngine.SuperSprite.__init__(self, scene)
        self.setImage("car.gif")
    
    def checkEvents(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.turnBy(5)
        if keys[pygame.K_RIGHT]:
            self.turnBy(-5)
        if keys[pygame.K_UP]:
            self.speedUp(.2)
        if keys[pygame.K_DOWN]:
            self.speedUp(-.2)
            
        self.drawTrace()

def main():
    game = gameEngine.Scene()
    game.background.fill((0xCC, 0xCC, 0xCC))

    car = Car(game)
    game.sprites = [car]

    game.start()

if __name__ == "__main__":
    main()