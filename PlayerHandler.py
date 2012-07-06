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

import socket
import asynchat
import re

from Command import *
from Constants import *

class PlayerHandler(asynchat.async_chat):
    ''' This handler deals with the connection with a particular client, relaying his 
        commands to the Game and affecting the gamestate, and then receiving the output
        from the server so that his local gamestate can mirror that of the server. 
    '''
    
    def __init__(self, sock, addr, delegate):
        asynchat.async_chat.__init__(self, sock=sock)
        self.addr = addr
        self.player = "" 
        self.outBuffer = ""
        self.inBuffer = ""
        self.set_terminator(";")
        self.game = ""
        self.commandForCurrentTimestep = 0
        self.shouldCommit = False
        self.initialized = False
        self.delegate = delegate
        
    def writable(self):
        return self.shouldCommit
        #return (len(self.outBuffer) > 0)
    
    def handle_write(self):
        sent = self.send(self.outBuffer)
        self.outBuffer = self.outBuffer[sent:]
        if len(self.outBuffer) == 0:
            self.shouldCommit = False
            
    def handle_close(self):
        if self.game:
            self.game.gameOver(self.player)
            self.close()
    
    def collect_incoming_data(self, data):
        self.inBuffer += data

    def found_terminator(self):
        if not self.initialized:
            m = re.match("Tunneler1.0", self.inBuffer)
            if m:
                self.initialized = True
            else:
                self.destroy()
        else:
            if self.game:
                self.parseCommand(self.inBuffer.strip())
            else:
                self.parsePreGameCommand(self.inBuffer.strip())
        self.inBuffer = ""
    
    def destroy(self):
        self.close()
        self.delegate.removePlayerHandler(self)
        
    def parsePreGameCommand(self, msg):
        m = re.match("%d" % GAME_START_CODE, msg)
        if m:
            self.delegate.handlerReadyToPlay(self)

    def parseCommand(self, msg):
        '''
        Parses a command sent from the client, and encapsulates it into an object. It then gives it
        to to Game for processing.
        '''
        
        m = re.match("([0-5]{0,2})\.([0-9]*)", msg)
        #print msg
        if m:
            if not self.commandForCurrentTimestep:
                timestep = int(m.group(2))
                if timestep == self.game.timestep:
                    cmd = ""
                
                    # Just a timestep was sent, no movement or shooting
                    if len(m.group(1)) == 0:
                        cmd = Command(self.player.id, NO_CHANGE, NO_CHANGE, timestep)
                    
                    # A single command was sent, either to move or to shoot
                    elif len(m.group(1)) == 1:
                        opcode = int(m.group(1))
                        if opcode == SHOOT:
                            cmd = Command(self.player.id, NO_CHANGE, opcode, timestep)
                        else:
                            cmd = Command(self.player.id, opcode, NO_CHANGE, timestep)
                        
                    # Two commands were sent. The first must be move, the next must be shoot.     
                    elif len(m.group(1)) == 2:
                        opcode1 = int(m.group(1)[0])
                        opcode2 = int(m.group(1)[1])
                    
                        cmd = Command(self.player.id, opcode1, opcode2, timestep)
                  
                    self.commandForCurrentTimeStep = cmd  
                    self.game.addCommand(cmd)
                else:
                    self.sendMessage("%d;" % BAD_TIMESTEP_CODE)
            else:
                self.sendMessage("%d;" % RESEND_CODE)
        else:
            self.sendMessage("%d;" % BAD_COMMAND_CODE)
            
    def getCurrentCommand(self):
        '''
        Takes the current command from the handler. The game calls this method when it is ready to process the next
        command. It returns the current command, and then clears that field.
        '''
        
        return self.commandForCurrentTimestep
            
    def sendMessage(self, msg):
        self.outBuffer += msg
        self.shouldCommit = True
        
    def commitChanges(self, changes):
        self.outBuffer += changes
        self.commandForCurrentTimestep = 0
        self.shouldCommit = True