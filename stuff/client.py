#*******************************************************************************
# Networking Test
# client.py
#
# Messing about with sockets.
#
#
#*******************************************************************************

import sys
import socket

class Client():

    def __init__(self):
        pass

    def connect(self):
        self.socket = socket.socket()
        self.socket.connect(("localhost", 2000))

def main():

    client = Client()
    client.connect()

#*******************************************************************************

if __name__ == '__main__':

    try:
        main()
    except:
        print sys.excepthook(*sys.exc_info())
        w = raw_input()