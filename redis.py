import redis

from constant import *

class Redis:
    def __init__(self):
        pass

    def connection(self):
        return redis.Redis(host=REDIS_HOST, port=6379, password=REDIS_PASS)

