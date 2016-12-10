import socket
import os

def getFile(sock):
    filename = sock.recv(1024)
    data = sock.recv(1024)
    filesize = long(data)
    f = open('new_'+filename, 'wb')
    data = sock.recv(1024)
    totalRecv = len(data)
    f.write(data)
    while totalRecv < filesize:
        data = sock.recv(1024)
        totalRecv += len(data)
        f.write(data)
        print "{0:.2f}".format((totalRecv/float(filesize))*100)+ "% Done"
    print "Download Complete!"
    f.close()

    sock.close();



def Main():
    host = '127.0.0.1'
    port = 5000

    s = socket.socket()
    s.bind((host, port))

    s.listen(5);

    print "Server Started..."

    while True:
        c, addr = s.accept()
        print "client connedted ip:<" + str(addr) + ">"
        getFile(c);

    s.close();

if __name__ == '__main__':
    Main()
