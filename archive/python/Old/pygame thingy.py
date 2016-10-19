Fred = "YAYYAYAYAYYAYAAAARGH!!!!"

import os, sys
import pygame
from pygame.locals import *

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

pygame.init()
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption('YARGH')
pygame.mouse.set_visible(1)

background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((250, 250, 250))

if pygame.font:
    font = pygame.font.Font(None, 36)
    text = font.render(Fred, 1, (10, 10, 10))
    textpos = text.get_rect(centerx=background.get_width()/2)
    background.blit(text, textpos)

screen.blit(background, (0, 0))
pygame.display.flip()

clock = pygame.time.Clock()

while 1:
    clock.tick(60)
    pygame.display.flip()
