from Constants import *
from Grid import *
from Object import *
from Dirt import *
from Player import *
from Viewport import *

class Base():   
    ''' The base is the area for the player to refuel on energy
    and shields. When a player is in his own base, he gets both
    energy and shields, and when he's in an opposing player's
    base, he gets only energy. Thus, the bases have to be 
    distinguished from each other. There are walls all around
    the base, with an empty space in the centre of each wall
    for the player to enter through. '''
   
    def __init__(self, p, TLC):
        '''The "p" argument for this  method defines which player the base
        is being created for. The coords argument gives the 
        coordinates of the top-left part of the base, so that
        the base can be inserted into the grid at the proper coords.
        These will be generated randomly under a set of rules
        defined by how many people are playing, etc... '''
        
        self.base = [['-', '-', EMPTY, '-', '-'],
                ['|', B1, B1, B1, '|'],
                ['|', B1, B1, B1, '|'],
                ['|', B1, B1, B1, '|'],
                ['-', '-', EMPTY, '-', '-']]
        
        # TLC is top-left coordinates of the base
        self.TLC = TLC
        coords2 = list(TLC)
        # BRC is the bottom-right coordinates of the base
        self.BRC = (coords2[0] + (len(self.base) - 1), coords2[1] + (len(self.base[4]) -1))

    def getTLC(self):
        return self.TLC

    def getBRC(self):
        return self.BRC

    def getItem(self):
        return self.base
