"""
用户界面模块
包含所有UI相关组件和功能
"""

import tkinter as tk
from tkinter import ttk

class ScrollableFrame(ttk.Frame):
    """可滚动的Frame组件，支持鼠标滚轮事件"""
    
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        
        # 创建画布和滚动条
        self.canvas = tk.Canvas(self)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)
        
        # 配置画布
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        # 创建窗口
        self.canvas_frame = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        
        # 配置画布响应滚动条
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        # 放置组件
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # 初始绑定滚轮事件
        self._recursive_bind(self.scrollable_frame)
        
        # 绑定画布调整大小事件
        self.canvas.bind("<Configure>", self._on_canvas_configure)
    
    def _on_canvas_configure(self, event):
        """画布大小变化时调整内部frame的宽度"""
        self.canvas.itemconfig(self.canvas_frame, width=event.width)
    
    def _on_mousewheel(self, event):
        """处理鼠标滚轮事件"""
        # 处理基于系统的不同事件类型
        if hasattr(event, 'num') and (event.num == 4 or event.num == 5):  # Linux
            direction = 1 if event.num == 4 else -1
            self.canvas.yview_scroll(-direction, "units")
        elif hasattr(event, 'delta'):  # Windows/macOS
            direction = event.delta // 120  # 标准化滚动方向
            self.canvas.yview_scroll(-direction, "units")
    
    def _bind_to_widget(self, widget):
        """将鼠标滚轮事件绑定到特定组件"""
        # Linux上的滚动事件
        widget.bind("<Button-4>", self._on_mousewheel)
        widget.bind("<Button-5>", self._on_mousewheel)
        # Windows/macOS上的滚动事件
        widget.bind("<MouseWheel>", self._on_mousewheel)
    
    def _recursive_bind(self, widget):
        """递归绑定所有子组件的滚轮事件"""
        self._bind_to_widget(widget)
        
        # 处理所有子组件
        for child in widget.winfo_children():
            self._bind_to_widget(child)
            if child.winfo_children():
                self._recursive_bind(child)
    
    def update(self):
        """重写update方法以确保滚轮事件在更新后保持有效"""
        super().update()
        # 更新后重新绑定所有子组件的滚轮事件
        self._recursive_bind(self.scrollable_frame)
    
    def after_update(self):
        """在控件更新后手动调用，确保正确的滚轮事件绑定"""
        self._recursive_bind(self.scrollable_frame)
        # 更新滚动区域配置
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        # 更新滚动条和画布
        self.update_idletasks()
        self.update()