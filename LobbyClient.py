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
import asyncore
import asynchat 

class LobbyClient(asyncore.dispatcher):
    def __init__(self, host, port, username):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port
        self.connect((host,port))
        self.username = username
        self.outBuffer = ""
    
    def writable(self):
        return (len(self.outBuffer) > 0)

    def handle_read(self):
        print self.recv(1024)
        if len(self.outBuffer) == 0:
            self.input() 
        
    def parseServerMessage(self, msg):
        pass

    def handle_write(self):
        sent = self.send(self.outBuffer)
        self.outBuffer = self.outBuffer[sent:]

    def input(self):
        self.outBuffer += raw_input("> ") + "\r\n"

if __name__ == "__main__":
    l = LobbyClient('localhost', 10000, 'daroot')
    asyncore.loop()


