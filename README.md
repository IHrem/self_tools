# Qt UI 自动化工具 (Windows版)

这是一个用于自动化操作Qt应用程序UI组件的工具，通过解析Qt组件的名称来进行点击操作，而不是使用OCR识别。专为Windows系统设计。

## 功能特点

- 通过Qt组件名称查找和点击UI元素
- 支持列出所有可用的UI组件
- 自动将目标应用程序置顶
- 精确的鼠标点击操作
- 支持Windows系统
- 使用Win32 API，稳定可靠

## 安装依赖

```bash
pip install -r requirements.txt
```

或者使用安装脚本：

```bash
# 使用批处理脚本
install.bat

# 使用PowerShell脚本
.\install.ps1
```

## 系统要求

- Windows 10/11
- Python 3.7+
- 目标应用程序必须支持Win32 API

## 使用方法

### 推荐使用简化版本

我们提供了两个版本：
- `operate_ui.py` - 完整版本（包含UI Automation API）
- `operate_ui_simple.py` - 简化版本（仅使用Win32 API，推荐）

### 1. 列出进程信息

首先查看当前运行的应用程序进程：

```bash
python operate_ui_simple.py processes
```

### 2. 列出所有UI组件

确保目标Qt应用程序在前台运行，然后执行：

```bash
python operate_ui_simple.py list
```

这将显示当前活跃窗口中的所有UI组件，包括：
- 组件名称
- 组件角色（按钮、文本框等）
- 组件位置坐标
- 组件尺寸

### 3. 点击指定组件

```bash
python operate_ui_simple.py <进程号pid> <组件名称> <要查找的组件名称>
```

参数说明：
- `进程号pid`: 目标Qt应用程序的进程ID
- `组件名称`: 要点击的组件名称
- `要查找的组件名称`: 用于验证的组件名称

### 示例

```bash
# 列出进程信息
python operate_ui_simple.py processes

# 列出所有组件
python operate_ui_simple.py list

# 点击名为"确定"的按钮
python operate_ui_simple.py 12345 "确定" "确定"
```

## 测试工具

运行测试脚本来验证安装和功能：

```bash
python test_simple.py
```

## 工作原理

1. **获取UI元素信息**: 使用Win32 API获取当前活跃窗口的所有UI元素信息
2. **解析组件数据**: 解析返回的组件名称、角色、位置和尺寸信息
3. **查找目标组件**: 根据组件名称查找匹配的UI元素
4. **执行点击操作**: 计算组件中心点并执行鼠标点击

## 注意事项

- 仅支持Windows系统
- 目标应用程序必须支持Win32 API
- 组件名称必须完全匹配
- 建议先使用`processes`命令查看进程ID
- 建议先使用`list`命令查看可用的组件名称
- 某些应用程序可能需要以管理员权限运行

## 依赖库

- `pyautogui`: 鼠标和键盘自动化操作
- `pywin32`: Windows API接口

## 故障排除

### 常见错误及解决方案

1. **ImportError: No module named 'win32gui'**
   ```bash
   pip install pywin32
   ```

2. **ImportError: No module named 'pyautogui'**
   ```bash
   pip install pyautogui
   ```

3. **无法获取UI元素**
   - 确保目标应用程序在前台且支持Win32 API
   - 尝试以管理员权限运行脚本
   - 检查应用程序是否被安全软件阻止

4. **找不到组件**
   - 使用`list`命令确认组件名称是否正确
   - 检查应用程序是否使用了自定义控件
   - 确保应用程序窗口处于活跃状态

5. **点击位置不准确**
   - 检查应用程序是否有缩放或高DPI设置
   - 确保屏幕分辨率设置正确
   - 尝试调整pyautogui的坐标系统

6. **权限问题**
   - 以管理员权限运行命令提示符
   - 检查Windows Defender或其他安全软件的设置
   - 确保Python有足够的系统权限

### 调试步骤

1. **运行测试脚本**
   ```bash
   python test_simple.py
   ```

2. **检查进程信息**
   ```bash
   python operate_ui_simple.py processes
   ```

3. **检查UI组件**
   ```bash
   python operate_ui_simple.py list
   ```

4. **手动测试点击**
   ```bash
   python operate_ui_simple.py <PID> <组件名> <验证组件名>
   ```

## 获取进程ID

可以使用以下命令获取目标应用程序的进程ID：

```bash
# 使用tasklist命令
tasklist | findstr "应用程序名称"

# 或使用PowerShell
Get-Process | Where-Object {$_.ProcessName -like "*应用程序名称*"}

# 或使用我们的工具
python operate_ui_simple.py processes
```

## 版本说明

- **v1.0**: 初始版本，支持基本的UI组件查找和点击
- **v1.1**: 添加了简化版本，提高稳定性
- **v1.2**: 添加了测试脚本和详细的故障排除指南 