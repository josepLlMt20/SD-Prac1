from xmlrpc.server import SimpleXMLRPCServer

class FilterServer:
    def __init__(self):
        self.queue = []
        self.results = []

    def submit_text(self, text):
        self.queue.append(text)
        return True

    def get_task(self):
        if self.queue:
            return self.queue.pop(0)
        return None

    def submit_result(self, filtered):
        self.results.append(filtered)
        return True

    def get_results(self):
        return self.results

server = SimpleXMLRPCServer(("localhost", 8010), allow_none=True)
server.register_instance(FilterServer())
print("[FilterServer] Corriendo en puerto 8010")
server.serve_forever()