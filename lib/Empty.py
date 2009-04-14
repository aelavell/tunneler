from Constants import *

class Empty():
    ''' The most basic object on the grid - it doesn't know
    anything, other than the fact that it is empty. 
    Doesn't even know its own coords. '''

    def __init__(self):
        self.setType(".") 
	
    def setType(self, type):
        self.type = type

    def getType(self):
        return self.type
    
    def __str__(self):
        return self.type 
