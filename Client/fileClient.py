import socket
import os

def sendFile(s):
    filename = raw_input("Filename? -> ")
    if filename != 'q':
        s.send(filename)
    else:
        exit();
    if os.path.isfile(filename):
        s.send(str(os.path.getsize(filename)))
        with open(filename, 'rb') as f:
                bytesToSend = f.read(1024)
                s.send(bytesToSend)
                while bytesToSend != "":
                    bytesToSend = f.read(1024)
                    s.send(bytesToSend)
                print("SEND COMPLETE")
    s.close()

def getFile(s):
    filename = raw_input("Filename? -> ")
    if filename != 'q':
        s.send(filename)
        data = s.recv(1024)
        if data[:6] == 'EXISTS':
            filesize = long(data[6:])
            message = raw_input("File exists, " + str(filesize) +"Bytes, download? (Y/N)? -> ")
            if message == 'Y':
                s.send("OK")
                f = open(filename, 'wb')
                data = s.recv(1024)
                totalRecv = len(data)
                f.write(data)
                while totalRecv < filesize:
                    data = s.recv(1024)
                    totalRecv += len(data)
                    f.write(data)
                    print "{0:.2f}".format((totalRecv/float(filesize))*100)+ "% Done"
                print "Download Complete!"
                f.close()
        else:
            print "File Does Not Exist!"


def Main():
    host = '127.0.0.1'
    port = 5000


    s = socket.socket()
    s.connect((host, port))

    print("What do you want to do?\n")
    choice = raw_input("1. Send File  2. Receive File")

    if(choice=="1"):
        s.send(choice)
        sendFile(s)
    if(choice=="2"):
        s.send(choice)
        getFile(s)

    s.close();


if __name__ == '__main__':
    Main()
