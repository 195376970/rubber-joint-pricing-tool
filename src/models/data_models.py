#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
数据模型模块
定义橡胶接头报价系统中使用的数据实体类
"""

class SphereItem:
    """球体（接头）数据类"""
    
    def __init__(self, type_name="", model="", cost_price=0.0):
        """
        初始化球体数据对象
        
        Args:
            type_name (str): 类型名称
            model (str): 型号规格
            cost_price (float): 成本价
        """
        self.type_name = type_name
        self.model = model
        self.cost_price = float(cost_price)
    
    def to_dict(self):
        """
        将对象转换为字典用于JSON序列化
        
        Returns:
            dict: 对象的字典表示
        """
        return {
            "type_name": self.type_name,
            "model": self.model,
            "cost_price": self.cost_price
        }
    
    @classmethod
    def from_dict(cls, data):
        """
        从字典创建对象
        
        Args:
            data (dict): 数据字典
            
        Returns:
            SphereItem: 创建的球体对象
        """
        return cls(
            type_name=data.get("type_name", ""),
            model=data.get("model", ""),
            cost_price=float(data.get("cost_price", 0.0))
        )
    
    def __str__(self):
        return f"{self.type_name} {self.model} (成本: ¥{self.cost_price:.2f})"


class FlangeItem:
    """法兰数据类"""
    
    def __init__(self, type_name="", model="", cost_price=0.0):
        """
        初始化法兰数据对象
        
        Args:
            type_name (str): 类型名称
            model (str): 型号规格
            cost_price (float): 成本价
        """
        self.type_name = type_name
        self.model = model
        self.cost_price = float(cost_price)
    
    def to_dict(self):
        """
        将对象转换为字典用于JSON序列化
        
        Returns:
            dict: 对象的字典表示
        """
        return {
            "type_name": self.type_name,
            "model": self.model,
            "cost_price": self.cost_price
        }
    
    @classmethod
    def from_dict(cls, data):
        """
        从字典创建对象
        
        Args:
            data (dict): 数据字典
            
        Returns:
            FlangeItem: 创建的法兰对象
        """
        return cls(
            type_name=data.get("type_name", ""),
            model=data.get("model", ""),
            cost_price=float(data.get("cost_price", 0.0))
        )
    
    def __str__(self):
        return f"{self.type_name} {self.model} (成本: ¥{self.cost_price:.2f})"


class QuotationItem:
    """报价项目类"""
    
    def __init__(self, sphere=None, flange1=None, flange2=None, quantity=1, profit_percentage=30.0):
        """
        初始化报价项目对象
        
        Args:
            sphere (SphereItem): 球体对象
            flange1 (FlangeItem): 第一个法兰对象
            flange2 (FlangeItem): 第二个法兰对象
            quantity (int): 数量
            profit_percentage (float): 利润百分比
        """
        self.sphere = sphere if sphere else SphereItem()
        self.flange1 = flange1 if flange1 else FlangeItem()
        self.flange2 = flange2 if flange2 else FlangeItem()
        self.quantity = int(quantity)
        self.profit_percentage = float(profit_percentage)
    
    @property
    def description(self):
        """获取产品描述"""
        return f"{self.sphere.type_name} {self.sphere.model} + {self.flange1.type_name} + {self.flange2.type_name}"
    
    @property
    def unit_cost_price(self):
        """计算单件成本价"""
        return self.sphere.cost_price + self.flange1.cost_price + self.flange2.cost_price
    
    @property
    def total_cost_price(self):
        """计算总成本价"""
        return self.unit_cost_price * self.quantity
    
    @property
    def unit_price(self):
        """计算单件销售价"""
        return self.unit_cost_price * (1 + self.profit_percentage / 100)
    
    @property
    def total_price(self):
        """计算总销售价"""
        return self.unit_price * self.quantity
    
    def to_dict(self):
        """
        将对象转换为字典用于JSON序列化
        
        Returns:
            dict: 对象的字典表示
        """
        return {
            "sphere": self.sphere.to_dict(),
            "flange1": self.flange1.to_dict(),
            "flange2": self.flange2.to_dict(),
            "quantity": self.quantity,
            "profit_percentage": self.profit_percentage
        }
    
    @classmethod
    def from_dict(cls, data):
        """
        从字典创建对象
        
        Args:
            data (dict): 数据字典
            
        Returns:
            QuotationItem: 创建的报价项目对象
        """
        return cls(
            sphere=SphereItem.from_dict(data.get("sphere", {})),
            flange1=FlangeItem.from_dict(data.get("flange1", {})),
            flange2=FlangeItem.from_dict(data.get("flange2", {})),
            quantity=int(data.get("quantity", 1)),
            profit_percentage=float(data.get("profit_percentage", 30.0))
        )
    
    def __str__(self):
        return (f"{self.description} x {self.quantity}件, "
                f"单价: ¥{self.unit_price:.2f}, "
                f"总价: ¥{self.total_price:.2f}")