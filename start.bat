@echo off
setlocal

echo 启动橡胶接头报价工具(开发环境)

:: 检查Python是否安装
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo Python未安装，请先安装Python 3.8或更高版本
    pause
    exit /b 1
)

:: 启动应用程序
python src/main.py
pause