from Constants import *
from Empty import *

class Object(Empty):
    ''' A more well-defined object. It has coordinates. '''
    
    def __init__(self, col, row, type):
        self.col = row 
        self.row = col 
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
        
    
        

