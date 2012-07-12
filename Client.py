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

import socket
import asyncore
import asynchat 
import re
import math
import sys
import pygame
from pygame.locals import *

from GUIConstants import *
from Constants import *
from Grid import *
from PlayerSprite import *
from Viewport import *
from Tools import *

class Client(asynchat.async_chat):
    def __init__(self, host, port):
        asynchat.async_chat.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port
        self.inBuffer = ""
        self.outBuffer = ""
        self.connect((host,port))
        self.outBuffer += "Tunneler1.0;"
        self.gameStarted = False
        self.grid = False
        self.players = []
        self.bullets = []
        self.playerID = False
        self.set_terminator(";")
        self.timestep = 0
        self.shotAtStep = -10
        self.movedAtStep = -10
        
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.HUDSurf = pygame.Surface((SCREEN_WIDTH, HUD_HEIGHT))
        pygame.mouse.set_visible(0)
        self.clock = pygame.time.Clock()
        pygame.font.init()
        self.font = pygame.font.Font(None, FONT_SIZE)
        self.titleFont = pygame.font.Font(None, TITLE_FONT_SIZE)
        self.displayTitleScreen()
        
    def collect_incoming_data(self, data):
        self.inBuffer += data

    def found_terminator(self):
        self.parseChange(self.inBuffer.strip())
        self.inBuffer = ""
        self.input()
        
    def handle_connect(self):
        pass
         
    def writable(self):
        return (len(self.outBuffer) > 0)

    def handle_write(self):
        sent = self.send(self.outBuffer)
        self.outBuffer = self.outBuffer[sent:]
        
    def parseInitialConditions(self, msg):
        '''
        The first thing the Server will do when the game is signaled to begin is to send 
        the initial conditions so that each client can set up, getting info about which player
        ID its been assigned, how large the grid is, and where the bases are for each player on 
        the grid.
        '''
        
        m = re.match("([0-9]*)\.([0-9]*)\.([0-9]*)\.([0-9]*)\.([0-9]*)\.([0-9]*)\.([0-9]*)\.([0-9]*)", msg)
        if m and int(m.group(1)) == GAME_START_CODE:
            # So the client knows which player it's displaying information for
            playerID = int(m.group(2))
            self.playerID = playerID
            
            numRows = int(m.group(3))
            numCols = int(m.group(4))
            aBaseRow = int(m.group(5))
            aBaseCol = int(m.group(6))
            bBaseRow = int(m.group(7))
            bBaseCol = int(m.group(8))
            
            # The player always starts off in the middle of his base
            myPlayer = False
            enemyPlayer = False
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
                
                self.players.append(PlayerSprite(i, playerRow, playerCol))
                if i == self.playerID: 
                    myPlayer = self.players[i-1]
                else:
                    enemyPlayer = self.players[i-1]
                i+= 1
            
            self.grid = Grid(numRows, numCols)
            self.grid.addBase(aBaseRow, aBaseCol, A_BASE_UNIT)
            self.grid.addBase(bBaseRow, bBaseCol, B_BASE_UNIT)
            self.gameStarted = True
            
            self.viewport = Viewport(self.grid, myPlayer, enemyPlayer)
        else:
            print "invalid initial conditions"
        
    def parseChange(self, msg):
        '''
        This is where the client picks apart a Change message sent from the server, and applies it
        to its own internal representation of what's going on in the game.
        
        It figures out which type of change each one is, then calls methods with the appropriate
        arguments for that particular change.
        '''
        
        if not self.gameStarted:    
            self.parseInitialConditions(msg)
            
        else:
            # The ; gets removed by the asynchat class
            msg += ";"
            tm = re.search("([0-9]*);", msg)
            changeTimestep = int(tm.group(1))
            if self.timestep == changeTimestep:
                msg = msg.rstrip(tm.group(0))
                
                m = re.match("([0-9]*\.)*[0-9]*,", msg)
                while m:
                    cmd = m.group(0)
                    i = 0
                    type = False
                    args = []
                    
                    # take the command apart and get its type and arguments
                    while cmd:
                        match = re.match("([0-9]*).", cmd)
                        if i == 0:
                            type = int(match.group(1))                              
                        else:
                            args.append(int(match.group(1)))
                                            
                        i += 1
                        cmd = cmd[len(match.group(0)):]
                    
                    if type == MOBILE_MOVE_CODE:
                        self.moveSprite(args[0], args[1], args[2])
                    elif type == MOBILE_DIRECTION_CODE:
                        self.makePlayerChangeDirection(args[0], args[1])
                    elif type == MOBILE_SPAWN_CODE:
                        self.spawnBullet(args[0], args[1], args[2])
                    elif type == MOBILE_DIE_CODE:
                        if args[0] > 2:
                            self.destroyBullet(args[0])
                    elif type == DIRT_LOSE_HEALTH_CODE:
                        self.grid.damageDirt(args[0], args[1], args[2])
                    elif type == DIRT_DIE_CODE:
                        self.grid.setObject(args[0], args[1], 0)
                    elif type == SET_HEALTH_CODE:
                        self.setPlayerHealth(args[0], args[1])
                    elif type == SET_ENERGY_CODE:
                        self.setPlayerEnergy(args[0], args[1])
                    elif type == GAME_OVER_CODE:
                        self.gameover(args[0])
                    
                    
                    msg = msg[len(m.group(0)):]
                    m = re.match("([0-9]*\.)*[0-9]*,", msg)
                
                self.timestep += 1
                
        self.displayTimestep()
        
    def spawnBullet(self, id, row, col):
        bullet = MobileSprite(id, row, col)
        bullet.setImage("bullet.png")
        self.viewport.addBullet(bullet)
        
    def destroyBullet(self, id):
        self.viewport.destroyBulletWithID(id)
        
    def setPlayerHealth(self, id, health):
        self.players[id-1].health = health
        
    def setPlayerEnergy(self, id, energy):
        self.players[id-1].energy = energy
                
    def moveSprite(self, id, row, col):
        if id < 3:
            player = self.players[id - 1]
            player.row = row
            player.col = col
        else:
            # bullets
            for bullet in self.viewport.bullets:
                if bullet.id == id:
                    bullet.row = row
                    bullet.col = col
            
    def makePlayerChangeDirection(self, id, direction):
        self.players[id-1].changeDirection(direction)
    
    def input(self):
        '''
        This is where the Client gets the player's input to send off to the server.
        It gets the keys that the player has pressed, and when the timer goes off,
        it packages those commands up and sends them off to the server.
        '''
        
        cmd = ""
        endInput = False
        noInput = False
        tick = 0
        commandHasMove = False
        while not endInput:
            movePart = False
            shootPart = False
            keydown = False
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print "Exiting"
                    self.exit()
                if event.type == KEYDOWN:
                    keydown = event.key
                    if event.key == LEFT_KEY:
                        self.movedAtStep = self.timestep
                        movePart = "%d" % LEFT
                    elif event.key == RIGHT_KEY:
                        self.movedAtStep = self.timestep
                        movePart = "%d" % RIGHT
                    elif event.key == UP_KEY:
                        self.movedAtStep = self.timestep
                        movePart = "%d" % UP
                    elif event.key == DOWN_KEY:
                        self.movedAtStep = self.timestep
                        movePart = "%d" % DOWN
                    elif event.key == SHOOT_KEY:
                        if self.shotAtStep not in range(self.timestep - SHOOT_TIMESTEP_WAIT, self.timestep):
                            self.shotAtStep = self.timestep
                            shootPart = "%d" % SHOOT
                    elif event.key == K_ESCAPE:
                        print "Escape key pressed"
                        self.exit()
          
            key = pygame.key.get_pressed()
            if key[LEFT_KEY]:
                if self.movedAtStep not in range(self.timestep - MOVE_TIMESTEP_WAIT, self.timestep):
                    self.movedAtStep = self.timestep
                    movePart = "%d" % LEFT
            if key[RIGHT_KEY]:
                if self.movedAtStep not in range(self.timestep - MOVE_TIMESTEP_WAIT, self.timestep):
                    self.movedAtStep = self.timestep
                    movePart = "%d" % RIGHT
            if key[UP_KEY]:
                if self.movedAtStep not in range(self.timestep - MOVE_TIMESTEP_WAIT, self.timestep):
                    self.movedAtStep = self.timestep
                    movePart = "%d" % UP
            if key[DOWN_KEY]:
                if self.movedAtStep not in range(self.timestep - MOVE_TIMESTEP_WAIT, self.timestep):
                    self.movedAtStep = self.timestep
                    movePart = "%d" % DOWN
            if key[SHOOT_KEY]:
                if self.shotAtStep not in range(self.timestep - SHOOT_TIMESTEP_WAIT, self.timestep):
                    self.shotAtStep = self.timestep
                    shootPart = "%d" % SHOOT
          
            tick += self.clock.tick_busy_loop(FPS)         
            # So the game doesn't wait forever  
            if tick > TICK_LIMIT:
                endInput = True 
        
        cmd = ""
        if movePart:
            cmd += movePart
        else:
            cmd += "0"
        if shootPart:
            cmd += shootPart
        else:
            cmd += "0"
        
        cmd += ".%d;" % self.timestep

        self.outBuffer += cmd
        
    def updateHUD(self):
        '''
        Shows the player's health and energy at the bottom of the screen.
        '''
        
        healthFontSurf = self.font.render("Health: %d" % self.viewport.player.health, True, (255, 255, 255))
        energyFontSurf = self.font.render("Energy: %d" % self.viewport.player.energy, True, (255, 255, 255))
        self.screen.blit(healthFontSurf, (7, VP_HEIGHT + 9))
        self.screen.blit(energyFontSurf, (7, VP_HEIGHT + 5 + FONT_SIZE))
        
    def displayTimestep(self):
        '''
        Gets the viewport to update to display the latest timestep.
        '''
        
        self.screen.fill((50, 50, 50))
        self.updateHUD()
        self.viewport.updateDisplay()
        self.screen.blit(self.viewport.surf, (0, 0))
        pygame.display.flip()
        
    def displayTitleScreen(self):
        '''
        When the user first opens the Client, they are smacked in the face with this Title screen.
        '''
        titleScreenImage = imageLoad("TitleScreen.png")
        breakLoop = False
        c = 0
        while not breakLoop:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print "Exiting"
                    self.exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        print "Escape key pressed"
                        self.exit()
                    if event.key == K_RETURN:
                        self.indicateReadiness()
                        breakLoop = True
                        
            self.screen.fill((0,0,0))
            self.screen.blit(titleScreenImage, (0,0))
            if not breakLoop:
                cs = self.titleFont.render("You are connected to %s." % self.host, False, (255, 255, 255))
                es = self.titleFont.render("Press ENTER when you are ready to play.", True, (255, 255, 255))
                self.screen.blit(cs, (45, 350))
                self.screen.blit(es, (10, 375))
            else:
                rs = self.font.render("READY...", True, (255, 255, 255))
                ws = self.titleFont.render("Waiting for other player...", True, (255,255,255))
                self.screen.blit(rs, (102, 230))
                self.screen.blit(ws, (70, 270))
            pygame.display.flip()

    def gameover(self, idOfLoser):
        '''
        When the game ends, the game displays the full grid and the loser.
        '''
        
        self.screen.fill((0,0,0))
        renderedFont = False
        if idOfLoser == self.viewport.player.id:
            renderedFont = self.font.render("LOSS.", False, (255,255,255))
        else:
            renderedFont = self.font.render("VICTORY.", False, (255,255,255))
        helpfulFont = self.titleFont.render("Press ESC to quit.", False, (255,255,255))
        self.screen.blit(renderedFont, (5, 5))
        self.screen.blit(helpfulFont, (5, 40))
        pygame.display.flip()
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print "Exiting"
                    self.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        print "Escape key pressed"
                        self.exit()

    def indicateReadiness(self):
        '''
        Tell the server that this client is ready to play a game.
        '''

        self.outBuffer += "%d;" % GAME_START_CODE
            
    def exit(self): 
        self.close()
        sys.exit(0)
            
if __name__ == "__main__":
    # Usage: python Client.py ip port
    if len(sys.argv) >= 3:
        c = Client(sys.argv[1], int(sys.argv[2]))
    else:
        c = Client('localhost', 61673)
    asyncore.loop()
