import socket
from socket import socket as Socket

import sys
import random
import math

class IRC_Client(object):
    
    def __init__(self, hostname, port, nick, name, channel):
        
        self.host = hostname
        self.port = port
        self.name = nick ##
        self.channel = channel
        
        if len(nick) >= 9:
            self.nick = nick[:9]
        else:
            self.nick = nick
        
        self.connection = Socket()
        self.inchannel = 0
    
    def connect(self):
        
        self.connection.connect((self.host,self.port))
    
    def register(self):
        
        self.message("NICK "+self.nick)
        self.message("USER "+self.nick+" 0 * :"+self.name)
        
        reg_pong = 0
        
        while not reg_pong:
            
            lines = self.recv()
            
            for line in lines:
                
                if line[:4] == "PING":
                    
                    self.message("PONG "+line[6:16])
                    reg_pong = 1
        
        # hack
        self.recv()
        self.recv()
        self.recv()
    
    def main(self):
        
        self.connect()
        self.register()
        
        self.message("JOIN "+self.channel)
        self.inchannel = 1
        
        while 1:
            
            lines = self.recv()
            
            for line in lines:
                
                if line == "": continue
                
                try:
                    
                    self.handle_line(line)
                
                except IndexError:
                    
                    print "Failed in handle line %s" % (line)
                    print sys.excepthook(*sys.exc_info())
    
    def handle_line(self, line):
        
        prefix, command, tail = self.parse_line(line)
        
        actions = [lambda : 0 ]
        
        if command == "PING":
            
            self.message("PONG %s") % (tail)
        
        elif command == "PRIVMSG":
            
            message = self.strip_privmsg(tail)
            print "|>"+message+"<|"
            
            if "go away, %s" % (self.name) in message:
                
                actions = [
                            lambda : self.say("Fuck off."),
                            lambda : self.quit("bah"),
                            lambda : self.quit("feh"),
                            lambda : self.say("Maybe later."),
                            lambda : self.say("No.")
                          ]
            
            elif message == "SIEG!" or message == "Sieg!" or \
                 message == "sieg!" or message == "SIEG" or \
                 message == "!SIEG" or message == "!sieg" :
                
                actions = [lambda : self.say("HEIL!")]
            
            elif message == "!schizo":
                
                actions = [lambda : self.say("go away, %s" % (self.nick))]
        
        action = random.choice(range(0,len(actions)))
        actions[action]()
        
    def strip_privmsg(self, tail):
        i = 0
        while tail[i] != ":":
            i+=1
        return tail[i+1:-2]
    
    def parse_line(self, line):
        
        line_i = 0
        
        # If prefix, extract prefix
        
        prefix = None
        
        if line[0] == ":":
            
            while line[line_i] != " ":
                
                line_i += 1
            
            prefix = line[1:line_i]
            
            if "!" in prefix:
                
                originator, remainder = prefix.split("!")
                
                if "@" in prefix:
                
                    user, host = remainder.split("@")
                
                else:
                    
                    host = ""
            
            elif "@" in prefix:
            
                originator, host = prefix.split("@")
                user = ""
            
            else:
                
                originator = prefix
                user, host = "", ""
            
            line_i += 1
            
            prefix = (originator, user, host)
        
        # Extract command
        
        command_start = line_i
        
        while line[line_i] != " ":
            
            line_i += 1
        
        command = line[command_start:line_i]
        
        # Extract tail
        
        tail = line[line_i+1:]
        
        return (prefix, command, tail)
    
    def message(self, msg):
        
        print msg
        
        msg = msg + "\r\n"
        msglen = len(msg)
        totalsent = 0
        
        while totalsent < len(msg):
        
            sent = self.connection.send(msg[totalsent:])
            totalsent += sent
    
    def recv(self):
        data = self.connection.recv(4096)
        if not data: sys.exit()
        lines = data.split("\r\n")
        for line in lines: print line
        return lines
    
    def say(self, string):
        self.message("PRIVMSG %s :%s" % (self.channel, string))
    
    def quit(self, string=""):
        self.message("QUIT %s" % (string))
        sys.exit()

def debugline(prefix, command, tail):

    print "Prefix:"
    if prefix:
        print "     Originator: %s" % (prefix[0])
        print "     User: %s" % (prefix[1])
        print "     Host: %s" % (prefix[2])
    else:
        print "     None."
    print "Command: %s" % (command)
    print "Tail: %s" % (tail)

cl = IRC_Client("irc.quakenet.org", 6667, "abot", "Abot", "#mount&blade")
cl.main()

def match_phrase(phrase_A, phrase_B, tolerance, case=0):
    
    if phrase_A == phrase_B: return 1

    difference = 0
    k = 5.0 # magic number, sorry :P
    max_error = int(math.floor((tolerance * len(phrase_A))/k))
    
    if len(phrase_A) == len(phrase_B):
        
        hash_A, hash_B = 0, 0
        
        # Actually this is shit. Hash needs work.
        for char in phrase_A.capitalize(): hash_A += ord(char)
        for char in phrase_B.capitalize(): hash_B += ord(char)
        
        i = 0
        
        while i < len(phrase_A):
            
            A = phrase_A[i]
            B = phrase_B[i]
            
            if A != B:
            
                if not case:
                
                    if A.capitalize() != B.capitalize():
                    
                        difference += 1
                else:
                
                    difference += 1
            
            i += 1
        
        if difference <= max_error:
            return 1
        else:
            return 0
        
    else:
        
        difference += abs(len(phrase_A)-len(phrase_B))