import xmlrpc.client
import threading
import time
from utils import measure_time, save_results_to_excel
import re

SERVER_URL = "http://localhost:8010/"

def worker_node():
    def worker():
        proxy = xmlrpc.client.ServerProxy(SERVER_URL)
        while True:
            text = proxy.get_task()
            if text:
                insults = proxy.get_insults()
                filtered = text
                for insult in insults:
                    pattern = re.compile(r'\b' + re.escape(insult) + r'\b', re.IGNORECASE)
                    filtered = pattern.sub("CENSORED", filtered)
                proxy.submit_result(filtered)
            else:
                time.sleep(0.1)
    threading.Thread(target=worker, daemon=True).start()

def test_insultfilter_with_n_workers(n_workers, n_messages=50):
    proxy = xmlrpc.client.ServerProxy(SERVER_URL)

    # Lanzar Workers
    for _ in range(n_workers):
        worker_node()
    time.sleep(2)

    # Asegurar algunos insults
    basic_insults = ["tonto", "idiota", "bobo", "cochino", "mierdolo"]
    for insult in basic_insults:
        proxy.submit_insult(insult)

    texts = [f"Este texto contiene la palabra {basic_insults[i % len(basic_insults)]}" for i in range(n_messages)]

    def send_texts():
        for text in texts:
            proxy.submit_text(text)

    _, duration = measure_time(send_texts)

    return {
        "Sistema": "InsultFilter",
        "Nodos": n_workers,
        "Mensajes": n_messages,
        "Tiempo Total (s)": round(duration, 2),
        "Tiempo por Mensaje (s)": round(duration/n_messages, 4)
    }

def main():
    results = []
    for nodes in [1, 2, 3]:
        res = test_insultfilter_with_n_workers(nodes)
        results.append(res)
    save_results_to_excel(results, filename="resultados_insultfilter.xlsx")

if __name__ == "__main__":
    main()
