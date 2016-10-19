""" spaceGE.py 
    extend the Scene class for input
    and demonstrate space-style motion
"""

import pygame, gameEngine
class Game(gameEngine.Scene):
    def __init__(self):
        gameEngine.Scene.__init__(self)
        self.setCaption("Space-style Motion in GameEngine")
        self.ship = gameEngine.SuperSprite(self)
        self.ship.setImage("ship.gif")
        self.sprites = [self.ship]
    
    def update(self):
        #change rotation to change orientation of ship
        #but not direction of motion
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.ship.rotateBy(-5)
        
        if keys[pygame.K_LEFT]:
            self.ship.rotateBy(5)
        
        if keys[pygame.K_UP]:
            #add a force vector to the ship in the
            #direction it's currently pointing
            self.ship.addForce(.2, self.ship.rotation)

def main():
    game = Game()
    game.start()
        
if __name__ == "__main__":
    main()
