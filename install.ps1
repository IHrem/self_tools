# Qt UI自动化工具安装脚本
Write-Host "正在安装Qt UI自动化工具的依赖..." -ForegroundColor Green
Write-Host ""

# 检查Python版本
Write-Host "检查Python版本..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "找到Python: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "错误: 未找到Python，请先安装Python 3.7+" -ForegroundColor Red
    Read-Host "按任意键退出"
    exit 1
}

Write-Host ""
Write-Host "升级pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip

Write-Host ""
Write-Host "安装依赖包..." -ForegroundColor Yellow
pip install -r requirements.txt

Write-Host ""
Write-Host "安装完成！" -ForegroundColor Green
Write-Host ""
Write-Host "使用方法:" -ForegroundColor Cyan
Write-Host "  列出所有组件: python operate_ui.py list"
Write-Host "  点击组件: python operate_ui.py <进程号pid> <组件名称> <要查找的组件名称>"
Write-Host ""
Write-Host "获取进程ID的方法:" -ForegroundColor Cyan
Write-Host "  tasklist | findstr '应用程序名称'"
Write-Host "  或使用PowerShell: Get-Process | Where-Object {`$_.ProcessName -like '*应用程序名称*'}"
Write-Host ""
Read-Host "按任意键退出" 