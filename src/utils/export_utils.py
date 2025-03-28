#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
导出工具模块
提供报价单导出为PDF和Excel的功能
"""

import os
import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
import pandas as pd

def export_to_pdf(quotations, filepath, settings, show_cost_price=False):
    """
    将报价单导出为PDF文件
    
    Args:
        quotations (list): 报价项目列表
        filepath (str): 输出文件路径
        settings (dict): 公司信息等设置
        show_cost_price (bool): 是否显示成本价和利润
    
    Returns:
        bool: 导出是否成功
    """
    try:
        # 创建一个文档
        doc = SimpleDocTemplate(
            filepath,
            pagesize=A4,
            leftMargin=2*cm,
            rightMargin=2*cm,
            topMargin=2*cm,
            bottomMargin=2*cm
        )
        
        # 获取样式
        styles = getSampleStyleSheet()
        title_style = styles["Title"]
        normal_style = styles["Normal"]
        
        # 自定义段落样式
        header_style = ParagraphStyle(
            'Header',
            parent=styles['Heading1'],
            fontSize=14,
            spaceAfter=10
        )
        
        # 初始化文档内容
        elements = []
        
        # 添加标题
        title = Paragraph("报价单", title_style)
        elements.append(title)
        elements.append(Spacer(1, 0.5*cm))
        
        # 添加公司信息
        company_info = [
            Paragraph(f"<b>公司名称:</b> {settings.get('company_name', '')}", normal_style),
            Paragraph(f"<b>联系方式:</b> {settings.get('contact_info', '')}", normal_style),
            Paragraph(f"<b>地址:</b> {settings.get('address', '')}", normal_style),
            Paragraph(f"<b>日期:</b> {datetime.datetime.now().strftime('%Y-%m-%d')}", normal_style)
        ]
        
        for info in company_info:
            elements.append(info)
            elements.append(Spacer(1, 0.2*cm))
        
        elements.append(Spacer(1, 0.5*cm))
        
        # 准备表格数据
        if show_cost_price:
            # 包含成本价和利润率的表头
            table_header = ["产品描述", "数量", "单位成本(¥)", "成本合计(¥)", "利润率(%)", "单价(¥)", "金额合计(¥)"]
        else:
            # 不包含成本和利润率的表头
            table_header = ["产品描述", "数量", "单价(¥)", "金额合计(¥)"]
        
        table_data = [table_header]
        
        # 总金额
        total_amount = 0
        
        # 填充表格数据
        for quotation in quotations:
            if show_cost_price:
                row = [
                    quotation.description,
                    quotation.quantity,
                    f"{quotation.unit_cost_price:.2f}",
                    f"{quotation.total_cost_price:.2f}",
                    f"{quotation.profit_percentage:.0f}",
                    f"{quotation.unit_price:.2f}",
                    f"{quotation.total_price:.2f}"
                ]
            else:
                row = [
                    quotation.description,
                    quotation.quantity,
                    f"{quotation.unit_price:.2f}",
                    f"{quotation.total_price:.2f}"
                ]
            table_data.append(row)
            total_amount += quotation.total_price
        
        # 添加总计行
        if show_cost_price:
            total_row = ["总计", "", "", "", "", "", f"{total_amount:.2f}"]
        else:
            total_row = ["总计", "", "", f"{total_amount:.2f}"]
        table_data.append(total_row)
        
        # 创建表格
        table = Table(table_data)
        
        # 设置表格样式
        table_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('ALIGN', (0, -1), (-1, -1), 'RIGHT'),
            ('ALIGN', (1, 1), (-1, -1), 'RIGHT'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ])
        table.setStyle(table_style)
        
        elements.append(table)
        
        # 添加备注
        elements.append(Spacer(1, 1*cm))
        elements.append(Paragraph("<b>备注:</b>", normal_style))
        elements.append(Paragraph("1. 本报价单有效期为30天。", normal_style))
        elements.append(Paragraph("2. 付款方式: 预付款30%，发货前付清余款。", normal_style))
        elements.append(Paragraph("3. 交货期: 合同签署后15个工作日内。", normal_style))
        
        # 构建文档
        doc.build(elements)
        
        return True
    except Exception as e:
        print(f"导出PDF失败: {e}")
        return False

def export_to_excel(quotations, filepath, settings, show_cost_price=False):
    """
    将报价单导出为Excel文件
    
    Args:
        quotations (list): 报价项目列表
        filepath (str): 输出文件路径
        settings (dict): 公司信息等设置
        show_cost_price (bool): 是否显示成本价和利润
    
    Returns:
        bool: 导出是否成功
    """
    try:
        # 准备数据
        if show_cost_price:
            # 包含成本价和利润率的数据
            data = {
                "产品描述": [],
                "数量": [],
                "单位成本(¥)": [],
                "成本合计(¥)": [],
                "利润率(%)": [],
                "单价(¥)": [],
                "金额合计(¥)": []
            }
            
            for quotation in quotations:
                data["产品描述"].append(quotation.description)
                data["数量"].append(quotation.quantity)
                data["单位成本(¥)"].append(round(quotation.unit_cost_price, 2))
                data["成本合计(¥)"].append(round(quotation.total_cost_price, 2))
                data["利润率(%)"].append(round(quotation.profit_percentage, 0))
                data["单价(¥)"].append(round(quotation.unit_price, 2))
                data["金额合计(¥)"].append(round(quotation.total_price, 2))
        else:
            # 不包含成本和利润率的数据
            data = {
                "产品描述": [],
                "数量": [],
                "单价(¥)": [],
                "金额合计(¥)": []
            }
            
            for quotation in quotations:
                data["产品描述"].append(quotation.description)
                data["数量"].append(quotation.quantity)
                data["单价(¥)"].append(round(quotation.unit_price, 2))
                data["金额合计(¥)"].append(round(quotation.total_price, 2))
        
        # 创建DataFrame
        df = pd.DataFrame(data)
        
        # 计算总金额
        total_amount = sum(quotation.total_price for quotation in quotations)
        
        # 创建Excel写入器
        with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
            # 写入报价数据
            df.to_excel(writer, sheet_name='报价单', index=False, startrow=5)
            
            # 获取工作簿和工作表
            workbook = writer.book
            worksheet = writer.sheets['报价单']
            
            # 写入标题和公司信息
            worksheet.cell(row=1, column=1, value="报价单")
            worksheet.cell(row=2, column=1, value=f"公司名称: {settings.get('company_name', '')}")
            worksheet.cell(row=3, column=1, value=f"联系方式: {settings.get('contact_info', '')}")
            worksheet.cell(row=4, column=1, value=f"日期: {datetime.datetime.now().strftime('%Y-%m-%d')}")
            
            # 添加总计行
            total_row = len(quotations) + 6  # 标题5行 + 数据行数 + 表头1行
            
            # 合并单元格用于总计
            if show_cost_price:
                worksheet.cell(row=total_row, column=1, value="总计")
                worksheet.cell(row=total_row, column=7, value=round(total_amount, 2))
            else:
                worksheet.cell(row=total_row, column=1, value="总计")
                worksheet.cell(row=total_row, column=4, value=round(total_amount, 2))
            
            # 设置列宽
            for i, column in enumerate(df.columns):
                column_width = max(len(column) * 1.2, df[column].astype(str).map(len).max() * 1.2)
                worksheet.column_dimensions[chr(65 + i)].width = column_width
        
        return True
    except Exception as e:
        print(f"导出Excel失败: {e}")
        return False