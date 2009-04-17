from Constants import *
from Grid import *
from Object import *
from Dirt import *
from Viewport import *

class Viewport():
    def __init__(self, grid, player):
        self.grid = grid
        self.player = player
        
    def HUD(self):
        ''' The HUD (Heads-Up Display) shows off the player's
        health and energy. '''
        
        print "Health: ", self.player.getHealth()
        print "Energy: ", self.player.getEnergy()
    
    def display(self):
        ''' Displays a view centered on the player.'''
        
        row = self.player.getRow() - (DISPLAY_SIZE / 2)
        maxRow = self.player.getRow() + (DISPLAY_SIZE / 2)
        maxCol = self.player.getCol() + (DISPLAY_SIZE / 2)
        while row <= maxRow:
            # If the row is within bounds of the grid
            if row >= 0 and row < GRID_SIZE:
                col = self.player.getCol() - (DISPLAY_SIZE / 2)
                while col <= maxCol:
                    if col < 0:
                        print FOG,
                    else:
                        print self.grid.get(col, row),
                    col += 1
                    
            # The row is fog, so just fill 'er up
            else:
                counter = 0
                while counter < DISPLAY_SIZE:
                    print FOG,
                    counter += 1
                
            # newline
            print 
                
            row += 1
            
