#!/usr/bin/env python3
"""
测试运行脚本
运行所有测试用例
"""

import pytest
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

if __name__ == "__main__":
    # 运行所有测试
    pytest.main(["--verbose", "--tb=short", "--cov=dbox", "--cov-report=html", "--cov-report=term-missing", "tests/"])
