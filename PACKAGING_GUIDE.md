# 打包配置指南

## 概述

本文档说明 dbox 项目的打包配置，确保发布时只包含必要的文件，排除测试文件和临时文件。

## 配置文件

### 1. pyproject.toml
- 使用 `[project]` 表定义项目元数据和依赖
- 使用 `[build-system]` 指定 hatchling 作为构建后端
- 通过 `[tool.hatch.build]` 控制打包包含的文件
- 版本号从 `dbox/__init__.py` 自动读取

### 2. .gitignore
- 排除开发工具和临时文件
- 排除构建产物

## 打包前检查清单

### ✅ 确保包含的文件
- [ ] `dbox/` 目录下的所有 Python 文件
- [ ] `README.md`
- [ ] `LICENSE`
- [ ] `pyproject.toml`

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

### 使用 uv (推荐)
```bash
# 清理之前的构建文件
rm -rf build dist dbox.egg-info

# 构建源码和 wheel 分发包
uv build

# 发布到 PyPI
uv publish

# 发布到指定仓库
uv publish --publish-url <仓库地址> --username <用户名> --password <密码>
```

### 使用 pip + build
```bash
# 清理之前的构建文件
rm -rf build dist dbox.egg-info

# 创建源码和 wheel 分发包
python -m build

# 发布到 PyPI
python -m twine upload dist/*
```

## 验证打包结果

1. 检查生成的 tar.gz 文件内容
2. 确保不包含 tests 目录
3. 确保不包含临时文件和构建文件
4. 确保包含所有必要的 dbox 模块

## 常见问题

### Q: tests 目录仍然被包含
A: 确保在 pyproject.toml 中 `[tool.hatch.build.targets.wheel]` 的 `packages` 只包含 `["dbox"]`

### Q: 版本号不对
A: 版本号从 `dbox/__init__.py` 中的 `__version__` 读取，修改后重新构建

### Q: uv publish 需要手动输入账号
A: 在 `~/.pypirc` 中配置好凭证，发布脚本 `release_to_laiye.sh` 会自动读取

## 最佳实践

1. **定期清理**: 打包前清理构建目录
2. **测试验证**: 解压生成的包验证内容
3. **版本管理**: 确保版本号正确
4. **依赖管理**: 确保 `[project.dependencies]` 完整且准确 