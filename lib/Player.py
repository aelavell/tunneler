from Constants import *
from Grid import *
from Object import *
from Dirt import *
from Base import *
from Viewport import *

class Player(Object):
    def __init__(self, col, row, grid):
        Object.__init__(self, col, row, PLAYER)
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
            if nextObj.getType() == DIRT:
                nextObj.decrementHealth()

            
            # This is an IF instead of an ELIF because 
            # if the player just crushed a piece of dirt, it will
            # become a '.', and so he can move. This code may change,
            # as it is dependent on order of the statements.
            if nextObj.getType() == EMPTY:
                self.grid.moveObj(col, row, self) 
            elif nextObj.getType() == FOG:
                # MUST FIX
                # Needs code to push row or col back to its
                # original value
                pass
            
