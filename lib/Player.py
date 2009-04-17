from Constants import *
from Grid import *
from Object import *
from Dirt import *
from Base import *
from Viewport import *

class Player(Object):
    def __init__(self, col, row, grid, whichPlayer, whichBase, enemyBase):
        Object.__init__(self, col, row, whichPlayer)
        self.grid = grid
        
        # object that is under the player initially
        under = self.grid.set(self, col, row)
        self.setUnderneath(under)
        
        self.base = whichBase
        self.enemyBase = enemyBase
        
        self.setHealth(MAX_HEALTH)
        self.setEnergy(MAX_ENERGY)
        
    def setHealth(self, health):
        ''' Set player's health to a particular value. '''
        
        # Don't let the health get set to above maximum value
        if health <= MAX_HEALTH:
            self.health = health
        else:
            self.health = MAX_HEALTH
            
    def getHealth(self):
        ''' Returns how much health the player has. '''
        
        return self.health
        
    def increaseHealth(self, amount):
        ''' Increases player's health. Won't go past
        max health. '''
        
        if (self.health + amount) <= MAX_HEALTH:
            self.health += amount
        # Otherwise, it would increase past maximum health
        else:
            self.health = MAX_HEALTH
            
    def decreaseHealth(self, amount):
        ''' Decreases player's health. '''
        
        self.health -= amount
            
    def setEnergy(self, energy):
        ''' Set the player's energy to a particular value. '''
        
        if energy <= MAX_ENERGY: 
            self.energy = energy
        else:
            self.energy = MAX_ENERGY
    
    def getEnergy(self):
        ''' Returns how much energy the player has. '''
        
        return self.energy
        
    def increaseEnergy(self, amount):
        ''' Increases player's energy by amount specified. 
        Will not increase past the max amount of energy. '''
        
        if (self.energy + amount) <= MAX_ENERGY:
            self.energy += amount
        # Otherwise, it would increase past maximum energy
        else:
            self.energy = MAX_ENERGY
        
    def decreaseEnergy(self, amount):
        ''' Decreases player's energy by amount specified. '''
        
        self.energy -= amount
    
    def setUnderneath(self, obj):
        ''' The player will always be on top of something
        in the grid - be it an empty space, or the floor of 
        a base, it will have to be remembered so it can be
        placed back onto the grid after the player has moved
        on. Also, when the player is on the floor of the base,
        special things happen to him, such as replenishment
        of health and energy. '''
        
        self.underneath = obj
        
    def getUnderneath(self):
        ''' Returns the part of the grid that is currently
        underneath the player. '''
        
        return self.underneath

    def move(self, direction):
        ''' Move the player along the grid. Direction should
        be: n, e, w, or s, which stand for north, east, west,
        south. '''
        
        nextObj = 'null'
        col = self.getCol() 
        row = self.getRow()
        
        if direction == 'n':
            row -= 1
            nextObj = self.grid.get(col,row)
        elif direction == 's':
            row += 1
            nextObj = self.grid.get(col,row)
        elif direction == 'e': 
            col += 1
            nextObj = self.grid.get(col,row)
        elif direction == 'w':
            col -= 1
            nextObj = self.grid.get(col,row)

        if nextObj != 'null':
            # The tank is tunneling through dirt
            if nextObj.getType() == DIRT:
                nextObj.decrementHealth()

            # The tank can move freely
            if nextObj.getType() == EMPTY:
                self.grid.moveObj(self, col, row) 
            elif nextObj.getType() == self.base or nextObj.getType == self.enemyBase:
                self.grid.moveObj(self, col, row) 
                
    def update(self):
        if self.underneath.getType() == self.base:
            self.increaseEnergy(1)
            self.increaseHealth(1)
        elif self.underneath.getType() == self.enemyBase:
            self.increaseEnergy(1)
            
        # Otherwise, the player is not in a base
        # His energy must be drained
        else:
            self.decreaseEnergy(1)
                
            
