import socket
import os

def sendFile(s):


def Main():
    host = '127.0.0.1'
    port = 5000

    s = socket.socket()
    s.connect((host, port))
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

    s.close()


if __name__ == '__main__':
    Main()
