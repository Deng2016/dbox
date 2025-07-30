import pytest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock
from dbox.file import (
    check_path_is_exits,
    ensure_empty_dir,
    compress_zip,
    extract_zip,
    rm,
    rm_safe,
    move_to_dir,
    copy_to_target,
    copy_to_target_by_pattern,
    read_file_raw_content,
    read_file_content,
    save_obj_to_file,
    save_json_to_file,
    get_newest_file,
    get_file_time,
    get_ini_config_object,
    save_ini_config_object,
    compare_dir,
    compare_file,
)


class TestFile:
    """测试文件操作函数"""

    def test_check_path_is_exits_file(self, temp_dir):
        """测试检查文件是否存在"""
        # 创建测试文件
        test_file = temp_dir / "test.txt"
        test_file.write_text("test content")

        # 测试文件存在
        check_path_is_exits(test_file)
        check_path_is_exits(str(test_file))

        # 测试指定文件类型
        check_path_is_exits(test_file, "file")

        # 测试文件不存在
        with pytest.raises(FileNotFoundError):
            check_path_is_exits(temp_dir / "nonexistent.txt")

    def test_check_path_is_exits_dir(self, temp_dir):
        """测试检查目录是否存在"""
        # 创建测试目录
        test_dir = temp_dir / "test_dir"
        test_dir.mkdir()

        # 测试目录存在
        check_path_is_exits(test_dir)
        check_path_is_exits(str(test_dir))

        # 测试指定目录类型
        check_path_is_exits(test_dir, "dir")

        # 测试目录不存在
        with pytest.raises(FileNotFoundError):
            check_path_is_exits(temp_dir / "nonexistent_dir")

    def test_ensure_empty_dir(self, temp_dir):
        """测试确保空目录"""
        test_dir = temp_dir / "test_dir"

        # 测试创建新目录
        ensure_empty_dir(test_dir)
        assert test_dir.exists()
        assert test_dir.is_dir()

        # 测试清空非空目录
        (test_dir / "test.txt").write_text("test")
        ensure_empty_dir(test_dir)
        assert len(list(test_dir.iterdir())) == 0

    def test_rm_file(self, temp_dir):
        """测试删除文件"""
        test_file = temp_dir / "test.txt"
        test_file.write_text("test content")

        rm(test_file)
        assert not test_file.exists()

    def test_rm_safe(self, temp_dir):
        """测试安全删除"""
        test_file = temp_dir / "test.txt"
        test_file.write_text("test content")

        rm_safe(test_file)
        assert not test_file.exists()

    def test_move_to_dir(self, temp_dir):
        """测试移动文件"""
        source_file = temp_dir / "source.txt"
        source_file.write_text("test content")
        target_dir = temp_dir / "target"
        target_dir.mkdir()

        move_to_dir(source_file, target_dir)
        assert not source_file.exists()
        assert (target_dir / "source.txt").exists()

    def test_copy_to_target(self, temp_dir):
        """测试复制文件"""
        source_file = temp_dir / "source.txt"
        source_file.write_text("test content")
        target_file = temp_dir / "target.txt"

        copy_to_target(source_file, target_file)
        assert target_file.exists()
        assert source_file.exists()  # 源文件应该还在

    def test_read_file_content(self, temp_dir):
        """测试读取文件内容"""
        test_file = temp_dir / "test.txt"
        test_file.write_text("test content")

        # 测试默认读取
        content = read_file_content(test_file)
        assert content == "test content"

        # 测试JSON读取
        json_file = temp_dir / "test.json"
        json_file.write_text('{"key": "value"}')
        content = read_file_content(json_file, _return="json")
        assert content == {"key": "value"}

    def test_save_json_to_file(self, temp_dir):
        """测试保存JSON文件"""
        test_data = {"name": "test", "value": 123}
        test_file = temp_dir / "test.json"

        save_json_to_file(test_data, test_file)
        assert test_file.exists()

        # 验证内容
        content = read_file_content(test_file, _return="json")
        assert content == test_data

    def test_get_newest_file(self, temp_dir):
        """测试获取最新文件"""
        # 创建多个文件
        files = []
        for i in range(3):
            file_path = temp_dir / f"file_{i}.txt"
            file_path.write_text(f"content {i}")
            files.append(file_path)

        # 测试获取最新文件
        newest = get_newest_file(str(temp_dir))
        assert newest is not None

    def test_get_file_time(self, temp_dir):
        """测试获取文件时间"""
        test_file = temp_dir / "test.txt"
        test_file.write_text("test content")

        # 测试创建时间
        create_time = get_file_time(test_file, "c")
        assert create_time is not None

        # 测试修改时间
        modify_time = get_file_time(test_file, "m")
        assert modify_time is not None

    def test_compare_file(self, temp_dir):
        """测试比较文件"""
        file1 = temp_dir / "file1.txt"
        file2 = temp_dir / "file2.txt"

        file1.write_text("same content")
        file2.write_text("same content")

        # 测试相同文件
        assert compare_file(str(file1), str(file2)) is True

        # 测试不同文件
        file2.write_text("different content")
        assert compare_file(str(file1), str(file2)) is False

    @patch("dbox.file.zipfile.ZipFile")
    def test_compress_zip(self, mock_zipfile, temp_dir):
        """测试压缩ZIP文件"""
        source_dir = temp_dir / "source"
        source_dir.mkdir()
        (source_dir / "test.txt").write_text("test content")

        compress_zip(str(source_dir), str(temp_dir / "test.zip"))
        mock_zipfile.assert_called_once()
