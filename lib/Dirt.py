from Constants import *
from Object import *

class Dirt(Object):
    def __init__(self, col, row, grid):
        Object.__init__(self, col, row, DIRT)
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
