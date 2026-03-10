#!/bin/bash

# 检查是否有未提交的修改或未跟踪的文件
# if [ -n "$(git status --porcelain)" ]; then
#     echo "❌ 错误：当前存在未提交的修改或未跟踪的文件，请先提交所有变更后再发布！"
#     git status --short
#     exit 1
# fi

# 获取 git commit short ID
commit_id=$(git rev-parse --short HEAD)
echo "当前 commit ID: $commit_id"

# 替换 dbox/__init__.py 中的 __commit_id__ 占位符
sed -i "s/__commit_id__ = \".*\"/__commit_id__ = \"$commit_id\"/" dbox/__init__.py

# 统一使用项目根目录下的 .venv 虚拟环境，不使用宿主机物理环境
PROJECT_VENV=".venv"
if [ ! -x "$PROJECT_VENV/bin/python" ]; then
    echo "❌ 未找到项目虚拟环境：$PROJECT_VENV"
    echo "请先在项目根目录执行：python3 -m venv .venv && source .venv/bin/activate && pip install -U build twine"
    exit 1
fi

PYTHON="$PROJECT_VENV/bin/python"
echo "Using project virtualenv: $PROJECT_VENV"

# 确认虚拟环境中已安装 pip
if ! "$PYTHON" -m pip --version >/dev/null 2>&1; then
    echo "❌ 虚拟环境中未找到 pip。"
    echo "请重新创建虚拟环境并安装依赖，例如："
    echo "  rm -rf .venv"
    echo "  python3 -m venv .venv"
    echo "  source .venv/bin/activate"
    echo "  pip install -U pip build twine"
    exit 1
fi

PIP="$PYTHON -m pip"
TWINE="$PYTHON -m twine"

# 显示版本信息
$PYTHON --version
$PIP --version

# 清理之前的构建文件
rm -rf build dist dbox.egg-info
echo "已清理之前的构建记录，按 Enter 键继续打包..."
read -r

# 安装/升级打包工具（在项目虚拟环境中执行）
$PIP install --upgrade build twine

# 构建源码和 wheel 分发包
$PYTHON -m build

# 检查分发包
$TWINE check dist/*

# 恢复 dbox/__init__.py 文件
git checkout dbox/__init__.py

echo "打包成功，需要发布到 [LaiYe 源]。按 Enter 键继续发布..."
read -r

# 发布到 laiye 源
$TWINE upload -r laiye dist/*
echo "发布成功！"
read -r -p "按 Enter 键退出"
