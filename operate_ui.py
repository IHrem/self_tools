import pyautogui
import pytesseract
from PIL import Image, ImageDraw
import sys
import time


def find_and_click_text(target_text):
    """在屏幕上查找所有与目标文字完全匹配的区域，全部左键点击两次并画红框和黄色大圆点标记点击位置，保存截图。鼠标先移动到截图坐标的黄色点，再换算后点击。"""
    screenshot = pyautogui.screenshot()
    data = pytesseract.image_to_data(screenshot, lang='chi_sim+eng', output_type=pytesseract.Output.DICT)
    draw = ImageDraw.Draw(screenshot)
    found = False
    # 计算缩放比例
    screen_w, screen_h = pyautogui.size()
    img_w, img_h = screenshot.size
    scale_x = screen_w / img_w
    scale_y = screen_h / img_h
    for i, text in enumerate(data['text']):
        if text.strip() == target_text:
            x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
            draw.rectangle([x, y, x + w, y + h], outline='red', width=2)
            center_x = x + w // 2
            center_y = y + h // 2
            # 画点击点
            draw.ellipse([center_x-8, center_y-8, center_x+8, center_y+8], fill='yellow', outline='red', width=2)
            # 计算实际点击坐标
            real_x = int(center_x * scale_x)
            real_y = int(center_y * scale_y)
            print(f"识别到文字 '{target_text}' 的位置: x={x}, y={y}, w={w}, h={h}, center=({center_x},{center_y}), 实际点击=({real_x},{real_y}), scale=({scale_x:.2f},{scale_y:.2f})")
            # 先移动到截图坐标的黄色点
            pyautogui.moveTo(center_x, center_y, duration=0.5)
            # 再移动到实际点击点并点击
            pyautogui.moveTo(real_x, real_y, duration=0.2)
            pyautogui.click(real_x, real_y)
            time.sleep(0.1)
            pyautogui.click(real_x, real_y)
            print(f"已左键点击文字按钮两次：{target_text}")
            found = True
    screenshot.save('debug_ocr_box.png')
    if not found:
        print(f"未找到按钮文字：{target_text}")
    return found

def check_text_exists(text):
    """截屏并用OCR识别是否存在指定文本"""
    screenshot = pyautogui.screenshot()
    ocr_result = pytesseract.image_to_string(screenshot, lang='chi_sim+eng')
    if text in ocr_result:
        print(f"找到了文本：{text}")
        return True
    else:
        print(f"未找到文本：{text}")
        return False

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("用法: python operate_ui.py <按钮文字> <要查找的文本>")
        sys.exit(1)
    button_text = sys.argv[1]
    check_text = sys.argv[2]
    time.sleep(3)  # 给用户切换到目标窗口的时间
    find_and_click_text(button_text)
    check_text_exists(check_text) 