from redis import Redis


class EruditCache(Redis):

    SET_KEY_PREFIX = "set"

    def make_set_key(self, localidentifier):
        if isinstance(localidentifier, str) and localidentifier.isalnum():
            return f"{self.SET_KEY_PREFIX}_{localidentifier}"
        else:
            return None

    def set(self, name, value, ex=None, px=None, nx=False, xx=False, localidentifiers=[]):
        pipeline = self.pipeline()
        for localidentifier in localidentifiers:
            set_key = self.make_set_key(localidentifier)
            if set_key:
                pipeline.sadd(set_key, name)
        result = pipeline.execute()
        return super().set(name, value, ex, px, nx, xx) + result.count(1)

    def delete(self, *names):
        pipeline = self.pipeline()
        for name in names:
            set_key = self.make_set_key(name)
            if set_key:
                keys = [key.decode() for key in self.smembers(set_key)]
                pipeline.delete(*keys)
                pipeline.srem(set_key, *keys)
        result = pipeline.execute()
        return super().delete(*names) + result.count(1)
