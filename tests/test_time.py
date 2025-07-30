import pytest
import time
import datetime
from unittest.mock import patch
from dbox.time import get_timestamp, get_current_time, str_to_time, time_to_str, timestamp_to_str, str_to_timestamp


class TestTime:
    """测试时间相关函数"""

    def test_get_timestamp_10_digits(self):
        """测试获取10位时间戳"""
        result = get_timestamp(10)
        assert len(str(result)) == 10
        assert isinstance(result, int)

    def test_get_timestamp_13_digits(self):
        """测试获取13位时间戳"""
        result = get_timestamp(13)
        assert len(str(result)) == 13
        assert isinstance(result, int)

    def test_get_timestamp_utc(self):
        """测试获取UTC时间戳"""
        result = get_timestamp(10, utc=True)
        assert len(str(result)) == 10
        assert isinstance(result, int)

    def test_get_timestamp_invalid_length(self):
        """测试无效长度参数"""
        with pytest.raises(AssertionError):
            get_timestamp(11)

    def test_get_current_time_short(self):
        """测试获取短格式当前时间"""
        result = get_current_time("short")
        assert isinstance(result, str)
        assert len(result.split("-")) == 3

    def test_get_current_time_long(self):
        """测试获取长格式当前时间"""
        result = get_current_time("long")
        assert isinstance(result, str)
        assert " " in result  # 包含时间部分

    def test_get_current_time_max(self):
        """测试获取最大格式当前时间"""
        result = get_current_time("max")
        assert isinstance(result, str)
        assert "." in result  # 包含微秒部分

    def test_get_current_time_custom_format(self):
        """测试获取自定义格式当前时间"""
        result = get_current_time("%Y-%m-%d")
        assert isinstance(result, str)
        assert len(result.split("-")) == 3

    def test_get_current_time_with_offset(self):
        """测试带偏移量的当前时间"""
        result1 = get_current_time("long")
        result2 = get_current_time("long", offset=3600)  # 1小时前
        assert result1 != result2

    def test_str_to_time_long_format(self):
        """测试字符串转时间-长格式"""
        time_str = "2023-01-01 12:00:00"
        result = str_to_time(time_str, "long")
        assert isinstance(result, datetime.datetime)
        assert result.year == 2023
        assert result.month == 1
        assert result.day == 1

    def test_str_to_time_short_format(self):
        """测试字符串转时间-短格式"""
        time_str = "2023-01-01"
        result = str_to_time(time_str, "short")
        assert isinstance(result, datetime.date)
        assert result.year == 2023
        assert result.month == 1
        assert result.day == 1

    def test_str_to_time_empty_string(self):
        """测试空字符串转时间"""
        with pytest.raises(ValueError):
            str_to_time("")

    def test_time_to_str_long_format(self):
        """测试时间转字符串-长格式"""
        dt = datetime.datetime(2023, 1, 1, 12, 0, 0)
        result = time_to_str(dt, "long")
        assert result == "2023-01-01 12:00:00"

    def test_time_to_str_short_format(self):
        """测试时间转字符串-短格式"""
        dt = datetime.datetime(2023, 1, 1, 12, 0, 0)
        result = time_to_str(dt, "short")
        assert result == "2023-01-01"

    def test_timestamp_to_str_10_digits(self):
        """测试时间戳转字符串-10位"""
        timestamp = int(time.time())
        result = timestamp_to_str(timestamp)
        assert isinstance(result, str)
        assert " " in result

    def test_timestamp_to_str_13_digits(self):
        """测试时间戳转字符串-13位"""
        timestamp = int(time.time() * 1000)
        result = timestamp_to_str(timestamp)
        assert isinstance(result, str)
        assert " " in result

    def test_timestamp_to_str_invalid_format(self):
        """测试无效时间戳格式"""
        with pytest.raises(ValueError):
            timestamp_to_str(12345)  # 5位数字

    def test_timestamp_to_str_custom_format(self):
        """测试自定义格式时间戳转字符串"""
        timestamp = int(time.time())
        result = timestamp_to_str(timestamp, "%Y-%m-%d")
        assert isinstance(result, str)
        assert len(result.split("-")) == 3

    def test_str_to_timestamp(self):
        """测试字符串转时间戳"""
        time_str = "2023-01-01 12:00:00"
        fmt = "%Y-%m-%d %H:%M:%S"
        result = str_to_timestamp(time_str, fmt)
        assert isinstance(result, float)
        assert result > 0
