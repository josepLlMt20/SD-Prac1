from xmlrpc.server import SimpleXMLRPCServer
import xmlrpc.client
import threading

class Receiver:
    def receive(self, insult):
        print(f"[Receiver] 📢 Recibido: {insult}")
        return True

def run_receiver():
    server = SimpleXMLRPCServer(("localhost", 8001), allow_none=True)
    server.register_instance(Receiver())
    print("[Receiver] Esperando insultos en puerto 8001")
    server.serve_forever()

threading.Thread(target=run_receiver, daemon=True).start()

proxy = xmlrpc.client.ServerProxy("http://localhost:8000/")
proxy.register_receiver("http://localhost:8001/")

import time
while True:
    time.sleep(1)
