import redis
from Redis.constants import INSULT_LIST

r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

def add_insult(insult):
    return r.sadd(INSULT_LIST, insult)

def get_insults():
    return list(r.smembers(INSULT_LIST))
