import redis

from settings import REDIS_HOST, REDIS_PORT

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)


def write_data_to_redis(key, value):
    r.set(key, value)

def get_data_from_redis(key):
    try:
        return r.get(key).decode()
    except:
        return None

def write_list_to_redis(key: str, value:str):
    r.lpush(key, value)

def get_and_remove_list_from_redis(key):
    colours = []
    while(r.llen(key)!=0):
        colours.append(r.lpop(key))
    return colours
