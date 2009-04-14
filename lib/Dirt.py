from Constants import *
from Object import *

class Dirt(Object):
    def __init__(self, x, y):
        Object.init(x, y)
        self.setType('d') 
        self.health = 3

    def decrementHealth(self):
        health -= 1
        if health <= 0:
            self.die()

    def die(self):
        ''' When the Dirt object dies, it becomes an empty space.'''
        self.setType('.')
