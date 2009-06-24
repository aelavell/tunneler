import pygame
from pygame.locals import *

from Tools import *
from Constants import *

class Object(pygame.sprite.Sprite):
    ''' Base class for all objects that are displayed
    on the game's Grid. '''
    
    def __init__(self, type, row, col):
        pygame.sprite.Sprite.__init__(self)
        self.setType(type) 
        self.row = row 
        self.col = col 
        self.coords = (row, col)
        self.setType(type)
        self.setImage("%s.png" %type)
        
    def setCoords(self, row, col):
        ''' Coords are the object's coordinates pertaining
        to the Grid. '''
        
        self.setRow(row)
        self.setCol(col)

    def setRow(self, row):
        self.row = row
    
    def getRow(self):
        return self.row

    def setCol(self, col):
        self.col = col

    def getCol(self):
        return self.col
	
    def setPosition(self, x, y):
        ''' Position is the object's position as far
        as pygame is concerned, pixel-wise. '''
        
        self.position = (x, y)
        self.rect.center = self.position
        
    def getPosition(self):
        return self.position
    
    def setImage(self, imageFileName):
        self.image, self.rect = imageLoad(imageFileName)
    
    def getImage(self):
        return self.image
    
    def setType(self, type):
        self.type = type

    def getType(self):
        return self.type
    
    def __str__(self):
        return self.getType() 
    
    def update(self):
        self.rect.center = self.position

    


  
        
    
        

