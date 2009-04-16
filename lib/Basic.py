from Constants import *

class Basic():
    ''' The most basic object on the grid - it doesn't
    even know its own coords. '''

    def __init__(self, type):
        self.setType(type) 
	
    def setType(self, type):
        self.type = type

    def getType(self):
        return self.type
    
    def __str__(self):
        return self.getType() 
