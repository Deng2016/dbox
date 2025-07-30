# dbox 单元测试

本项目包含全面的单元测试用例，覆盖了所有主要模块的功能。

## 测试结构

```
tests/
├── __init__.py              # 测试包初始化
├── conftest.py              # pytest配置和通用fixtures
├── test_utils.py            # 工具函数测试
├── test_file.py             # 文件操作测试
├── test_cache.py            # 缓存功能测试
├── test_time.py             # 时间处理测试
├── test_testdata.py         # 测试数据生成测试
├── test_my_http.py          # HTTP请求测试
├── test_db_oper.py          # 数据库操作测试
├── test_encrypt.py          # 加密功能测试
├── test_net.py              # 网络功能测试
├── test_samba.py            # Samba操作测试
├── test_flow.py             # 流程控制测试
├── test_git.py              # Git操作测试
├── test_message.py          # 消息发送测试
└── test_all.py              # 测试运行脚本
```

## 运行测试

### Windows
```bash
run_tests.bat
```

### Linux/Mac
```bash
chmod +x run_tests.sh
./run_tests.sh
```

### 手动运行
```bash
# 安装测试依赖
pip install -r requirements-test.txt

# 运行所有测试
python -m pytest tests/ -v

# 运行带覆盖率报告的测试
python -m pytest tests/ -v --cov=dbox --cov-report=html --cov-report=term-missing

# 运行特定测试文件
python -m pytest tests/test_utils.py -v

# 运行特定测试类
python -m pytest tests/test_utils.py::TestUtils -v

# 运行特定测试方法
python -m pytest tests/test_utils.py::TestUtils::test_pop_key_from_dict -v
```

## 测试覆盖范围

### 已测试的模块

1. **utils.py** - 工具函数
   - 字典操作函数
   - 命令执行函数
   - JSON处理函数
   - 字符串转换函数
   - 布尔值转换函数
   - 输入处理函数
   - 性能统计装饰器
   - 数字补齐函数
   - 调用者信息函数
   - Excel列名转换函数

2. **file.py** - 文件操作
   - 路径检查函数
   - 目录操作函数
   - 文件压缩/解压函数
   - 文件删除函数
   - 文件移动/复制函数
   - 文件内容读取函数
   - 文件保存函数
   - 文件时间获取函数
   - 文件比较函数

3. **cache.py** - 缓存功能
   - Redis连接管理
   - 缓存对象获取
   - 批量删除操作
   - JSON数据处理
   - 文件缓存操作
   - 哈希操作

4. **time.py** - 时间处理
   - 时间戳生成
   - 时间格式化
   - 时间转换函数
   - 时间比较函数

5. **testdata.py** - 测试数据生成
   - 随机数据生成
   - 随机字符串生成
   - UUID生成
   - 拼音转换
   - 姓名生成
   - 身份证号生成
   - 手机号生成
   - 银行卡号生成

6. **my_http.py** - HTTP请求
   - GET/POST/PUT/DELETE请求
   - JSON数据处理
   - 请求头处理
   - 超时处理
   - 错误处理

7. **db_oper.py** - 数据库操作
   - 数据库连接
   - SQL执行
   - 参数化查询
   - 事务处理
   - 错误处理

8. **encrypt.py** - 加密功能
   - MD5/SHA1/SHA256/SHA512哈希
   - Base64编码/解码
   - URL编码/解码
   - 自定义加密类

9. **net.py** - 网络功能
   - 主机名获取
   - IP地址获取
   - MAC地址获取
   - 网络连通性测试
   - 端口检查

10. **samba.py** - Samba操作
    - Samba连接
    - 文件上传/下载
    - 文件列表获取
    - 文件删除
    - 目录操作

11. **flow.py** - 流程控制
    - 流程创建
    - 流程执行
    - 流程验证
    - 流程状态管理
    - 流程日志

12. **git.py** - Git操作
    - 仓库克隆
    - 代码拉取/推送
    - 分支操作
    - 提交操作
    - 状态查看

13. **message.py** - 消息发送
    - 邮件发送
    - 短信发送
    - 微信消息
    - 钉钉消息
    - 飞书消息
    - Slack消息
    - Telegram消息

## 测试特点

### 1. 全面覆盖
- 覆盖所有主要函数和方法
- 包含正常流程和异常流程
- 测试边界条件和错误情况

### 2. 模拟外部依赖
- 使用 `unittest.mock` 模拟外部服务
- 避免对真实网络/数据库的依赖
- 确保测试的独立性和可重复性

### 3. 参数化测试
- 测试多种输入参数组合
- 验证不同场景下的行为
- 确保函数的健壮性

### 4. 错误处理测试
- 测试异常情况的处理
- 验证错误信息的准确性
- 确保系统的稳定性

### 5. 性能测试
- 测试大数据量处理
- 验证内存使用情况
- 确保性能符合要求

## 测试配置

### pytest.ini
- 配置测试路径和文件模式
- 设置测试标记
- 配置覆盖率报告

### conftest.py
- 定义通用测试fixtures
- 配置测试环境
- 提供模拟对象

### requirements-test.txt
- 测试依赖包列表
- 确保测试环境的一致性

## 覆盖率报告

运行测试后会在 `htmlcov/` 目录生成详细的覆盖率报告，包括：

- 总体覆盖率统计
- 每个文件的覆盖率详情
- 未覆盖代码行的标识
- 分支覆盖率分析

## 持续集成

测试脚本支持在CI/CD环境中运行：

```yaml
# GitHub Actions示例
- name: Run tests
  run: |
    pip install -r requirements-test.txt
    python -m pytest tests/ --cov=dbox --cov-report=xml
```

## 注意事项

1. **依赖安装**: 运行测试前需要安装测试依赖
2. **环境隔离**: 建议在虚拟环境中运行测试
3. **模拟对象**: 测试使用模拟对象，不会影响真实系统
4. **覆盖率目标**: 目标覆盖率80%以上
5. **测试维护**: 新增功能时需要添加相应的测试用例

## 故障排除

### 常见问题

1. **ImportError**: 检查是否正确安装了依赖包
2. **MockError**: 检查模拟对象的配置是否正确
3. **AssertionError**: 检查测试用例的预期结果是否正确
4. **TimeoutError**: 检查网络相关测试的超时设置

### 调试技巧

1. 使用 `-s` 参数查看print输出
2. 使用 `--pdb` 参数进入调试模式
3. 使用 `-x` 参数在第一个失败时停止
4. 使用 `--lf` 参数只运行上次失败的测试 