import pyautogui
from PIL import Image, ImageDraw
import sys
import time
import subprocess
import re
import ctypes
from ctypes import wintypes
import win32gui
import win32process
import win32con
import win32api


# Windows UI Automation API
try:
    import comtypes.client as cc
    from comtypes.gen import UIAutomationClient as UIA
    UIA_AVAILABLE = True
except ImportError:
    UIA_AVAILABLE = False
    print("警告: 未安装comtypes库，将使用备用方法")


def get_all_ui_elements():
    """获取当前活跃窗口的所有UI元素信息"""
    if UIA_AVAILABLE:
        return get_ui_elements_with_uia()
    else:
        return get_ui_elements_with_win32()


def get_ui_elements_with_uia():
    """使用Windows UI Automation API获取UI元素"""
    try:
        # 初始化UI Automation
        automation = cc.CreateObject("UIAutomationClient.CUIAutomation")
        
        # 获取前台窗口
        foreground_window = win32gui.GetForegroundWindow()
        if not foreground_window:
            print("无法获取前台窗口")
            return []
        
        # 获取窗口的UI Automation元素
        hwnd = wintypes.HWND(foreground_window)
        element = automation.ElementFromHandle(hwnd)
        
        elements = []
        collect_ui_elements(element, elements, automation)
        return elements
        
    except Exception as e:
        print(f"UI Automation API错误: {e}")
        return []


def collect_ui_elements(element, elements_list, automation, depth=0):
    """递归收集UI元素"""
    if depth > 10:  # 限制递归深度
        return
    
    try:
        # 获取元素信息
        name = element.CurrentName or ""
        control_type = element.CurrentControlType
        bounding_rectangle = element.CurrentBoundingRectangle
        
        if name and control_type:
            element_info = {
                'name': name,
                'role': str(control_type),
                'position': (int(bounding_rectangle.left), int(bounding_rectangle.top)),
                'size': (int(bounding_rectangle.right - bounding_rectangle.left), 
                        int(bounding_rectangle.bottom - bounding_rectangle.top))
            }
            elements_list.append(element_info)
        
        # 递归获取子元素
        try:
            children = element.FindAll(UIA.TreeScope.TreeScope_Children, 
                                     automation.CreateTrueCondition())
            for child in children:
                collect_ui_elements(child, elements_list, automation, depth + 1)
        except:
            pass  # 忽略子元素获取错误
            
    except Exception as e:
        pass  # 忽略单个元素的错误


def get_ui_elements_with_win32():
    """使用Win32 API获取UI元素（备用方法）"""
    try:
        # 获取前台窗口
        foreground_window = win32gui.GetForegroundWindow()
        if not foreground_window:
            print("无法获取前台窗口")
            return []
        
        elements = []
        
        # 枚举窗口的所有子控件
        def enum_child_windows(hwnd, lparam):
            try:
                # 获取控件信息
                window_text = win32gui.GetWindowText(hwnd)
                class_name = win32gui.GetClassName(hwnd)
                rect = win32gui.GetWindowRect(hwnd)
                
                if window_text:  # 只添加有文本的控件
                    element_info = {
                        'name': window_text,
                        'role': class_name,
                        'position': (rect[0], rect[1]),
                        'size': (rect[2] - rect[0], rect[3] - rect[1])
                    }
                    elements.append(element_info)
            except:
                pass
            return True
        
        win32gui.EnumChildWindows(foreground_window, enum_child_windows, None)
        return elements
        
    except Exception as e:
        print(f"Win32 API错误: {e}")
        return []


def find_qt_component_by_name(target_name):
    """通过Qt组件名称查找UI元素"""
    ui_elements = get_all_ui_elements()
    return find_component_by_name(ui_elements, target_name)


def find_component_by_name(elements, target_name):
    """在UI元素列表中查找指定名称的组件"""
    for element in elements:
        if element.get('name') == target_name:
            return element
    return None


def list_all_components():
    """列出所有可用的UI组件"""
    elements = get_all_ui_elements()
    print(f"\n找到 {len(elements)} 个UI组件:")
    print("-" * 60)
    for i, element in enumerate(elements, 1):
        name = element.get('name', 'Unknown')
        role = element.get('role', 'Unknown')
        position = element.get('position', (0, 0))
        size = element.get('size', (0, 0))
        print(f"{i:2d}. 名称: {name}")
        print(f"    角色: {role}")
        print(f"    位置: {position}")
        print(f"    尺寸: {size}")
        print()


def click_qt_component(component):
    """点击Qt组件"""
    if not component or 'position' not in component:
        print(f"无法获取组件位置信息")
        return False
    
    x, y = component['position']
    # 获取组件尺寸用于计算中心点
    if 'size' in component:
        width, height = component['size']
        center_x = x + width // 2
        center_y = y + height // 2
    else:
        center_x, center_y = x, y
    
    print(f"找到组件 '{component.get('name', 'Unknown')}' 位置: ({x}, {y}), 中心点: ({center_x}, {center_y})")
    
    # 移动到组件中心并点击
    pyautogui.moveTo(center_x, center_y, duration=0.5)
    pyautogui.click(center_x, center_y)
    time.sleep(0.1)
    pyautogui.click(center_x, center_y)  # 双击
    print(f"已点击组件: {component.get('name', 'Unknown')}")
    
    return True


def find_and_click_qt_component(target_name):
    """查找并点击Qt组件"""
    component = find_qt_component_by_name(target_name)
    if component:
        return click_qt_component(component)
    else:
        print(f"未找到组件: {target_name}")
        return False


def check_component_exists(component_name):
    """检查Qt组件是否存在"""
    component = find_qt_component_by_name(component_name)
    if component:
        print(f"找到了组件: {component_name}")
        return True
    else:
        print(f"未找到组件: {component_name}")
        return False


def bring_app_to_front(pid):
    """通过进程号将对应 app 置顶（前台）"""
    try:
        # 查找指定PID的窗口
        def enum_windows_callback(hwnd, lparam):
            try:
                _, window_pid = win32process.GetWindowThreadProcessId(hwnd)
                if window_pid == pid:
                    # 激活窗口
                    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                    win32gui.SetForegroundWindow(hwnd)
                    return False  # 停止枚举
            except:
                pass
            return True
        
        win32gui.EnumWindows(enum_windows_callback, None)
        print(f"已将进程 {pid} 的窗口置顶")
        
    except Exception as e:
        print(f"置顶进程 {pid} 失败: {e}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法:")
        print("  列出所有组件: python operate_ui.py list")
        print("  点击组件: python operate_ui.py <进程号pid> <组件名称> <要查找的组件名称>")
        sys.exit(1)
    
    if sys.argv[1] == "list":
        # 列出所有可用的UI组件
        list_all_components()
    elif len(sys.argv) == 4:
        pid = int(sys.argv[1])
        component_name = sys.argv[2]
        check_component = sys.argv[3]
        
        bring_app_to_front(pid)
        time.sleep(3)  # 给系统反应时间
        find_and_click_qt_component(component_name)
        check_component_exists(check_component)
    else:
        print("用法:")
        print("  列出所有组件: python operate_ui.py list")
        print("  点击组件: python operate_ui.py <进程号pid> <组件名称> <要查找的组件名称>")
        sys.exit(1) 