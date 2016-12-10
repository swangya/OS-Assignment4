#CSE 3320
#LAB 4
#Swangya Saurav


import socket
import os

def getFile(sock):
    filename = sock.recv(1024)
    data = sock.recv(1024)
    print "Lenth received is: " + data
    filesize = long(data)
    f = open(filename, 'wb')
    data1 = sock.recv(1024)
    totalRecv = len(data1)
    f.write(data1)
    while totalRecv < filesize:
        data1 = sock.recv(1024)
        totalRecv += len(data1)
        f.write(data1)
        print "{0:.2f}".format((totalRecv/float(filesize))*100)+ "% Done"
    print("FILE RECEIVED")
    f.close()
    data = None
    data1 = None
    sock.close();

def sendFile(sock):
    filename = sock.recv(1024)
    if os.path.isfile(filename):
        sock.send("EXISTS " + str(os.path.getsize(filename)))
        userResponse = sock.recv(1024)
        if userResponse[:2] == 'OK':
            with open(filename, 'rb') as f:
                bytesToSend = f.read(1024)
                sock.send(bytesToSend)
                while bytesToSend != "":
                    bytesToSend = f.read(1024)
                    sock.send(bytesToSend)
    else:
        sock.send("ERR ")

    sock.close()


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
        choice = c.recv(1024)

        if(choice=="1"):
            getFile(c)
        if(choice=="2"):
            sendFile(c)

    s.close();

if __name__ == '__main__':
    Main()
