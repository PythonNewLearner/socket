import socket
import logging
import threading


logging.basicConfig(level=logging.INFO, format='%(asctime)s %(threadName)s %(thread)s %(message)s')

class UdpServer:
    def __init__(self,ip='127.0.0.1',port=9999):
        self.addr =ip,port
        self.server = socket.socket(type=socket.SOCK_DGRAM)  # define UDP server
        #self.event = threading.Event()
        self.clients = set() #store visited clients

    def start(self):
        self.server.bind(self.addr)
        threading.Thread(target=self.recv).start()

    def recv(self):
        while True:                   #not self.event.is_set():
            data,info = self.server.recvfrom(1024)

            if data.strip() == b'quit': #remove client if client's send 'quit'
                self.clients.remove(info)
                continue

            self.clients.add(info)
            msg = '{}. from {}:{}'.format(data.decode(), *info).encode()
            logging.info(msg)
            for r in self.clients:
                self.server.sendto(msg,r)  #send to client but cannot ganrantee client is able to receive it

    def stop(self):
        self.server.close()
        #self.event.set()

s = UdpServer()
s.start()
#s.stop()