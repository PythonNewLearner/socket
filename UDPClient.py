import socket
import logging
import threading

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(threadName)s %(thread)s %(message)s')


class UdpClient:
    def __init__(self,ip='127.0.0.1',port=9999):
        self.addr =ip,port
        self.client = socket.socket(type=socket.SOCK_DGRAM)  # define UDP server
        #self.event = threading.Event()

    def start(self):
        self.client.connect(self.addr)
        threading.Thread(target=self.recv).start()

    def recv(self):
        while True:
            data,server = self.client.recvfrom(1024)
            logging.info(data)
            logging.info(server)

    def send(self,msg:str):
        self.client.send(msg.encode())

    def stop(self):
        self.client.close()


client = UdpClient()
client.start()
while True:
    msg = input(">>>>")
    client.send(msg)