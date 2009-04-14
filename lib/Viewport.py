from Constants import *
from Grid import *
from Object import *
from Dirt import *
from Base import *
from Viewport import *

class Viewport():
    def __init__(self, grid):
        self.grid = grid
    
    def display(self):
        row = 0
        while row < DISPLAY_SIZE:
            col = 0
            while col < DISPLAY_SIZE:
                print self.grid.get(col, row),
                col += 1
                
            # newline
            print 
            
            row += 1
