import redis


class RedisClient:
    def __init__(self, host='localhost', port=6379, db=0):
        self.host = host
        self.port = port
        self.db = db
        self.client = redis.StrictRedis(host=host, port=port, db=db)

    def connect(self):
        try:
            # Test connection
            self.client.ping()
            return True
        except ConnectionError:
            return False

    def set(self, key, value):
        return self.client.set(key, value)

    def get(self, key):
        return self.client.get(key)

    def hset(self, key, field, value):
        self.client.hset(key, field, value)

    def hget(self, key, field):
        return self.client.hget(key, field)

    def hgetall(self, key):
        return self.client.hgetall(key)

    def hdel(self, key, field):
        return self.client.hdel(key, field)

    def delete(self, key):
        return self.client.delete(key)
