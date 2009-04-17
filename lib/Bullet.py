from Constants import *
from Player import *
from Movable import *
from Grid import *

class Bullet(Movable):
    def __init__(self, col, row, direction, grid, player):
        Movable.__init__(self, col, row, direction, grid, BULLET)
        self.player = player
  
        self.player.addBullet(self)
        
        # The bullet starts ON a collidable
        if self.underneath.getType() in COLLIDABLES:
            self.collide(self.underneath)
            
    def move(self):
        ''' The bullet will move straight until it collides with
        something. '''
        
        col, row = self.handleDirection(self.direction)
            
        nextObj = self.grid.get(col, row)
        
        if nextObj.getType() in COLLIDABLES:
            self.collide(nextObj)
        else:
            # Move on 
            self.grid.moveObj(self, col, row)
            
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
            self.grid.set(self.underneath.getUnderneath(), self.col, self.row)
        else:
            self.grid.set(self.underneath, self.col, self.row)
            
        self.player.removeBullet(self)
