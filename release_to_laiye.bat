@echo off
rmdir /q /s build
rmdir /q /s dist
rmdir /q /s dbox.egg-info
echo "After the last packing record is cleared, press any key to continue packing"
pause

pip install --upgrade setuptools wheel twine
python setup.py sdist bdist_wheel
twine check dist/*
echo "Packaging successful, need to publish to pypi source and LaiYe source. Press any key to continue publishing"
pause

twine upload -r laiye dist/*
twine upload dist/*
echo "Release success"
pause
