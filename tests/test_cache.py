import pytest
import json
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock
from dbox.cache import (
    get_cache_obj,
    get_redis_pool,
    get_redis_handler,
    batch_delete_key,
    MyRedis,
    MyCache,
    MyDict,
    hget,
)


class TestCache:
    """测试缓存相关函数"""

    @patch("dbox.cache.os.environ")
    def test_get_cache_obj_with_redis(self, mock_environ, mock_redis):
        """测试获取Redis缓存对象"""
        mock_environ.get.return_value = "test_redis_connect"

        with patch("dbox.cache.MyRedis") as mock_myredis:
            mock_myredis.return_value = mock_redis
            result = get_cache_obj()
            assert result == mock_redis

    @patch("dbox.cache.os.environ")
    def test_get_cache_obj_without_redis(self, mock_environ, temp_dir):
        """测试获取文件缓存对象"""
        mock_environ.get.return_value = None
        mock_environ.__getitem__.return_value = str(temp_dir)

        result = get_cache_obj()
        assert isinstance(result, MyCache)

    @patch("dbox.cache.os.environ")
    def test_get_redis_pool(self, mock_environ):
        """测试获取Redis连接池"""
        mock_environ.get.return_value = "test_redis_connect"

        with patch("dbox.cache.to_decode") as mock_decode:
            mock_decode.return_value = '{"host": "localhost", "port": 6379, "pass": "password"}'

            with patch("dbox.cache.ConnectionPool") as mock_pool:
                get_redis_pool()
                mock_pool.assert_called_once()

    def test_get_redis_handler_success(self, mock_redis):
        """测试成功获取Redis处理器"""
        with patch("dbox.cache.get_redis_pool") as mock_pool:
            mock_pool.return_value = MagicMock()

            result = get_redis_handler()
            assert result == mock_redis

    def test_get_redis_handler_failure(self):
        """测试获取Redis处理器失败"""
        with patch("dbox.cache.get_redis_pool") as mock_pool:
            mock_pool.side_effect = Exception("Connection failed")

            result = get_redis_handler()
            assert result is None

    def test_batch_delete_key(self, mock_redis):
        """测试批量删除键"""
        mock_redis.keys.return_value = ["key1", "key2"]

        with patch("dbox.cache.get_redis_handler") as mock_handler:
            mock_handler.return_value = mock_redis
            batch_delete_key(0, "test*")
            mock_redis.delete.assert_called_once_with("key1", "key2")


class TestMyRedis:
    """测试MyRedis类"""

    def test_batch_delete(self, mock_redis):
        """测试批量删除"""
        mock_redis.keys.return_value = ["key1", "key2"]

        redis = MyRedis(0)
        redis.batch_delete("test*")
        mock_redis.delete.assert_called_once_with("key1", "key2")

    def test_get_to_json_success(self, mock_redis):
        """测试成功获取JSON对象"""
        mock_redis.get.return_value = '{"name": "test", "value": 123}'

        redis = MyRedis(0)
        result = redis.get_to_json("test_key")
        assert isinstance(result, MyDict)
        assert result.name == "test"
        assert result.value == 123

    def test_get_to_json_failure(self, mock_redis):
        """测试获取JSON对象失败"""
        mock_redis.get.return_value = "invalid json"

        redis = MyRedis(0)
        result = redis.get_to_json("test_key")
        assert result is None

    def test_set_obj(self, mock_redis):
        """测试设置对象"""
        test_data = {"name": "test", "value": 123}

        redis = MyRedis(0)
        result = redis.set_obj("prefix", test_data)
        assert result is not None
        mock_redis.set.assert_called_once()

    def test_push_obj(self, mock_redis):
        """测试推送对象"""
        test_data = {"name": "test", "value": 123}

        redis = MyRedis(0)
        redis.push_obj("queue", test_data)
        mock_redis.rpush.assert_called_once()

    def test_pop_obj_success(self, mock_redis):
        """测试成功弹出对象"""
        mock_redis.lpop.return_value = '{"name": "test", "value": 123}'

        redis = MyRedis(0)
        result = redis.pop_obj("queue")
        assert result == {"name": "test", "value": 123}

    def test_pop_obj_failure(self, mock_redis):
        """测试弹出对象失败"""
        mock_redis.lpop.return_value = "invalid json"

        redis = MyRedis(0)
        result = redis.pop_obj("queue")
        assert result == "invalid json"


