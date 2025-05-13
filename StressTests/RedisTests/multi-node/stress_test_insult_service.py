import redis
import time
import threading
from Redis.insults_data import add_insult
from Redis.constants import INSULT_QUEUE, INSULT_LIST

NUM_INSULTS = 1000
NODES       = [1, 2, 3]

def reset_redis():
    r = redis.Redis(decode_responses=True)
    r.delete(INSULT_QUEUE)
    r.delete(INSULT_LIST)

def preload_queue():
    r = redis.Redis(decode_responses=True)
    for i in range(NUM_INSULTS):
        r.rpush(INSULT_QUEUE, f"Insult-{i}")

def worker_loop(node_id):
    r = redis.Redis(decode_responses=True)
    processed = 0
    while True:
        item = r.blpop(INSULT_QUEUE, timeout=1)
        if not item:
            break
        _, insult = item
        # add_insult en Redis
        add_insult(insult)
        processed += 1
    print(f"[Nodo {node_id}] Processats {processed} insults.")

def run_scaling_test(num_nodes):
    print(f"\n🧪 Escalat amb {num_nodes} node(s)")
    reset_redis()
    preload_queue()

    threads = []
    start = time.time()
    for nid in range(1, num_nodes + 1):
        t = threading.Thread(target=worker_loop, args=(nid,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()
    duration = time.time() - start

    print(f"⏱ Temps total (consum): {duration:.2f}s")
    return duration

if __name__ == "__main__":
    results = []
    for n in NODES:
        dur = run_scaling_test(n)
        results.append((n, dur))

    print("\n📊 Speedups:")
    base = results[0][1]
    for nodes, dur in results:
        speedup = base / dur
        print(f" • {nodes} node(s): {dur:.2f}s → {speedup:.2f}×")
