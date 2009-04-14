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
        nextObj = 'null'
        x = self.getX()
        y = self.getY() 

        if direction == 'n':
            y -= 1
            nextObj = self.grid.read(x,y)
        elif direction == 's':
            y += 1
            nextObj = self.grid.read(x,y)
        elif direction == 'e': 
            x += 1
            nextObj = self.grid.read(x,y)
        elif direction == 'w':
            x -= 1
            nextObj = self.grid.read(x,y)

        if nextObj != 'null':
            if nextObj.getType() == 'd':
                nextObj.decrementHealth()
            elif nextObj.getType() == '.':
                self.grid.moveObj(x, y, self) 
            
