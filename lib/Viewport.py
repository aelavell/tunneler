from Constants import *
from Grid import *
from Object import *
from Dirt import *
from Base import *
from Viewport import *

class Viewport():
    def __init__(self, grid, player):
        self.grid = grid
        self.player = player
    
    def display(self):
        row = self.player.getRow() - (DISPLAY_SIZE / 2)
        maxRow = self.player.getRow() + (DISPLAY_SIZE / 2)
        maxCol = self.player.getCol() + (DISPLAY_SIZE / 2)
        while row < maxRow:
            col = self.player.getCol() - (DISPLAY_SIZE / 2)
            while col < maxCol:
                print self.grid.get(col, row),
                col += 1
                
            # newline
            print 
            
            row += 1
