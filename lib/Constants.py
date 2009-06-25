from pygame.locals import *

DISPLAY_SIZE = 13
GRID_SIZE = 30
DIRT_HEALTH = 3
# should always be an odd number > 1, so that base entrances line up
BASE_SIZE = 5

# Pygame-related
MAX_FPS = 30
VP_WIDTH = 312
VP_HEIGHT = 400
SCREEN_HEIGHT = 400
SCREEN_WIDTH = 666
FONT_SIZE = 40
PIXELS_PER_UNIT = 24

# Health / Energy
MAX_HEALTH = 100
MAX_ENERGY = 100
HEALTH_INCREASE_TIME = 1 * MAX_FPS / 2
ENERGY_INCREASE_TIME = 1 * MAX_FPS / 2
AWAY_ENERGY_INCREASE_TIME = 1 * MAX_FPS
# every x number of seconds energy will decrease
ENERGY_DECREASE_TIME = 3 * MAX_FPS
SHOOTING_ENERGY_DECREASE = .1

P1 = 'p1'
B1 = 'b1'
P2 = 'p2'
B2 = 'b2'
DIRT = 'd'
EMPTY  = 'e'
FOG = 'f'
V_WALL = 'vw'
H_WALL = 'hw'
BULLET = 'b'

NORTH = 'n'
EAST = 'e'
WEST = 'w'
SOUTH = 's'
NORTHEAST = 'ne'
NORTHWEST = 'nw'
SOUTHEAST = 'se'
SOUTHWEST = 'sw'

# A player can move over his own bullet without effect
MOVABLES = [EMPTY, B1, B2, BULLET]
COLLIDABLES = [P1, P2, H_WALL, V_WALL, FOG, DIRT]
KILLABLES = [P1, P2, DIRT]
TEMPORARIES = [BULLET]
BASES = [B1, B2]

# append debugging errors to this to get printed by viewport
error = []
DEBUG = True

# Controls
P1_CONTROLS  = {NORTH: K_w, SOUTH: K_s, EAST: K_d, WEST: K_a, 'SHOOT': K_SPACE}
P2_CONTROLS = {NORTH: K_UP, SOUTH: K_DOWN, EAST: K_RIGHT, WEST: K_LEFT, 'SHOOT': K_RCTRL}

