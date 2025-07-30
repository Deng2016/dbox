import pytest
import tempfile
import os
from pathlib import Path
from unittest.mock import patch, MagicMock


@pytest.fixture
def temp_dir():
    """创建临时目录"""
    with tempfile.TemporaryDirectory() as tmp_dir:
        yield Path(tmp_dir)


@pytest.fixture
def mock_redis():
    """模拟 Redis 连接"""
    with patch("dbox.cache.Redis") as mock_redis_class:
        mock_redis = MagicMock()
        mock_redis.ping.return_value = True
        mock_redis_class.return_value = mock_redis
        yield mock_redis


@pytest.fixture
def mock_pymysql():
    """模拟 PyMySQL 连接"""
    with patch("dbox.db_oper.pymysql") as mock_pymysql:
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_pymysql.connect.return_value = mock_conn
        yield mock_pymysql


@pytest.fixture
def mock_requests():
    """模拟 requests 库"""
    with patch("dbox.my_http.requests") as mock_requests:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '{"test": "data"}'
        mock_response.json.return_value = {"test": "data"}
        mock_requests.get.return_value = mock_response
        mock_requests.post.return_value = mock_response
        yield mock_requests


@pytest.fixture
def mock_smb():
    """模拟 SMB 连接"""
    with patch("dbox.samba.SMBConnection") as mock_smb_class:
        mock_conn = MagicMock()
        mock_smb_class.return_value = mock_conn
        yield mock_conn


@pytest.fixture
def sample_data():
    """提供测试用的样本数据"""
    return {
        "test_dict": {"key1": "value1", "key2": "value2"},
        "test_list": [1, 2, 3, 4, 5],
        "test_string": "test_string",
        "test_bytes": b"test_bytes",
        "test_json": '{"name": "test", "value": 123}',
    }
