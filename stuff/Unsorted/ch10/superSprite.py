""" superSprite.py 
    show a very basic form of supersprite
"""

import pygame, gameEngine

def main():
    game = gameEngine.Scene()
    ship = gameEngine.SuperSprite(game)
    
    #customize the ship sprite
    ship.setImage("ship.gif")
    ship.setAngle(135)
    ship.setSpeed(5)
    ship.setBoundAction(ship.BOUNCE)
    
    #customize the scene
    game.setCaption("Introducing Super Sprite!")
    game.background.fill((0x33, 0x33, 0x99))
    game.sprites = [ship]
    
    #let 'er rip!
    game.start()
    
if __name__ == "__main__":
    main()