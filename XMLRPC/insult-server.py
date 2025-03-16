from xmlrpc.server import SimpleXMLRPCServer
import random

class InsultServer:
    def __init__(self):
        self.insults = []

    def add_insult(self, insult):
        """Agrega un insulto a la lista."""
        self.insults.append(insult)
        return f"Insulto agregado: {insult}"

    def get_insults(self):
        """Devuelve la lista completa de insultos."""
        return self.insults

    def insult_me(self):
        """Devuelve un insulto aleatorio."""
        if self.insults:
            return random.choice(self.insults)
        return "No hay insultos en la lista."

# Configuración del servidor
server = SimpleXMLRPCServer(('localhost', 8000))
server.register_instance(InsultServer())

print("Servidor InsultServer corriendo en el puerto 8000...")
server.serve_forever()
