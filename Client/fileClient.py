#CSE 3320
#LAB 4
#Swangya Saurav
#1001054908


import socket
import os, random

from Crypto.Cipher import AES
from Crypto.Hash import SHA256

def encrypt(key, filename):
	chunksize = 64*1024
	outputFile = "(encrypted)"+filename
	filesize = str(os.path.getsize(filename)).zfill(16)
	IV = ''

	for i in range(16):
		IV += chr(random.randint(0, 0xFF))

	encryptor = AES.new(key, AES.MODE_CBC, IV)

	with open(filename, 'rb') as infile:
		with open(outputFile, 'wb') as outfile:
			outfile.write(filesize)
			outfile.write(IV)

			while True:
				chunk = infile.read(chunksize)

				if len(chunk) == 0:
					break
				elif len(chunk) % 16 != 0:
					chunk += ' ' * (16 - (len(chunk) % 16))

				outfile.write(encryptor.encrypt(chunk))


def decrypt(key, filename):
	chunksize = 64*1024
	outputFile = filename[11:]

	with open(filename, 'rb') as infile:
		filesize = long(infile.read(16))
		IV = infile.read(16)

		decryptor = AES.new(key, AES.MODE_CBC, IV)

		with open(outputFile, 'wb') as outfile:
			while True:
				chunk = infile.read(chunksize)

				if len(chunk) == 0:
					break

				outfile.write(decryptor.decrypt(chunk))
			outfile.truncate(filesize)


def getKey(password):
	hasher = SHA256.new(password)
	return hasher.digest()


def sendFile(s):
    filename = raw_input("Filename -> ")
    password = raw_input("Password for this File -> ")

    encrypt(getKey(password), filename)

    filename = "(encrypted)"+filename

    if filename != 'q':
        s.send(filename)
    else:
        exit();
    if os.path.isfile(filename):
        print "Sending data: " + str(os.path.getsize(filename))
        s.send(str(os.path.getsize(filename)))
        with open(filename, 'rb') as f:
                bytesToSend = f.read(1024)
                s.send(bytesToSend)
                while bytesToSend != "":
                    bytesToSend = f.read(1024)
                    s.send(bytesToSend)
                print("SEND COMPLETE")

    s.close()
    os.remove(filename)

def getFile(s):
    filename = raw_input("Filename do not include '(encrypted)' -> ")
    password = raw_input("Password for this File -> ")
    filename1 = filename

    filename = "(encrypted)"+filename

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

                decrypt(getKey(password), filename)
        else:
            print "File Does Not Exist!"

        s.close()
        os.remove(filename)


def Main():
    host = '127.0.0.1'
    port = 5000


    s = socket.socket()
    s.connect((host, port))

    print("\nWhat do you want to do?\n")
    choice = raw_input("\t1. Send File\n  \t2. Receive File\n \t-> ")

    if(choice=="1"):
        s.send(choice)
        sendFile(s)
    elif(choice=="2"):
        s.send(choice)
        getFile(s)

    s.close();


if __name__ == '__main__':
    Main()
