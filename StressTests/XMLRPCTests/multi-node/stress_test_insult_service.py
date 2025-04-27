import xmlrpc.client
import threading
import time
from utils import measure_time, save_results_to_excel

SERVER_URL = "http://localhost:8000/"
RECEIVER_STATUS = {}

class Receiver:
    def __init__(self, port):
        self.received_count = 0
        self.lock = threading.Lock()
        self.port = port

    def receive(self, insult):
        with self.lock:
            self.received_count += 1
        return True

    def get_received_count(self):
        with self.lock:
            return self.received_count

def receiver_node(port):
    from xmlrpc.server import SimpleXMLRPCServer

    receiver = Receiver(port)
    server = SimpleXMLRPCServer(("localhost", port), allow_none=True)
    server.register_instance(receiver)

    threading.Thread(target=server.serve_forever, daemon=True).start()

    RECEIVER_STATUS[port] = receiver

    proxy = xmlrpc.client.ServerProxy(SERVER_URL)
    proxy.register_receiver(f"http://localhost:{port}/")

def test_insultservice_with_n_receivers(n_receivers, n_messages=50):
    RECEIVER_STATUS.clear()
    base_port = 8010

    for i in range(n_receivers):
        receiver_node(base_port + i)
    time.sleep(2)

    proxy = xmlrpc.client.ServerProxy(SERVER_URL)

    insults = [f"Insult {i}" for i in range(n_messages)]

    for insult in insults:
        proxy.add_insult(insult)

    start_time = time.time()

    while True:
        all_received = True
        for receiver in RECEIVER_STATUS.values():
            if receiver.get_received_count() < n_messages:
                all_received = False
                break

        if all_received:
            break

        time.sleep(0.5)

    end_time = time.time()
    total_duration = end_time - start_time

    return {
        "Sistema": "InsultService",
        "Nodos": n_receivers,
        "Mensajes": n_messages,
        "Tiempo Total (s)": round(total_duration, 2),
        "Tiempo por Mensaje (s)": round(total_duration/n_messages, 4)
    }

def main():
    results = []
    for nodes in [1, 2, 3]:
        res = test_insultservice_with_n_receivers(nodes)
        results.append(res)
    save_results_to_excel(results, filename="resultados_insultservice_broadcast.xlsx")

if __name__ == "__main__":
    main()
