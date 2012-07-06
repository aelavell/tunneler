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

from Mobile import *
from Constants import *

class Player(Mobile):
    def __init__(self, id, row, col, game):
        Mobile.__init__(self, id, row, col, game)
        self.health = MAX_PLAYER_HEALTH
        self.energy = MAX_PLAYER_ENERGY
        self.loseEnergyTimer = 0
        self.gainEnergyTimer = 0
        self.gainHealthTimer = 0
        self.game = game

    def loseHealth(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.die()
            return ""
        else:
            return "%d.%d.%d," %(SET_HEALTH_CODE, self.id, self.health)

    def gainHealth(self, amount):
        self.health += amount
        if self.health > MAX_PLAYER_HEALTH:
            self.health = MAX_PLAYER_HEALTH
        return "%d.%d.%d," %(SET_HEALTH_CODE, self.id, self.health)

    def loseEnergy(self, amount):
        self.energy -= amount
        if self.energy <= 0:
            self.die()
            return ""
        else:
            return "%d.%d.%d," %(SET_ENERGY_CODE, self.id, self.energy)

    def gainEnergy(self, amount):
        self.energy += amount
        if self.energy > MAX_PLAYER_ENERGY:
            self.energy = MAX_PLAYER_ENERGY
        return "%d.%d.%d," %(SET_ENERGY_CODE, self.id, self.energy)
    
    def shoot(self):
        change = self.loseEnergy(SHOOT_ENERGY_LOSS)
        
        if self.direction == LEFT:
            change += self.game.spawnBullet(self.row, self.col - 1, LEFT)   
        elif self.direction == RIGHT:
            change += self.game.spawnBullet(self.row, self.col + 1, RIGHT)
        elif self.direction == UP:
            change += self.game.spawnBullet(self.row - 1, self.col, UP)
        elif self.direction == DOWN:
            change += self.game.spawnBullet(self.row + 1, self.col, DOWN)
        
        return change
        
    def die(self):
        self.game.gameOver(self)
			
    def move(self, direction):
        change = ""
	
        newRow = self.row
        newCol = self.col
        if self.direction == direction:
            if (direction == LEFT):
                newCol -= 1
            elif direction == RIGHT:
                newCol += 1
            elif direction == UP:
                newRow -= 1
            elif direction == DOWN:
                newRow += 1

        canMoveToCoord = False
        # make sure the player can move to the coordinates and is not trying to move off the grid
        if self.game.grid.coordsInGrid(newRow, newCol):
            # if the desired movement is dirt, gotta damage it and see if you can move
            if self.game.grid.objectIsDirt(newRow, newCol):
                change = self.game.grid.damageDirt(newRow, newCol, MOVE_DIRT_DAMAGE)
                # the dirt is gone, move the object immediately into the spot last occupied by the dirt
                if change[0] == DIRT_DIE_CODE:
                    canMoveToCoord = True
            else:
                # there could be a bullet or a player in the coordinate you're moving into
                bullet = self.game.bulletAt(newRow, newCol)
                if self.game.playerAt(newRow, newCol):
                    # you can't move to that location, so do nothing
                    pass
                elif bullet:
                    # you can move to that location, but you'll get damaged and destroy the bullet
                    canMoveToCoord = True
                    change += self.loseHealth(BULLET_PLAYER_DAMAGE)
                    change += self.game.destroyBullet(bullet)
                else:
                    canMoveToCoord = True
                
            if canMoveToCoord:
                self.row = newRow
                self.col = newCol
                change += "%d.%d.%d.%d," %(MOBILE_MOVE_CODE, self.id, newRow, newCol)
			
		# change direction regardless of whatever else happens	
        if self.direction != direction:
            self.direction = direction
            change += "%d.%d.%d," %(MOBILE_DIRECTION_CODE, self.id, self.direction)
				
        return change
        
    def passTimestep(self):
        change = ""

        ground = self.game.grid.objectAt(self.row, self.col)
        if ground == A_BASE_UNIT or  ground == B_BASE_UNIT:
	        # If you're in a base, you always gain energy, regardless of whether it's yours or his
            self.loseEnergyTimer = 0
            self.gainEnergyTimer += 1
            if self.gainEnergyTimer == GAIN_ENERGY_TIMEOUT:
                if self.energy < MAX_PLAYER_ENERGY:
                    change += self.gainEnergy(1)
                self.gainEnergyTimer = 0
	        # if you're in your own base, you regenerate health
            if self.id == 1 and ground == A_BASE_UNIT or self.id == 2 and ground == B_BASE_UNIT:
                if self.health < MAX_PLAYER_HEALTH:
                    self.gainHealthTimer += 1
                    if self.gainHealthTimer == GAIN_HEALTH_TIMEOUT:
                        change += self.gainHealth(1)
                        self.gainHealthTimer = 0
        else:
            self.gainEnergyTimer = 0
            self.gainHealthTimer = 0
            self.loseEnergyTimer += 1
    	    if self.loseEnergyTimer == LOSE_ENERGY_TIMEOUT:
    	        self.loseEnergyTimer = 0
                change += self.loseEnergy(1)

        return change
