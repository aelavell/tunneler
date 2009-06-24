import pygame
import os
import sys

root = sys.path[0]

def imageLoad(name):
    image = pygame.image.load(root + '/data/' + name).convert()

    image = image.convert()

    return image, image.get_rect()