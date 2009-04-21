MAX_FPS = 30
DISPLAY_SIZE = 11
GRID_SIZE = 300
DIRT_HEALTH = 3
# should always be an odd number > 1, so that base entrances line up
BASE_SIZE = 5

# Health / Energy
MAX_HEALTH = 100
MAX_ENERGY = 100
HEALTH_INCREASE_TIME = 1 * MAX_FPS / 2
ENERGY_INCREASE_TIME = 1 * MAX_FPS / 2
AWAY_ENERGY_INCREASE_TIME = 1 * MAX_FPS
# every x number of seconds energy will decrease
ENERGY_DECREASE_TIME = 3 * MAX_FPS
SHOOTING_ENERGY_DECREASE = .1

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

# A player can move over his own bullet without effect
MOVABLES = [EMPTY, B1, B2, BULLET]
COLLIDABLES = [P1, P2, H_WALL, V_WALL, FOG, DIRT]
KILLABLES = [P1, P2, DIRT]
TEMPORARIES = [BULLET]
BASES = [B1, B2]

# append debugging errors to this to get printed by viewport
error = []
DEBUG = True

