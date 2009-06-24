import pygame
from pygame.locals import *

from Object import *

class Movable(Object):
    ''' If an object is movable, it has to be able to 
    have things underneath it. This is common to all 
    movable objects. The actual move() method is left 
    up to the particular object. '''

    def __init__(self, type, row, col, direction, grid):
        Object.__init__(self, type, row, col)
        self.setGrid(grid)
        
        # Set the player on the grid, and get 
        # whatever is initially underneath the object
        under = grid.set(self, row, col)
        self.setUnderneath(under)
        
        self.setDirection(direction)
        
    def setGrid(self, grid):
        self.grid = grid
        
    def getGrid(self, grid):
        return self.grid
        
    def setDirection(self, direction):
        ''' The direction of the object will determine
        different things for different objects. For the player,
        the direction will determine where it shoots. For a
        bullet, it determines where it goes.
        
        Directions should be n,e,w or s. '''
        
        self.direction = direction
        
    def getDirection(self):
        ''' Returns the direction the object is facing. '''
        
        return self.direction

    def setUnderneath(self, obj):
        ''' The object will always be on top of something
        in the grid - be it an empty space, or the floor of 
        a base, it will have to be remembered so it can be
        placed back onto the grid after the player has moved
        on. '''
        
        self.underneath = obj
        
    def getUnderneath(self):
        ''' Returns the part of the grid that is currently
        underneath the object. '''
        
        return self.underneath
    
    def handleDirection(self, direction):
        ''' Translates a direction string such as "north"
        to a tangible change in row and column. Takes the
        objects' current row and column as a baseline,
        but does NOT change them directly. Returns the
        modified row and column instead. '''
        
        row = self.row
        col = self.col
        
        if direction == NORTH:
            row -= 1
        elif direction == EAST:
            col += 1
        elif direction == WEST:
            col -= 1
        elif direction == SOUTH:
            row += 1
            
        return row, col
