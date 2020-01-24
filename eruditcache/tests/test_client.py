import pytest

from unittest.mock import call, patch

from eruditcache.client import EruditCache


class TestEruditCache:
    @pytest.mark.parametrize("localidentifier, expected_set_key", (
        ("foo", "set_foo"),
        ("bar", "set_bar"),
        ("123", "set_123"),
        ("foo bar", None),
        ("", None),
        ([], None),
        (None, None),
        (True, None),
        (False, None),
    ))
    def test_make_set_key(self, localidentifier, expected_set_key):
        cache = EruditCache()
        assert cache.make_set_key(localidentifier) == expected_set_key

    @pytest.mark.parametrize("key, localidentifiers, expected_calls", (
        ("foo", [], []),
        ("foo", [None], []),
        ("foo", ["bar"], [
            call().sadd("set_bar", "foo"),
        ]),
        ("foo", ["bar", "baz"], [
            call().sadd("set_bar", "foo"),
            call().sadd("set_baz", "foo"),
        ]),
    ))
    @patch("eruditcache.client.EruditCache.pipeline")
    @patch("redis.Redis.set")
    def test_set(self, mock_set, mock_pipeline, key, localidentifiers, expected_calls):
        mock_set.return_value = 1
        mock_pipeline.return_value.execute.return_value = [1] * len(expected_calls)
        cache = EruditCache()
        result = cache.set(key, "", localidentifiers=localidentifiers)
        assert result == 1 + len(expected_calls)
        cache.pipeline.assert_has_calls([call()])
        cache.pipeline.assert_has_calls(expected_calls, any_order=True)
        cache.pipeline.assert_has_calls([call().execute()])

    @pytest.mark.parametrize("localidentifier, smembers, expected_calls", (
        ("foo", {}, []),
        ("foo", {b"bar"}, [
            call().delete("bar"),
            call().srem("set_foo", "bar"),
        ]),
        ("foo", {b"bar", b"baz"}, [
            call().delete("bar", "baz"),
            call().srem("set_foo", "bar", "baz"),
        ]),
    ))
    @patch("eruditcache.client.EruditCache.smembers")
    @patch("eruditcache.client.EruditCache.pipeline")
    @patch("redis.Redis.delete")
    def test_delete(
        self,
        mock_delete,
        mock_pipeline,
        mock_smembers,
        localidentifier,
        smembers,
        expected_calls,
    ):
        mock_delete.return_value = 1
        mock_pipeline.return_value.execute.return_value = [1] * len(expected_calls)
        mock_smembers.return_value = smembers
        cache = EruditCache()
        result = cache.delete(localidentifier)
        assert result == 1 + len(expected_calls)
        cache.pipeline.assert_has_calls([call()])
        cache.pipeline.assert_has_calls(expected_calls, any_order=True)
        cache.pipeline.assert_has_calls([call().execute()])
