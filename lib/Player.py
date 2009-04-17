from Constants import *
from Grid import *
from Movable import *
from Dirt import *
from Viewport import *
from Bullet import *

class Player(Movable):
    def __init__(self, col, row, grid, player, enemy, whichBase, enemyBase):
        Movable.__init__(self, col, row, SOUTH, grid, player)
        
        self.base = whichBase
        self.enemy = enemy
        self.enemyBase = enemyBase
        
        self.setHealth(MAX_HEALTH)
        self.setEnergy(MAX_ENERGY)
        
        # If the player shoots a bullet, it's added to
        # this array, so the game will know to move it
        # one more step every frame
        self.bullets = []
        
    def getEnemy(self):
        return self.enemy
        
    def shoot(self):
        ''' Shoots a bullet in the direction that the 
        player is currently facing. '''
        
        col, row = self.handleDirection(self.direction)
        
        # Create the bullet (it adds itself to the bullet list)
        bullet = Bullet(col, row, self.direction, self.grid, self)
        
    def addBullet(self, bullet):
        self.bullets.append(bullet)
        
    def removeBullet(self, bullet):
        self.bullets.remove(bullet)
        
    def getBullets(self):
        return self.bullets
        
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
        
    def move(self, direction):
        ''' Move the player along the grid.'''
        
        self.setDirection(direction)
    
        col, row = self.handleDirection(direction)
        
        nextObj = self.grid.get(col, row)

        # The tank is tunneling through dirt
        if nextObj.getType() == DIRT:
            nextObj.decrementHealth()

        # The tank can move freely
        if nextObj.getType() in MOVABLES:
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
                
            
