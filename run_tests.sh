#!/bin/bash

echo "Running dbox unit tests..."
echo

# 检查虚拟环境中是否已安装依赖
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment and installing dependencies..."
    uv venv && uv sync --group test
fi

echo
echo "Running tests with coverage..."
uv run pytest tests/ -v --cov=dbox --cov-report=html --cov-report=term-missing

echo
echo "Tests completed. Coverage report generated in htmlcov/ directory."
