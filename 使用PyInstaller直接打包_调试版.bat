@echo off
setlocal

echo ==============================================
echo     橡胶接头报价工具打包脚本（调试版）
echo ==============================================
echo.

:: 安装依赖
echo 正在安装依赖...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo 安装依赖失败，请检查网络或requirements.txt文件
    pause
    exit /b 1
)

:: 打包应用程序
echo.
echo 正在打包应用程序...
echo.

python -m PyInstaller --noconfirm --onefile --console --name "橡胶接头报价工具_调试版" ^
  --add-data "assets;assets" ^
  --add-data "data;data" ^
  --hidden-import "tkinter" ^
  --hidden-import "pandas" ^
  --hidden-import "openpyxl" ^
  --hidden-import "reportlab" ^
  --hidden-import "src.ui" ^
  --hidden-import "src.models" ^
  --hidden-import "src.utils" ^
  main.py

if %errorlevel% neq 0 (
    echo 打包失败，请检查错误信息
    pause
    exit /b 1
)

echo.
echo 打包完成！调试版可执行文件位于 dist 目录中
echo.

pause