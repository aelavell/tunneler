from Constants import *
from Grid import *
from Object import *
from Dirt import *
from Base import *
from Viewport import *

class Player(Object):
    def __init__(self, col, row, grid):
        Object.__init__(self, col, row, P1)
        self.grid = grid
        self.grid.set(col, row, self)

    def move(self, direction):
        nextObj = 'null'
        col = self.getCol() 
        row = self.getRow()
        
        if direction == 'n':
            row -= 1
            nextObj = self.grid.get(col,row)
        elif direction == 's':
            row += 1
            nextObj = self.grid.get(col,row)
        elif direction == 'e': 
            col += 1
            nextObj = self.grid.get(col,row)
        elif direction == 'w':
            col -= 1
            nextObj = self.grid.get(col,row)

        if nextObj != 'null':
            # The tank is tunneling through dirt
            if nextObj.getType() == DIRT:
                nextObj.decrementHealth()

            # The tank can move freely
            if nextObj.getType() == EMPTY:
                self.grid.moveObj(col, row, self) 
            elif nextObj.getType() == FOG:
                pass
            elif nextObj.getType() == H_WALL:
                pass
            
