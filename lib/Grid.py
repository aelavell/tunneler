import copy
from Constants import *
from Player import *
from Object import *
from Dirt import *
from Base import *
from Viewport import *

class Grid():
    ''' The grid keeps track of what's going on at all points at
    all times of the game. It will vary in size based on how many
    players there are, and the size of map selected. A small grid
    for 2 players will be different from a small grid for 4 players,
    for example. s
    '''
    
    def __init__(self, gridSize, pCount, fill): 
        '''gridSize is the size of the grid defined by the variables passed
        to this method. This variable is used to make the number of
        rows and the number of columns. The grid is a square, so if 
        gridSize = 20, then the grid will be 20col20. The default status
        of a unit on the grid is "d", which stands for dirt. This is
        given in the "fill" argument.
        
        This init method merely calls the create method to set up a 
        grid filled with dirt. Bases will be added with another method 
        later. '''
        
        row = []
        self.grid = []
            
        rowCounter = 0
        # Fill the grid with rows
        while rowCounter < gridSize:
            row = []

            # Fill the row with columns 
            colCounter = 0
            while colCounter < gridSize:
                dirt = Dirt(colCounter, rowCounter) 
                row.append(dirt)
                colCounter += 1
        
            self.grid.append(row)
            rowCounter += 1

    def moveObj(self, newCol, newRow, obj):
        ''' 
        Movable objects can only move onto empty space. 
        They can't move onto dirt, or walls, or other movable 
        objects. They can't move off the grid.
        They leave an empty space in their wake.
        
        Also handles the actual setting of the object's new
        col and row.
        '''
        
        # Make sure the move is in-bounds
        if self.isInBounds(newCol, newRow):
            # Make an empty space in object's place on the grid
            oldCol = obj.getCol()
            oldRow = obj.getRow()
            empty = Empty(EMPTY) 
            self.set(oldCol, oldRow, empty)
            
            # Move the object
            # Update the object's coords
            obj.setCoords(newCol, newRow)
            # Put the object in the new place on the grid
            self.set(newCol, newRow, obj)

    def set(self, col, row, obj):
        ''' Puts an object in a particular place on the grid,
        if in bounds. '''
        
        if self.isInBounds(col, row):
            self.grid[col][row] = obj
        else:
            print "Could not set object at ", col, " ", row

    def get(self, col, row):
        ''' Returns the object at the location specified, if
        it is in the Grid. Otherwise returns fog, because
        it is out of the bounds of the Grid. '''
        
        if self.isInBounds(col, row):
            return self.grid[col][row]
        else:
            fog = Empty(FOG)
            return fog
            
    def isInBounds(self, col, row):
        ''' Encapsulates a boolean test to see whether or not
        a set of coordinates in the bounds of the grid. '''
        
        if col >= 0 and col < GRID_SIZE and row > 0 and row < GRID_SIZE:
            return True
        else:
            return False
            
    def replace(self, obj):   
        ''' Method that abstracts the basic replacing of objects on the 
        grid. ins is the instance of a class that is being dealt with,
        and obj is what will be taking the place of what is currently
        on the grid.
        
        SAMPLE INPUT:
        replace(base1, base1.base)'''
        
        # l is the top left coord, r is the bottom right coord of
        # the given object
        l = obj.TLC
        r = obj.BRC

        item = obj.getItem()
       
        # GRC is the grid row coordinate
        # GCC is the grid column coordinate
        # IRC is the instance row coordinate
        # ICC is the instance col coordinate
        GRC = l[0]
        IRC = 0
        while GRC <= r[0]:
            GCC = l[1]
            ICC = 0
            while GCC <= r[1]:
                self.grid[GRC][GCC] = item[IRC][ICC]
                GCC += 1
                ICC += 1
            GRC += 1
            IRC += 1
