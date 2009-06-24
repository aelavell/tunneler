import sys, os
from Grid import *
from Basic import *
from Object import *
from Movable import *
from Player import *
from Constants import *
import pygame
from pygame.locals import *

class Game():
    def __init__(self):
        # Required to get pygame's event handling
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.mouse.set_visible(0)
        self.clock = pygame.time.Clock()
        #pygame.event.set_grab(True)
        
        self.grid = Grid()
        self.grid.addBase(B1, 10, 10)  
        self.grid.addBase(B2, 3, 4)
        
        self.player1 = Player(5, 6, self.grid, P1, P2, B1, B2)
        self.player2 = Player(12, 12, self.grid, P2, P1, B2, B1)
        self.player1.setControls(P1_CONTROLS)
        self.player2.setControls(P2_CONTROLS)
        self.players = [self.player1, self.player2]
        
        self.vp1 = Viewport(self.grid, self.player1)
        self.vp2 = Viewport(self.grid, self.player2)
        self.viewports = [self.vp1, self.vp2]
            
    def startGame(self):
        ''' Starts the game. '''
        
        self.gameOn = True        
    
    def endGame(self):
        ''' Ends the game. '''
        
        self.gameOn = False

    def mainLoop(self):
        self.startGame()
        
        # Main game loop
        while self.gameOn:
            for player in self.players:
                player.update()
                
                if player.isDead():
                    self.endGame()
                    
                for bullet in player.getBullets():
                    bullet.move()
                
            x = 0
            for viewport in self.viewports:
                # Display everything
                viewport.createSprites()
                viewport.updateDisplay()
                self.screen.blit(viewport.getDisplay(), (x, 0))
                x += 425
            
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.endGame()
            
            # keep the game running at the right speed
            self.clock.tick(MAX_FPS)
            pygame.display.flip()
        
