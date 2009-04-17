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
            # Keep on goin
            self.grid.moveObj(self, col, row)
            
    def collide(self, object):
        if object.getType() in KILLABLES:
            if object.getType() == DIRT:
                object.decrementHealth()
        
        self.die()
                
    def die(self):
        self.grid.set(self.underneath, self.col, self.row)
        self.player.removeBullet(self)
