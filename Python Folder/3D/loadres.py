import pygame; from pygame.locals import *
def basic_import_image(pathname):
    image = pygame.image.load(pathname)
    return image

def import_bitmap(pathname):
    return pygame.image.load(pathname)