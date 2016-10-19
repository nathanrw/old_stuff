#*******************************************************************************
#
#
#*******************************************************************************

from socket import socket as Socket
from threading import Thread
from msvcrt import getch

#*******************************************************************************
# 
#*******************************************************************************
class Server():

    def __init__(self):
        
        self.socket = Socket()
        self.socket.bind(("", 2001))
        self.socket.listen(5)

        self.log = []

        self.clients = []

    def start(self):

        print "*"*79
        print "* Server Started."
        print "*"*79
        print ""

        while 1:

            clientsocket, address = self.socket.accept()
            
            client = ClientThread()
            client.init(clientsocket, address, self)
            client.start()

    def addClient(self, client):
        if not client in self.clients:
            self.clients.append(client)

    def removeClient(self, client):
        if client in self.clients:
            self.clients.remove(client)

    def post(self, msg, client):
        self.log.append(msg)
        print client.name + ": " + msg
        for c in self.clients:
            c.post(client.name + ": " + msg)

#*******************************************************************************
# 
#*******************************************************************************            
class ClientThread(Thread):

    def init(self, clientsocket, address, server):
        self.clientsocket = clientsocket
        self.address = address
        self.server = server
        self.server.addClient(self)
        self.name = None

    def run(self):

        while 1:
            try:
                msg = self.clientsocket.recv(100)
            except:
                self.server.removeClient(self)
                return
            if self.name:
                self.server.post(msg, self)
            else:
                self.name = msg

        self.server.removeClient(self)

    def post(self, msg):
        self.clientsocket.send(msg)

#*******************************************************************************
# 
#*******************************************************************************
class Client():

    def __init__(self, host, port):

        self.name = raw_input("Enter a name: ")

        self.host = host
        self.port = port

        self.chars = ""

        self.reciever = RecieverThread()
        self.reciever.init(self)
        self.reciever.start()

    def post(self, msg):
        print msg

    def start(self):
        self.chars = ""
        while 1:
            char = getch()
            if ord(char) == 13:
                self.reciever.send(str(self.chars))
                self.chars = ""
            else:
                self.chars = self.chars + char
                self.showUserInput()
    def showUserInput(self):
        print "\r" + "=> " + self.chars,
    def hideUserInput(self):
        print "\r",

#*******************************************************************************
# 
#*******************************************************************************
class RecieverThread(Thread):
    
    def init(self, client):
        self.socket = Socket()
        self.socket.connect((client.host, client.port))
        self.client = client
        self.send(self.client.name)

    def run(self):
        while 1:
            msg = self.socket.recv(100)
            self.client.hideUserInput()
            self.client.post(msg)
            self.client.showUserInput()

    def send(self, msg):
        self.client.hideUserInput()
        self.socket.send(msg)
        self.client.showUserInput()