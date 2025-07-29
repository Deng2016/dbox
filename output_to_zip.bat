@echo off

python --version
pip --version


SET packageName=dbox
SET outputFolder=D:\release_to_zip\%packageName%
SET myDomain=www.uibot123.cn
SET pipSource0=http://%myDomain%:1234/
SET pipSource1=https://pypi.tuna.tsinghua.edu.cn/simple
SET zip=C:\Program Files\7-Zip\7z.exe
SET outputZipName=D:\release_to_zip\%packageName%.zip

if exist %outputFolder% (
    rd /q /s %outputFolder%
    echo Deleting an existing Directory: %outputFolder%
)
mkdir %outputFolder%
echo Recreate directory: %outputFolder%

if exist %outputZipName% (
    del %outputZipName%
    echo Delete existing compressed files: %outputZipName%
)

echo Installing the package: %packageName%, from %pipSource1%
pip install -t %outputFolder% -i %pipSource1% %packageName%
echo Installing the package: %packageName%, from %pipSource0%
pip install -t %outputFolder% -U -i %pipSource0% %packageName% --trusted-host %myDomain%
echo Installing the package successfully: %packageName%. Delete redundant packages
pause

rd /q /s %outputFolder%\Crypto
rd /q /s %outputFolder%\requests
rd /q /s %outputFolder%\urllib3
rd /q /s %outputFolder%\redis
for /d %%G in ("%outputFolder%\requests-*dist-info") do rd /q /s "%%~G"
for /d %%G in ("%outputFolder%\urllib3-*dist-info") do rd /q /s "%%~G"
for /d %%G in ("%outputFolder%\pycryptodome-*dist-info") do rd /q /s "%%~G"
for /d %%G in ("%outputFolder%\redis-*dist-info") do rd /q /s "%%~G"


"%zip%" a %outputZipName% "%outputFolder%"\*