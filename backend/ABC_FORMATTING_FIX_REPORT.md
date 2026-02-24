# A、B、C列格式化修复报告

## 问题描述

用户要求：
1. **A列（お客様管理番号）**：用字符串方式写入Excel表格
2. **B列（佐川問合せ番号HAWB）**：用字符串方式写入Excel表格
3. **C列（配達指定日）**：用"YYYY-MM-DD"格式化，并用字符串方式写入Excel表格

## 根本原因

### 1. source_cols是JSON字符串

在MySQL数据库中，`field_pipelines`表的`source_cols`字段类型为JSON，但实际存储的是JSON字符串（如`["お客様管理番号"]`），Python的SQLAlchemy JSON类型字段没有自动解析为Python列表。

当遍历source_cols时，实际上是遍历字符串的每个字符，导致无法正确匹配列数据。

### 2. 缺少格式化逻辑

`excel_writer.py`中的`write_excel_file_by_columns`函数没有对特定列进行格式化处理：
- 数字类型的A列应该转换为字符串
- 日期类型的C列应该格式化为"YYYY-MM-DD"字符串

## 修复方案

### 1. 修复delivery_processor.py

#### 1.1 添加JSON字符串解析逻辑（第230-250行）

```python
# 遍历field_pipelines配置
for pipeline in field_pipelines:
    target_col = pipeline.get('target_col')
    target_header = pipeline.get('target_header')
    map_op = pipeline.get('map_op')
    source_cols = pipeline.get('source_cols', [])
    # 确保source_cols是列表
    if isinstance(source_cols, str):
        import json
        try:
            source_cols = json.loads(source_cols)
        except Exception as e:
            logger.warning(f"解析source_cols JSON失败: {source_cols}, 错误: {e}")
            source_cols = []
    field_type = pipeline.get('field_type')
    rule_ref = pipeline.get('rule_ref', [])
    depends_on = pipeline.get('depends_on', [])
    # 确保depends_on也是列表
    if isinstance(depends_on, str):
        import json
        try:
            depends_on = json.loads(depends_on)
        except Exception as e:
            logger.warning(f"解析depends_on JSON失败: {depends_on}, 错误: {e}")
            depends_on = []
    order = pipeline.get('order', 0)
```

### 2. 修复excel_writer.py

#### 2.1 添加格式化函数（第8-50行）

```python
def format_as_string(value: Any) -> str:
    """
    将值格式化为字符串
    
    输入：
        - value: 任意值
    
    输出：
        - 字符串值
    """
    if value is None:
        return ''
    if isinstance(value, datetime):
        return value.strftime('%Y-%m-%d')
    return str(value)

def format_date_as_yyyy_mm_dd(value: Any) -> str:
    """
    将日期值格式化为YYYY-MM-DD格式的字符串
    
    输入：
        - value: 日期值（datetime对象、字符串等）
    
    输出：
        - YYYY-MM-DD格式的字符串
    """
    if value is None:
        return ''
    if isinstance(value, datetime):
        return value.strftime('%Y-%m-%d')
    if isinstance(value, str):
        # 如果已经是字符串，尝试解析后重新格式化
        try:
            # 尝试解析常见日期格式
            for fmt in ['%Y-%m-%d', '%Y/%m/%d', '%Y年%m月%d日', '%d/%m/%Y', '%m/%d/%Y']:
                try:
                    parsed_date = datetime.strptime(value, fmt)
                    return parsed_date.strftime('%Y-%m-%d')
                except ValueError:
                    continue
        except Exception:
            pass
    # 如果无法解析，直接返回字符串
    return str(value)
```

#### 2.2 在写入时应用格式化（第151-172行）

