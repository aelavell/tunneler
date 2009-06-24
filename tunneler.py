import sys
# The first element in the sys.path list is the top level directory 
# of the program
root = sys.path[0]
sys.path.append(root + "/lib")

from Game import *
	   
if __name__ == "__main__":
	g = Game()
	g.mainLoop()
