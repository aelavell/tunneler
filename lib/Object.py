from Constants import *
from Basic import *

class Object(Basic):
    ''' A more well-defined object. It has coordinates. '''
    
    def __init__(self, col, row, type):
        self.col = col 
        self.row = row 
        self.coords = [col, row]
        self.setType(type)

    def setCoords(self, col, row):
        self.setCol(col)
        self.setRow(row)

    def setCol(self, col):
        self.col = col
    
    def getCol(self):
        return self.col

    def setRow(self, row):
        self.row = row

    def getRow(self):
        return self.row
        
    
        

