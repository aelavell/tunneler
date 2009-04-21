import copy
from Constants import *
from Player import *
from Object import *
from Dirt import *
from Viewport import *

class Grid():
    ''' The grid keeps track of what's going on at all points at
    all times of the game. It will vary in size based on how many
    players there are, and the size of map selected. A small grid
    for 2 players will be different from a small grid for 4 players,
    for example. s
    '''
    
    def __init__(self): 
        row = []
        self.grid = []
            
        rowCounter = 0
        # Fill the grid with rows
        while rowCounter < GRID_SIZE:
            row = []

            # Fill the row with columns 
            colCounter = 0
            while colCounter < GRID_SIZE:
                dirt = Dirt(colCounter, rowCounter, self) 
                row.append(dirt)
                colCounter += 1
        
            self.grid.append(row)
            rowCounter += 1

    def moveObj(self, obj, newCol, newRow):
        ''' 
        Handles moving an object around the grid,
        checking if it is in bounds.
        Also handles the actual setting of the object's new
        col and row.
        '''
        
        # Make sure the move is in-bounds
        if self.isInBounds(newCol, newRow):
            # Make an empty space in object's place on the grid
            oldCol = obj.getCol()
            oldRow = obj.getRow()
            # This was under the object, return it to the grid
            underneath = obj.getUnderneath()
            
            # If two temporary objects (I.E. bullets)
            # move over each other, then one of them will 
            # try to reset the ground erroneously to be
            # a bullet, instead of the ground
            if underneath.getType() in TEMPORARIES:
                self.set(underneath.getUnderneath(), oldCol, oldRow)
            else:
                self.set(underneath, oldCol, oldRow)
            
            # Move the object
            # Update the object's coords
            obj.setCoords(newCol, newRow)
            # Get what the object will be on top of now
            newUnder = self.get(newCol, newRow)
            # Add it to the object
            obj.setUnderneath(newUnder)
            # Put the object in the new place on the grid
            self.set(obj, newCol, newRow)

    def set(self, obj, col, row):
        ''' Puts an object in a particular place on the grid,
        if in bounds. 
        
        Returns the old object that was on the Grid before the
        argument object was set down. If off the grid, returns
        fog. '''
        
        if self.isInBounds(col, row):
            # Get the old object
            oldObj = self.grid[col][row]
            # Set the new one down
            self.grid[col][row] = obj
            return oldObj
        else:
            fog = Basic(FOG)
            return fog

    def get(self, col, row):
        ''' Returns the object at the location specified, if
        it is in the Grid. Otherwise returns fog, because
        it is out of the bounds of the Grid. '''
        
        if self.isInBounds(col, row):
            return self.grid[col][row]
        else:
            fog = Basic(FOG)
            return fog
            
    def isInBounds(self, col, row):
        ''' Encapsulates a boolean test to see whether or not
        a set of coordinates in the bounds of the grid. '''
        
        if col >= 0 and col < GRID_SIZE and row >= 0 and row < GRID_SIZE:
            return True
        else:
            return False
    
    def addBase(self, base, topLeftCol, topLeftRow):
        ''' Adds a base for a particular player. 
        BASE_SIZE is defined in the constants.py file.
        It should always be and odd number.'''
        
        empty = Basic(EMPTY)
        hWall = Basic(H_WALL)
        vWall = Basic(V_WALL)
        
        rowDelimeter = topLeftRow + BASE_SIZE
        colDelimeter = topLeftCol + BASE_SIZE
        
        rowCounter = topLeftRow
        # Generate the base
        while rowCounter < rowDelimeter:
            colCounter = topLeftCol
            
            while colCounter < colDelimeter:
                # If it's the first or last row
                if rowCounter == topLeftRow or rowCounter == rowDelimeter - 1:
                    # if it's half-way, make an entrance
                    if (colCounter - topLeftCol) == ((colDelimeter - topLeftCol) / 2 ):
                        self.set(empty, colCounter, rowCounter)
                    # Otherwise, a horizontal wall
                    else:
                        self.set(hWall, colCounter, rowCounter)
                
                # If it's any row in-between
                else:
                    # If it's the side of the base
                    if colCounter == topLeftCol or colCounter == colDelimeter - 1:
                        self.set(vWall, colCounter, rowCounter)
                    # It's in the base
                    else:
                        baseFloor = Object(colCounter, rowCounter, base)
                        self.set(baseFloor, colCounter, rowCounter)
                       
                colCounter += 1
            
            rowCounter += 1
                    
