import redis

from constant import redis_host, redis_pass, redis_db

class Redis(object):
    def connection(self):
        return redis.Redis(host=redis_host, port=6379, password=redis_pass, db=redis_db)

