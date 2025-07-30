import pytest
import json
import time
from unittest.mock import patch, MagicMock
from dbox.utils import (
    pop_key_from_dict,
    execute_cmd,
    check_shell_run_result,
    my_json_serializable,
    json_to_str,
    byte_to_str,
    bytes_to_str,
    to_boolean,
    get_digit_from_input,
    stat_func_elapsed,
    polishing_int,
    get_caller_info,
    get_caller_desc,
    get_excel_col_name_by_index,
)


class TestUtils:
    """测试工具函数"""

    def test_pop_key_from_dict(self):
        """测试从字典中弹出键值"""
        test_dict = {"a": 1, "b": 2, "c": 3}

        # 测试存在的键
        result = pop_key_from_dict(test_dict, "b")
        assert result == 2
        assert "b" not in test_dict

        # 测试不存在的键
        result = pop_key_from_dict(test_dict, "d", default=99)
        assert result == 99
        assert "d" not in test_dict

    @patch("dbox.utils.subprocess.run")
    def test_execute_cmd_success(self, mock_run):
        """测试成功执行命令"""
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = b"success output"
        mock_result.stderr = b""
        mock_run.return_value = mock_result

        result = execute_cmd(["echo", "test"])
        assert result == mock_result
        mock_run.assert_called_once()

    @patch("dbox.utils.subprocess.run")
    def test_execute_cmd_failure(self, mock_run):
        """测试命令执行失败"""
        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_result.stdout = b""
        mock_result.stderr = b"error output"
        mock_run.return_value = mock_result

        with pytest.raises(Exception):
            execute_cmd(["invalid", "command"], check=True)

    def test_check_shell_run_result(self):
        """测试检查shell运行结果"""
        # 测试成功情况
        assert check_shell_run_result(0) is True
        assert check_shell_run_result(0, "成功") is True

        # 测试失败情况
        assert check_shell_run_result(1) is False
        assert check_shell_run_result(1, "失败") is False

    def test_my_json_serializable(self):
        """测试JSON序列化"""
        # 测试字典
        result = my_json_serializable({"key": "value"})
        assert result == {"key": "value"}

        # 测试列表
        result = my_json_serializable([1, 2, 3])
        assert result == [1, 2, 3]

        # 测试字符串
        result = my_json_serializable("test")
        assert result == "test"

    def test_json_to_str(self):
        """测试JSON转字符串"""
        test_data = {"name": "test", "value": 123}
        result = json_to_str(test_data)
        assert isinstance(result, str)
        assert "name" in result
        assert "test" in result

    def test_byte_to_str(self):
        """测试字节转字符串"""
        # 测试UTF-8编码
        result = byte_to_str(b"test string", "utf-8")
        assert result == "test string"

        # 测试默认编码
        result = byte_to_str(b"test string")
        assert result == "test string"

        # 测试None值
        result = byte_to_str(None)
        assert result == ""

    def test_bytes_to_str(self):
        """测试bytes_to_str函数"""
        result = bytes_to_str(b"test bytes")
        assert result == "test bytes"

    def test_to_boolean(self):
        """测试布尔值转换"""
        # 测试True值
        assert to_boolean(True) is True
        assert to_boolean(1) is True
        assert to_boolean("true") is True
        assert to_boolean("yes") is True

        # 测试False值
        assert to_boolean(False) is False
        assert to_boolean(0) is False
        assert to_boolean("false") is False
        assert to_boolean("no") is False
        assert to_boolean("") is False
        assert to_boolean(None) is False

    @patch("builtins.input")
    def test_get_digit_from_input(self, mock_input):
        """测试获取数字输入"""
        mock_input.return_value = "5"
        result = get_digit_from_input([1, 2, 3, 4, 5])
        assert result == 5

    def test_stat_func_elapsed(self):
        """测试函数耗时统计装饰器"""

        @stat_func_elapsed
        def test_func():
            time.sleep(0.1)
            return "test"

        result = test_func()
        assert result == "test"

    def test_polishing_int(self):
        """测试数字补齐"""
        # 测试补齐
        result = polishing_int(5, 3)
        assert result == "005"

        # 测试不需要补齐
        result = polishing_int(123, 3)
        assert result == "123"

        # 测试长度不足
        result = polishing_int(123, 5)
        assert result == "00123"

    def test_get_caller_info(self):
        """测试获取调用者信息"""
        result = get_caller_info(1)
        assert isinstance(result, dict)
        assert "filename" in result
        assert "lineno" in result
        assert "func_name" in result

    def test_get_caller_desc(self):
        """测试获取调用者描述"""
        result = get_caller_desc(1)
        assert isinstance(result, str)

    def test_get_excel_col_name_by_index(self):
        """测试Excel列名转换"""
        # 测试A列
        assert get_excel_col_name_by_index(0) == "A"

        # 测试Z列
        assert get_excel_col_name_by_index(25) == "Z"

        # 测试AA列
        assert get_excel_col_name_by_index(26) == "AA"

        # 测试AB列
        assert get_excel_col_name_by_index(27) == "AB"
