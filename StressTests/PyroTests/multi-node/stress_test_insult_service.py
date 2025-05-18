import Pyro4
import time
import subprocess
import sys
from threading import Thread
from StressTests.data_manager import guardar_resultats
from datetime import datetime

NODES = ["InsultService1", "InsultService2", "InsultService3"]
SERVER_SCRIPT = "../../../Pyro/InsultService/server.py"
TASK_LOADS = [1000, 2500, 5000, 10000]


def launch_servers(names):
    processes = []
    for name in names:
        p = subprocess.Popen([sys.executable, SERVER_SCRIPT, name])
        processes.append(p)
        time.sleep(1.5)
    return processes


def stop_servers(processes):
    for p in processes:
        p.terminate()
        p.wait()


def run_scaling_test(node_count, num_insults):
    active_nodes = NODES[:node_count]
    server_procs = launch_servers(active_nodes)

    proxies = [Pyro4.Proxy(f"PYRONAME:{name}") for name in active_nodes]
    insults_per_node = num_insults // node_count

    print(f"[TEST] {node_count} node(s) | {num_insults} peticions...")
    start_time = time.time()

    threads = []

    def enviar(proxy, start_idx):
        for i in range(insults_per_node):
            proxy.add_insult(f"Insult-{start_idx + i}")

    for i, proxy in enumerate(proxies):
        t = Thread(target=enviar, args=(proxy, i * insults_per_node))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    duration = time.time() - start_time
    stop_servers(server_procs)
    return duration


if __name__ == "__main__":
    all_results = []

    for num_insults in TASK_LOADS:
        print(f"\n### TEST AMB {num_insults} PETICIONS ###")
        results = []
        for n in [1, 2, 3]:
            d = run_scaling_test(n, num_insults)
            results.append((n, d))
            print(f"[RESULT] {n} node(s) ➝ {d:.2f}s")

        base = results[0][1]
        for n, dur in results:
            speedup = base / dur if n > 1 else 1.0
            all_results.append({
                "Test": "InsultService",
                "Middleware": "PyRO",
                "Mode": "Multi-node",
                "Clients": n,
                "Num Tasks": num_insults,
                "Temps Total (s)": round(dur, 2),
                "Speedup": round(speedup, 2),
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })

    guardar_resultats(all_results, sheet_name="PyRO_Multi_Service")
