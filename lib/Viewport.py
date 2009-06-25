import pygame
from pygame.locals import *

from Constants import *
from Grid import *
from Object import *
from Dirt import *
from Viewport import *

class Viewport():
    def __init__(self, grid, player):
        self.grid = grid
        self.player = player
        self.surf = pygame.Surface((375, SCREEN_HEIGHT))
        self.sprites = pygame.sprite.Group()
        pygame.font.init()
        self.font = pygame.font.Font(None, FONT_SIZE)
        
    def HUD(self):
        ''' The HUD (Heads-Up Display) shows off the player's
        health and energy. '''
        
        print "Health: ", self.player.getHealth()
        print "Energy: ", self.player.getEnergy()
    
    def createSprites(self):
        ''' Displays a view centered on the player.'''
        
        self.sprites.empty()
        rowCount = 1
        row = self.player.getRow() - (DISPLAY_SIZE / 2)
        maxRow = self.player.getRow() + (DISPLAY_SIZE / 2)
        maxCol = self.player.getCol() + (DISPLAY_SIZE / 2)
        while row <= maxRow:
            colCount = 1
            col = self.player.getCol() - (DISPLAY_SIZE / 2)
            while col <= maxCol:
                sprite = self.grid.get(row, col)
                sprite.setPosition(colCount * PIXELS_PER_UNIT / 2, rowCount * PIXELS_PER_UNIT / 2)
                self.sprites.add(sprite)
                col += 1
                colCount += 1              
                
            row += 1
            rowCount += 1
            
    def updateDisplay(self):
        self.sprites.update()
        self.surf.fill((0,0,0))
        self.sprites.draw(self.surf)
        health = pygame.font.Font.render(self.font, "Health: %s" %self.player.getHealth(), FONT_SIZE, (255,255,255))
        energy = pygame.font.Font.render(self.font, "Energy: %s" %self.player.getEnergy(), FONT_SIZE, (255,255,255))
        self.surf.blit(health, (0, 375))
        self.surf.blit(energy, (0, 425))
            
    def getDisplay(self):
        return self.surf
            
