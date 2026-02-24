# DEFAULT操作修复报告

## 问题描述

依頼主、依頼主住所、依頼主電話三列配置为DEFAULT操作，当源值为空时应使用默认值，但实际所有行的值都被替换成了默认值。

## 根本原因

### 1. rule_params获取逻辑问题

在`delivery_processor.py`的`_execute_field_handler`方法中，DEFAULT操作的rule_params获取逻辑不完整：

**原始代码（第357-370行）：**
```python
# 获取规则参数
rule_params = {}
if pipeline:
    rule_params_json = pipeline.get('rule_params_json')
    if rule_params_json:
        if map_op == 'CONST':
            # CONST操作直接使用rule_params_json
            rule_params = rule_params_json
        elif rule_ref and len(rule_ref) > 0:
            # 其他操作从rule_params_json中获取对应规则的参数
            rule_params = rule_params_json.get(rule_ref[0], {})
```

**问题：** DEFAULT操作没有对应的分支，导致rule_params保持为空字典`{}`。

### 2. column_data_map映射问题

在`delivery_processor.py`和`customs_processor.py`的`_process_columns`方法中，column_data_map的构建逻辑有问题：

**原始代码：**
```python
column_data_map = {}
for col in column_data:
    col_source_cols = col.get('source_cols')
    if col_source_cols:
        column_data_map[col_source_cols] = col.get('data')
```

**问题：**
- `excel_reader.py`返回的`column_data`中，`source_cols`字段存储的是列字母（如"J"）
- 但`field_pipelines`中的`source_cols`存储的是表头名称（如"依頼主"）
- 导致`column_data_map`的key是列字母，而查找时用的是表头名称，查找失败
- 因此`source_value`总是为`None`，总是使用默认值

## 修复方案

### 1. 修复delivery_processor.py

#### 1.1 修复rule_params获取逻辑（第357-370行）

```python
# 获取规则参数
rule_params = {}
if pipeline:
    rule_params_json = pipeline.get('rule_params_json')
    if rule_params_json:
        if map_op == 'CONST':
            # CONST操作直接使用rule_params_json
            rule_params = rule_params_json
        elif map_op == 'DEFAULT':
            # DEFAULT操作：rule_params_json直接就是默认值
            rule_params = rule_params_json
        elif rule_ref and len(rule_ref) > 0:
            # 其他操作从rule_params_json中获取对应规则的参数
            rule_params = rule_params_json.get(rule_ref[0], {})
```

#### 1.2 修复column_data_map构建逻辑（第209-214行）

```python
# 构建列数据映射
# 建立表头名称到列字母的映射，以及列字母到数据的映射
header_to_col_letter = {}  # 表头 -> 列字母
col_letter_to_data = {}    # 列字母 -> 数据
for col in column_data:
    col_source_cols = col.get('source_cols')  # 列字母
    col_header = col.get('head')               # 表头名称
    if col_source_cols:
        col_letter_to_data[col_source_cols] = col.get('data')
        if col_header:
            header_to_col_letter[col_header] = col_source_cols

# 构建最终的column_data_map：表头名称 -> 数据
column_data_map = {}
for header, col_letter in header_to_col_letter.items():
    if col_letter in col_letter_to_data:
        column_data_map[header] = col_letter_to_data[col_letter]
```

### 2. 修复customs_processor.py

同样修复了`customs_processor.py`中的column_data_map构建逻辑（第315-319行）。

## 数据库配置

三列的配置已更新为DEFAULT操作：

| 列 | map_op | source_cols | rule_params_json (默认值) |
|----|--------|-------------|---------------------------|
| J (依頼主) | DEFAULT | ["依頼主"] | DIDA |
| K (依頼主住所) | DEFAULT | ["依頼主住所"] | 千葉県流山市平方8061GLPALFALINK81F13番シャッター |
| M (依頼主電話) | DEFAULT | ["依頼主電話"] | 0471377848 |

## 测试结果

### 测试文件

创建测试文件，包含3行数据：
- 第2行：J、K、M列为空
- 第3行：J、K、M列有值
- 第4行：J、K、M列为空

### 测试结果

```
第2行 (空值应使用默认值):
  J列(依頼主): 实际='DIDA', 期望='DIDA' [通过]
  K列(依頼主住所): 实际='千葉県流山市平方8061GLPALFALINK81F13番シャッター', 期望='千葉県流山市平方8061GLPALFALINK81F13番シャッター' [通过]
  M列(依頼主電話): 实际='0471377848', 期望='0471377848' [通过]

第3行 (有值应保持源值):
  J列(依頼主): 实际='別の依頼主', 期望='別の依頼主' [通过]
  K列(依頼主住所): 实际='東京都千代田区千代田1-1-1', 期望='東京都千代田区千代田1-1-1' [通过]
  M列(依頼主電話): 实际='03-1111-1111', 期望='03-1111-1111' [通过]

第4行 (空值应使用默认值):
  J列(依頼主): 实际='DIDA', 期望='DIDA' [通过]
  K列(依頼主住所): 实际='千葉県流山市平方8061GLPALFALINK81F13番シャッター', 期望='千葉県流山市平方8061GLPALFALINK81F13番シャッター' [通过]
  M列(依頼主電話): 实际='0471377848', 期望='0471377848' [通过]

[成功] DEFAULT操作测试通过！
```

## 修复的文件

1. `backend/app/services/delivery_processor.py`
   - 修复DEFAULT操作的rule_params获取逻辑
   - 修复column_data_map构建逻辑

2. `backend/app/services/customs_processor.py`
   - 修复column_data_map构建逻辑

## 工作原理

DEFAULT操作使用`copy_equal_to(source_value, default_value)`函数：
- 如果source_value为空（None或空字符串），返回default_value
- 否则返回source_value

这样可以确保：
1. 源文件中有值时，保持源值不变
2. 源文件中为空时，使用默认值

## 测试脚本

创建了以下测试脚本：
- `test_default_operation.py` - 测试DEFAULT操作的函数逻辑
- `debug_default_operation.py` - 调试DEFAULT操作的参数传递
- `create_delivery_test_with_empty_jkm.py` - 创建测试文件
- `test_delivery_jkm_processing.py` - 完整的流程测试

所有测试均通过！
