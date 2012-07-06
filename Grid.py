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

import random
import math

from Constants import *

class Grid:
    ''' The grid represents all of the immobile objects in the game.

    It is represented as follows:

    -2 player 2 base
    -1 player 1 base
    0 empty
    1, 2, 3 dirt
    '''

    def __init__(self, numRows, numCols):
        # The grid's id is always zero
        self.id = 0
        
        self.numRows = numRows
        self.numCols = numCols
        self.usedQuads = []
        self.reformatWithDirt()
        
    def addBase(self, baseRow, baseCol, baseUnit):
        ''' 
        Overwrites a section of the grid with the base unit given.
        '''
        
        if baseUnit == A_BASE_UNIT:
            self.aBaseRow = baseRow
            self.aBaseCol = baseCol
        else:
            self.bBaseRow = baseRow
            self.bBaseCol = baseCol
        
        rowIndex = baseRow
        while rowIndex < BASE_SIZE + baseRow:
            colIndex = baseCol
            while colIndex < BASE_SIZE + baseCol:
                self.matrix[rowIndex][colIndex] = baseUnit
                colIndex += 1
            rowIndex += 1
            
    def createRandomBasePosition(self):
        ''' 
        Returns the row and column information of the top left corner for
        a randomly generated base position.
        '''

        possibleQuadrants = [1, 2, 3, 4]
        for quad in self.usedQuads:
            possibleQuadrants.remove(quad) 
        random.shuffle(possibleQuadrants)
        quad = possibleQuadrants[0]
        self.usedQuads.append(quad)

        numRows = self.numRows
        numCols = self.numCols

        topLeftRow = 0
        topLeftCol = 0
        bottomRightRow = math.floor(numRows / 2)
        bottomRightCol = math.floor(numCols / 2)

        if quad == 1:
            pass
        elif quad == 2:
            topLeftCol = math.floor(numCols / 2)
            bottomRightCol = numCols
        elif quad == 3:
            topLeftRow = math.floor(numRows / 2) + 1
            bottomRightRow = numRows
        elif quad == 4:
            topLeftRow = math.floor(numRows / 2) + 1
            topLeftCol = math.floor(numCols / 2) + 1
            bottomRightRow = numRows
            bottomRightCol = numCols
            
        baseTopLeftRow = random.randint(topLeftRow, bottomRightRow - BASE_SIZE)
        baseTopLeftCol = random.randint(topLeftCol, bottomRightCol - BASE_SIZE)    
            
        return baseTopLeftRow, baseTopLeftCol
    
    def reformatWithDirt(self):
        '''
        Initializes the matrix and fills it with dirt.
        '''
        
        self.matrix = []

        rowIndex = 0
        while rowIndex < self.numRows:
            row = []

            colIndex = 0
            while colIndex < self.numCols:
                row.append(3)
                colIndex += 1

            self.matrix.append(row)
            rowIndex += 1
          
    def setObject(self, row, col, value):
        self.matrix[row][col] = value
           
    def objectAt(self, row, col):
        if self.coordsInGrid(row, col):
            return self.matrix[row][col]
        else:
            return NOTHING_UNIT
            
    def coordsInGrid(self, row, col):
        '''
        Returns true if the coords are in the grid,
        false if they are outside the bounds.
        '''
        
        if row < 0 or col < 0 or row >= self.numRows or col >= self.numCols:
            return False
        else:
            return True
        
    def objectIsDirt(self, row, col):
        '''
        Dirt is represented as nonzero number (currently 1, 2, or 3).
        This method lets you know if a unit at a particular coordinate is 
        dirt or not.
        '''
        
        return self.matrix[row][col] > 0

    def damageDirt(self, row, col, amount):
        ''' The only immobile type of unit on the grid that can take damage
        is dirt, which is represented as an int > 0. '''

        change = ""
        if not self.objectIsDirt(row, col):
	        return change
		
        unit = self.matrix[row][col]  
        unit -= amount
        if unit < 0:
            unit = 0
        self.matrix[row][col] = unit
       
        # the dirt died
        if unit == 0:
            change = "%d.%d.%d," % (DIRT_DIE_CODE, row, col)
        # otherwise it just lost health
        else:
            change = "%d.%d.%d.%d," % (DIRT_LOSE_HEALTH_CODE, row, col, amount)
			
        return change

    def printGrid(self):
        ''' Convenience method to print a terminal-friendly look at the grid. '''

        for row in self.matrix:
            print row
        print ""