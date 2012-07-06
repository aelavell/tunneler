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

import sys
import socket
import asyncore
import asynchat
import re

from Game import *
from PlayerHandler import *
            
class Server(asyncore.dispatcher):
    ''' 
    This is the class handling Tunneler's initial connections. It creates 
    handlers for each of the clients, and it creates the game itself.
    '''
    
    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)
        self.playerHandlers = []
        self.readyHandlers = []
        self.game = False
        self.inBuffer = ""

    def handle_accept(self):
        ''' The server will only accept new connections when it does not
            have a game running. '''

        if not self.game:
            pair = self.accept()
            if pair is None:
                pass
            else:
                sock, addr = pair
                # This is required so that things like nmap won't crash the server
                try:
                    ph = PlayerHandler(sock, addr, self)
                    self.playerHandlers.append(ph)
                    print "%s has connected." % repr(addr)
                except:
                    pass
                
    def removePlayerHandler(self, handler):
        self.playerHandlers.remove(handler)
        
    def handlerReadyToPlay(self, handler):
        '''
        When a player is ready to play, it will send the server a specific message indicating
        that this is the case. When enough players are ready, the game will commence.
        '''
        
        self.readyHandlers.append(handler)
        if len(self.readyHandlers) == 2:
            self.startGame()
                
    def sendMessageToAllClients(self, message, username):
        for lobbyHandler in self.lobbyHandlers:
            lobbyHandler.outBuffer += "%s says: %s" % (username, message)

    def startGame(self):  
        '''
        Spawns an instance of the Game class, passing the handlers for the clients 
        who want to play a game as initialization.
        '''
          
        if len(self.readyHandlers) >= 2:
            numRows = 100
            numCols = 100
            self.game = Game(self.readyHandlers, numRows, numCols, self) 
            
    def gameOver(self):
        self.game = False
        self.readyHandlers = []
            
if __name__ == "__main__":
    if len(sys.argv) >= 3:
        s = Server(sys.argv[1], int(sys.argv[2]))
    else:
        c = Server('localhost', 61673)

    asyncore.loop()

