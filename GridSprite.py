'''
Copyright 2011 Allan Lavell 
This file is part of Tunneler2.

   Tunneler2 is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   Tunneler2 is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with Tunneler2.  If not, see <http://www.gnu.org/licenses/>.
'''

import pygame
from pygame.locals import *

from Tools import *
from Constants import *

class GridSprite(pygame.sprite.Sprite):
    ''' Base class for all objects that are displayed on the game's grid
    using Pygame. '''
    
    def __init__(self, id, row, col):
        pygame.sprite.Sprite.__init__(self)
        self.row = row 
        self.col = col  
        self.id = id
        self.position = False
        self.image = False

    def setPosition(self, topLeftX, topLeftY):
        ''' Position is the object's position as far
        as pygame is concerned, pixel-wise. '''
        
        self.position = (topLeftX, topLeftY)
        self.rect.topleft = self.position
         
    def setImage(self, imageFileName):
        self.image = imageLoad("%s" % imageFileName)
        self.rect = self.image.get_rect()
    
    def update(self):
        self.rect.center = self.position