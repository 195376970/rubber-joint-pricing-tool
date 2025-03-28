#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
数据管理模块
负责数据的加载、保存和处理
"""

import os
import json
import csv
import pandas as pd
from src.models.data_models import SphereItem, FlangeItem, QuotationItem

class DataManager:
    """数据管理器类，处理数据的加载、保存和操作"""
    
    def __init__(self, data_dir="data"):
        """
        初始化数据管理器
        
        Args:
            data_dir (str): 数据目录路径
        """
        # 获取基础路径
        if getattr(import sys; sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        
        self.data_dir = os.path.join(base_path, data_dir)
        
        # 确保数据目录存在
        os.makedirs(self.data_dir, exist_ok=True)
        
        # 数据文件路径
        self.spheres_file = os.path.join(self.data_dir, "spheres.json")
        self.flanges_file = os.path.join(self.data_dir, "flanges.json")
        self.quotations_file = os.path.join(self.data_dir, "quotations.json")
        self.settings_file = os.path.join(self.data_dir, "settings.json")
        
        # 初始化数据容器
        self.spheres = []  # 球体列表
        self.flanges = []  # 法兰列表
        self.quotations = []  # 报价项目列表
        self.settings = {
            "company_name": "橡胶接头有限公司",
            "contact_info": "电话: 010-12345678",
            "address": "地址: 北京市朝阳区xxx路xx号",
            "show_cost_price": False
        }
        
        # 加载数据
        self.load_all()
    
    def load_all(self):
        """加载所有数据"""
        self.load_spheres()
        self.load_flanges()
        self.load_quotations()
        self.load_settings()
    
    def save_all(self):
        """保存所有数据"""
        self.save_spheres()
        self.save_flanges()
        self.save_quotations()
        self.save_settings()
    
    # =========== 球体数据处理 ===========
    
    def load_spheres(self):
        """
        从JSON文件加载球体数据
        
        Returns:
            bool: 加载是否成功
        """
        try:
            if os.path.exists(self.spheres_file):
                with open(self.spheres_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                self.spheres = [SphereItem.from_dict(item) for item in data]
                return True
            return False
        except Exception as e:
            print(f"加载球体数据失败: {e}")
            return False
    
    def save_spheres(self):
        """
        保存球体数据到JSON文件
        
        Returns:
            bool: 保存是否成功
        """
        try:
            with open(self.spheres_file, 'w', encoding='utf-8') as f:
                json.dump([sphere.to_dict() for sphere in self.spheres], f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"保存球体数据失败: {e}")
            return False
    
    def add_sphere(self, sphere):
        """
        添加球体数据
        
        Args:
            sphere (SphereItem): 要添加的球体对象
            
        Returns:
            bool: 添加是否成功
        """
        try:
            # 检查是否已存在相同类型和型号的球体
            for i, existing in enumerate(self.spheres):
                if existing.type_name == sphere.type_name and existing.model == sphere.model:
                    # 更新成本价
                    self.spheres[i].cost_price = sphere.cost_price
                    self.save_spheres()
                    return True
            
            # 不存在则添加新的
            self.spheres.append(sphere)
            self.save_spheres()
            return True
        except Exception as e:
            print(f"添加球体数据失败: {e}")
            return False
    
    def remove_sphere(self, index):
        """
        移除指定索引处的球体数据
        
        Args:
            index (int): 要移除的球体索引
            
        Returns:
            bool: 移除是否成功
        """
        try:
            if 0 <= index < len(self.spheres):
                del self.spheres[index]
                self.save_spheres()
                return True
            return False
        except Exception as e:
            print(f"移除球体数据失败: {e}")
            return False
    
    def get_sphere_types(self):
        """
        获取所有球体类型列表
        
        Returns:
            list: 不重复的球体类型列表
        """
        types = set()
        for sphere in self.spheres:
            types.add(sphere.type_name)
        return sorted(list(types))
    
    def get_sphere_models(self, type_name=None):
        """
        获取指定类型的球体型号列表
        
        Args:
            type_name (str, optional): 球体类型名称。如果为None，返回所有型号
            
        Returns:
            list: 球体型号列表
        """
        models = set()
        for sphere in self.spheres:
            if type_name is None or sphere.type_name == type_name:
                models.add(sphere.model)
        return sorted(list(models))
    
    def find_sphere(self, type_name, model):
        """
        查找指定类型和型号的球体
        
        Args:
            type_name (str): 球体类型
            model (str): 球体型号
            
        Returns:
            SphereItem: 找到的球体对象，未找到则返回None
        """
        for sphere in self.spheres:
            if sphere.type_name == type_name and sphere.model == model:
                return sphere
        return None
    
    def import_spheres_from_csv(self, file_path):
        """
        从CSV文件导入球体数据
        
        Args:
            file_path (str): CSV文件路径
        
        Returns:
            tuple: (success, message)
        """
        try:
            spheres = []
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if "type_name" in row and "model" in row and "cost_price" in row:
                        sphere = SphereItem(
                            type_name=row["type_name"],
                            model=row["model"],
                            cost_price=float(row["cost_price"])
                        )
                        spheres.append(sphere)
            
            if spheres:
                self.spheres = spheres
                self.save_spheres()
                return True, f"成功导入 {len(spheres)} 条球体数据"
            else:
                return False, "没有有效的数据"
                
        except Exception as e:
            return False, f"导入失败: {e}"
    
    def import_spheres_from_excel(self, file_path):
        """
        从Excel文件导入球体数据
        
        Args:
            file_path (str): Excel文件路径
        
        Returns:
            tuple: (success, message)
        """
        try:
            df = pd.read_excel(file_path)
            required_columns = ["type_name", "model", "cost_price"]
            
            # 检查必要的列是否存在
            if not all(col in df.columns for col in required_columns):
                return False, "Excel文件缺少必要的列：type_name, model, cost_price"
            
            spheres = []
            for _, row in df.iterrows():
                sphere = SphereItem(
                    type_name=row["type_name"],
                    model=row["model"],
                    cost_price=float(row["cost_price"])
                )
                spheres.append(sphere)
            
            if spheres:
                self.spheres = spheres
                self.save_spheres()
                return True, f"成功导入 {len(spheres)} 条球体数据"
            else:
                return False, "没有有效的数据"
                
        except Exception as e:
            return False, f"导入失败: {e}"
    
    # =========== 法兰数据处理 ===========
    
    def load_flanges(self):
        """
        从JSON文件加载法兰数据
        
        Returns:
            bool: 加载是否成功
        """
        try:
            if os.path.exists(self.flanges_file):
                with open(self.flanges_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                self.flanges = [FlangeItem.from_dict(item) for item in data]
                return True
            return False
        except Exception as e:
            print(f"加载法兰数据失败: {e}")
            return False
    
    def save_flanges(self):
        """
        保存法兰数据到JSON文件
        
        Returns:
            bool: 保存是否成功
        """
        try:
            with open(self.flanges_file, 'w', encoding='utf-8') as f:
                json.dump([flange.to_dict() for flange in self.flanges], f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"保存法兰数据失败: {e}")
            return False
    
    def add_flange(self, flange):
        """
        添加法兰数据
        
        Args:
            flange (FlangeItem): 要添加的法兰对象
            
        Returns:
            bool: 添加是否成功
        """
        try:
            # 检查是否已存在相同类型和型号的法兰
            for i, existing in enumerate(self.flanges):
                if existing.type_name == flange.type_name and existing.model == flange.model:
                    # 更新成本价
                    self.flanges[i].cost_price = flange.cost_price
                    self.save_flanges()
                    return True
            
            # 不存在则添加新的
            self.flanges.append(flange)
            self.save_flanges()
            return True
        except Exception as e:
            print(f"添加法兰数据失败: {e}")
            return False
    
    def remove_flange(self, index):
        """
        移除指定索引处的法兰数据
        
        Args:
            index (int): 要移除的法兰索引
            
        Returns:
            bool: 移除是否成功
        """
        try:
            if 0 <= index < len(self.flanges):
                del self.flanges[index]
                self.save_flanges()
                return True
            return False
        except Exception as e:
            print(f"移除法兰数据失败: {e}")
            return False
    
    def get_flange_types(self):
        """
        获取所有法兰类型列表
        
        Returns:
            list: 不重复的法兰类型列表
        """
        types = set()
        for flange in self.flanges:
            types.add(flange.type_name)
        return sorted(list(types))
    
    def get_flange_models(self, type_name=None):
        """
        获取指定类型的法兰型号列表
        
        Args:
            type_name (str, optional): 法兰类型名称。如果为None，返回所有型号
            
        Returns:
            list: 法兰型号列表
        """
        models = set()
        for flange in self.flanges:
            if type_name is None or flange.type_name == type_name:
                models.add(flange.model)
        return sorted(list(models))
    
    def find_flange(self, type_name, model):
        """
        查找指定类型和型号的法兰
        
        Args:
            type_name (str): 法兰类型
            model (str): 法兰型号
            
        Returns:
            FlangeItem: 找到的法兰对象，未找到则返回None
        """
        for flange in self.flanges:
            if flange.type_name == type_name and flange.model == model:
                return flange
        return None
    
    def import_flanges_from_csv(self, file_path):
        """
        从CSV文件导入法兰数据
        
        Args:
            file_path (str): CSV文件路径
        
        Returns:
            tuple: (success, message)
        """
        try:
            flanges = []
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if "type_name" in row and "model" in row and "cost_price" in row:
                        flange = FlangeItem(
                            type_name=row["type_name"],
                            model=row["model"],
                            cost_price=float(row["cost_price"])
                        )
                        flanges.append(flange)
            
            if flanges:
                self.flanges = flanges
                self.save_flanges()
                return True, f"成功导入 {len(flanges)} 条法兰数据"
            else:
                return False, "没有有效的数据"
                
        except Exception as e:
            return False, f"导入失败: {e}"
    
    def import_flanges_from_excel(self, file_path):
        """
        从Excel文件导入法兰数据
        
        Args:
            file_path (str): Excel文件路径
        
        Returns:
            tuple: (success, message)
        """
        try:
            df = pd.read_excel(file_path)
            required_columns = ["type_name", "model", "cost_price"]
            
            # 检查必要的列是否存在
            if not all(col in df.columns for col in required_columns):
                return False, "Excel文件缺少必要的列：type_name, model, cost_price"
            
            flanges = []
            for _, row in df.iterrows():
                flange = FlangeItem(
                    type_name=row["type_name"],
                    model=row["model"],
                    cost_price=float(row["cost_price"])
                )
                flanges.append(flange)
            
            if flanges:
                self.flanges = flanges
                self.save_flanges()
                return True, f"成功导入 {len(flanges)} 条法兰数据"
            else:
                return False, "没有有效的数据"
                
        except Exception as e:
            return False, f"导入失败: {e}"
    
    # =========== 报价数据处理 ===========
    
    def load_quotations(self):
        """
        从JSON文件加载报价数据
        
        Returns:
            bool: 加载是否成功
        """
        try:
            if os.path.exists(self.quotations_file):
                with open(self.quotations_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                self.quotations = [QuotationItem.from_dict(item) for item in data]
                return True
            return False
        except Exception as e:
            print(f"加载报价数据失败: {e}")
            return False
    
    def save_quotations(self):
        """
        保存报价数据到JSON文件
        
        Returns:
            bool: 保存是否成功
        """
        try:
            with open(self.quotations_file, 'w', encoding='utf-8') as f:
                json.dump([quotation.to_dict() for quotation in self.quotations], f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"保存报价数据失败: {e}")
            return False
    
    def add_quotation(self, quotation):
        """
        添加报价项目
        
        Args:
            quotation (QuotationItem): 要添加的报价项目
            
        Returns:
            bool: 添加是否成功
        """
        try:
            self.quotations.append(quotation)
            self.save_quotations()
            return True
        except Exception as e:
            print(f"添加报价数据失败: {e}")
            return False
    
    def remove_quotation(self, index):
        """
        移除指定索引处的报价项目
        
        Args:
            index (int): 要移除的报价项目索引
            
        Returns:
            bool: 移除是否成功
        """
        try:
            if 0 <= index < len(self.quotations):
                del self.quotations[index]
                self.save_quotations()
                return True
            return False
        except Exception as e:
            print(f"移除报价数据失败: {e}")
            return False
    
    def clear_quotations(self):
        """
        清空所有报价项目
        
        Returns:
            bool: 清空是否成功
        """
        try:
            self.quotations = []
            self.save_quotations()
            return True
        except Exception as e:
            print(f"清空报价数据失败: {e}")
            return False
    
    # =========== 设置处理 ===========
    
    def load_settings(self):
        """
        从JSON文件加载设置
        
        Returns:
            bool: 加载是否成功
        """
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    self.settings = json.load(f)
                return True
            return False
        except Exception as e:
            print(f"加载设置失败: {e}")
            return False
    
    def save_settings(self):
        """
        保存设置到JSON文件
        
        Returns:
            bool: 保存是否成功
        """
        try:
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"保存设置失败: {e}")
            return False
    
    def update_setting(self, key, value):
        """
        更新设置项
        
        Args:
            key (str): 设置项名称
            value: 设置项值
            
        Returns:
            bool: 更新是否成功
        """
        try:
            self.settings[key] = value
            self.save_settings()
            return True
        except Exception as e:
            print(f"更新设置失败: {e}")
            return False