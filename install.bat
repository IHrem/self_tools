@echo off
echo 正在安装Qt UI自动化工具的依赖...
echo.

echo 检查Python版本...
python --version
if errorlevel 1 (
    echo 错误: 未找到Python，请先安装Python 3.7+
    pause
    exit /b 1
)

echo.
echo 升级pip...
python -m pip install --upgrade pip

echo.
echo 安装依赖包...
pip install -r requirements.txt

echo.
echo 安装完成！
echo.
echo 使用方法:
echo   列出所有组件: python operate_ui.py list
echo   点击组件: python operate_ui.py ^<进程号pid^> ^<组件名称^> ^<要查找的组件名称^>
echo.
pause 