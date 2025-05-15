import time
import math
import multiprocessing
import pika
from StressTests.data_manager import guardar_resultats
from datetime import datetime
from collections import deque

# Constants
Tr = 2.0  # Temps objectiu de resposta en segons
T = 0.5   # Temps que tarda 1 worker en processar un missatge
C = 1 / T # Capacitat = 2 missatges/segon

MIN_WORKERS = 1
MAX_WORKERS = 100

workers = []
backlog_hist = deque(maxlen=5)
inicio = time.time()
ultimo_backlog = 0
ultimo_tiempo = time.time()

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

def stop_worker(p):
    p.terminate()
    p.join()

def scaler_loop():
    global ultimo_backlog, ultimo_tiempo

    while True:
        ahora = time.time()
        tiempo_ciclo = ahora - ultimo_tiempo
        ultimo_tiempo = ahora

        B = get_backlog()
        required = math.ceil(B / (Tr * C))
        required = min(max(required, MIN_WORKERS), MAX_WORKERS)

        current = len(workers)
        ajuste_realizado = required - current

        # Estimación de lambda (tasa de llegada de mensajes)
        lambda_estimado = max(0, B - ultimo_backlog) / tiempo_ciclo
        ultimo_backlog = B

        # Media móvil del backlog
        backlog_hist.append(B)
        media_backlog = sum(backlog_hist) / len(backlog_hist)

        print(f"[Scaler] Backlog: {B}, Current: {current}, Required: {required}")

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
        }
        guardar_resultats([result], sheet_name="EscaladoDinámico")

        # Ajustar workers
        if required > current:
            for i in range(required - current):
                workers.append(start_worker(worker_number=current + i + 1))

        elif required < current:
            for _ in range(current - required):
                stop_worker(workers.pop())

        time.sleep(5)

if __name__ == "__main__":
    scaler_loop()
