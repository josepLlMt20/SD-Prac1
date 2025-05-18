import redis
import time
import threading
from Redis.insults_data import add_insult
from Redis.constants import INSULT_QUEUE, INSULT_LIST
from StressTests.data_manager import guardar_resultats
from datetime import datetime

NODES = [1, 2, 3]
TASK_SIZES = [1000, 2500, 5000, 10000]

def reset_redis():
    r = redis.Redis(decode_responses=True)
    r.delete(INSULT_QUEUE)
    r.delete(INSULT_LIST)

def preload_queue(num_insults):
    r = redis.Redis(decode_responses=True)
    for i in range(num_insults):
        r.rpush(INSULT_QUEUE, f"Insult-{i}")

def worker_loop(node_id):
    r = redis.Redis(decode_responses=True)
    processed = 0
    while True:
        item = r.blpop(INSULT_QUEUE, timeout=1)
        if not item:
            break
        _, insult = item
        add_insult(insult)
        processed += 1
    print(f"[Nodo {node_id}] Processats {processed} insults.")

def run_scaling_test(num_nodes, num_insults):
    print(f"\n🧪 Escalat amb {num_nodes} node(s) i {num_insults} insults...")
    reset_redis()
    preload_queue(num_insults)

    threads = []
    start = time.time()
    for nid in range(1, num_nodes + 1):
        t = threading.Thread(target=worker_loop, args=(nid,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()
    duration = time.time() - start

    print(f"⏱ Temps total: {duration:.2f}s")
    return duration

if __name__ == "__main__":
    all_data = []

    for task_size in TASK_SIZES:
        results = []
        for n in NODES:
            dur = run_scaling_test(n, task_size)
            results.append((n, dur))

        base_time = results[0][1]
        print(f"\n📊 Resultats amb {task_size} insults:")
        for n, dur in results:
            speedup = base_time / dur if n > 1 else 1.0
            print(f" • {n} node(s): {dur:.2f}s → {speedup:.2f}×")
            all_data.append({
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Test": "InsultService",
                "Middleware": "Redis",
                "Mode": "Multi-node",
                "Clients": n,
                "Num Tasks": task_size,
                "Temps Total (s)": round(dur, 2),
                "Speedup": round(speedup, 2)
            })

    guardar_resultats(all_data, sheet_name="Redis_Multi_Service")
