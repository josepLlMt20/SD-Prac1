from xmlrpc.server import SimpleXMLRPCServer

class Receiver:
    def receive(self, insult):
        print(f"[Receiver] 📢 Recibido: {insult}")
        return True

server = SimpleXMLRPCServer(("localhost", 8001), allow_none=True)
server.register_instance(Receiver())
print("[Receiver] Esperando insultos en puerto 8001")
server.serve_forever()