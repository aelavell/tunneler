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
        under = self.grid.set(col, row, self)
        # object that is under the player initially
        self.setUnderneath(under)
        
    def setUnderneath(self, obj):
        ''' The player will always be on top of something
        in the grid - be it an empty space, or the floor of 
        a base, it will have to be remembered so it can be
        placed back onto the grid after the player has moved
        on. Also, when the player is on the floor of the base,
        special things happen to him, such as replenishment
        of health and energy. '''
        
        self.underneath = obj
        
    def getUnderneath(self):
        ''' Returns the part of the grid that is currently
        underneath the player. '''
        
        return self.underneath

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
                
    def update(self):
        # placeholder for healing / energy replacement
        if self.underneath.type() == B1:
            pass
            
