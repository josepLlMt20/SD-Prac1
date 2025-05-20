import Pyro4
import time
import random
from multiprocessing import Process
from Pyro.InsultFilter.worker import run_worker
from StressTests.data_manager import guardar_resultats
from datetime import datetime

CLIENTS_LIST = [1, 2, 3]
TASK_SIZES = [1000, 2500, 5000, 10000]

def start_workers(n):
    processes = []
    for _ in range(n):
        p = Process(target=run_worker)
        p.start()
        processes.append(p)
    time.sleep(1)
    return processes

def send_texts(filter_service, num_texts):
    insults = ["pedorro", "cabezón", "tontaco", "paco", "picapollo"]
    subjects = ["Mi jefe", "Ese tipo", "Tu primo", "El informático", "Josep"]
    actions = ["es un", "parece un", "se comporta como", "claramente es un"]

    for _ in range(num_texts):
        text = f"{random.choice(subjects)} {random.choice(actions)} {random.choice(insults)}"
        filter_service.submit_text(text)

def run_scaling_test(num_clients, num_texts):
    filter_service = Pyro4.Proxy("PYRONAME:FilterService")
    filter_service.reset()

    print(f"\n[Test] Enviant {num_texts} textos amb {num_clients} worker(s)...")
    worker_processes = start_workers(num_clients)

    start = time.time()
    send_texts(filter_service, num_texts)
    time.sleep(0.2)

    while True:
        results = filter_service.get_results()
        if len(results) >= num_texts:
            break
        time.sleep(0.05)

    end = time.time()
    duration = end - start

    print(f"Temps total amb {num_clients} worker(s): {duration:.2f}s")

    for p in worker_processes:
        p.terminate()
        p.join()

    return duration

def main():
    all_data = []

    for num_texts in TASK_SIZES:
        results = []
        for clients in CLIENTS_LIST:
            duration = run_scaling_test(clients, num_texts)
            results.append((clients, duration))

        base_time = results[0][1]

        print(f"\n📊 Resultats amb {num_texts} textos:")
        for clients, dur in results:
            speedup = base_time / dur if clients > 1 else 1.0
            print(f" • {clients} worker(s): {dur:.2f}s (speedup: {speedup:.2f}x)")
            all_data.append({
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Test": "InsultFilter",
                "Middleware": "PyRO",
                "Mode": "Multi-node",
                "Clients": clients,
                "Num Tasks": num_texts,
                "Temps Total (s)": round(dur, 2),
                "Speedup": round(speedup, 2)
            })

    guardar_resultats(all_data, sheet_name="PyRO_Multi_Filter")

if __name__ == "__main__":
    main()
