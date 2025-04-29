from xmlrpc.server import SimpleXMLRPCServer

class FilterServer:
    def __init__(self):
        self.text_queue = []   # Texts normals a filtrar
        self.insults = []      # Insults (paraules) per censurar
        self.results = []      # Texts filtrats

    def submit_text(self, text):
        self.text_queue.append(text)
        return True

    def get_task(self):
        if self.text_queue:
            return self.text_queue.pop(0)
        return None

    def submit_result(self, filtered):
        self.results.append(filtered)
        return True

    def get_results(self):
        return self.results

    def submit_insult(self, insult):
        insult = insult.lower()
        if insult not in self.insults:
            self.insults.append(insult)
            return True
        return False

    def get_insults(self):
        return self.insults

    def reset(self):
        self.text_queue = []
        self.results = []
        self.insults = []
        return True

server = SimpleXMLRPCServer(("localhost", 8010), allow_none=True)
server.register_instance(FilterServer())
print("[FilterServer] Corriendo en puerto 8010")
server.serve_forever()
