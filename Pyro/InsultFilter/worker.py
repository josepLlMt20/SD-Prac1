import Pyro4
import time
import re

def run_worker():
    filter_service = Pyro4.Proxy("PYRONAME:FilterService")
    print("[WORKER] Iniciat i esperant tasques...")

    while True:
        text = filter_service.get_task()
        if not text:
            time.sleep(0.5)
            continue

        insults = filter_service.get_insults()
        filtered = text
        for insult in insults:
            pattern = re.compile(r'\b' + re.escape(insult) + r'\b', re.IGNORECASE)
            filtered = pattern.sub("CENSORED", filtered)

        filter_service.submit_result(filtered)
        print(f"[WORKER] Resultat: {filtered}")
