from typing import Tuple

from redis import Redis


class RedisKeyTagging(Redis):
    """
    A Redis client with key tagging and invalidation by tag features.
    """

    TAG_KEY_PREFIX = "tag:"

    def get_tag_key(self, tag):
        """
        Get the key for a given ``tag`` by prexing it with the ``TAG_KEY_PREFIX`` class attribute.
        """
        if tag is not None and isinstance(tag, str) and tag.strip():
            return f"{self.TAG_KEY_PREFIX}{tag}"
        else:
            return None

    def set(self, name, value, ex=None, px=None, nx=False, xx=False, tags=[]):
        """
        Set the value at key ``name`` to ``value``

        ``ex`` sets an expire flag on key ``name`` for ``ex`` seconds.

        ``px`` sets an expire flag on key ``name`` for ``px`` milliseconds.

        ``nx`` if set to True, set the value at key ``name`` to ``value`` only
            if it does not exist.

        ``xx`` if set to True, set the value at key ``name`` to ``value`` only
            if it already exists.

        ``tags`` add the key ``name`` to every tag in the ``tags`` list.
        """
        pipeline = self.pipeline()
        for tag in tags:
            tag_key = self.get_tag_key(tag)
            if tag_key:
                pipeline.sadd(tag_key, name)
        pipeline.execute()
        return super().set(name, value, ex, px, nx, xx)

    def delete_keys_by_tag(self, tag: str) -> Tuple[int, int]:
        """
        Delete all keys from a given tag and remove those keys from the tag.

        :returns: a tuple containing the number of deleted keys and the number of keys removed from
            the tag
        """
        tag_key = self.get_tag_key(tag)
        if tag_key:
            keys = [key.decode() for key in self.smembers(tag_key)]
            if keys:
                pipeline = self.pipeline()
                pipeline.delete(*keys)
                pipeline.srem(tag_key, *keys)
                results = pipeline.execute()
                return tuple(results)
        return 0, 0
