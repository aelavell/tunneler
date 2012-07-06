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

class Command:
    ''' 
    Commands from the client can have a move part, and a shoot
    part. Shoot is a boolean, either a client is shooting at a
    given timestep or it is not. Move can be any of 4 values, 
    that indicate whether it is moving left, right, up, or
    down.
    '''
    
    def __init__(self, id, move, shoot, timestep):
        self.id = id
        self.move = move
        self.shoot = shoot
