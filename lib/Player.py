from Constants import *
from Grid import *
from Object import *
from Dirt import *
from Base import *
from Viewport import *

class Player(Object):
    def __init__(self, x, y, grid):
        Object.__init__(self, x, y, '@')
        self.grid = grid
        self.grid.set(x, y, self)

    def move(self, direction):
        nextObj = null

        if direction == 'n':
            nextObj = self.grid.read(self.y - 1)

        if nextObj != null:
            if nextObj.getType() == 'd':
                nextObj.decrementHealth()
            elif nextObj.getType() == '.':
                xOffset = self.getX()
                yOffset = self.getY() + 1
                self.grid.moveObj(xOffset, yOffset, self) 
