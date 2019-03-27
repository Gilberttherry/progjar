import socket
import select
import time

CLIENT_IP = "127.0.0.2"
PORT = 9000
NAMAFILE= "/new_%s"


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((CLIENT_IP, PORT))

while True:
    data, addr = sock.recvfrom(1024)
    print("sedang menerima "+data)
    if data:
        print "nama file :", data
        file_name = NAMAFILE % data

    f = open(file_name, 'wb+')

    while True:
        ready = select.select([sock], [], [], 10)
        if ready[0]:
            data, addr = sock.recvfrom(8192)
            f.write(data)
        else:
            print "file %s telah diterima" % file_name
            f.close()
break
