import time
import math
import multiprocessing
import pika
import psutil
from StressTests.data_manager import guardar_resultats
from datetime import datetime
from collections import deque

# Constants
Tr = 2.0
T = 0.5
C = 1 / T

MIN_WORKERS = 1
MAX_WORKERS = 100

workers = []
backlog_hist = deque(maxlen=5)
inicio = time.time()
ultimo_backlog = 0
ultimo_tiempo = time.time()
downscale_counter = 0

def get_backlog():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    q = channel.queue_declare(queue='insult_queue', passive=True)
    message_count = q.method.message_count
    connection.close()
    return message_count

def start_worker(worker_number=None):
    worker_id = f"Worker-{worker_number if worker_number is not None else len(workers) + 1}"
    p = multiprocessing.Process(target=start_worker_process, args=(worker_id,))
    p.start()
    return p

def start_worker_process(worker_id):
    from worker import start_worker
    start_worker(worker_id)

def stop_worker(worker_tuple):
    proc, _ = worker_tuple
    proc.terminate()
    proc.join()

def get_workers_metrics(workers):
    total_cpu = 0.0
    total_mem = 0.0
    for proc, pid in workers:
        try:
            p = psutil.Process(pid)
            total_cpu += p.cpu_percent(interval=0.1)
            total_mem += p.memory_info().rss / (1024 * 1024)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return round(total_cpu, 2), round(total_mem, 2)

def scaler_loop():
    global ultimo_backlog, ultimo_tiempo, downscale_counter

    while True:
        ahora = time.time()
        tiempo_ciclo = ahora - ultimo_tiempo
        ultimo_tiempo = ahora

        B = get_backlog()
        lambda_estimado = max(0, B - ultimo_backlog) / tiempo_ciclo
        ultimo_backlog = B

        required = math.ceil((B + lambda_estimado * Tr) / C)
        required = min(max(required, MIN_WORKERS), MAX_WORKERS)

        current = len(workers)
        ajuste_realizado = required - current

        backlog_hist.append(B)
        media_backlog = sum(backlog_hist) / len(backlog_hist)

        cpu_total, ram_total = get_workers_metrics(workers)

        print(f"[Scaler] Backlog: {B}, λ: {lambda_estimado:.2f}, Current: {current}, Required: {required} | CPU: {cpu_total}%, RAM: {ram_total}MB")

        # Guardar métricas
        result = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "tiempo_sistema": round(ahora - inicio, 2),
            "backlog": B,
            "media_backlog_5": round(media_backlog, 2),
            "lambda_estimado": round(lambda_estimado, 2),
            "workers_activos": current,
            "workers_requeridos": required,
            "ajuste_realizado": ajuste_realizado,
            "tiempo_ciclo": round(tiempo_ciclo, 2),
            "cpu_total_pct": cpu_total,
            "ram_total_mb": ram_total
        }
        guardar_resultats([result], sheet_name="EscaladoDinámico")

        # Escalado con histéresis
        if required > current:
            for i in range(required - current):
                p = start_worker(worker_number=current + i + 1)
                workers.append((p, p.pid))
            downscale_counter = 0
        elif required < current:
            downscale_counter += 1
            if downscale_counter >= 3:
                for _ in range(current - required):
                    stop_worker(workers.pop())
                downscale_counter = 0
        else:
            downscale_counter = 0

        time.sleep(5)

if __name__ == "__main__":
    scaler_loop()
