#!/usr/bin/env python3
"""
测试脚本 - 验证Windows UI自动化工具的功能
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from operate_ui_simple import *
    print("✅ 成功导入operate_ui_simple模块")
except ImportError as e:
    print(f"❌ 导入失败: {e}")
    sys.exit(1)

def test_basic_functions():
    """测试基本功能"""
    print("\n🔍 测试基本功能...")
    
    # 测试获取进程信息
    print("\n1. 测试获取进程信息:")
    try:
        get_process_info()
        print("✅ 获取进程信息成功")
    except Exception as e:
        print(f"❌ 获取进程信息失败: {e}")
    
    # 测试获取UI元素
    print("\n2. 测试获取UI元素:")
    try:
        elements = get_all_ui_elements()
        print(f"✅ 获取到 {len(elements)} 个UI元素")
        if elements:
            print("   示例元素:")
            for i, elem in enumerate(elements[:3]):  # 只显示前3个
                print(f"   {i+1}. {elem.get('name', 'Unknown')} ({elem.get('role', 'Unknown')})")
    except Exception as e:
        print(f"❌ 获取UI元素失败: {e}")

def test_list_components():
    """测试列出组件功能"""
    print("\n📋 测试列出组件功能...")
    try:
        list_all_components()
        print("✅ 列出组件功能正常")
    except Exception as e:
        print(f"❌ 列出组件功能失败: {e}")

def main():
    """主测试函数"""
    print("🧪 Windows UI自动化工具测试")
    print("=" * 50)
    
    # 检查依赖
    print("📦 检查依赖...")
    try:
        import pyautogui
        print("✅ pyautogui 已安装")
    except ImportError:
        print("❌ pyautogui 未安装")
        return
    
    try:
        import win32gui
        print("✅ pywin32 已安装")
    except ImportError:
        print("❌ pywin32 未安装")
        return
    
    # 运行测试
    test_basic_functions()
    test_list_components()
    
    print("\n🎉 测试完成!")
    print("\n💡 使用提示:")
    print("   1. 先运行: python operate_ui_simple.py processes")
    print("   2. 找到目标进程ID后，运行: python operate_ui_simple.py list")
    print("   3. 找到目标组件名称后，运行: python operate_ui_simple.py <PID> <组件名> <验证组件名>")

if __name__ == "__main__":
    main() 