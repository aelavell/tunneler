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

import pygame
from pygame.locals import *

from Constants import *
from GUIConstants import *
from Grid import *
from GridSprite import *
from PlayerSprite import *

class Viewport():
    '''
    Takes the game and displays it on the screen using Pygame.
    '''
    
    def __init__(self, grid, player, enemyPlayer):
        self.grid = grid
        self.player = player
        self.enemyPlayer = enemyPlayer
        self.players = [player, enemyPlayer]
        self.bullets = []
        self.surf = pygame.Surface((VP_WIDTH, VP_HEIGHT))
        self.sprites = pygame.sprite.OrderedUpdates()
        self.font = pygame.font.Font(None, FONT_SIZE)
        
    def addBullet(self, bullet):
        self.bullets.append(bullet)
        
    def destroyBulletWithID(self, id):
        for bullet in self.bullets:
            if bullet.id == id:
                self.bullets.remove(bullet)
                break
    
    def createSprites(self):
        ''' Creates a group of sprites represent the grid surrounding the player
        and the player himself. '''
        
        self.sprites.empty()
        rowCount = 0
        row = self.player.row - (NUM_UNITS / 2)
        maxRow = self.player.row + (NUM_UNITS / 2)
        maxCol = self.player.col + (NUM_UNITS / 2)
        while row <= maxRow:
            colCount = 0
            col = self.player.col - (NUM_UNITS / 2)
            while col <= maxCol:
                playerSprite = False
                sprite = False
                getFromGrid = True
                for player in self.players:
                    if player.row == row and player.col == col:
                        #getFromGrid = False
                        playerSprite = player
                        break 
                        
                for bullet in self.bullets:
                    if bullet.row == row and bullet.col == col:
                        #print bullet
                        #getFromGrid = False
                        playerSprite = bullet
                        break
                          
                if getFromGrid:  
                    id = self.grid.objectAt(row, col)
                    
                    if id != NOTHING_UNIT:
                        sprite = GridSprite(id, row, col)
                    
                        if id == 0:
                            sprite.setImage("e.png")
                        if id == 1:
                            sprite.setImage("d1.png")
                        elif id == 2: 
                            sprite.setImage("d2.png")
                        elif id == 3:
                            sprite.setImage("d3.png")
                        elif id == A_BASE_UNIT:
                            sprite.setImage("a.png")
                        elif id == B_BASE_UNIT:
                            sprite.setImage("b.png")
                
                if sprite: 
                    sprite.setPosition(colCount * PIXELS_PER_UNIT, rowCount * PIXELS_PER_UNIT)
                    self.sprites.add(sprite)
                if playerSprite: 
                    playerSprite.setPosition(colCount * PIXELS_PER_UNIT, rowCount * PIXELS_PER_UNIT)
                    self.sprites.add(playerSprite)
                col += 1
                colCount += 1              
                
            row += 1
            rowCount += 1
            
    def updateDisplay(self):
        #self.sprites.update()
        self.createSprites()
        self.surf.fill((128,128,128))
        self.sprites.draw(self.surf)
        #health = pygame.font.Font.render(self.font, "Health: %s" %self.player.getHealth(), FONT_SIZE, (255,255,255))
        #energy = pygame.font.Font.render(self.font, "Energy: %s" %self.player.getEnergy(), FONT_SIZE, (255,255,255))
        #self.surf.blit(health, (0, 325))
        #self.surf.blit(energy, (0, 365))
            
