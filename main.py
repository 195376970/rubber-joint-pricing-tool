#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
橡胶接头价格管理与报价小工具
主程序入口 - 用于PyInstaller打包
"""

import sys
import os

# 将当前目录添加到路径，确保可以导入模块
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# 调用实际的主程序
from src.main import main

if __name__ == "__main__":
    main()