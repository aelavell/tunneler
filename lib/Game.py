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
        
        gridSize = 30 
        self.grid = Grid(gridSize, 2, 'd')
        base1 = Base('r', (0,0))
        base2 = Base('b', (10,10))
        #grid.replace(base1)        
        #grid.replace(base2)       

        self.player = Player(2, 2, self.grid)

    def mainLoop(self):
        done = False
        refreshCount = 0
        
        # Main game loop
        while not done:
            if refreshCount == REFRESH_RATE:
                if os.name == 'posix':
                    os.system('clear')
                elif os.name in ("nt", "dos", "ce"):
                # DOS/Windows
                    os.system('CLS')

                for row in self.grid.read([0,0], [10,10]):
                    print 
                    for item in row:
                        print item,
                
                refreshCount = 0 

            for event in pygame.event.get():
                if (event.type == KEYUP) or (event.type == KEYDOWN):
                    if event.key == K_ESCAPE:
                        done = True
                    elif event.key == K_a:
                        print "wong"
                    elif event.key == K_w:
                        pass


            refreshCount += 1

        