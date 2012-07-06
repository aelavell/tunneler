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

from Command import *
from Constants import *
from Mobile import *

class Bullet(Mobile):
    def __init__(self, id, row, col, direction, game):
        Mobile.__init__(self, id, row, col, game)
        self.direction = direction
        self.justSpawned = True
        
    def keepMoving(self):
        destroyed = False
        change = ""

        newRow = self.row
        newCol = self.col
        if self.direction == LEFT:
            newCol -= 1
        elif self.direction == RIGHT:
            newCol += 1
        elif self.direction == UP:
            newRow -= 1
        elif self.direction == DOWN:
            newRow += 1

        canMoveToCoord = False
        # make sure the bullet can move to the coordinates and is not trying to move off the grid
        if self.game.grid.coordsInGrid(newRow, newCol):
            # if the desired movement is dirt, gotta damage it
            if self.game.grid.objectIsDirt(newRow, newCol):
                change = self.game.grid.damageDirt(newRow, newCol, BULLET_DIRT_DAMAGE)
                change += self.game.destroyBullet(self)
                destroyed = True
            else:
                # there could be a bullet or a player in the coordinate you're moving into
                playerHit = self.game.playerAt(newRow, newCol)
                if playerHit:
                    change += playerHit.loseHealth(BULLET_PLAYER_DAMAGE)
                    change += self.game.destroyBullet(self)
                    destroyed = True
                elif self.game.bulletAt(newRow, newCol):
                    # COULD destroy other bullets and itself if they collide
                    canMoveToCoord = True
                else:
                    canMoveToCoord = True

            if canMoveToCoord and not destroyed:
                self.row = newRow
                self.col = newCol
                change += "%d.%d.%d.%d," %(MOBILE_MOVE_CODE, self.id, newRow, newCol)
        if not canMoveToCoord and not destroyed:
            # the bullet hit the edge of the grid and thus dies
            change += self.game.destroyBullet(self)
            destroyed = True

        return change
    
    def collide(self):
        pass