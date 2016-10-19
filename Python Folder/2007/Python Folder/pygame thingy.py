import os, sys
import pygame
from pygame.locals import *

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

running = 1

def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', name
        raise SystemExit, message
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

def load_sound(name):
    class NoneSound:
        def play(self): pass
    if not pygame.mixer:
        return NoneSound()
    fullname = os.path.join('data', name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error, message:
        print 'Cannot load sound:', wav
        raise SystemExit, message
    return sound

pygame.init()
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption('YARGH')
pygame.mouse.set_visible(1)

background, background_rect = load_image(chimp.bmp)

if pygame.font:
    font = pygame.font.Font(None, 36)
    text = font.render("You're Ghey!", 1, (10, 10, 10))
    textpos = 30, 30
    background.blit(text, textpos)

screen.blit(background, (0, 0))
pygame.display.flip()

clock = pygame.time.Clock()

while running == 1:
    clock.tick(60)
    pygame.display.flip()
