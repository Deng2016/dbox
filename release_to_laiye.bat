@echo off
setlocal

chcp 65001


for /f "tokens=*" %%i in ('git rev-parse --short HEAD') do set commit_id=%%i
if "%commit_id%"=="" (
    echo ERROR: Failed to get commit ID
    pause
    exit /b 1
)
echo Current commit ID: %commit_id%

python -c "import re; content = open('dbox/__init__.py', 'r', encoding='utf-8').read(); new_content = re.sub(r'__commit_id__ = \".*\"', f'__commit_id__ = \"%commit_id%\"', content); open('dbox/__init__.py', 'w', encoding='utf-8').write(new_content); print(f'Updated __commit_id__ to: %commit_id%')"

echo Verifying the update...
findstr "__commit_id__" dbox/__init__.py

python --version
pip --version

rd /q /s build
rd /q /s dist
rd /q /s dbox.egg-info
echo "After the last packing record is cleared, press any key to continue packing"
pause

pip install --upgrade setuptools wheel twine
python setup.py sdist bdist_wheel
twine check dist/*
git checkout dbox/__init__.py

echo "Packaging successful, need to publish to [LaiYe source]. Press any key to continue publishing"
pause

twine upload dist/*
twine upload -r laiye dist/*
echo "Release success"
pause

endlocal
