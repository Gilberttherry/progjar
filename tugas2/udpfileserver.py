import socket
import time
import sys

Client=["127.0.0.2","127.0.0.1"];
SERVER_PORT = 9000
file_name=["bart.png","axe.jpeg"];

for clients in Client: 
	for x in file_name: 
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

		sock.sendto(x, (clients, SERVER_PORT))
		print "Sending %s ..." % x

		f = open(x, "rb")
		data = f.read()
		while(data):
		    if(sock.sendto(data, (clients, SERVER_PORT))):
		        data = f.read()

		sock.close()
		f.close()
		time.sleep(10)
