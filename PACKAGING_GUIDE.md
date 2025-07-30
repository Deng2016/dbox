# 打包配置指南

## 概述

本文档说明 dbox 项目的打包配置，确保发布时只包含必要的文件，排除测试文件和临时文件。

## 配置文件

### 1. setup.py
- 使用 `find_packages(exclude=["tests", "tests.*"])` 排除测试包
- 在 `exclude_package_data` 中排除不必要的文件

### 2. MANIFEST.in
- 明确指定包含和排除的文件
- 使用 `global-exclude` 排除整个目录
- 使用 `exclude` 排除特定文件

### 3. .gitignore
- 排除开发工具和临时文件
- 排除构建产物

## 打包前检查清单

### ✅ 确保包含的文件
- [ ] `dbox/` 目录下的所有 Python 文件
- [ ] `README.md`
- [ ] `LICENSE`
- [ ] `pyproject.toml`
- [ ] `setup.py`

### ❌ 确保排除的文件和目录
- [ ] `tests/` 目录
- [ ] `build/` 目录
- [ ] `dist/` 目录
- [ ] `*.egg-info/` 目录
- [ ] `.pytest_cache/` 目录
- [ ] `.git/` 目录
- [ ] `.vscode/` 目录
- [ ] `.idea/` 目录
- [ ] `*.log` 文件
- [ ] `*.out` 文件
- [ ] `*.zip` 文件
- [ ] `*.bat` 文件
- [ ] `pytest.ini`
- [ ] `README_TESTS.md`
- [ ] `lab.py`
- [ ] `*.pyc` 文件
- [ ] `__pycache__/` 目录

## 打包命令

```bash
# 清理之前的构建文件
rmdir /s /q build dist dbox.egg-info

# 创建源码分发包
python setup.py sdist

# 创建轮子包
python setup.py bdist_wheel
```

## 验证打包结果

1. 检查生成的 tar.gz 文件内容
2. 确保不包含 tests 目录
3. 确保不包含临时文件和构建文件
4. 确保包含所有必要的 dbox 模块

## 常见问题

### Q: tests 目录仍然被包含
A: 确保在 setup.py 中使用 `exclude=["tests", "tests.*"]`，并删除 tests 目录中的 `__init__.py` 文件

### Q: 构建文件被包含
A: 在 MANIFEST.in 中使用 `global-exclude` 排除整个目录

### Q: 临时文件被包含
A: 在 .gitignore 中正确配置，并在 MANIFEST.in 中明确排除

## 最佳实践

1. **定期清理**: 打包前清理构建目录
2. **测试验证**: 解压生成的包验证内容
3. **版本管理**: 确保版本号正确
4. **依赖管理**: 确保 install_requires 完整且准确 