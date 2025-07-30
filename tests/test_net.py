import pytest
import socket
from unittest.mock import patch, MagicMock
from dbox.net import get_hostname, get_ip_address, get_mac_address, ping_host, check_port_open, get_network_info


class TestNet:
    """测试网络相关函数"""

    @patch("dbox.net.socket.gethostname")
    def test_get_hostname(self, mock_gethostname):
        """测试获取主机名"""
        mock_gethostname.return_value = "test-host"
        result = get_hostname()
        assert result == "test-host"

    @patch("dbox.net.socket.gethostbyname")
    def test_get_ip_address(self, mock_gethostbyname):
        """测试获取IP地址"""
        mock_gethostbyname.return_value = "192.168.1.1"
        result = get_ip_address()
        assert result == "192.168.1.1"

    @patch("dbox.net.socket.gethostbyname")
    def test_get_ip_address_with_hostname(self, mock_gethostbyname):
        """测试获取指定主机名的IP地址"""
        mock_gethostbyname.return_value = "10.0.0.1"
        result = get_ip_address("test-host")
        assert result == "10.0.0.1"

    @patch("dbox.net.socket.gethostbyname")
    def test_get_ip_address_failure(self, mock_gethostbyname):
        """测试获取IP地址失败"""
        mock_gethostbyname.side_effect = socket.gaierror("Name or service not known")
        result = get_ip_address("invalid-host")
        assert result is None

    @patch("dbox.net.uuid.getnode")
    def test_get_mac_address(self, mock_getnode):
        """测试获取MAC地址"""
        mock_getnode.return_value = 123456789
        result = get_mac_address()
        assert isinstance(result, str)
        assert len(result.split(":")) == 6

    @patch("dbox.net.subprocess.run")
    def test_ping_host_success(self, mock_run):
        """测试成功ping主机"""
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_run.return_value = mock_result

        result = ping_host("192.168.1.1")
        assert result is True

    @patch("dbox.net.subprocess.run")
    def test_ping_host_failure(self, mock_run):
        """测试ping主机失败"""
        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_run.return_value = mock_result

        result = ping_host("192.168.1.999")
        assert result is False

    @patch("dbox.net.socket.socket")
    def test_check_port_open_success(self, mock_socket):
        """测试检查端口开放成功"""
        mock_sock = MagicMock()
        mock_socket.return_value = mock_sock
        mock_sock.connect.return_value = None

        result = check_port_open("192.168.1.1", 80)
        assert result is True
        mock_sock.close.assert_called_once()

    @patch("dbox.net.socket.socket")
    def test_check_port_open_failure(self, mock_socket):
        """测试检查端口开放失败"""
        mock_sock = MagicMock()
        mock_socket.return_value = mock_sock
        mock_sock.connect.side_effect = socket.error("Connection refused")

        result = check_port_open("192.168.1.1", 9999)
        assert result is False
        mock_sock.close.assert_called_once()

    @patch("dbox.net.socket.socket")
    def test_check_port_open_timeout(self, mock_socket):
        """测试检查端口开放超时"""
        mock_sock = MagicMock()
        mock_socket.return_value = mock_sock
        mock_sock.connect.side_effect = socket.timeout("Connection timed out")

        result = check_port_open("192.168.1.1", 80, timeout=1)
        assert result is False
        mock_sock.close.assert_called_once()

    def test_get_network_info(self):
        """测试获取网络信息"""
        result = get_network_info()
        assert isinstance(result, dict)
        assert "hostname" in result
        assert "ip_address" in result
        assert "mac_address" in result

    @patch("dbox.net.get_hostname")
    @patch("dbox.net.get_ip_address")
    @patch("dbox.net.get_mac_address")
    def test_get_network_info_with_mocks(self, mock_mac, mock_ip, mock_hostname):
        """测试使用模拟获取网络信息"""
        mock_hostname.return_value = "test-host"
        mock_ip.return_value = "192.168.1.1"
        mock_mac.return_value = "00:11:22:33:44:55"

        result = get_network_info()
        assert result["hostname"] == "test-host"
        assert result["ip_address"] == "192.168.1.1"
        assert result["mac_address"] == "00:11:22:33:44:55"

    @patch("dbox.net.socket.socket")
    def test_check_port_open_with_timeout(self, mock_socket):
        """测试带超时的端口检查"""
        mock_sock = MagicMock()
        mock_socket.return_value = mock_sock
        mock_sock.connect.return_value = None

        result = check_port_open("192.168.1.1", 80, timeout=5)
        assert result is True
        mock_sock.settimeout.assert_called_once_with(5)

    @patch("dbox.net.socket.socket")
    def test_check_port_open_invalid_host(self, mock_socket):
        """测试检查无效主机的端口"""
        mock_sock = MagicMock()
        mock_socket.return_value = mock_sock
        mock_sock.connect.side_effect = socket.gaierror("Name or service not known")

        result = check_port_open("invalid-host", 80)
        assert result is False

    @patch("dbox.net.socket.socket")
    def test_check_port_open_invalid_port(self, mock_socket):
        """测试检查无效端口"""
        mock_sock = MagicMock()
        mock_socket.return_value = mock_sock
        mock_sock.connect.side_effect = socket.error("Invalid port")

        result = check_port_open("192.168.1.1", 99999)
        assert result is False

    def test_ping_host_invalid_address(self):
        """测试ping无效地址"""
        result = ping_host("invalid-address")
        assert result is False

    def test_ping_host_empty_address(self):
        """测试ping空地址"""
        result = ping_host("")
        assert result is False

    def test_ping_host_none_address(self):
        """测试ping None地址"""
        result = ping_host(None)
        assert result is False

    @patch("dbox.net.socket.gethostname")
    def test_get_hostname_exception(self, mock_gethostname):
        """测试获取主机名异常"""
        mock_gethostname.side_effect = Exception("Hostname error")
        result = get_hostname()
        assert result is None

    @patch("dbox.net.uuid.getnode")
    def test_get_mac_address_exception(self, mock_getnode):
        """测试获取MAC地址异常"""
        mock_getnode.side_effect = Exception("MAC address error")
        result = get_mac_address()
        assert result is None
