@echo off
echo Running dbox unit tests...
echo.

REM 检查是否安装了pytest
python -c "import pytest" 2>nul
if errorlevel 1 (
    echo Installing test dependencies...
    pip install -r requirements-test.txt
)

echo.
echo Running tests with coverage...
python -m pytest tests/ -v --cov=dbox --cov-report=html --cov-report=term-missing

echo.
echo Tests completed. Coverage report generated in htmlcov/ directory.
pause 