from xmlrpc.server import SimpleXMLRPCServer
import xmlrpc.client
import threading
import random
import time

class InsultService:
    def __init__(self):
        self.insults = []
        self.subscribers = []

    def add_insult(self, insult):
        if insult not in self.insults:
            self.insults.append(insult)
            return True
        return False

    def get_insults(self):
        return self.insults

    def register_receiver(self, url):
        if url not in self.subscribers:
            self.subscribers.append(url)
            return True
        return False

    def broadcast_insult(self, insult):
        for url in self.subscribers:
            try:
                proxy = xmlrpc.client.ServerProxy(url)
                proxy.receive(insult)
            except Exception as e:
                print(f"Error notifying {url}: {e}")
        return True

    def start_broadcast(self):
        def broadcast_loop():
            while True:
                if self.insults and self.subscribers:
                    insult = random.choice(self.insults)
                    self.broadcast_insult(insult)
                time.sleep(5)

        threading.Thread(target=broadcast_loop, daemon=True).start()
        return True

server = SimpleXMLRPCServer(("localhost", 8000), allow_none=True)
service = InsultService()
service.start_broadcast()
server.register_instance(service)
print("[InsultService] Running on port 8000")
server.serve_forever()