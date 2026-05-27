#!/bin/bash

# 从 .pypirc 中读取指定 section 的配置值
get_pypirc_value() {
    local section="$1"
    local key="$2"
    local file="$HOME/.pypirc"
    [ ! -f "$file" ] && return 1
    # 找到 [section] 到下一个 [ 之间的区域，提取 key=value
    sed -n "/^\[$section\]/,/^\[/p" "$file" \
        | grep -i "^[[:space:]]*$key[[:space:]]*=" \
        | head -1 \
        | sed 's/^[^=]*=[[:space:]]*//; s/[[:space:]]*$//; s/\r//'
}

# 获取 git commit short ID
commit_id=$(git rev-parse --short HEAD)
echo "当前 commit ID: $commit_id"

# 替换 dbox/__init__.py 中的 __commit_id__ 占位符
sed -i "s/__commit_id__ = \".*\"/__commit_id__ = \"$commit_id\"/" dbox/__init__.py

# 统一使用项目根目录下的 .venv 虚拟环境
PROJECT_VENV=".venv"
if [ ! -f "$PROJECT_VENV/bin/uv" ] && [ ! -x "$PROJECT_VENV/bin/python" ]; then
    echo "❌ 未找到项目虚拟环境：$PROJECT_VENV"
    echo "请先在项目根目录执行：uv venv && uv sync"
    exit 1
fi

echo "Using project virtualenv: $PROJECT_VENV"

# 显示版本信息
$PROJECT_VENV/bin/python --version
uv --version

# 清理之前的构建文件
rm -rf build dist dbox.egg-info
echo "已清理之前的构建记录，按 Enter 键继续打包..."
read -r

# 使用 uv 构建分发包
uv build

# 恢复 dbox/__init__.py 文件
git checkout dbox/__init__.py

echo "打包成功。"
echo "按 Enter 键先发布到 PyPI（https://pypi.org），如不需要可直接 Ctrl+C 退出。"
read -r

# 从 .pypirc 读取 PyPI 凭证
PYPI_USERNAME=$(get_pypirc_value "pypi" "username")
PYPI_PASSWORD=$(get_pypirc_value "pypi" "password")

if [ "$PYPI_USERNAME" = "__token__" ]; then
    uv publish --token "$PYPI_PASSWORD"
else
    uv publish --username "$PYPI_USERNAME" --password "$PYPI_PASSWORD"
fi
if [ $? -ne 0 ]; then
    echo "❌ 发布到 PyPI 失败，终止发布流程。"
    read -r -p "按 Enter 键退出"
    exit 1
fi
echo "✅ 已发布到 PyPI。"

echo "按 Enter 键继续发布到 [LaiYe 源]..."
read -r

# 从 .pypirc 读取 LaiYe 凭证
LAIYE_USERNAME=$(get_pypirc_value "laiye" "username")
LAIYE_PASSWORD=$(get_pypirc_value "laiye" "password")
LAIYE_URL=$(get_pypirc_value "laiye" "repository")

uv publish --publish-url "$LAIYE_URL" --username "$LAIYE_USERNAME" --password "$LAIYE_PASSWORD"
if [ $? -ne 0 ]; then
    echo "❌ 发布到 LaiYe 失败。"
    read -r -p "按 Enter 键退出"
    exit 1
fi
echo "✅ 已发布到 [LaiYe 源]。"
read -r -p "按 Enter 键退出"
