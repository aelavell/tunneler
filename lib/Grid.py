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
    for example. '''
    
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

    def moveObj(self, obj, newRow, newCol):
        ''' Handles moving an object around the grid,
        checking if it is in bounds. Also handles the 
        actual setting of the object's new
        row and col. '''
        
        # Make sure the move is in-bounds
        if self.isInBounds(newRow, newCol):
            # Make an empty space in object's place on the grid
            oldRow = obj.getRow()
            oldCol = obj.getCol()
            # This was under the object, return it to the grid
            underneath = obj.getUnderneath()
            
            # If two temporary objects (I.E. bullets)
            # move over each other, then one of them will 
            # try to reset the ground erroneously to be
            # a bullet, instead of the ground
            if underneath.getType() in TEMPORARIES:
                self.set(underneath.getUnderneath(), oldRow, oldCol)
            else:
                self.set(underneath, oldRow, oldCol)
            
            # Move the object
            # Update the object's coords
            obj.setCoords(newRow, newCol)
            # Get what the object will be on top of now
            newUnder = self.get(newRow, newCol)
            # Add it to the object
            obj.setUnderneath(newUnder)
            # Put the object in the new place on the grid
            self.set(obj, newRow, newCol)

    def set(self, obj, row, col):
        ''' Puts an object in a particular place on the grid,
        if in bounds. 
        
        Returns the old object that was on the Grid before the
        argument object was set down.'''
        
        if self.isInBounds(row, col):
            # Get the old object
            oldObj = self.grid[row][col]
            # Set the new one down
            self.grid[row][col] = obj
            return oldObj
        else:
            fog = Object(FOG, row, col)
            return fog

    def get(self, row, col):
        ''' Returns the object at the location specified, if
        it is in the Grid. Otherwise returns fog, because
        it is out of the bounds of the Grid. '''
        
        if self.isInBounds(row, col):
            return self.grid[row][col]
        else:
            fog = Object(FOG, row, col)
            return fog
            
    def isInBounds(self, row, col):
        ''' Encapsulates a boolean test to see whether or not
        a set of coordinates in the bounds of the grid. '''
        
        if row >= 0 and row < GRID_SIZE and col >= 0 and col < GRID_SIZE:
            return True
        else:
            return False
    
    def addBase(self, base, topLeftRow, topLeftCol):
        ''' Adds a base for a particular player. 
        BASE_SIZE is defined in the constants.py file.
        It should always be and odd number.'''
        
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
                        empty = Object(EMPTY, rowCounter, colCounter)
                        self.set(empty, rowCounter, colCounter)
                    # Otherwise, a horizontal wall
                    else:
                        hWall = Object(H_WALL, rowCounter, colCounter)
                        self.set(hWall, rowCounter, colCounter)
                
                # If it's any row in-between
                else:
                    # If it's the side of the base
                    if colCounter == topLeftCol or colCounter == colDelimeter - 1:
                        vWall = Object(V_WALL, rowCounter, colCounter)
                        self.set(vWall, rowCounter, colCounter)
                    # It's in the base
                    else:
                        baseFloor = Object(base, rowCounter, colCounter)
                        self.set(baseFloor, rowCounter, colCounter)
                       
                colCounter += 1
            
            rowCounter += 1
    
    def addBaseRandomly(self, base):
        ''' Adds a base in a random location on the grid.'''
        
