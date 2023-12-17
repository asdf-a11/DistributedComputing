import socket
import _thread as thread
import time
import math
CONFMSG = "Conf."
PORT = 1500
MAX_PER_PACKET = 4095
def SelfIp():
    return socket.gethostbyname(socket.gethostname())
class Client():
    def __init__(self,ip,port):
        self.ip = ip
        self.port = port
        self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.soc.settimeout(3)
        self.soc.connect((self.ip,self.port))
    def recive(self,convert_type = None):
        return reciveProtocol(self.soc,convert_type)
    def send(self,item):
        sendProtocol(self.soc,item)
    def rawRecive(self,size):
        return self.soc.recv(size)
    def rawSend(self,b):
        if type(b) == str:b = b.encode("utf-8")
        self.soc.send(b)
class ServerClient():
    def __init__(self,network,address):
        self.soc = network
        self.address = address
        self.new = True
        self.dead = False
    def send(self,item):
        try:
            sendProtocol(self.soc,item)
        except Exception:
            self.dead = True
            print("Error when sending to client addr -> ", self.address)
    def recive(self,convert_type = None):
        try:
            return reciveProtocol(self.soc,convert_type)
        except Exception:
            self.dead = True
            print("Error when reciving to client addr -> ", self.address)
            return None
    def rawRecive(self,size):
        return self.soc.recv(size)
    def rawSend(self,b):
        if type(b) == str:b = b.encode("utf-8")
        self.soc.send(b)
class Server():
    def __init__(self,port=PORT):
        self.port = port
        self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.soc.bind(("",self.port))
        self.setListen(100)
        self.clientList = []
        self.clientListLock = False
        self.acceptClientThread = thread.start_new_thread(self.acceptNewClients,())
        self.killAcceptThead = False        
    def acceptNewClients(self):
        while not self.killAcceptThead:
            time.sleep(0.5)
            network,address = self.soc.accept()
            self.clientListLock = True
            newClient = ServerClient(network,address)
            self.clientList.append(newClient)     
            self.clientListLock = False       
    def setListen(self,num):
        self.listen = num
        self.soc.listen(self.listen)
    def sendIndex(self,ind,st):
        if self.clientList[ind].dead:
            self.clientList.pop(ind)
        else:
            self.clientList[ind].send(st)
    def sendAll(self,st):
        for i in range(len(self.clientList)):
            self.sendIdx(i, st)
    #can be class or idx
    def disconnectClient(self,client):
        idx = client
        if type(client) == Client:
            idx = self.clientList.index(client)
        self.clientList.pop(idx)

def sendProtocol(soc,item,is_confirm=True):
    byteList = item
    if type(item) == str:byteList = bytes(item, 'utf-8')
    if type(item) == int:byteList = item.to_bytes(8, byteorder='big')    
    soc.send(len(byteList).to_bytes(8, byteorder='big'))
    rem = len(byteList)
    while rem > 0:
        packetSize = min(rem, MAX_PER_PACKET)
        soc.send(byteList[:packetSize])
        byteList = byteList[packetSize:]
        rem -= packetSize
    soc.send(byteList) 

def reciveProtocol(soc,convert_type=None,is_confirm=True):
    size = int.from_bytes(soc.recv(8), "big") 
    rem = size
    b = b""
    while rem > 0:
        packetSize = min(rem, MAX_PER_PACKET)
        b += soc.recv(packetSize)
        rem -= packetSize
    return b


