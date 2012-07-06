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

from Constants import *
from MobileSprite import *

class PlayerSprite(MobileSprite):    
    def __init__(self, id, row, col):
        MobileSprite.__init__(self, id, row, col)
        self.health = MAX_PLAYER_HEALTH
        self.energy = MAX_PLAYER_ENERGY
        self.changeDirection(DOWN)
    
    def changeDirection(self, direction):
        self.direction = direction
        self.setImage("p%d-%d.png" % (self.id, self.direction))
        self.image.set_colorkey((255,255,255))
        #self.setImage("d.png")
    
