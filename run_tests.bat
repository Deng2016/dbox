@echo off
echo Running dbox unit tests...
echo.

if not exist ".venv" (
    echo Creating virtual environment and installing dependencies...
    uv venv && uv sync --group test
)

echo.
echo Running tests with coverage...
uv run pytest tests/ -v --cov=dbox --cov-report=html --cov-report=term-missing

echo.
echo Tests completed. Coverage report generated in htmlcov/ directory.
pause
