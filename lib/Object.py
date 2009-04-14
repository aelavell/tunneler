from Constants import *
from Empty import *

class Object(Empty):
    def __init__(self, col, row, type):
        self.x = row 
        self.y = col 
        self.coords = [col, row]
        self.setType(type)

    def getCoords(self):
        return self.coords

    def setCoords(self, x, y):
        self.x = x
        self.y = y
        self.coords = [x,y]

    def getX(self):
        return self.x

    def getY(self):
        return self.y

