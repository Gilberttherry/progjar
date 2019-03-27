import sys
import socket
import threading
import os

PORT = 9930
SERVER = "127.0.0.1"
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind the socket to the port
print >>sys.stderr, 'starting up'
sock.bind((SERVER, PORT))
# Listen for incoming connections
sock.listen(5)


class a:
    def __init__(self,conn):
        self.conn = conn
        self.cwd = os.path.dirname(os.path.realpath(__file__))

    def handleRequest(self):
        while True:
            self.send("READY $"+self.cwd+": ")
            data = self.conn.recv(1024)
            sockInfo = self.conn.getsockname()
            if len(data) == 0:
                print "Selesai " + str(sockInfo[0]) + ":" + str(sockInfo[1])
                return
            else:
                self.parseRequest(data)

                
    def parseRequest(self, request):
		#List
        if request[:4] == "list":
            self.sendList()
		#request
        if request[:3] == "req":
            self.reqfile(request[4:].rstrip())
		#Kirim
        elif request[:5] == "kirim":
            self.krmfile(request[6:].rstrip())
        else:
            self.send("[ERR] File Tidak Ada")
	
    def send(self, packet):
        self.conn.send(packet.ljust(1024))

    def recv(self):
        return self.conn.recv(1024)

    def sendList(self):
        files = os.listdir(self.cwd)
        res = ""
        for file in files:
            res += file + "\n"
        self.send(res)

    def krmfile(self, fileName):
        fp = open(fileName, "wb+")
        self.send("OK")
        received = 0
        while True:
            data = self.recv()
            if data[:3] == "END":
                fp.close()
                print "Diterima " + fileName
                break
            else:
                fp.write(data) 
                received += len(data)
                #print "Received "+ str(received)

    def reqfile(self, name):
        fp = None
        try:
            fp = open(self.cwd + "/" + name, "rb")
            self.send("OK")
        except e:
            self.send("[ERR] " + e)
            return
        payload = fp.read()
        sentSize = 0
        addr = self.conn.getsockname()
        fp.close()
        while True:
            signal = self.recv()
            if signal[:2] == "OK":
                break
            else:
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
        self.send("Sended")



while True:
    print "Waiting"
    conn, addr = sock.accept()
    print 'Incoming connection from', addr
    aktiv = a(conn)
    thread = threading.Thread(target=aktiv.handleRequest)
    thread.start()

            

