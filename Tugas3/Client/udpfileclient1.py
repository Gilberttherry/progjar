import sys
import socket
import threading
import os

SERVER_PORT = 9930
SERVER_IP = "127.0.0.1"

class ClientConnection:
    def __init__(self, conn):
        print "command : ls, kirim 'nama' dan req 'nama'"
        self.conn = conn
        connInfo = conn.getsockname()
        print "Connected to " + str(connInfo[0]) + ":" + str(connInfo[1])
    def run(self):
        while True:
            request = sock.recv(1024).rstrip()
            print request,
            if request[:5] == "READY":
                cmd = raw_input()
                self.parseRequest(cmd)
            
    def parseRequest(self, request):
        if request[:5] == "kirim":
            self.krmfile(request[6:])
        elif request[:3] == "req":
            self.reqfile(request[4:])
        elif request[:3] == "ls":
            self.send("list")
            print self.recv().rstrip()
        else:
            self.send("$")
            print self.recv().rstrip()

    def reqfile(self, fileName):
        self.send("req " + fileName)
        ok = self.recv()
        if ok[:2] != "OK":
            print "[ERR] Invalid response : " + ok
            return
        self.send("OK")
        fp = open(fileName, "wb+")
        received = 0
        while True:
            data = self.recv()
            if data[:3] == "END":
                fp.close()
                print "End of " + fileName
                break
            else:
                fp.write(data) 
                received += len(data)
                #print "Received "+ str(received)
                
    def krmfile(self, name):
        fp = None
        try:
            fp = open(name, "rb")
        except:
            print "[ERR] File Tidak Ada"
            return
        payload = fp.read()
        sentSize = 0
        addr = self.conn.getsockname()
        fp.close()
        self.send("kirim "+name)
        signal = self.recv()
        if signal[:2] != "OK":
            print "[ERR] Invalid response"
            return
        for i in range((len(payload)/1024) + 1):
            data = []
            if (i+1)*1024 > len(payload):
                data = payload[i*1024:len(payload)]
                sentSize += len(data)
                data.ljust(1024)
            else:
                data = payload[i*1024:(i+1)*1024]
                sentSize += len(data)
            self.send(data)
        self.send("END")

    def send(self, payload):
        self.conn.send(payload.ljust(1024))

    def recv(self):
        return self.conn.recv(1024)

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
print >>sys.stderr, 'connecting '
sock.connect((SERVER_IP,SERVER_PORT))

conn = ClientConnection(sock)
conn.run()
