from Constants import *
from Empty import *

class Object(Empty):
    ''' A more well-defined object. It has coordinates. '''
    
    def __init__(self, col, row, type):
        self.col = row 
        self.row = col 
        self.coords = [col, row]
        self.setType(type)

    def getCoords(self):
        return self.coords

    def setCoords(self, col, row):
        self.col = col
        self.row = row
        self.coords = [col,row]

    def getCol(self):
        return self.col

    def getRow(self):
        return self.row
        

