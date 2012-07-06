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

import math
import re   

from Grid import *
from Player import *
from Command import *
from Constants import *
from Bullet import *

class Game:
    ''' The Game encapsulates all of the information about a particular round of 
    tunneler. It knows the state of the grid, the players, which particular timestep
    we are on, etc. '''

    def __init__(self, playerHandlers, numRows, numCols, server):
        self.timestep = 0 
        self.changes = ""
        self.handlersReady = []
        self.commands = []
        self.bullets = []
        self.nextBulletID = 3
        self.server = server
        self.gameAlreadyOver = False
        
        self.grid = Grid(numRows, numCols)
        aBaseRow, aBaseCol = self.grid.createRandomBasePosition()
        bBaseRow, bBaseCol = self.grid.createRandomBasePosition()
        self.grid.addBase(aBaseRow, aBaseCol, A_BASE_UNIT)
        self.grid.addBase(bBaseRow, bBaseCol, B_BASE_UNIT)
        
        self.playerHandlers = playerHandlers
        self.createPlayers(aBaseRow, aBaseCol, bBaseRow, bBaseCol)
        self.sendInitialGameConditions()
    
    def createPlayers(self, aBaseRow, aBaseCol, bBaseRow, bBaseCol):
        '''
        The players start off in the middle of their respective bases. This 
        method creates the objects used to model them.
        '''
        
        i = 1
        while i < 3:
            playerRow = 0
            playerCol = 0
            if i == 1:
                playerRow = aBaseRow + int(math.ceil(BASE_SIZE / 2))
                playerCol = aBaseCol + int(math.ceil(BASE_SIZE / 2))
            else:
                playerRow = bBaseRow + int(math.ceil(BASE_SIZE / 2))
                playerCol = bBaseCol + int(math.ceil(BASE_SIZE / 2))

            self.playerHandlers[i-1].player = Player(i, playerRow, playerCol, self)
            self.playerHandlers[i-1].game = self
            
            i+= 1
        
    def sendInitialGameConditions(self):
        '''
        When both clients have connected and are ready to go, the server sends the initial data that
        each handler requires to create the initial gamestate. They are:
        
        Game start code - Indicates to the client that the game is starting
        Player id - These have been assigned by the server, so the client is just told if it's id 1 or id 2
        numRows, numCols - The size of the grid
        Base Coordinates - The coordinates of the top left corners of the bases
        '''
        
        print "Send init conditions"
        for playerHandler in self.playerHandlers:
            playerHandler.sendMessage("%d.%d.%d.%d.%d.%d.%d.%d;" %(GAME_START_CODE, playerHandler.player.id, self.grid.numRows, self.grid.numCols, self.grid.aBaseRow, self.grid.aBaseCol, self.grid.bBaseRow, self.grid.bBaseCol))
            
    def addChange(self, change):
        if change != "":
		    self.changes += change

    def terminateChangesForCurrentTimestep(self):
        '''
        Simply adds the timestep to the change string and the terminating semi-colon.
        '''
        
        self.changes += "%d;" % self.timestep;
        print self.changes

    def executeCommand(self, command):
        '''
        Takes a command object (which was parsed and set up by the playerHandlers), 
        and executes it.
        '''
        
        player = ""
        handler = ""
        for h in self.playerHandlers:
            if h.player.id == command.id:
                player = h.player
                handler = h
        
        if command.move != NO_CHANGE:
            change = player.move(command.move)
            if change:
                self.addChange(change)
        if command.shoot != NO_CHANGE:
            change = player.shoot()
            if change:
                self.addChange(change)
                
    def playerAt(self, row, col):
        '''
        Returns the the player at a particular row and col if there is player there,
        false if no player is at that location.
        '''
        
        result = False
        for ph in self.playerHandlers:
            if ph.player.row == row and ph.player.col == col:
                result = ph.player
                break
        
        return result
        
    def bulletAt(self, row, col):
        '''
        Returns the id of the bullet at a particular row and col if there is player there,
        false if no bullet is at that location.
        '''
        result = False
        for bullet in self.bullets:
            if bullet.row == row and bullet == col:
                result = bullet.id
                break
        
        return result
        
    def spawnBullet(self, row, col, direction):
        '''
        Spawns a new bullet in the grid, assigning it the next available bullet id.
        If the bullet is spawned on dirt, or another player, it is not actually created,
        the dirt or the player is simply damaged.
        '''
        
        change = ""
        if self.grid.coordsInGrid(row, col):
            playerHit = self.playerAt(row, col)
            if self.grid.objectIsDirt(row, col):
                change = self.grid.damageDirt(row, col, BULLET_DIRT_DAMAGE)
            
            elif playerHit:
                change = playerHit.loseHealth(BULLET_PLAYER_DAMAGE)
            else:
                self.bullets.append(Bullet(self.nextBulletID, row, col, direction, self))
                change = "%d.%d.%d.%d," %(MOBILE_SPAWN_CODE, self.nextBulletID, row, col)
                self.nextBulletID += 1
        
        return change
        
    def destroyBullet(self, bullet):
        self.bullets.remove(bullet)
        return "%d.%d," % (MOBILE_DIE_CODE, bullet.id)
    
    def addCommand(self, cmd):
        '''
        Adds a command from a PlayerHandler. There can only be one command per handler
        per timestep.
        '''
        
        if len(self.commands) > 0 and cmd.id != self.commands[0].id or len(self.commands) == 0:
            self.commands.append(cmd)
            
        if len(self.commands) == 2:
            self.nextTimestep()
            self.commands = []
        
    def nextTimestep(self):
        '''
        This is where the magic happens. All of the commands are executed, any bullets that exist are moved
        along, and the players either lose or gain energy depending where they are on the grid. All of
        these changes are documented, and sent across the network to each of hte clients.
        '''
        
        for cmd in self.commands:
            self.executeCommand(cmd)
            
        for bullet in self.bullets:
            # Bullets move twice per timestep
            firstChange = bullet.keepMoving()
            self.addChange(firstChange)
            if not re.search("%d.%d" % (MOBILE_DIE_CODE, bullet.id), firstChange):
                # The bullet should start off 1 unit away from the player when it's firt created
                if not bullet.justSpawned:
                    self.addChange(bullet.keepMoving())
                else:
                    bullet.justSpawned = False
             
        for ph in self.playerHandlers:
            self.addChange(ph.player.passTimestep())
        
        self.terminateChangesForCurrentTimestep()

        for playerHandler in self.playerHandlers:
            playerHandler.commitChanges(self.changes)

        self.changes = ""
        self.timestep += 1
        
    def gameOver(self, playerWhoLost):  
        '''
        Tells the server and the clients that the game has ended.
        '''
        
        if not self.gameAlreadyOver:
            self.addChange("%d.%d," % (GAME_OVER_CODE, playerWhoLost.id))
            self.terminateChangesForCurrentTimestep()
            for playerHandler in self.playerHandlers:
                playerHandler.commitChanges(self.changes)
            self.server.gameOver()
            self.gameAlreadyOver = True
        