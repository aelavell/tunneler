from Constants import *
from Object import *

class BaseFloor(Object):
    ''' The floor of a base has special properties -
    it heals the owner of the base, and replenishes 
    their energy. If an enemy is on the basefloor,
    it doesn't heal them, but it does replenish their
    energy, albeit more slowly. '''
    
    def __init__(self, col, row, type):
        Object.__init__(col, row, type)
        
    
