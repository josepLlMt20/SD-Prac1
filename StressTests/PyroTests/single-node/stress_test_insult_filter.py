import Pyro4
import time
import random
from multiprocessing import Process
from Pyro.InsultFilter.worker import run_worker
from StressTests.data_manager import guardar_resultats
from datetime import datetime

NUM_TEXTS = 1000
NUM_WORKERS = 1

def start_workers(n):
    processes = []
    for _ in range(n):
        p = Process(target=run_worker)
        p.start()
        processes.append(p)
    return processes

def main():
    filter_service = Pyro4.Proxy("PYRONAME:FilterService")

    # Iniciar workers
    worker_processes = start_workers(NUM_WORKERS)

    # Enviar textos
    insults = ["pedorro", "cabezón", "tontaco", "paco", "picapollo"]
    subjects = ["Mi jefe", "Ese tipo", "Tu primo", "El informático", "Josep"]
    actions = ["es un", "parece un", "se comporta como", "claramente es un"]

    print(f"[STRESS TEST] Enviant {NUM_TEXTS} textos...")
    start = time.time()

    for _ in range(NUM_TEXTS):
        text = f"{random.choice(subjects)} {random.choice(actions)} {random.choice(insults)}"
        filter_service.submit_text(text)

    print("[STRESS TEST] Esperant resultats...")
    while True:
        results = filter_service.get_results()
        if len(results) >= NUM_TEXTS:
            break
        time.sleep(0.2)

    duration = time.time() - start
    rps = NUM_TEXTS / duration

    print(f"\n📊 Resultats:")
    print(f" - Temps total: {duration:.2f} s")
    print(f" - RPS: {rps:.2f}")

    data = [{
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Test": "InsultFilter",
        "Middleware": "PyRO",
        "Mode": "Single-node",
        "Clients": 1,
        "Num Tasks": NUM_TEXTS,
        "Temps Total (s)": round(duration, 2),
        "RPS": round(rps, 2)
    }]
    guardar_resultats(data, sheet_name="PyRO_Single_Filter")

    for p in worker_processes:
        p.terminate()
        p.join()

if __name__ == "__main__":
    main()
