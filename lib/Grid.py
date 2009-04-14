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
    for example. 
    
    Units on the grid can have several different types of status: 
    
    d - dirt
    e - empty
    b1 - player 1's base
    b2 - player 2's base (etc.)
    hw - horizontal wall
    vw - vertical wall
    blcw - bottom left corner wall
    brcw - bottom right corner wall
    tlcw - top left corner wall 
    trcw - top right corner wall '''
    
    def __init__(self, gridSize, pCount, fill): 
        '''gridSize is the size of the grid defined by the variables passed
        to this method. This variable is used to make the number of
        rows and the number of columns. The grid is a square, so if 
        gridSize = 20, then the grid will be 20x20. The default status
        of a unit on the grid is "d", which stands for dirt. This is
        given in the "fill" argument.
        
        This init method merely calls the create method to set up a 
        grid filled with dirt. Bases will be added with another method 
        later. '''
        
        row = []
        self.grid = []
            
        rowCounter = 0
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

    def moveObj(self, newX, newY, obj):
        ''' Won't do any error-checking of its own, because it's assuming
        whatever is calling it already did the moving math. 
        
        Movable objects can only move onto empty space. They can't move
        onto dirt, or walls, or other movable objects. 
        So that will leave an empty space in their wake.
        '''
        
        # Make an empty in its place on the grid
        oldX = obj.getX()
        oldY = obj.getY()
        empty = Empty() 
        self.set(oldX, oldY, empty)
        
        # Move the object
        obj.setCoords(newX, newY)
        self.set(newX, newY, obj)

    def set(self, x, y, obj):
        ''' Sets an object in a particular place on the grid. '''

        self.grid[y][x] = obj

    def read(self, x, y):
        ''' Returns the object at the location specified. '''

        return self.grid[x][y]

    def readArea(self, TLC, BRC):
        ''' Method for reading data off of the grid. Takes the top left
        coordinate to the bottom right coordinate,
        and returns the values of all of the list items in between those
        two coordinates in the form of a list.'''
        
        output = []
        y = TLC[1] 
        brx = BRC[0]
        bry = BRC[1]
        
        while y <= bry:
            x = TLC[0]
            row = []
            
            if y < 0 or y >= len(self.grid):
                while x <= brx:
                    row.append('f')
                    x += 1
            else:
                while x <= brx:
                    # if x is off the grid (smaller than 0, append fog)
                    if x < 0 or x >= len(self.grid): row.append('f')
                    else: row.append(self.grid[y][x])
                    x += 1
            output.append(row)
            y += 1
        
        return output
            
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
