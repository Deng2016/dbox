#!/bin/bash

echo "Running dbox unit tests..."
echo

# 检查是否安装了pytest
if ! python -c "import pytest" 2>/dev/null; then
    echo "Installing test dependencies..."
    pip install -r requirements-test.txt
fi

echo
echo "Running tests with coverage..."
python -m pytest tests/ -v --cov=dbox --cov-report=html --cov-report=term-missing

echo
echo "Tests completed. Coverage report generated in htmlcov/ directory." 