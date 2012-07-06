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

from Command import *
from Constants import *
from GridSprite import *

class MobileSprite(GridSprite):
    def __init__(self, id, row, col):
        GridSprite.__init__(self, id, row, col)
        