from Constants import *

class Object():
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.coords = [x, y]
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

    def setType(self, type):
        self.type = type

    def getType(self):
        return self.type
    
    def __str__(self):
        return type
