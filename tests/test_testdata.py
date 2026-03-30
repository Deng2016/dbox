import pytest
import datetime
from unittest.mock import patch
from dbox.testdata import (
    get_date,
    get_datetime,
    get_timestamp,
    get_random_date,
    get_random_string,
    get_uuid,
    get_pinyin,
    get_name,
    generate_id_card,
    generate_mobile_number,
    generate_phone_serial_number,
    generate_bank_card_number,
    get_bank_bin,
    get_special_character,
    validate_id_card,
)


class TestTestData:
    """测试测试数据生成函数"""

    def test_get_date_default(self):
        """测试获取当前日期"""
        result = get_date()
        assert isinstance(result, str)
        assert len(result) == 10
        assert result.count("-") == 2

    def test_get_date_with_offset_positive(self):
        """测试获取偏移日期-未来"""
        result = get_date(10)
        assert isinstance(result, str)
        today = datetime.date.today()
        expected = (today + datetime.timedelta(days=10)).strftime("%Y-%m-%d")
        assert result == expected

    def test_get_date_with_offset_negative(self):
        """测试获取偏移日期-过去"""
        result = get_date(-10)
        assert isinstance(result, str)
        today = datetime.date.today()
        expected = (today + datetime.timedelta(days=-10)).strftime("%Y-%m-%d")
        assert result == expected

    def test_get_datetime_default(self):
        """测试获取当前日期时间"""
        result = get_datetime()
        assert isinstance(result, str)
        assert len(result) == 19
        assert result.count("-") == 2
        assert result.count(":") == 2

    def test_get_datetime_with_offset_positive(self):
        """测试获取偏移日期时间-未来"""
        result = get_datetime(3600)
        assert isinstance(result, str)
        now = datetime.datetime.now()
        expected = (now + datetime.timedelta(seconds=3600)).strftime("%Y-%m-%d %H:%M:%S")
        assert result == expected

    def test_get_datetime_with_offset_negative(self):
        """测试获取偏移日期时间-过去"""
        result = get_datetime(-3600)
        assert isinstance(result, str)
        now = datetime.datetime.now()
        expected = (now + datetime.timedelta(seconds=-3600)).strftime("%Y-%m-%d %H:%M:%S")
        assert result == expected

    def test_get_timestamp_10_digits(self):
        """测试获取10位时间戳（秒级）"""
        result = get_timestamp()
        assert isinstance(result, int)
        assert len(str(result)) == 10

    def test_get_timestamp_13_digits(self):
        """测试获取13位时间戳（毫秒级）"""
        result = get_timestamp(length=13)
        assert isinstance(result, int)
        assert len(str(result)) == 13

    def test_get_timestamp_with_offset(self):
        """测试获取偏移时间戳"""
        result = get_timestamp(offset=3600)
        assert isinstance(result, int)

    def test_get_timestamp_invalid_length(self):
        """测试无效时间戳长度"""
        with pytest.raises(ValueError, match="length参数仅支持10"):
            get_timestamp(length=12)

    def test_get_random_date_default(self):
        """测试默认随机日期生成"""
        result = get_random_date()
        assert isinstance(result, str)
        assert len(result.split("-")) == 3

    def test_get_random_date_with_dates(self):
        """测试指定日期范围的随机日期生成"""
        start_date = "2023-01-01"
        end_date = "2023-12-31"
        result = get_random_date(start_date, end_date)
        assert isinstance(result, str)
        assert len(result.split("-")) == 3

    def test_get_random_date_custom_format(self):
        """测试自定义格式的随机日期生成"""
        result = get_random_date(date_format="%Y%m%d")
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

    @patch("dbox.testdata.get_name")
    @patch("dbox.testdata.Pinyin")
    def test_get_pinyin_without_name(self, mock_pinyin, mock_get_name):
        """测试获取拼音-未指定姓名"""
        mock_get_name.return_value = "李四"
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
        result = get_name(1)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_get_name_female(self):
        """测试获取姓名-女性"""
        result = get_name(2)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_generate_id_card_default(self):
        """测试获取身份证号-默认"""
        result = generate_id_card()
        assert isinstance(result, str)
        assert len(result) == 18

    def test_generate_id_card_male(self):
        """测试获取身份证号-男性"""
        result = generate_id_card(1)
        assert isinstance(result, str)
        assert len(result) == 18

    def test_generate_id_card_female(self):
        """测试获取身份证号-女性"""
        result = generate_id_card(2)
        assert isinstance(result, str)
        assert len(result) == 18

    def test_validate_id_card_valid(self):
        """测试验证有效的身份证号-18位"""
        # 使用 generate_id_card 生成有效身份证进行测试
        valid_id = generate_id_card()
        result = validate_id_card(valid_id)
        assert result == valid_id[-1]

    def test_validate_id_card_calculate_from_17_digits(self):
        """测试从17位计算校验码"""
        # 生成有效身份证，截取前17位进行计算
        valid_id = generate_id_card()
        id_17 = valid_id[:17]
        result = validate_id_card(id_17)
        assert isinstance(result, str)
        assert len(result) == 1
        assert result == valid_id[-1]

    def test_validate_id_card_invalid_length(self):
        """测试无效身份证号长度"""
        result = validate_id_card("12345")
        assert result is False

    def test_validate_id_card_invalid_characters(self):
        """测试包含无效字符的身份证号（前17位包含字母）"""
        result = validate_id_card("11010119900307A31X")
        assert result is False

    def test_validate_id_card_invalid_check_code(self):
        """测试无效校验码"""
        # 生成有效身份证，修改最后一位为错误值
        valid_id = generate_id_card()
        wrong_id = valid_id[:-1] + ("0" if valid_id[-1] != "0" else "1")
        result = validate_id_card(wrong_id)
        assert result == ""

    def test_generate_mobile_number(self):
        """测试获取手机号"""
        result = generate_mobile_number()
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
                "153",
                "155",
                "156",
                "157",
                "158",
                "159",
                "170",
                "171",
                "172",
                "173",
                "174",
                "175",
                "176",
                "177",
                "178",
                "180",
                "181",
                "182",
                "183",
                "184",
                "185",
                "186",
                "187",
                "188",
                "189",
            )
        )

    def test_generate_phone_serial_number(self):
        """测试获取手机串号"""
        result = generate_phone_serial_number()
        assert isinstance(result, str)
        assert "-" in result
        parts = result.split("-")
        assert len(parts) == 3
        assert len(parts[0]) == 4
        assert len(parts[1]) == 4
        assert len(parts[2]) == 5

    def test_generate_bank_card_number_default(self):
        """测试获取银行卡号-默认"""
        result = generate_bank_card_number(card_count=1, return_single=True)
        # 注意：原函数返回的是列表还是单个值取决于return_single参数
        # 我们只验证函数能正常工作
        assert result is not None

    def test_generate_bank_card_number_multiple(self):
        """测试获取银行卡号-多个"""
        result = generate_bank_card_number(card_count=3)
        assert isinstance(result, list)
        assert len(result) == 3

    def test_generate_bank_card_number_specific_bank(self):
        """测试获取银行卡号-指定银行"""
        result = generate_bank_card_number(card_count=1, bank_code="ICBC")
        assert result is not None

    def test_get_bank_bin_default(self):
        """测试获取银行卡BIN-默认"""
        result = get_bank_bin(num=1)
        assert isinstance(result, list)
        assert len(result) >= 1

    def test_get_bank_bin_multiple(self):
        """测试获取银行卡BIN-多个"""
        result = get_bank_bin(num=3)
        assert isinstance(result, list)
        assert len(result) == 3

    def test_get_bank_bin_specific_bank(self):
        """测试获取银行卡BIN-指定银行"""
        result = get_bank_bin(num=1, bank="ICBC")
        assert isinstance(result, list)
        assert len(result) >= 1

    def test_get_special_character(self):
        """测试获取特殊字符"""
        result = get_special_character(5)
        assert isinstance(result, str)
        assert len(result) == 5
