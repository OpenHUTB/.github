@echo off
setlocal

rem 使用脚本所在目录，支持从其他盘符及含空格的路径启动。
cd /d "%~dp0"
if errorlevel 1 goto failed

set PYTHONUTF8=1

where conda >nul 2>nul

if %errorlevel% neq 0 (
    echo conda is not installed. Please install Anaconda or Miniconda first.
    curl https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe -o .\miniconda.exe
    if errorlevel 1 goto failed
    start /wait "" .\miniconda.exe /S
    if errorlevel 1 goto failed
    del .\miniconda.exe
    echo conda has been installed. Please restart the command prompt and run this script again.
    goto failed
)

echo conda is installed in:
where conda


call conda info --envs | findstr /R /C:"^mkdocs " >nul
if %errorlevel% neq 0 (
    echo mkdocs virtual environment does not exist. Creating
    call conda create -n mkdocs python=3.11 -y
    if errorlevel 1 goto failed
    call conda activate mkdocs
    if errorlevel 1 goto failed
    python -m pip install -r requirements.txt
    if errorlevel 1 goto failed
    python -m pip install git+https://github.com/OpenHUTB/mkdocs.git
    if errorlevel 1 goto failed
    echo mkdocs virtual environment has been created.
)
call conda activate mkdocs
if errorlevel 1 goto failed



set host_ip=127.0.0.1
set "PORT=8000"
set "CHECK_URL=http://%host_ip%:%PORT%"

rem 构建成功后再打开浏览器，失败时保留终端中的错误信息。
python -m mkdocs build
if errorlevel 1 goto failed
start "" "%CHECK_URL%"
python -m mkdocs serve --dev-addr "%host_ip%:%PORT%" --livereload
exit /b %errorlevel%

:failed
echo Preview setup or build failed. Please check the errors above.
exit /b 1
