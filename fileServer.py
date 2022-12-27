import socket
import threading
import os

def RetrFile(name, sock):
    filename = sock.recv(1024)
    if os.path.isfile(filename):
        sock.send("EXISTS " + str(os.path.getsize(filename)))
        userResponse = sock.recv(1024)
        if userResponse[:2] == 'OK':
            print("Outbound File Transfer File: " + filename)
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
    host = '0.0.0.0'
    port = 5000


    s = socket.socket()
    s.bind((host,port))

    s.listen(5)

    print("Server Started.")
    while True:
        c, addr = s.accept()
        print("Inbound Client Connection: " + str(addr))
        t = threading.Thread(target=RetrFile, args=("RetrThread", c))
        t.start()
         
    s.close()
    print("Terminating Client Connection: " + str(addr))

if __name__ == '__main__':
    Main()