import pygame
from pygame.locals import *

from Constants import *
from Player import *
from Movable import *
from Grid import *

class Bullet(Movable):
    def __init__(self, row, col, direction, grid, player):
        Movable.__init__(self, BULLET, row, col, direction, grid)
        self.player = player
  
        self.player.addBullet(self)
        
        # The bullet starts ON a collidable
        if self.underneath.getType() in COLLIDABLES:
            self.collide(self.underneath)
            
    def move(self):
        ''' The bullet will move straight until it collides with
        something. '''
        
        row, col = self.handleDirection(self.direction)
            
        nextObj = self.grid.get(row, col)
        
        if nextObj.getType() in COLLIDABLES:
            # This needs to happen, because when the player
            # shoots and moves at the same time he will
            # step on his bullet immediately after he shoots
            # it. This is an easy way around it
            if nextObj != self.player:
                self.collide(nextObj)
        else:
            # Move on 
            self.grid.moveObj(self, row, col)
            
    def collide(self, object):
        if object.getType() in KILLABLES:
            if object.getType() == DIRT:
                object.decrementHealth()
            elif object.getType() == self.player.getEnemy():
                object.decreaseHealth(10)
        
        self.die()
                
    def die(self):
        # If the bullet happens to collide with the other
        # player just as they shoot a bullet, THIS needs
        # to happen
        if self.underneath.getType() in TEMPORARIES:
            self.grid.set(self.underneath.getUnderneath(), self.row, self.col)
        else:
            self.grid.set(self.underneath, self.row, self.col)
            
        self.player.removeBullet(self)