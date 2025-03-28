@echo off
setlocal enabledelayedexpansion

echo ==============================================
echo     橡胶接头报价工具一键打包发布脚本
echo ==============================================
echo.

:: 设置变量
set APP_NAME=橡胶接头报价工具
set ZIP_NAME=橡胶接头报价工具
set VERSION=5.0

:: 安装依赖
echo 正在安装依赖...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo 安装依赖失败，请检查网络或requirements.txt文件
    pause
    exit /b 1
)

:: 清理之前的打包文件
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist "*.spec" del /f /q *.spec

:: 打包应用程序
echo.
echo 正在打包应用程序...
echo.

python -m PyInstaller --noconfirm --onefile --windowed --name "%APP_NAME%" ^
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

:: 创建启动脚本
echo 创建启动脚本...
(
echo @echo off
echo setlocal
echo.
echo start "" "%APP_NAME%.exe"
) > dist\启动报价工具.bat

:: 创建使用说明
echo 创建使用说明文件...
(
echo 橡胶接头报价工具 V%VERSION% 使用说明
echo.
echo 一、系统要求
echo -----------
echo Windows 7/8/10/11 操作系统
echo.
echo 二、启动方法
echo -----------
echo 1. 双击"启动报价工具.bat"即可启动应用程序
echo 2. 或直接双击"%APP_NAME%.exe"
echo.
echo 三、使用方法
echo -----------
echo 1. 数据导入：使用"数据导入"选项卡导入球体和法兰数据
echo 2. 报价计算：在"快速报价"选项卡中选择配件并计算价格
echo 3. 导出报价：使用"导出报价单"选项卡导出PDF或Excel格式的报价单
echo 4. 设置：在"设置"选项卡中配置公司信息等
echo.
echo 四、注意事项
echo -----------
echo 1. 首次使用时，建议先在"设置"中配置好公司信息
echo 2. 可通过导入示例数据快速熟悉系统功能
echo 3. 如有任何问题，请联系技术支持
) > dist\使用说明.txt

:: 创建ZIP包
echo 创建发布包...
cd dist
if exist "%ZIP_NAME%.zip" del /f /q "%ZIP_NAME%.zip"
powershell Compress-Archive -Path * -DestinationPath "%ZIP_NAME%.zip"
cd ..

echo.
echo 打包完成！发布文件位于 dist 目录中
echo - 可执行文件: dist\%APP_NAME%.exe
echo - 发布压缩包: dist\%ZIP_NAME%.zip
echo.

pause