import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
from dbox.samba import (
    connect_samba,
    upload_file,
    download_file,
    list_files,
    delete_file,
    create_directory,
    remove_directory,
)


class TestSamba:
    """测试Samba相关函数"""

    @patch("dbox.samba.SMBConnection")
    def test_connect_samba_success(self, mock_smb, mock_smb_conn):
        """测试成功连接Samba"""
        mock_conn = MagicMock()
        mock_conn.connect.return_value = True
        mock_smb.return_value = mock_conn

        result = connect_samba("server", "username", "password", "client_name")
        assert result == mock_conn
        mock_conn.connect.assert_called_once()

    @patch("dbox.samba.SMBConnection")
    def test_connect_samba_failure(self, mock_smb, mock_smb_conn):
        """测试连接Samba失败"""
        mock_conn = MagicMock()
        mock_conn.connect.return_value = False
        mock_smb.return_value = mock_conn

        result = connect_samba("server", "username", "password", "client_name")
        assert result is None

    @patch("dbox.samba.SMBConnection")
    def test_connect_samba_exception(self, mock_smb, mock_smb_conn):
        """测试连接Samba异常"""
        mock_conn = MagicMock()
        mock_conn.connect.side_effect = Exception("Connection failed")
        mock_smb.return_value = mock_conn

        result = connect_samba("server", "username", "password", "client_name")
        assert result is None

    @patch("dbox.samba.connect_samba")
    def test_upload_file_success(self, mock_connect, mock_smb_conn):
        """测试成功上传文件"""
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn

        local_file = Path("test_file.txt")
        remote_path = "remote/test_file.txt"

        result = upload_file("server", "username", "password", local_file, remote_path)
        assert result is True
        mock_conn.storeFile.assert_called_once()

    @patch("dbox.samba.connect_samba")
    def test_upload_file_failure(self, mock_connect, mock_smb_conn):
        """测试上传文件失败"""
        mock_connect.return_value = None

        local_file = Path("test_file.txt")
        remote_path = "remote/test_file.txt"

        result = upload_file("server", "username", "password", local_file, remote_path)
        assert result is False

    @patch("dbox.samba.connect_samba")
    def test_upload_file_exception(self, mock_connect, mock_smb_conn):
        """测试上传文件异常"""
        mock_conn = MagicMock()
        mock_conn.storeFile.side_effect = Exception("Upload failed")
        mock_connect.return_value = mock_conn

        local_file = Path("test_file.txt")
        remote_path = "remote/test_file.txt"

        result = upload_file("server", "username", "password", local_file, remote_path)
        assert result is False

    @patch("dbox.samba.connect_samba")
    def test_download_file_success(self, mock_connect, mock_smb_conn):
        """测试成功下载文件"""
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn

        remote_path = "remote/test_file.txt"
        local_file = Path("local_test_file.txt")

        result = download_file("server", "username", "password", remote_path, local_file)
        assert result is True
        mock_conn.retrieveFile.assert_called_once()

    @patch("dbox.samba.connect_samba")
    def test_download_file_failure(self, mock_connect, mock_smb_conn):
        """测试下载文件失败"""
        mock_connect.return_value = None

        remote_path = "remote/test_file.txt"
        local_file = Path("local_test_file.txt")

        result = download_file("server", "username", "password", remote_path, local_file)
        assert result is False

    @patch("dbox.samba.connect_samba")
    def test_download_file_exception(self, mock_connect, mock_smb_conn):
        """测试下载文件异常"""
        mock_conn = MagicMock()
        mock_conn.retrieveFile.side_effect = Exception("Download failed")
        mock_connect.return_value = mock_conn

        remote_path = "remote/test_file.txt"
        local_file = Path("local_test_file.txt")

        result = download_file("server", "username", "password", remote_path, local_file)
        assert result is False

    @patch("dbox.samba.connect_samba")
    def test_list_files_success(self, mock_connect, mock_smb_conn):
        """测试成功列出文件"""
        mock_conn = MagicMock()
        mock_conn.listPath.return_value = [
            MagicMock(filename="file1.txt", isDirectory=False),
            MagicMock(filename="file2.txt", isDirectory=False),
            MagicMock(filename="dir1", isDirectory=True),
        ]
        mock_connect.return_value = mock_conn

        result = list_files("server", "username", "password", "remote_path")
        assert isinstance(result, list)
        assert len(result) == 2  # 只返回文件，不包括目录

    @patch("dbox.samba.connect_samba")
    def test_list_files_failure(self, mock_connect, mock_smb_conn):
        """测试列出文件失败"""
        mock_connect.return_value = None

        result = list_files("server", "username", "password", "remote_path")
        assert result == []

    @patch("dbox.samba.connect_samba")
    def test_list_files_exception(self, mock_connect, mock_smb_conn):
        """测试列出文件异常"""
        mock_conn = MagicMock()
        mock_conn.listPath.side_effect = Exception("List failed")
        mock_connect.return_value = mock_conn

        result = list_files("server", "username", "password", "remote_path")
        assert result == []

    @patch("dbox.samba.connect_samba")
    def test_delete_file_success(self, mock_connect, mock_smb_conn):
        """测试成功删除文件"""
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn

        remote_path = "remote/test_file.txt"

        result = delete_file("server", "username", "password", remote_path)
        assert result is True
        mock_conn.deleteFiles.assert_called_once()

    @patch("dbox.samba.connect_samba")
    def test_delete_file_failure(self, mock_connect, mock_smb_conn):
        """测试删除文件失败"""
        mock_connect.return_value = None

        remote_path = "remote/test_file.txt"

        result = delete_file("server", "username", "password", remote_path)
        assert result is False

    @patch("dbox.samba.connect_samba")
    def test_delete_file_exception(self, mock_connect, mock_smb_conn):
        """测试删除文件异常"""
        mock_conn = MagicMock()
        mock_conn.deleteFiles.side_effect = Exception("Delete failed")
        mock_connect.return_value = mock_conn

        remote_path = "remote/test_file.txt"

        result = delete_file("server", "username", "password", remote_path)
        assert result is False

    @patch("dbox.samba.connect_samba")
    def test_create_directory_success(self, mock_connect, mock_smb_conn):
        """测试成功创建目录"""
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn

        remote_path = "remote/new_directory"

        result = create_directory("server", "username", "password", remote_path)
        assert result is True
        mock_conn.createDirectory.assert_called_once()

    @patch("dbox.samba.connect_samba")
    def test_create_directory_failure(self, mock_connect, mock_smb_conn):
        """测试创建目录失败"""
        mock_connect.return_value = None

        remote_path = "remote/new_directory"

        result = create_directory("server", "username", "password", remote_path)
        assert result is False

    @patch("dbox.samba.connect_samba")
    def test_create_directory_exception(self, mock_connect, mock_smb_conn):
        """测试创建目录异常"""
        mock_conn = MagicMock()
        mock_conn.createDirectory.side_effect = Exception("Create directory failed")
        mock_connect.return_value = mock_conn

        remote_path = "remote/new_directory"

        result = create_directory("server", "username", "password", remote_path)
        assert result is False

    @patch("dbox.samba.connect_samba")
    def test_remove_directory_success(self, mock_connect, mock_smb_conn):
        """测试成功删除目录"""
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn

        remote_path = "remote/old_directory"

        result = remove_directory("server", "username", "password", remote_path)
        assert result is True
        mock_conn.deleteDirectory.assert_called_once()

    @patch("dbox.samba.connect_samba")
    def test_remove_directory_failure(self, mock_connect, mock_smb_conn):
        """测试删除目录失败"""
        mock_connect.return_value = None

        remote_path = "remote/old_directory"

        result = remove_directory("server", "username", "password", remote_path)
        assert result is False

    @patch("dbox.samba.connect_samba")
    def test_remove_directory_exception(self, mock_connect, mock_smb_conn):
        """测试删除目录异常"""
        mock_conn = MagicMock()
        mock_conn.deleteDirectory.side_effect = Exception("Remove directory failed")
        mock_connect.return_value = mock_conn

        remote_path = "remote/old_directory"

        result = remove_directory("server", "username", "password", remote_path)
        assert result is False

    def test_connect_samba_with_defaults(self, mock_smb_conn):
        """测试使用默认参数连接Samba"""
        with patch("dbox.samba.SMBConnection") as mock_smb:
            mock_conn = MagicMock()
            mock_conn.connect.return_value = True
            mock_smb.return_value = mock_conn

            result = connect_samba("server", "username", "password")
            assert result == mock_conn

    def test_upload_file_with_string_path(self, mock_smb_conn):
        """测试使用字符串路径上传文件"""
        with patch("dbox.samba.connect_samba") as mock_connect:
            mock_conn = MagicMock()
            mock_connect.return_value = mock_conn

            result = upload_file("server", "username", "password", "test_file.txt", "remote/test_file.txt")
            assert result is True

    def test_download_file_with_string_path(self, mock_smb_conn):
        """测试使用字符串路径下载文件"""
        with patch("dbox.samba.connect_samba") as mock_connect:
            mock_conn = MagicMock()
            mock_connect.return_value = mock_conn

            result = download_file("server", "username", "password", "remote/test_file.txt", "local_test_file.txt")
            assert result is True
