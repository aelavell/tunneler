'''
Copyright 2011 Allan Lavell 
This file is part of Tunneler2.

   Tunneler2 is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   Tunneler2 is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with Tunneler2.  If not, see <http://www.gnu.org/licenses/>.
'''

MOVE_DIRT_DAMAGE = 1
BULLET_DIRT_DAMAGE = 2
BULLET_PLAYER_DAMAGE = 25
SHOOT_ENERGY_LOSS = 2
SHOOT_TIMESTEP_WAIT = 3
MOVE_TIMESTEP_WAIT = 0

SET_HEALTH_CODE = 10
SET_ENERGY_CODE = 12
MOBILE_DIE_CODE = 14
MOBILE_MOVE_CODE = 15   
MOBILE_DIRECTION_CODE = 16
MOBILE_SPAWN_CODE = 17
DIRT_LOSE_HEALTH_CODE = 18
DIRT_DIE_CODE = 19
GAME_OVER_CODE = 20
GAME_START_CODE = 21
BAD_COMMAND_CODE = 22
BAD_TIMESTEP_CODE = 23
RESEND_CODE = 24

MAX_PLAYER_ENERGY = 100
MAX_PLAYER_HEALTH = 100

LOSE_ENERGY_TIMEOUT = 10
GAIN_ENERGY_TIMEOUT = 2
GAIN_HEALTH_TIMEOUT = 10

BASE_SIZE = 5
A_BASE_UNIT = -1
B_BASE_UNIT = -2
NOTHING_UNIT = -3

NO_CHANGE = 0
LEFT = 1
RIGHT = 2
UP = 3
DOWN = 4
SHOOT = 5


