#*******************************************************************************
# Networking Test
# server.py
#
# Messing about with sockets.
#
#
#*******************************************************************************

import sys
import socket
import threading

#*******************************************************************************

class ClientThread(threading.Thread):

    def run(self):
        pass

#*******************************************************************************

class Server():

    def __init__(self):

        self.socket = socket.socket()
        self.socket.bind(("",2000))
        self.socket.listen(5)

        print "Server initialised."

    def run(self):

        print "Server running."

        while 1:

            (clientsocket, address) = self.socket.accept()
            print clientsocket, address

            clientThread = ClientThread()
            clientThread.start()

#*******************************************************************************

def main():

    server = Server()
    server.run()

#*******************************************************************************

if __name__ == '__main__':

    try:
        main()
    except:
        print sys.excepthook(*sys.exc_info())
        w = raw_input()