```python
logger.info(f"开始按列写入数据 - 共 {num_rows} 行, {num_cols} 列")

for col_idx, col_name in enumerate(headers, start=1):
    if col_name in column_data:
        for row_idx, value in enumerate(column_data[col_name], start=current_row):
            # 根据列名进行特殊处理
            if col_idx == 1 and col_name == 'お客様管理番号':
                # A列：お客様管理番号，用字符串方式写入
                formatted_value = format_as_string(value)
            elif col_idx == 2 and col_name == '佐川問合せ番号HAWB':
                # B列：佐川問合せ番号HAWB，用字符串方式写入
                formatted_value = format_as_string(value)
            elif col_idx == 3 and col_name == '配達指定日':
                # C列：配達指定日，格式化为YYYY-MM-DD字符串
                formatted_value = format_date_as_yyyy_mm_dd(value)
            else:
                # 其他列，直接写入
                formatted_value = value

            worksheet.cell(row=row_idx, column=col_idx, value=formatted_value)
            logger.debug(f"写入单元格 - 行号: {row_idx}, 列号: {col_idx}, 列名: {col_name}, 值: {value}, 格式化值: {formatted_value}")

logger.info(f"按列写入完成 - 共 {num_rows} 行, {num_cols} 列")
```

## 测试结果

### 测试数据

创建了3行测试数据：
- 第2行：A列=123456(数字), B列='SG123456789'(字符串), C列=datetime(2026,2,10)
- 第3行：A列=789012(数字), B列='SG987654321'(字符串), C列='2026-02-11'(字符串)
- 第4行：A列=345678(数字), B列='SG456789123'(字符串), C列='2026年2月12日'(中文日期字符串)

### 测试结果

```
第2行 (A列数字转字符串，C列datetime格式化):
  A列(お客様管理番号): 实际='123456', 类型=str, 期望='123456', 期望类型=str [通过]
  B列(佐川問合せ番号HAWB): 实际='SG123456789', 类型=str, 期望='SG123456789', 期望类型=str [通过]
  C列(配達指定日): 实际='2026-02-10', 类型=str, 期望='2026-02-10', 期望类型=str [通过]

第3行 (A列数字转字符串，C列字符串保持):
  A列(お客様管理番号): 实际='789012', 类型=str, 期望='789012', 期望类型=str [通过]
  B列(佐川問合せ番号HAWB): 实际='SG987654321', 类型=str, 期望='SG987654321', 期望类型=str [通过]
  C列(配達指定日): 实际='2026-02-11', 类型=str, 期望='2026-02-11', 期望类型=str [通过]

第4行 (A列数字转字符串，C列中文日期格式化):
  A列(お客様管理番号): 实际='345678', 类型=str, 期望='345678', 期望类型=str [通过]
  B列(佐川問合せ番号HAWB): 实际='SG456789123', 类型=str, 期望='SG456789123', 期望类型=str [通过]
  C列(配達指定日): 实际='2026-02-12', 类型=str, 期望='2026-02-12', 期望类型=str [通过]

[成功] A、B、C列格式化测试通过！
```

## 格式化功能

### A列（お客様管理番号）
- 数字 → 字符串：`123456` → `'123456'`
- 保留原值：保持字符串形式

### B列（佐川問合せ番号HAWB）
- 字符串 → 字符串：保持原值不变
- 确保以字符串方式写入

### C列（配達指定日）
支持多种输入格式的日期：
- datetime对象：`datetime(2026, 2, 10)` → `'2026-02-10'`
- 标准日期字符串：`'2026-02-11'` → `'2026-02-11'`
- 中文日期字符串：`'2026年2月12日'` → `'2026-02-12'`
- 斜杠分隔日期：`'2026/02/13'` → `'2026-02-13'`
- 其他格式：尝试解析，失败则返回原字符串

## 修复的文件

1. `backend/app/services/delivery_processor.py`
   - 添加source_cols和depends_on的JSON字符串解析逻辑

2. `backend/app/services/excel_writer.py`
   - 添加format_as_string函数：将值转换为字符串
   - 添加format_date_as_yyyy_mm_dd函数：将日期格式化为YYYY-MM-DD字符串
   - 在write_excel_file_by_columns中添加对A、B、C列的特殊处理

## 测试脚本

创建了以下测试和调试脚本：
- `create_test_abc_columns.py` - 创建测试文件
- `test_abc_formatting.py` - 完整的格式化测试
- `debug_abc_processing.py` - 调试处理过程
- `check_abc_columns.py` - 检查列配置
- `check_result_file_abc.py` - 检查结果文件

所有测试均通过！
