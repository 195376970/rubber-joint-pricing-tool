# 橡胶接头价格管理与报价小工具 - 项目指南

## Project Overview

This document serves as a comprehensive guide for AI assistants working on this project. It outlines the project structure, code organization, and guidelines for making changes to ensure code consistency and avoid errors.

## Tech Stack

- **Programming Language**: Python 3.8+
- **UI Framework**: Tkinter
- **Data Handling**: JSON (for storage), Pandas (for import/export)
- **PDF Generation**: ReportLab
- **Excel Handling**: Pandas, openpyxl

## Project Structure

```
/
├── assets/                 # 资源文件目录
│   ├── fonts/              # 字体文件
│   └── samples/            # 示例数据文件
│       ├── sphere_sample.csv
│       └── flange_sample.csv
├── data/                   # 数据存储目录
│   ├── spheres.json        # 球体数据
│   ├── flanges.json        # 法兰数据
│   ├── quotations.json     # 报价记录
│   └── settings.json       # 应用设置
├── src/                    # 源代码目录
│   ├── models/             # 数据模型
│   │   ├── data_models.py  # 数据实体类
│   │   └── data_manager.py # 数据管理器
│   ├── ui/                 # 用户界面
│   │   ├── app.py          # 主应用程序类
│   │   ├── tab_import.py   # 导入数据选项卡
│   │   ├── tab_quotation.py# 报价选项卡 
│   │   ├── tab_export.py   # 导出选项卡
│   │   └── tab_settings.py # 设置选项卡
│   ├── utils/              # 工具类
│   │   └── export_utils.py # 导出工具
│   └── main.py             # 程序入口点
├── main.py                 # 用于打包的主入口点
├── 一键打包发布.bat        # 一键式打包脚本
├── 清理打包文件.bat        # 清理临时打包文件脚本
├── requirements.txt        # 依赖项列表
└── README.md               # 项目说明文档
```

## Core Code Modules and Relationships

### 1. Data Models (`src/models/data_models.py`)

Key classes:
- `SphereItem`: 球体数据类，包含 `type_name`, `model`, `cost_price` 属性
- `FlangeItem`: 法兰数据类，包含 `type_name`, `model`, `cost_price` 属性
- `QuotationItem`: 报价项目类，包含 `sphere`, `flange1`, `flange2`, `quantity`, `profit_percentage` 属性

**Important Note**: The application uses a cost-based pricing model. Products don't store selling prices directly; instead, prices are calculated dynamically based on cost_price and profit_percentage.

```python
# 关键代码片段: 价格计算方式
@property
def total_price(self):
    """根据成本价和利润百分比计算总单价"""
    return self.total_cost_price * (1 + self.profit_percentage / 100)
```

### 2. Data Management (`src/models/data_manager.py`)

The `DataManager` class handles loading, saving, and querying data. Key methods:
- Data loading/saving: `load_spheres()`, `save_spheres()`, etc.
- Data import: `import_spheres_from_csv()`, `import_flanges_from_excel()`, etc.
- Data querying: `find_sphere()`, `get_sphere_types()`, etc.

### 3. UI Components

Each tab is implemented as a class derived from `ttk.Frame`:
- `ImportTab`: 数据导入/管理界面，支持CSV/Excel导入和手动录入
- `QuotationTab`: 报价计算界面，选择配件并计算价格
- `ExportTab`: 报价单导出界面，支持PDF和Excel格式
- `SettingsTab`: 设置界面，配置公司信息等

The main application class `RubberJointPricingApp` manages these tabs.

### 4. ScrollableFrame System

The application implements a robust scrolling system through the `ScrollableFrame` class in `src/ui/__init__.py`, which provides:

- Scrollable regions for all tab content
- Mouse wheel event binding for intuitive scrolling
- Recursive event binding to all child widgets
- Event rebinding after UI updates

Key event handling code:
```python
def _on_mousewheel(self, event):
    """Handle mouse wheel events"""
    # Handle different event types based on the system
    if hasattr(event, 'num') and (event.num == 4 or event.num == 5):  # Linux
        direction = 1 if event.num == 4 else -1
        self.canvas.yview_scroll(-direction, "units")
    elif hasattr(event, 'delta'):  # Windows/macOS
        direction = event.delta // 120  # Normalize scroll direction
        self.canvas.yview_scroll(-direction, "units")

def _recursive_bind(self, widget):
    """Recursively bind wheel events to all child widgets"""
    self._bind_to_widget(widget)
    
    # Process all child widgets
    for child in widget.winfo_children():
        self._bind_to_widget(child)
        if child.winfo_children():
            self._recursive_bind(child)
```

This system ensures consistent scrolling behavior across different platforms and dynamically created widgets.

### 5. Export Utilities (`src/utils/export_utils.py`)

Contains functions for exporting quotations to PDF and Excel:
- `export_to_pdf()`
- `export_to_excel()`

## Code Style Guidelines

To maintain consistency throughout the codebase, follow these style guidelines:

### Naming Conventions

1. **Class Names**: Use PascalCase (e.g., `SphereItem`, `DataManager`)
2. **Method/Function Names**: Use snake_case (e.g., `load_spheres`, `find_flange`)
3. **Private Methods**: Prefix with underscore (e.g., `_create_widgets`, `_on_button_click`)
4. **Constants**: Use UPPER_CASE (e.g., `DEFAULT_MARGIN`, `FONT_NAME`)
5. **Variables**: Use descriptive snake_case (e.g., `sphere_type`, `cost_price`)

