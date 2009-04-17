import sys, os
from Grid import *
from Base import *
from Object import *
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
        
        self.grid = Grid()
        self.grid.addBase(B1, 3, 4)  
        
        self.player = Player(6, 8, self.grid)
        self.vp = Viewport(self.grid, self.player)
        
    def clearScreen(self):
        if os.name == 'posix':
            os.system('clear')
        elif os.name in ("nt", "dos", "ce"):
            # DOS/Windows
            os.system('CLS')
            
    def mainLoop(self):
        done = False
        refreshCount = 0
        
        # Main game loop
        while not done:
            if refreshCount == REFRESH_RATE:
                self.clearScreen()

                self.player.update()
                
                # Display everything
                self.vp.display()
                self.vp.HUD()
                
                refreshCount = 0 

            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        done = True
                    elif event.key == K_w:
                        self.player.move('n') 
                    elif event.key == K_s:
                        self.player.move('s')
                    elif event.key == K_d:
                        self.player.move('e')
                    elif event.key == K_a:
                        self.player.move('w')

            refreshCount += 1

        # The game's over, clear the terminal
        #self.clearScreen()
        
