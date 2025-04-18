import os
from RabbitMQ.constants import INSULT_LIST_FILE

def add_insult(insult):
    insults = get_insults()
    if insult not in insults:
        with open(INSULT_LIST_FILE, "a") as f:
            f.write(insult + "\n")
        return True
    return False

def get_insults():
    if not os.path.exists(INSULT_LIST_FILE):
        return []
    with open(INSULT_LIST_FILE, "r") as f:
        return [line.strip() for line in f.readlines()]