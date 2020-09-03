import redis

from constant import redis_host, redis_pass

class Redis(object):
    def connection(self):
        return redis.Redis(host=redis_host, port=6379, password=redis_pass)

