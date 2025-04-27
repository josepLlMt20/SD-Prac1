import xmlrpc.client
import threading
import time
from xmlrpc.server import SimpleXMLRPCServer


# --- Setup: fem un fake receiver per veure si rebem broadcast
class TestReceiver:
    def __init__(self):
        self.received = []

    def receive(self, insult):
        print(f"[TestReceiver] 📢 Rebuda insult: {insult}")
        self.received.append(insult)
        return True


def start_test_receiver():
    server = SimpleXMLRPCServer(("localhost", 8001), allow_none=True)
    receiver = TestReceiver()
    server.register_instance(receiver)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return receiver


# --- Iniciem el test
def test_insult_service():
    receiver = start_test_receiver()
    service_proxy = xmlrpc.client.ServerProxy("http://localhost:8000/")

    # 1. Afegir insults
    service_proxy.add_insult("Ets més lent que una tortuga amb ressaca.")
    service_proxy.add_insult("Tens menys gràcia que un semàfor trencat.")

    # 2. Recuperar insults
    insults = service_proxy.get_insults()
    print(f"[Test] Insults guardats: {insults}")

    # 3. Registrar el receiver
    service_proxy.register_receiver("http://localhost:8001/")

    # 4. Esperar al broadcast (ja corre en background)
    print("[Test] Esperant broadcast...")
    time.sleep(7)  # Esperem més de 5 segons per assegurar-nos que arriba

    # 5. Comprovar que hem rebut insults
    if receiver.received:
        print("[Test] Broadcast rebut correctament ✅")
    else:
        print("[Test] Error: No s'ha rebut cap broadcast ❌")


if __name__ == "__main__":
    test_insult_service()
