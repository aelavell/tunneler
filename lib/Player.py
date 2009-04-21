from Constants import *
from Grid import *
from Movable import *
from Dirt import *
from Viewport import *
from Bullet import *

class Player(Movable):
    def __init__(self, col, row, grid, player, enemy, whichBase, enemyBase):
        # Set it to a dummy value until it gets initialized
        self.underneath = 0
        
        Movable.__init__(self, col, row, SOUTH, grid, player)
        
        self.base = whichBase
        self.enemy = enemy
        self.enemyBase = enemyBase
        
        # The timer is used to regulate decreasing/increasing
        # health and energy
        self.healthTimer = 0
        self.energyTimer = 0
        
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
        
        self.decreaseEnergy(SHOOTING_ENERGY_DECREASE)
        
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
            
    def setUnderneath(self, obj):
        ''' As soon as the player moves on to a specific
        type of terrain, certain things must happen. 
        For example, if he moves onto his base, 
        a timer has to be started to heal him. '''
        
        # As long as it's not before player's been
        # initialized on the grid
        if self.underneath != 0:
            # player has moved to a new type of terrain
            if self.underneath != obj:
                self.healthTimer = 0
                self.energyTimer = 0
                
        self.underneath = obj
            
    def update(self):
        if self.underneath.getType() in BASES:
            self.healthTimer += 1
        self.energyTimer += 1
        
        if self.underneath.getType() == self.base:
            if self.healthTimer == HEALTH_INCREASE_TIME:
                self.increaseHealth(1)
                self.healthTimer = 0
            if self.energyTimer == ENERGY_INCREASE_TIME:
                self.increaseEnergy(1)
                self.energyTimer = 0
                
        elif self.underneath.getType() == self.enemyBase:
            if self.energyTimer == AWAY_ENERGY_INCREASE_TIME:
                self.increaseEnergy(1)
                self.energyTimer = 0
            
        # Otherwise, the player is not in a base
        # His energy must be drained
        else:
            if self.energyTimer == ENERGY_DECREASE_TIME:
                self.decreaseEnergy(1)
                self.energyTimer = 0
                
            
