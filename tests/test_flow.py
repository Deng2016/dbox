import pytest
import json
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch, mock_open, MagicMock
from dbox.flow import (
    get_engine_version_info,
    get_flow_info,
    update_flow_info,
    compare_version_number,
    flow_global_param_convert,
    get_next_version,
    version_increment,
    is_ignore,
    is_author,
    get_file_list_by_suffix,
    get_flow_version,
    get_flow_author,
    is_uuid,
    is_version_no,
    get_flow_name,
    clean_flow,
)


class TestFlow:
    """测试流程相关函数"""

    def setup_method(self):
        """测试前的设置"""
        # 设置测试路径
        self.flow_path = Path(__file__).parent / "resource" / "软件自动化-浏览器"
        self.deputy_abs_path = Path(__file__).parent / "resource" / "Deputy.exe"
        self.flow_file_path = Path(__file__).parent / "resource" / "软件自动化-浏览器" / "main.prj"

        # 创建临时目录用于测试
        self.temp_dir = Path(tempfile.mkdtemp())
        self.test_flow_dir = self.temp_dir / "test_flow"
        self.test_flow_dir.mkdir()

        # 创建测试用的流程文件
        self.test_flow_file = self.test_flow_dir / "main.prj"
        self.test_flow_config = {
            "name": "测试流程",
            "version": "1.0.0",
            "author": "测试作者",
            "description": "这是一个测试流程",
        }

        # 创建测试用的版本文件
        self.test_version_file = self.test_flow_dir / "res"
        self.test_version_file.mkdir()
        (self.test_version_file / "version.txt").write_text("1.0.0", encoding="utf-8")
        (self.test_version_file / "author.txt").write_text("测试作者", encoding="utf-8")

    def teardown_method(self):
        """测试后的清理"""
        # 清理临时目录
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)

    def test_get_engine_version_info(self):
        """测试获取引擎版本信息"""
        # 模拟版本文件内容
        version_content = {
            "Product": "UiBot Enterprise",
            "Version": "6.0.0.221121",
            "Build": "2022.11.21.1912",
            "InstructionSet": "x64"
        }

        result = get_engine_version_info(self.deputy_abs_path)

        assert result["arch"] == "x64"
        assert result["raw_version"] == "6.0.0.221121"
        assert result["version"] == "6.0.0"
        assert result["language"] == "zh-cn"
        assert result["build_date"] == "2022.11.21.1912"
        assert result["edition"] == "enterprise"
        assert result["package"] == "creator"

    def test_get_flow_info(self):
        """测试获取流程信息"""
        result = get_flow_info(self.flow_file_path)

        assert result["name"] == "浏览器"
        assert result["version"] == "6.0.0.211215"

    def test_compare_version_number(self):
        """测试版本号比较"""
        # 测试相等
        assert compare_version_number("1.0.0", "1.0.0") == 0

        # 测试第一个版本号不同
        assert compare_version_number("2.0.0", "1.0.0") > 0
        assert compare_version_number("1.0.0", "2.0.0") < 0

        # 测试第二个版本号不同
        assert compare_version_number("1.1.0", "1.0.0") > 0
        assert compare_version_number("1.0.0", "1.1.0") < 0

        # 测试第三个版本号不同
        assert compare_version_number("1.0.1", "1.0.0") > 0
        assert compare_version_number("1.0.0", "1.0.1") < 0

        # 测试不同级别比较
        assert compare_version_number("1.0.1", "1.0.0", level=2) == 0
        assert compare_version_number("1.1.0", "1.0.0", level=1) == 0

    def test_compare_version_number_invalid_format(self):
        """测试版本号格式不一致的情况"""
        with pytest.raises(ValueError, match="版本格式不一致"):
            compare_version_number("1.0.0", "1.0")

    def test_flow_global_param_convert_to_str(self):
        """测试流程全局参数转换为字符串格式"""
        # 5.2.0以后版本格式转换为5.2.0以前版本格式
        old_format_params = [{"var": "param1", "type": "none"}, {"var": "param2", "type": "none"}]

        result = flow_global_param_convert(old_format_params, str)
        assert result == ["param1", "param2"]

    def test_flow_global_param_convert_to_dict(self):
        """测试流程全局参数转换为字典格式"""
        # 5.2.0以前版本格式转换为5.2.0以后版本格式
        new_format_params = ["param1", "param2"]

        result = flow_global_param_convert(new_format_params, dict)
        assert result == [{"var": "param1", "type": "none"}, {"var": "param2", "type": "none"}]

    def test_get_next_version(self):
        """测试获取下一版本号"""
        assert get_next_version("1.0.0") == "1.0.1"
        assert get_next_version("1.0.9") == "1.0.10"
        assert get_next_version("2.1.5") == "2.1.6"
        assert get_next_version("2.1.99999") == "2.1.100000"

    def test_version_increment(self):
        """测试版本号递增"""
        assert version_increment("1.0.0", step=10) == "1.0.1"
        assert version_increment("1.0.9", step=10) == "1.1.0"
        assert version_increment("1.9.9", step=10) == "2.0.0"
        assert version_increment("1.9.9", step=100) == "1.9.10"
        assert version_increment("1.99.99", step=100) == "2.0.0"
        assert version_increment("1.0.0", step=5) == "1.0.1"
        assert version_increment("1.4.4", step=5) == "2.0.0"

    def test_is_ignore_name_match(self):
        """测试按名称忽略流程"""
        ignore_file_path1 = Path(__file__).parent / "resource" / "ignore1.txt"
        result1 = is_ignore(ignore_file_path1, self.flow_file_path)
        assert result1 is True

        ignore_file_path2 = Path(__file__).parent / "resource" / "ignore2.txt"
        result2 = is_ignore(ignore_file_path2, self.flow_file_path)
        assert result2 is False

    @patch("dbox.file.check_path_is_exits")
    def test_is_ignore_file_not_exists(self, mock_check_path):
        """测试忽略文件不存在的情况"""
        mock_check_path.side_effect = FileNotFoundError()

        result = is_ignore(self.temp_dir / "not_exists.txt", self.flow_file_path)
        assert result is False

    @patch("dbox.flow.get_flow_author")
    def test_is_author(self, mock_get_author):
        """测试判断是否为流程作者"""
        mock_get_author.return_value = "测试作者"

        assert is_author("测试作者", self.flow_file_path) is True
        assert is_author("其他作者", self.flow_file_path) is False

    @patch("dbox.flow.get_flow_name")
    @patch("dbox.flow.get_flow_version")
    @patch("dbox.flow.get_flow_author")
    @patch("dbox.flow.is_ignore")
    def test_get_file_list_by_suffix(self, mock_is_ignore, mock_get_author, mock_get_version, mock_get_name):
        """测试获取特定扩展名文件列表"""
        # 创建测试文件
        test_files = [
            self.test_flow_dir / "flow1.prj",
            self.test_flow_dir / "flow2.prj",
            self.test_flow_dir / "subdir" / "flow3.prj",
        ]

        for file_path in test_files:
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.touch()

        # 模拟函数返回值
        mock_get_name.return_value = "测试流程"
        mock_get_version.return_value = "1.0.0"
        mock_get_author.return_value = "测试作者"
        mock_is_ignore.return_value = False

        result = get_file_list_by_suffix(self.test_flow_dir, "prj")

        assert len(result) == 3
        assert all(file.suffix == ".prj" for file in result)

    @patch("dbox.file.check_path_is_exits")
    def test_get_flow_version(self, mock_check_path):
        """测试获取流程版本"""
        with patch("builtins.open", mock_open(read_data="1.0.0")):
            result = get_flow_version(self.flow_file_path)

        assert result == "1.0.0"

    @patch("dbox.file.check_path_is_exits")
    def test_get_flow_author(self, mock_check_path):
        """测试获取流程作者"""
        with patch("builtins.open", mock_open(read_data="测试作者")):
            result = get_flow_author(self.flow_file_path)

        assert result == "测试作者"

    def test_is_uuid(self):
        """测试UUID格式判断"""
        # 有效的UUID
        valid_uuid = "123e4567-e89b-12d3-a456-426614174000"
        assert is_uuid(valid_uuid) == valid_uuid

        # 无效的UUID
        assert is_uuid("invalid-uuid") is False
        assert is_uuid("123e4567-e89b-12d3-a456") is False
        assert is_uuid("") is False

    def test_is_version_no(self):
        """测试版本号格式判断"""
        # 有效的版本号
        assert is_version_no("1.0.0") == "1.0.0"
        assert is_version_no("2.1.5") == "2.1.5"

        # 无效的版本号
        assert is_version_no("1.0") is False
        assert is_version_no("0.1.0") is False
        assert is_version_no("1.0.0.0") == "1.0.0"
        assert is_version_no("") is False
        assert is_version_no("1.0.0") == "1.0.0"  # 这个应该通过

    @patch("dbox.file.check_path_is_exits")
    def test_get_flow_name_from_stem(self, mock_check_path):
        """测试从文件名获取流程名称（非main文件）"""
        flow_file = self.test_flow_dir / "test_flow.prj"
        result = get_flow_name(flow_file)
        assert result == "test_flow"

    def test_get_flow_name(self):
        """测试从JSON文件获取流程名称"""
        result = get_flow_name(self.flow_file_path)
        assert result == "浏览器"

        result = get_flow_name(Path(__file__).parent / "resource" / "大量日志任务" / "main.flowc")
        assert result == "大量日志任务"

    @patch("dbox.file.check_path_is_exits")
    def test_clean_flow(self, mock_check_path):
        """测试清理流程目录"""
        # 创建测试文件
        test_files = [
            self.test_flow_dir / "test.bot",
            self.test_flow_dir / "test.flowc",
            self.test_flow_dir / "test.taskc",
            self.test_flow_dir / "test.cme",
            self.test_flow_dir / "test.bak",
            self.test_flow_dir / "log" / "test.log",
            self.test_flow_dir / "tempgit" / "test",
            self.test_flow_dir / "config.json",
            self.test_flow_dir / ".git" / "test",
        ]

        for file_path in test_files:
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.touch()

        # 创建保留的文件
        keep_files = [self.test_flow_dir / "main.prj", self.test_flow_dir / "res" / "version.txt"]

        for file_path in keep_files:
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.touch()

        clean_flow(self.test_flow_dir)

        # 验证临时文件被删除
        for file_path in test_files:
            assert not file_path.exists()

        # 验证保留文件仍然存在
        for file_path in keep_files:
            assert file_path.exists()

    def test_flow_global_param_convert_invalid_type(self):
        """测试流程全局参数转换时遇到子流程的情况"""
        params_with_subflow = [{"var": "param1", "type": "subflow"}, {"var": "param2", "type": "none"}]

        with pytest.raises(ValueError, match="流程中用到了子流程"):
            flow_global_param_convert(params_with_subflow, str)
