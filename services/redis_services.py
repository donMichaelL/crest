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