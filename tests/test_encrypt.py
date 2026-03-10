import pytest
import os
import tempfile
import jwt
from unittest.mock import patch, MagicMock
from dbox.encrypt import (
    to_encode,
    to_decode,
    sum_md5,
    md5sum,
    md5_file,
    md5_str,
    jwt_decode,
    MyCrypto,
)


class TestEncrypt:
    """测试加密模块"""

    def test_to_encode(self):
        """测试base64编码"""
        result = to_encode("hello world")
        assert isinstance(result, str)
        assert result == "aGVsbG8gd29ybGQ="

    def test_to_decode(self):
        """测试base64解码"""
        result = to_decode("aGVsbG8gd29ybGQ=")
        assert isinstance(result, str)
        assert result == "hello world"

    def test_to_encode_decode_roundtrip(self):
        """测试base64编码解码往返"""
        original = "test string 123!@#"
        encoded = to_encode(original)
        decoded = to_decode(encoded)
        assert decoded == original

    def test_sum_md5_string(self):
        """测试字符串MD5"""
        result = sum_md5("hello")
        assert isinstance(result, str)
        assert len(result) == 32

    def test_sum_md5_integer(self):
        """测试整数MD5"""
        result = sum_md5(12345)
        assert isinstance(result, str)
        assert len(result) == 32

    def test_sum_md5_consistent(self):
        """测试MD5一致性"""
        result1 = sum_md5("test")
        result2 = sum_md5("test")
        assert result1 == result2

    def test_md5_str(self):
        """测试字符串MD5函数"""
        result = md5_str("hello world")
        assert isinstance(result, str)
        assert len(result) == 32

    def test_md5_str_consistent(self):
        """测试字符串MD5一致性"""
        result1 = md5_str("test string")
        result2 = md5_str("test string")
        assert result1 == result2

    def test_md5_file(self):
        """测试文件MD5"""
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
            f.write("test content")
            temp_path = f.name

        try:
            result = md5_file(temp_path)
            assert isinstance(result, str)
            assert len(result) == 32
        finally:
            os.unlink(temp_path)

    def test_md5sum_with_string(self):
        """测试md5sum字符串模式"""
        result = md5sum(_string="test")
        assert isinstance(result, str)
        assert len(result) == 32

    def test_md5sum_with_file(self):
        """测试md5sum文件模式"""
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
            f.write("test file content")
            temp_path = f.name

        try:
            result = md5sum(_file_path=temp_path)
            assert isinstance(result, str)
            assert len(result) == 32
        finally:
            os.unlink(temp_path)

    def test_md5sum_no_params(self):
        """测试md5sum无参数时抛出异常"""
        with pytest.raises(ValueError):
            md5sum()

    def test_jwt_decode(self):
        """测试JWT解码"""
        # 创建一个测试JWT token
        payload = {"user": "test", "exp": 9999999999}
        token = jwt.encode(payload, "secret", algorithm="HS256")

        result = jwt_decode(token)
        assert isinstance(result, dict)
        assert result["user"] == "test"

    def test_jwt_decode_with_options(self):
        """测试JWT解码带选项"""
        payload = {"user": "test"}
        token = jwt.encode(payload, "secret", algorithm="HS256")

        result = jwt_decode(
            token, verify_signature=False, verify_exp=False, verify_aud=False
        )
        assert isinstance(result, dict)
        assert result["user"] == "test"


class TestMyCrypto:
    """测试MyCrypto加密类"""

    def test_sha256(self):
        """测试SHA256哈希"""
        result = MyCrypto.sha256("test data")
        assert isinstance(result, str)
        assert len(result) == 64

    def test_sha256_consistent(self):
        """测试SHA256一致性"""
        result1 = MyCrypto.sha256("test")
        result2 = MyCrypto.sha256("test")
        assert result1 == result2

    def test_encrypt_decrypt_with_xsrf_token(self):
        """测试使用xsrf_token的加密解密往返"""
        data = "secret message"
        token = "test_token_123"

        encrypted = MyCrypto.encrypt(data, xsrf_token=token)
        assert isinstance(encrypted, str)
        assert encrypted != data

        decrypted = MyCrypto.decrypt(encrypted, xsrf_token=token)
        assert decrypted == data

    def test_encrypt_decrypt_with_old_secret(self):
        """测试使用old_secret的加密解密往返"""
        data = "another secret message"
        secret = "my_secret_key_that_is_32_bytes_long"

        encrypted = MyCrypto.encrypt(data, old_secret=secret)
        assert isinstance(encrypted, str)
        assert encrypted != data

        decrypted = MyCrypto.decrypt(encrypted, old_secret=secret)
        assert decrypted == data

    def test_encrypt_no_key(self):
        """测试加密时没有key抛出异常"""
        with pytest.raises(ValueError, match="key cannot be None"):
            MyCrypto.encrypt("data")

    def test_decrypt_no_key(self):
        """测试解密时没有key抛出异常"""
        with pytest.raises(ValueError, match="key cannot be None"):
            MyCrypto.decrypt("encrypted_data")

    def test_encrypt_short_secret(self):
        """测试短密钥的加密解密"""
        data = "test data"
        short_secret = "short"  # 少于32字符

        encrypted = MyCrypto.encrypt(data, old_secret=short_secret)
        decrypted = MyCrypto.decrypt(encrypted, old_secret=short_secret)
        assert decrypted == data

    def test_encrypt_long_secret(self):
        """测试长密钥的加密解密"""
        data = "test data"
        long_secret = "a" * 50  # 超过32字符

        encrypted = MyCrypto.encrypt(data, old_secret=long_secret)
        decrypted = MyCrypto.decrypt(encrypted, old_secret=long_secret)
        assert decrypted == data

    def test_aes_cbc_encrypt_decrypt(self):
        """测试AES CBC加密解密"""
        key = "0123456789abcdef0123456789abcdef"  # 32字节
        iv = "0123456789abcdef"  # 16字节
        content = "test AES CBC content"

        encrypted = MyCrypto.aes_cbc_encrypt(key, content, iv)
        assert isinstance(encrypted, str)
        assert encrypted != content

        decrypted = MyCrypto.aes_cbc_decrypt(key, encrypted, iv)
        assert decrypted == content

    def test_rsa_encrypt_decrypt(self):
        """测试RSA加密解密"""
        # 生成RSA密钥对用于测试
        from Crypto.PublicKey import RSA

        key = RSA.generate(2048)
        private_key = key.export_key().decode("utf-8")
        public_key = key.publickey().export_key().decode("utf-8")

        # 提取PEM格式中的关键部分（去掉头部和尾部）
        pub_key_content = "\n".join(public_key.split("\n")[1:-1])
        priv_key_content = "\n".join(private_key.split("\n")[1:-1])

        data = "secret RSA message"

        encrypted = MyCrypto.rsa_encrypt(pub_key_content, data)
        assert isinstance(encrypted, str)
        assert encrypted != data

        decrypted = MyCrypto.rsa_decrypt(priv_key_content, encrypted)
        assert decrypted == data
