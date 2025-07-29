# DBox - 个人常用工具类封装

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-2025.8.1.1-orange.svg)](https://pypi.org/project/dbox/)

DBox 是一个功能丰富的 Python 工具类库，封装了日常开发中常用的功能模块，包括文件操作、网络请求、数据库操作、加密解密、Git 操作、缓存管理等。

## 🚀 主要功能

### 📁 文件操作 (`file.py`)
- 文件路径检查和验证
- 文件压缩和解压 (ZIP, TGZ)
- 文件复制、移动、删除
- 目录遍历和文件搜索
- 文件内容读取和写入

### 🌐 网络工具 (`net.py`, `my_http.py`)
- HTTP 请求封装
- 网络连接检测
- 文件下载功能
- URL 解析和处理
- 网络流量转换工具

### 🔐 加密安全 (`encrypt.py`)
- MD5/SHA256 哈希计算
- AES 加密解密
- RSA 加密解密
- JWT Token 处理
- 文件完整性校验

### 💾 数据存储 (`cache.py`, `db_oper.py`)
- Redis 缓存操作
- MySQL 数据库连接池
- 数据库统计和比较
- 缓存数据管理

### 🔧 Git 操作 (`git.py`, `github.py`, `gitea.py`)
- Git 仓库管理
- GitHub API 集成
- Gitea API 集成
- 分支和标签操作
- Release 管理

### 📊 测试数据 (`testdata.py`)
- 随机数据生成
- 身份证号码生成和校验
- 银行卡号生成
- 手机号码生成
- 中文姓名生成

### 🖥️ 系统工具 (`windows.py`)
- Windows 系统信息获取
- 进程管理
- 网络配置
- 管理员权限检查

### 📡 消息通知 (`feishu.py`, `message.py`)
- 飞书消息推送
- 企业微信消息发送
- 消息格式化

### ⏰ 时间工具 (`time.py`)
- 时间格式转换
- 时间戳处理
- 日期计算

### 📂 文件共享 (`samba.py`)
- Samba 文件服务器连接
- 文件上传下载
- 目录创建和管理

### 🔄 工作流 (`flow.py`)
- 流程文件管理
- 版本控制
- 流程信息更新

## 📦 安装

### 从 PyPI 安装
```bash
pip install dbox
```

### 从 GitHub 安装最新版本
```bash
pip install git+https://github.com/Deng2016/dbox@master
```

### 开发模式安装
```bash
git clone https://github.com/Deng2016/dbox.git
cd dbox
pip install -e .
```

## 🔧 环境要求

- Python 3.7+
- 依赖包：
  - requests >= 2.26.0
  - redis == 3.5.3
  - pycryptodome == 3.11.0
  - xpinyin == 0.7.6
  - pysmb == 1.2.10
  - pyjwt == 2.8.0
  - pytz >= 2025.2

## 📖 使用示例

### 基本使用
```python
from dbox import logger, configure_logger

# 配置日志
configure_logger(level=logging.INFO, log_file="app.log")

# 使用日志
logger.info("Hello DBox!")
```

### 文件操作
```python
from dbox import file

# 检查文件是否存在
file.check_path_is_exits("path/to/file.txt")

# 压缩文件
file.compress_zip("source_dir", "output.zip")
```

### 网络请求
```python
from dbox import my_http
import requests

response = requests.get("https://api.example.com/data")
my_http.check_response(response, "获取数据")
```

### 加密解密
```python
from dbox import encrypt

# MD5 计算
md5_hash = encrypt.md5sum(_string="Hello World")

# AES 加密
crypto = encrypt.MyCrypto()
encrypted = crypto.encrypt("Hello World", "secret_key")
```

### 缓存操作
```python
from dbox import cache

# 获取 Redis 连接
redis_handler = cache.get_redis_handler()

# 设置缓存
redis_handler.set("key", "value", ex=3600)
```

### Git 操作
```python
from dbox import git

# 拉取代码
git.pull_repo("path/to/repo", branch="main")

# 推送代码
git.push_local_update("path/to/repo", "commit message")
```

### 测试数据生成
```python
from dbox import testdata

# 生成随机日期
random_date = testdata.get_random_data("2023-01-01", "2023-12-31")

# 生成身份证号
id_card = testdata.get_idcards(sex=1)  # 1=男性

# 生成银行卡号
bank_card = testdata.get_bank_no(num=1, bank="ICBC")
```

## 🔧 配置

### 环境变量配置

某些功能需要配置环境变量：

```bash
# Redis 配置
export REDIS_DB_CONNECT='{"host":"localhost","port":6379,"db":0}'

# Git 配置
export GIT_CI_API_URL="https://api.github.com"
export GIT_CI_TOKEN="your_github_token"

# Samba 配置
export COM_SAMBA='{"username":"user","password":"pass","host":"192.168.1.100"}'
```

## 📝 更新历史

### 2025.8.1.1
- 项目重命名：从 `deng` 改为 `dbox`
- 修复所有类型注解问题
- 优化代码结构和错误处理
- 更新依赖包版本

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 👨‍💻 作者

- **dqy** - *初始工作* - [Deng2016](https://github.com/Deng2016)
- 邮箱：yu12377@163.com

## 🙏 致谢

感谢所有为这个项目做出贡献的开发者！

---

⭐ 如果这个项目对您有帮助，请给它一个星标！
