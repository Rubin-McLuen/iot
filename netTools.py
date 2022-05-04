from socket import *

def getIPAddress():
    s = socket(AF_INET, SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

def getMessage(sock):
    data = sock.recv(1024)
    print(data.decode())
    return data.decode('ascii')

def sendMessage(sock, msg):
    print(msg)
    sock.send(msg.encode('ascii'))

def sendError(s):
    errorMsg = "Unexpected response. Connection terminated."
    sendMessage(s, errorMsg)
    print(errorMsg)
    s.close()
