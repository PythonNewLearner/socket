import socketserver
import threading
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(threadName)s %(thread)s %(message)s')

class ChatHandler(socketserver.BaseRequestHandler):
    clients = {}
    def setup(self):
        super().setup()
        self.event = threading.Event()
        self.clients[self.client_address] = self.request

    def finish(self):
        super().finish()
        self.event.set()
        self.clients.pop(self.client_address)

    def handle(self):
        while not self.event.is_set():
            sock = self.request
            self.raddr = self.client_address
            data = sock.recv(1024)
            logging.info(data)
            if data == b'':
                break
            for c in self.clients.values():
                c.send(data)

server = socketserver.ThreadingTCPServer(('127.0.0.1',9999), ChatHandler)
threading.Thread(target=server.serve_forever,name='server').start()

