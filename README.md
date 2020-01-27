# EruditCache

## Description

This package provides the ``EruditCache`` class which extends the ``Redis`` class from
[redis-py](https://github.com/andymccurdy/redis-py). Two methods are extended to add those features:

* ``set()``: When setting a key into Redis, an additional argument can be passed,
``localidentifiers``, which is a list of object IDs. Each of those IDs will correspond to a
[Redis set](https://redis.io/topics/data-types#sets) and the key being set will be added to those
sets.
* ``delete()``: When all the keys concerning an object need to be invalidated, the object ID can be
passed to this method. All the keys contained in the set associated with this object will be
invalidated.

## Documentation

https://erudit.pages.erudit.org/docs/Apps/www/cache.html

## Tests

```
$ py.test
```
