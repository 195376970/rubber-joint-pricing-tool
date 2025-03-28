#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
橡胶接头价格管理与报价小工具
主程序入口
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox
import traceback

# 确保路径设置正确
def get_base_path():
    """获取基础路径，在开发环境和PyInstaller环境中都能正确工作"""
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        return sys._MEIPASS
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 设置资源路径
BASE_PATH = get_base_path()
ASSETS_PATH = os.path.join(BASE_PATH, "assets")
DATA_PATH = os.path.join(BASE_PATH, "data")

# 创建数据目录（如果不存在）
def ensure_data_directory():
    """确保数据目录存在"""
    if not os.path.exists(DATA_PATH):
        try:
            os.makedirs(DATA_PATH)
            print(f"创建数据目录: {DATA_PATH}")
        except Exception as e:
            print(f"创建数据目录失败: {e}")

def main():
    """应用程序入口点"""
    try:
        # 确保数据目录存在
        ensure_data_directory()
        
        # 导入应用程序主类
        from src.ui.app import RubberJointPricingApp
        
        # 创建主窗口
        root = tk.Tk()
        root.title("橡胶接头价格管理与报价工具 V5.0")
        root.geometry("1024x768")
        
        # 初始化应用程序
        app = RubberJointPricingApp(root)
        app.pack(fill="both", expand=True)
        
        # 显示主窗口
        root.update()
        root.minsize(root.winfo_width(), root.winfo_height())
        
        # 启动主循环
        root.mainloop()
        
    except Exception as e:
        # 捕获并显示任何未处理的异常
        error_msg = f"应用程序启动失败: {str(e)}\n{traceback.format_exc()}"
        print(error_msg)
        messagebox.showerror("启动错误", error_msg)
        sys.exit(1)

if __name__ == "__main__":
    main()