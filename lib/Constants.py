MAX_FPS = 30
DISPLAY_SIZE = 11
GRID_SIZE = 30
DIRT_HEALTH = 1
# should always be an odd number, so that base entrances line up
BASE_SIZE = 9

# Health / Energy
MAX_HEALTH = 100
MAX_ENERGY = 100
HEALTH_INCREASE_RATE = 1
ENERGY_INCREASE_RATE = 1

P1 = '@'
B1 = '#'
P2 = '$'
B2 = '&'
DIRT = 'd'
EMPTY  = '.'
FOG = 'f'
V_WALL = '|'
H_WALL = '-'
BULLET = '*'
NORTH = 'n'
EAST = 'e'
WEST = 'w'
SOUTH = 's'

COLLIDABLES = [P1, P2, H_WALL, V_WALL, FOG, DIRT]
KILLABLES = [P1, P2, DIRT]

# append debugging errors to this to get printed by viewport
error = []
DEBUG = True

