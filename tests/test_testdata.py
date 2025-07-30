import pytest
import datetime
from unittest.mock import patch
from dbox.testdata import (
    get_random_data,
    get_random_string,
    get_uuid,
    get_pinyin,
    get_name,
    get_idcards,
    get_mobile_no,
    get_phone_serial_no,
    get_bank_no,
    get_bank_bin,
    get_special_character,
)


class TestTestData:
    """测试测试数据生成函数"""

    def test_get_random_data_default(self):
        """测试默认随机日期生成"""
        result = get_random_data()
        assert isinstance(result, str)
        assert len(result.split("-")) == 3

    def test_get_random_data_with_dates(self):
        """测试指定日期范围的随机日期生成"""
        start_date = "2023-01-01"
        end_date = "2023-12-31"
        result = get_random_data(start_date, end_date)
        assert isinstance(result, str)
        assert len(result.split("-")) == 3

    def test_get_random_data_custom_format(self):
        """测试自定义格式的随机日期生成"""
        result = get_random_data(_format="%Y%m%d")
        assert isinstance(result, str)
        assert len(result) == 8

    def test_get_random_string_default(self):
        """测试默认随机字符串生成"""
        result = get_random_string()
        assert isinstance(result, str)
        assert len(result) == 32

    def test_get_random_string_custom_length(self):
        """测试自定义长度的随机字符串生成"""
        result = get_random_string(10)
        assert isinstance(result, str)
        assert len(result) == 10

    def test_get_random_string_digits_only(self):
        """测试仅数字的随机字符串生成"""
        result = get_random_string(10, "d")
        assert isinstance(result, str)
        assert len(result) == 10
        assert result.isdigit()

    def test_get_random_string_letters_only(self):
        """测试仅字母的随机字符串生成"""
        result = get_random_string(10, "l")
        assert isinstance(result, str)
        assert len(result) == 10
        assert result.isalpha()
        assert result.islower()

    def test_get_random_string_uppercase_only(self):
        """测试仅大写字母的随机字符串生成"""
        result = get_random_string(10, "u")
        assert isinstance(result, str)
        assert len(result) == 10
        assert result.isalpha()
        assert result.isupper()

    def test_get_uuid_32(self):
        """测试32位UUID生成"""
        result = get_uuid(32)
        assert isinstance(result, str)
        assert len(result) == 32
        assert "-" not in result

    def test_get_uuid_36(self):
        """测试36位UUID生成"""
        result = get_uuid(36)
        assert isinstance(result, str)
        assert len(result) == 36
        assert result.count("-") == 4

    def test_get_uuid_custom_length(self):
        """测试自定义长度UUID生成"""
        result = get_uuid(16)
        assert isinstance(result, str)
        assert len(result) == 16

    @patch("dbox.testdata.Pinyin")
    def test_get_pinyin_with_name(self, mock_pinyin):
        """测试获取拼音-指定姓名"""
        mock_pinyin_instance = mock_pinyin.return_value
        mock_pinyin_instance.get_pinyin.return_value = "zhang san"

        result = get_pinyin("张三")
        assert isinstance(result, tuple)
        assert len(result) == 2
        assert result[0] == "zhang san"
        assert result[1] == "张三"

    @patch("dbox.testdata.Pinyin")
    def test_get_pinyin_without_name(self, mock_pinyin):
        """测试获取拼音-未指定姓名"""
        mock_pinyin_instance = mock_pinyin.return_value
        mock_pinyin_instance.get_pinyin.return_value = "li si"

        result = get_pinyin()
        assert isinstance(result, tuple)
        assert len(result) == 2

    def test_get_name_default(self):
        """测试获取姓名-默认"""
        result = get_name()
        assert isinstance(result, str)
        assert len(result) > 0

    def test_get_name_male(self):
        """测试获取姓名-男性"""
        result = get_name("男")
        assert isinstance(result, str)
        assert len(result) > 0

    def test_get_name_female(self):
        """测试获取姓名-女性"""
        result = get_name("女")
        assert isinstance(result, str)
        assert len(result) > 0

    def test_get_idcards_default(self):
        """测试获取身份证号-默认"""
        result = get_idcards()
        assert isinstance(result, str)
        assert len(result) == 18

    def test_get_idcards_male(self):
        """测试获取身份证号-男性"""
        result = get_idcards(1)
        assert isinstance(result, str)
        assert len(result) == 18

    def test_get_idcards_female(self):
        """测试获取身份证号-女性"""
        result = get_idcards(2)
        assert isinstance(result, str)
        assert len(result) == 18

    def test_get_mobile_no(self):
        """测试获取手机号"""
        result = get_mobile_no()
        assert isinstance(result, str)
        assert len(result) == 11
        assert result.startswith(
            (
                "130",
                "131",
                "132",
                "133",
                "134",
                "135",
                "136",
                "137",
                "138",
                "139",
                "150",
                "151",
                "152",
                "155",
                "158",
                "170",
                "171",
                "172",
                "173",
                "174",
                "175",
                "176",
                "177",
                "178",
                "179",
                "181",
                "186",
                "187",
                "188",
                "189",
            )
        )

    def test_get_phone_serial_no(self):
        """测试获取手机串号"""
        result = get_phone_serial_no()
        assert isinstance(result, str)
        assert "-" in result
        parts = result.split("-")
        assert len(parts) == 3
        assert len(parts[0]) == 4
        assert len(parts[1]) == 4
        assert len(parts[2]) == 5

    def test_get_bank_no_default(self):
        """测试获取银行卡号-默认"""
        result = get_bank_no()
        assert isinstance(result, list)
        assert len(result) == 1

    def test_get_bank_no_multiple(self):
        """测试获取银行卡号-多个"""
        result = get_bank_no(num=3)
        assert isinstance(result, list)
        assert len(result) == 3

    def test_get_bank_no_specific_bank(self):
        """测试获取银行卡号-指定银行"""
        result = get_bank_no(bank="ICBC")
        assert isinstance(result, list)
        assert len(result) == 1

    def test_get_bank_bin_default(self):
        """测试获取银行卡BIN-默认"""
        result = get_bank_bin()
        assert isinstance(result, list)
        assert len(result) == 1

    def test_get_bank_bin_multiple(self):
        """测试获取银行卡BIN-多个"""
        result = get_bank_bin(num=3)
        assert isinstance(result, list)
        assert len(result) == 3

    def test_get_bank_bin_specific_bank(self):
        """测试获取银行卡BIN-指定银行"""
        result = get_bank_bin(bank="ICBC")
        assert isinstance(result, list)
        assert len(result) == 1

    def test_get_special_character(self):
        """测试获取特殊字符"""
        result = get_special_character(5)
        assert isinstance(result, str)
        assert len(result) == 5
