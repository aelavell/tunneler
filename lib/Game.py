import sys, os
from Grid import *
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
        screen = pygame.display.set_mode((1, 1))
        pygame.mouse.set_visible(0)
        self.clock = pygame.time.Clock()
        #pygame.event.set_grab(True)
        
        self.grid = Grid()
        self.grid.addBase(B1, 10, 10)  
        self.grid.addBase(B2, 3, 4)
        
        p1Controls = {NORTH: K_w, SOUTH: K_s, EAST: K_d, WEST: K_a, 'SHOOT': K_SPACE}
        p2Controls = {NORTH: K_UP, SOUTH: K_DOWN, EAST: K_RIGHT, WEST: K_LEFT, 'SHOOT': K_RCTRL}
        
        self.player1 = Player(5, 6, self.grid, P1, P2, B1, B2)
        self.player2 = Player(12, 12, self.grid, P2, P1, B2, B1)
        self.player1.setControls(p1Controls)
        self.player2.setControls(p2Controls)
        self.players = [self.player1, self.player2]
        
        self.vp1 = Viewport(self.grid, self.player1)
        self.vp2 = Viewport(self.grid, self.player2)
        self.viewports = [self.vp1, self.vp2]
        
    def clearScreen(self):
        if os.name == 'posix':
            os.system('clear')
        elif os.name in ("nt", "dos", "ce"):
            # DOS/Windows
            os.system('CLS')
            
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
            self.clearScreen()

            for player in self.players:
                player.update()
                
                if player.isDead():
                    self.endGame()
                    
                for bullet in player.getBullets():
                    bullet.move()
                
            for viewport in self.viewports:
                # Display everything
                viewport.display()
                viewport.HUD()
                if DEBUG == True:
                    for e in error:
                        print e
            
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.endGame()
            
            # keep the game running at the right speed
            self.clock.tick(MAX_FPS)

        # The game's over, clear the terminal
        #self.clearScreen()
        
