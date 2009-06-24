import pygame
from pygame.locals import *

from Constants import *
from Object import *

class Dirt(Object):
    def __init__(self, row, col, grid):
        Object.__init__(self, DIRT, row, col)
        self.health = DIRT_HEALTH
        self.grid = grid

    def decrementHealth(self):
        self.health -= 1
        if self.health <= 0:
            self.die()

    def die(self):
        # This code does not work for some reason
        #empty = Basic(EMPTY)
        #self.grid.set(empty, self.col, self.row)

        # this does
        self.setType(EMPTY)
        self.setImage(EMPTY)
