#!/usr/bin/env python
# coding:utf-8
"""将个人封装的公共方法打包"""
from setuptools import setup, find_packages
from dbox import __version__


PACKAGE_NAME = "dbox"
PACKAGE_VERSION = __version__

setup(
    name=PACKAGE_NAME,
    version=PACKAGE_VERSION,
    description="Personal method encapsulation",
    url="https://github.com/Deng2016/dbox",
    author="dqy",
    author_email="yu12377@163.com",
    license="MIT",
    # 避免生成 Core Metadata 的 License-File 字段（部分 twine/packaging 环境会误报不识别）
    license_files=[],
    packages=find_packages(exclude=["tests", "tests.*"]),
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    package_data={
        "dbox": ["*.py"],
    },
    python_requires=">=3.12",
    install_requires=[
        "requests~=2.32.5",
        "redis~=7.3.0",
        "pycryptodome~=3.23.0",
        "xpinyin~=0.7.7",
        "pysmb~=1.2.13",
        "pyjwt~=2.11.0",
        "pytz~=2026.1.post1",
    ],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: Implementation",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
        "Topic :: Software Development :: Libraries",
    ],
)
