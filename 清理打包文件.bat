@echo off
setlocal

echo ==============================================
echo     清理PyInstaller打包生成的临时文件
echo ==============================================
echo.

echo 正在清理临时文件...

:: 删除build目录
if exist build (
    echo 删除 build 目录...
    rmdir /s /q build
)

:: 删除spec文件
if exist *.spec (
    echo 删除 spec 文件...
    del /f /q *.spec
)

:: 删除__pycache__目录
echo 删除 __pycache__ 目录...
for /d /r . %%d in (__pycache__) do @if exist "%%d" rmdir /s /q "%%d"

:: 删除.pyc文件
echo 删除 .pyc 文件...
del /s /q *.pyc 2>nul

:: 删除.pyo文件
echo 删除 .pyo 文件...
del /s /q *.pyo 2>nul

echo.
echo 清理完成！
echo.

pause