### Documentation Standards

1. **Module Docstrings**: Each file should have a module-level docstring explaining its purpose
   ```python
   """
   数据模型模块
   定义球体和法兰的数据结构
   """
   ```

2. **Class/Function Docstrings**: Follow Google-style docstrings
   ```python
   def function_name(param1, param2):
       """
       简短描述函数功能
       
       Args:
           param1 (type): 参数1的说明
           param2 (type): 参数2的说明
       
       Returns:
           type: 返回值的说明
       """
   ```

3. **Inline Comments**: Use sparingly for non-obvious code

### Code Organization

1. **Imports**: Group imports in the following order:
   - Standard library imports
   - Third-party imports
   - Local application imports

2. **Class Methods Order**:
   - `__init__` and other special methods first
   - Public methods
   - Private methods

3. **UI Method Organization**:
   - UI creation methods (`_create_widgets`, etc.)
   - Event handlers (`_on_*` methods)
   - Data handling methods

## Modification Guidelines

### For Data Model Changes

When modifying data models:
1. Update the appropriate class in `src/models/data_models.py`
2. Update the `to_dict()` and `from_dict()` methods to ensure data can be saved/loaded
3. Update import/export functions in `DataManager` to handle new fields
4. Update UI components to display/input the new fields

### For UI Changes

When modifying UI components:
1. Each tab is self-contained in its own file in the `src/ui/` directory
2. Follow the existing widget hierarchy and naming conventions
3. New controls should be added to the appropriate tab class
4. Follow the pattern of separating UI creation from event handling

### Adding New Features

1. First identify which module(s) need to be modified
2. Make changes to data models if needed
3. Update the UI components
4. Test the feature thoroughly

## Testing Strategy

Manual testing is the primary method for this application. When implementing changes, test according to these guidelines:

### Functional Testing

1. **Data Model Changes**:
   - Test serialization/deserialization (saving and loading)
   - Verify new fields are correctly populated and accessed
   - Test data validation logic

2. **UI Changes**:
   - Test all user interactions with new UI elements
   - Verify UI updates correctly reflect data changes
   - Test edge cases (empty fields, invalid inputs)
   - Check for visual consistency with existing UI

3. **Import/Export Features**:
   - Test with valid input files
   - Test with invalid/malformed input files
   - Verify exported files contain all required data
   - Test compatibility with different file formats

### Cross-Feature Testing

Test interactions between components:
1. After data import, verify data appears correctly in quotation tab
2. After creating quotations, verify they can be correctly exported
3. After changing settings, verify they affect exports correctly

### Regression Testing

After any change:
1. Verify existing functionality still works
2. Test core workflows: data import → quotation creation → export

## Common Code Patterns

### Event Handling Pattern

```python
# 按钮事件处理示例
ttk.Button(frame, text="计算价格", command=self._calculate_price).grid(...)

def _calculate_price(self):
    # Handle the calculation
    ...
```

### Data Display and Filtering Pattern

```python
# 表格数据显示示例
tree = ttk.Treeview(container, columns=columns, show="headings")
for item in data:
    tree.insert("", "end", values=(item.attribute1, item.attribute2, ...))

# 筛选实现示例
def _filter_data(self, tree, filter_value):
    # Clear table
    for item in tree.get_children():
        tree.delete(item)
    
    # Apply filter and repopulate
    filtered_data = [item for item in all_data if item.matches(filter_value)]
    for item in filtered_data:
        tree.insert("", "end", values=(item.attribute1, item.attribute2, ...))
```

## Troubleshooting Common Issues

1. **File Paths**: Always use `os.path.join()` for path handling to ensure cross-platform compatibility
2. **Data Loading**: Check if files exist before attempting to load them
3. **UI Update**: Use StringVar and other variable types for dynamic UI updates
4. **Data Validation**: Always validate user input before processing

## Future Development Areas

- Enhanced data filtering capabilities
- Bulk operations for data management
- More export formats
- User permissions/roles

## Application Packaging

The application can be packaged into a standalone executable for distribution to computers without Python installed. This is accomplished using PyInstaller with custom batch scripts.

### Packaging Scripts

1. **一键打包发布.bat**: One-click packaging script that:
   - Installs required dependencies
   - Packages the application with PyInstaller
   - Creates a startup script
   - Generates a user manual
   - Produces a distribution zip file
   - Cleans up temporary files

2. **清理打包文件.bat**: Cleanup script that removes temporary files generated during packaging:
   - PyInstaller build directory
   - Spec files
   - Debug versions
   - Cache directories
   - Backup files

### Packaging Process

The packaging process uses absolute imports to ensure correct module loading in the packaged application. The main.py file in the root directory serves as an entry point that properly initializes the Python path before importing the actual application code.

```python
# Example of the entry point in main.py
import sys
import os

# Add current directory to path to ensure modules can be imported
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Import and run the actual application
from src.main import main

if __name__ == "__main__":
    main()
```

### Distribution Package

The final distribution package includes:
- The executable file (`橡胶接头报价工具.exe`)
- A startup batch file (`启动报价工具.bat`)
- A user manual (`使用说明.txt`)
- Assets and data directories

This distribution package can be deployed to any Windows computer without requiring Python or additional dependencies to be installed.

---

When modifying this project, always reference this guide to understand the overall architecture and coding patterns. This will help ensure consistent, error-free changes that maintain the integrity of the application.