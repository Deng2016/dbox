import pytest
import json
from unittest.mock import patch, MagicMock
from dbox.my_http import (
    get, post, put, delete, get_json, post_json, put_json, delete_json,
    get_with_headers, post_with_headers, put_with_headers, delete_with_headers
)


class TestMyHttp:
    """测试HTTP请求函数"""

    @patch('dbox.my_http.requests.get')
    def test_get_success(self, mock_get, mock_requests):
        """测试GET请求成功"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "success response"
        mock_get.return_value = mock_response
        
        result = get("http://example.com")
        assert result.status_code == 200
        assert result.text == "success response"

    @patch('dbox.my_http.requests.get')
    def test_get_with_params(self, mock_get, mock_requests):
        """测试带参数的GET请求"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        params = {"key": "value"}
        get("http://example.com", params=params)
        mock_get.assert_called_once_with("http://example.com", params=params, timeout=30)

    @patch('dbox.my_http.requests.post')
    def test_post_success(self, mock_post, mock_requests):
        """测试POST请求成功"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "success response"
        mock_post.return_value = mock_response
        
        result = post("http://example.com", data={"key": "value"})
        assert result.status_code == 200
        assert result.text == "success response"

    @patch('dbox.my_http.requests.put')
    def test_put_success(self, mock_put, mock_requests):
        """测试PUT请求成功"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "success response"
        mock_put.return_value = mock_response
        
        result = put("http://example.com", data={"key": "value"})
        assert result.status_code == 200
        assert result.text == "success response"

    @patch('dbox.my_http.requests.delete')
    def test_delete_success(self, mock_delete, mock_requests):
        """测试DELETE请求成功"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "success response"
        mock_delete.return_value = mock_response
        
        result = delete("http://example.com")
        assert result.status_code == 200
        assert result.text == "success response"

    @patch('dbox.my_http.requests.get')
    def test_get_json_success(self, mock_get, mock_requests):
        """测试GET JSON请求成功"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"key": "value"}
        mock_get.return_value = mock_response
        
        result = get_json("http://example.com")
        assert result == {"key": "value"}

    @patch('dbox.my_http.requests.get')
    def test_get_json_failure(self, mock_get, mock_requests):
        """测试GET JSON请求失败"""
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        
        result = get_json("http://example.com")
        assert result is None

    @patch('dbox.my_http.requests.post')
    def test_post_json_success(self, mock_post, mock_requests):
        """测试POST JSON请求成功"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"key": "value"}
        mock_post.return_value = mock_response
        
        result = post_json("http://example.com", {"data": "value"})
        assert result == {"key": "value"}

    @patch('dbox.my_http.requests.post')
    def test_post_json_failure(self, mock_post, mock_requests):
        """测试POST JSON请求失败"""
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_post.return_value = mock_response
        
        result = post_json("http://example.com", {"data": "value"})
        assert result is None

    @patch('dbox.my_http.requests.put')
    def test_put_json_success(self, mock_put, mock_requests):
        """测试PUT JSON请求成功"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"key": "value"}
        mock_put.return_value = mock_response
        
        result = put_json("http://example.com", {"data": "value"})
        assert result == {"key": "value"}

    @patch('dbox.my_http.requests.delete')
    def test_delete_json_success(self, mock_delete, mock_requests):
        """测试DELETE JSON请求成功"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"key": "value"}
        mock_delete.return_value = mock_response
        
        result = delete_json("http://example.com")
        assert result == {"key": "value"}

    @patch('dbox.my_http.requests.get')
    def test_get_with_headers(self, mock_get, mock_requests):
        """测试带请求头的GET请求"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        headers = {"Authorization": "Bearer token"}
        get_with_headers("http://example.com", headers)
        mock_get.assert_called_once_with("http://example.com", headers=headers, timeout=30)

    @patch('dbox.my_http.requests.post')
    def test_post_with_headers(self, mock_post, mock_requests):
        """测试带请求头的POST请求"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response
        
        headers = {"Content-Type": "application/json"}
        data = {"key": "value"}
        post_with_headers("http://example.com", data, headers)
        mock_post.assert_called_once_with("http://example.com", data=data, headers=headers, timeout=30)

    @patch('dbox.my_http.requests.put')
    def test_put_with_headers(self, mock_put, mock_requests):
        """测试带请求头的PUT请求"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_put.return_value = mock_response
        
        headers = {"Content-Type": "application/json"}
        data = {"key": "value"}
        put_with_headers("http://example.com", data, headers)
        mock_put.assert_called_once_with("http://example.com", data=data, headers=headers, timeout=30)

    @patch('dbox.my_http.requests.delete')
    def test_delete_with_headers(self, mock_delete, mock_requests):
        """测试带请求头的DELETE请求"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_delete.return_value = mock_response
        
        headers = {"Authorization": "Bearer token"}
        delete_with_headers("http://example.com", headers)
        mock_delete.assert_called_once_with("http://example.com", headers=headers, timeout=30)

    @patch('dbox.my_http.requests.get')
    def test_get_timeout(self, mock_get, mock_requests):
        """测试GET请求超时"""
        mock_get.side_effect = Exception("Timeout")
        
        with pytest.raises(Exception):
            get("http://example.com")

    @patch('dbox.my_http.requests.post')
    def test_post_timeout(self, mock_post, mock_requests):
        """测试POST请求超时"""
        mock_post.side_effect = Exception("Timeout")
        
        with pytest.raises(Exception):
            post("http://example.com", {"data": "value"})

    @patch('dbox.my_http.requests.get')
    def test_get_json_exception(self, mock_get, mock_requests):
        """测试GET JSON请求异常"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.side_effect = Exception("JSON decode error")
        mock_get.return_value = mock_response
        
        result = get_json("http://example.com")
        assert result is None 