class TestMyCache:
    """测试MyCache类"""

    def test_init_new_cache(self, temp_dir):
        """测试初始化新缓存"""
        cache_file = temp_dir / "cache.json"
        cache = MyCache(cache_file)

        assert cache_file.exists()
        assert isinstance(cache._dict, dict)

    def test_init_existing_cache(self, temp_dir):
        """测试初始化已存在的缓存"""
        cache_file = temp_dir / "cache.json"
        test_data = {"key1": "value1", "key2": "value2"}
        cache_file.write_text(json.dumps(test_data))

        cache = MyCache(cache_file)
        assert cache._dict == test_data

    def test_exists(self, temp_dir):
        """测试检查键是否存在"""
        cache = MyCache(temp_dir / "cache.json")
        cache.set("test_key", "test_value")

        assert cache.exists("test_key") is True
        assert cache.exists("nonexistent_key") is False

    def test_get(self, temp_dir):
        """测试获取值"""
        cache = MyCache(temp_dir / "cache.json")
        cache.set("test_key", "test_value")

        assert cache.get("test_key") == "test_value"
        assert cache.get("nonexistent_key") is None

    def test_delete(self, temp_dir):
        """测试删除键"""
        cache = MyCache(temp_dir / "cache.json")
        cache.set("test_key", "test_value")

        cache.delete("test_key")
        assert not cache.exists("test_key")

    def test_set(self, temp_dir):
        """测试设置值"""
        cache = MyCache(temp_dir / "cache.json")
        cache.set("test_key", "test_value")

        assert cache.get("test_key") == "test_value"

    def test_setex(self, temp_dir):
        """测试设置带过期时间的值"""
        cache = MyCache(temp_dir / "cache.json")
        cache.setex("test_key", 3600, "test_value")

        assert cache.get("test_key") == "test_value"

    def test_hmset(self, temp_dir):
        """测试设置哈希映射"""
        cache = MyCache(temp_dir / "cache.json")
        mapping = {"field1": "value1", "field2": "value2"}
        cache.hmset("hash_key", mapping)

        assert cache.get("hash_key") == mapping

    def test_hgetall(self, temp_dir):
        """测试获取哈希所有字段"""
        cache = MyCache(temp_dir / "cache.json")
        mapping = {"field1": "value1", "field2": "value2"}
        cache.hmset("hash_key", mapping)

        result = cache.hgetall("hash_key")
        assert result == mapping

    def test_hset(self, temp_dir):
        """测试设置哈希字段"""
        cache = MyCache(temp_dir / "cache.json")
        cache.hset("hash_key", "field1", "value1")

        result = cache.hgetall("hash_key")
        assert result == {"field1": "value1"}


class TestMyDict:
    """测试MyDict类"""

    def test_init(self):
        """测试初始化"""
        data = {"key1": "value1", "key2": "value2"}
        my_dict = MyDict(data)

        assert my_dict["key1"] == "value1"
        assert my_dict["key2"] == "value2"

    def test_getattr(self):
        """测试属性访问"""
        data = {"name": "test", "value": 123}
        my_dict = MyDict(data)

        assert my_dict.name == "test"
        assert my_dict.value == 123

    def test_setattr(self):
        """测试属性设置"""
        my_dict = MyDict()
        my_dict.new_key = "new_value"

        assert my_dict["new_key"] == "new_value"

    def test_delattr(self):
        """测试属性删除"""
        data = {"key1": "value1", "key2": "value2"}
        my_dict = MyDict(data)

        del my_dict.key1
        assert "key1" not in my_dict


class TestHget:
    """测试hget函数"""

    def test_hget_success(self, mock_redis):
        """测试成功获取哈希值"""
        mock_redis.hget.return_value = "test_value"

        with patch("dbox.cache.MyRedis") as mock_myredis:
            mock_myredis.return_value = mock_redis
            result = hget("hash_key", "field_key")
            assert result == "test_value"

    def test_hget_none(self, mock_redis):
        """测试获取不存在的哈希值"""
        mock_redis.hget.return_value = None

        with patch("dbox.cache.MyRedis") as mock_myredis:
            mock_myredis.return_value = mock_redis
            result = hget("hash_key", "field_key", default="default_value")
            assert result == "default_value"

    def test_hget_with_type_conversion(self, mock_redis):
        """测试带类型转换的哈希值获取"""
        mock_redis.hget.return_value = "123"

        with patch("dbox.cache.MyRedis") as mock_myredis:
            mock_myredis.return_value = mock_redis
            result = hget("hash_key", "field_key", _type=int)
            assert result == 123
