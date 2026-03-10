import pytest
from dbox import addressinfo
from dbox import bankinfo


class TestAddressInfo:
    """测试地址信息模块"""

    def test_addr_exists(self):
        """测试addr变量存在"""
        assert hasattr(addressinfo, "addr")
        assert isinstance(addressinfo.addr, list)

    def test_addr_not_empty(self):
        """测试地址数据不为空"""
        assert len(addressinfo.addr) > 0

    def test_addr_structure(self):
        """测试地址数据结构"""
        for item in addressinfo.addr:
            assert isinstance(item, tuple)
            assert len(item) == 2
            assert isinstance(item[0], int)  # 地区代码
            assert isinstance(item[1], str)  # 地区名称

    def test_addr_has_beijing(self):
        """测试包含北京数据"""
        beijing = (110000, "北京市")
        assert beijing in addressinfo.addr

    def test_addr_has_shanghai(self):
        """测试包含上海数据"""
        shanghai = (310000, "上海市")
        found = any(item[0] == 310000 for item in addressinfo.addr)
        assert found, "上海市数据未找到"

    def test_addr_code_positive(self):
        """测试地区代码为正数"""
        for code, name in addressinfo.addr:
            assert code > 0, f"地区代码 {code} 应该是正数"

    def test_addr_name_not_empty(self):
        """测试地区名称不为空"""
        for code, name in addressinfo.addr:
            assert len(name) > 0, f"地区 {code} 的名称不能为空"

    def test_addr_unique_codes(self):
        """测试地区代码唯一性"""
        codes = [code for code, name in addressinfo.addr]
        assert len(codes) == len(set(codes)), "存在重复的地区代码"


class TestBankInfo:
    """测试银行信息模块"""

    def test_bank_list_exists(self):
        """测试bank_list变量存在"""
        assert hasattr(bankinfo, "bank_list")
        assert isinstance(bankinfo.bank_list, list)

    def test_bank_bin_list_exists(self):
        """测试bank_bin_list变量存在"""
        assert hasattr(bankinfo, "bank_bin_list")
        assert isinstance(bankinfo.bank_bin_list, list)

    def test_bank_list_not_empty(self):
        """测试银行列表不为空"""
        assert len(bankinfo.bank_list) > 0

    def test_bank_bin_list_not_empty(self):
        """测试银行BIN列表不为空"""
        assert len(bankinfo.bank_bin_list) > 0

    def test_bank_list_structure(self):
        """测试银行列表结构"""
        for bank in bankinfo.bank_list:
            assert isinstance(bank, dict)
            assert "key" in bank
            assert "name" in bank
            assert isinstance(bank["key"], str)
            assert isinstance(bank["name"], str)

    def test_bank_bin_list_structure(self):
        """测试银行BIN列表结构"""
        for bin_info in bankinfo.bank_bin_list:
            assert isinstance(bin_info, dict)
            assert "bin" in bin_info
            assert "bank" in bin_info
            assert "type" in bin_info
            assert "length" in bin_info
            assert "name" in bin_info
            assert isinstance(bin_info["bin"], str)
            assert isinstance(bin_info["bank"], str)
            assert isinstance(bin_info["type"], str)
            assert isinstance(bin_info["length"], str)
            assert isinstance(bin_info["name"], str)

    def test_major_banks_exist(self):
        """测试主要银行存在"""
        major_banks = ["ICBC", "CCB", "ABC", "BOC", "CMB"]
        bank_keys = [bank["key"] for bank in bankinfo.bank_list]

        for bank_key in major_banks:
            assert bank_key in bank_keys, f"主要银行 {bank_key} 未找到"

    def test_icbc_in_bank_list(self):
        """测试工商银行在列表中"""
        icbc = next((b for b in bankinfo.bank_list if b["key"] == "ICBC"), None)
        assert icbc is not None
        assert icbc["name"] == "中国工商银行"

    def test_ccb_in_bank_list(self):
        """测试建设银行在列表中"""
        ccb = next((b for b in bankinfo.bank_list if b["key"] == "CCB"), None)
        assert ccb is not None
        assert ccb["name"] == "中国建设银行"

    def test_bank_list_unique_keys(self):
        """测试银行key唯一性"""
        keys = [bank["key"] for bank in bankinfo.bank_list]
        assert len(keys) == len(set(keys)), "存在重复的银行key"

    def test_all_bank_refs_exist(self):
        """测试BIN列表中的银行引用都存在"""
        bank_keys = {bank["key"] for bank in bankinfo.bank_list}

        for bin_info in bankinfo.bank_bin_list:
            assert (
                bin_info["bank"] in bank_keys
            ), f"BIN列表中的银行 {bin_info['bank']} 不存在于银行列表中"

    def test_bin_not_empty(self):
        """测试BIN号不为空"""
        for bin_info in bankinfo.bank_bin_list:
            assert len(bin_info["bin"]) > 0, "BIN号不能为空"

    def test_bank_name_not_empty(self):
        """测试银行名称不为空"""
        for bank in bankinfo.bank_list:
            assert len(bank["name"]) > 0, "银行名称不能为空"

    def test_card_type_valid(self):
        """测试银行卡类型有效"""
        valid_types = {"DC", "CC", "SCC", "PC"}  # 借记卡、信用卡、准贷记卡、预付费卡
        for bin_info in bankinfo.bank_bin_list:
            assert (
                bin_info["type"] in valid_types
            ), f"无效的卡类型: {bin_info['type']}"

    def test_card_length_is_digit(self):
        """测试卡号长度为数字"""
        for bin_info in bankinfo.bank_bin_list:
            assert bin_info["length"].isdigit(), f"卡号长度应该是数字: {bin_info['length']}"

    def test_card_length_positive(self):
        """测试卡号长度为正数"""
        for bin_info in bankinfo.bank_bin_list:
            length = int(bin_info["length"])
            assert length > 0, f"卡号长度应该是正数: {length}"
