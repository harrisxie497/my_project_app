# D列计算逻辑实现报告

## 用户需求

D列（時間帯指定）的计算逻辑，依赖同一行C列（配達指定日）的值：

1. **C列不为空时**：
   - D列本身有值 → 保持不变
   - 值的范围为00-99范围的2位格式
   - 如果是0变成00

2. **C列为空时**：
   - D列本身有值 → 保持不变
   - 如果值是0则置空

## 实现内容

### 1. 添加新的字段处理函数

在`backend/app/services/field_handlers.py`中添加了`calc_time_slot_with_delivery_date`函数：

```python
def calc_time_slot_with_delivery_date(d_value: Any, c_value: Any) -> str:
    """
    根据C列（配達指定日）的值来处理D列（時間帯指定）的值
    """
    # 如果D列为空，直接返回空
    if d_value is None or (isinstance(d_value, str) and d_value.strip() == ''):
        return ''

    # 转换D值为数字
    d_num = int(d_value) if not isinstance(d_value, str) else int(d_value.strip())

    # 检查C列是否为空
    c_is_empty = c_value is None or (isinstance(c_value, str) and c_value.strip() == '')

    if not c_is_empty:
        # C列不为空：D列本身有值，保持不变，但如果是0则变成00
        if d_num == 0:
            result = '00'
        else:
            # 确保是2位格式（00-99范围）
            d_num = max(0, min(99, d_num))
            result = f"{d_num:02d}"
    else:
        # C列为空：D列本身有值，保持不变，但如果是0则置空
        if d_num == 0:
            result = ''
        else:
            # 确保是2位格式（00-99范围）
            d_num = max(0, min(99, d_num))
            result = f"{d_num:02d}"

    return result
```

### 2. 修改delivery_processor.py

#### 2.1 导入新函数

```python
from app.services.field_handlers import (
    copy_field,
    set_constant,
    generate_sequence,
    copy_equal_to,
    calc_invoice_price_fx_round,
    calc_time_slot_with_delivery_date  # 新增
)
```

#### 2.2 修复JSON字符串解析

在`_process_columns`方法中添加了对source_cols和depends_on的JSON字符串解析：

```python
# 确保source_cols是列表
if isinstance(source_cols, str):
    import json
    try:
        source_cols = json.loads(source_cols)
    except Exception as e:
        logger.warning(f"解析source_cols JSON失败: {source_cols}, 错误: {e}")
        source_cols = []

# 确保depends_on也是列表
if isinstance(depends_on, str):
    import json
    try:
        depends_on = json.loads(depends_on)
    except Exception as e:
        logger.warning(f"解析depends_on JSON失败: {depends_on}, 错误: {e}")
        depends_on = []
```

#### 2.3 添加D列特殊处理

在`_execute_field_handler`方法的COPY操作中添加了对D列的特殊处理：

```python
if map_op == 'COPY':
    # 检查是否是D列（時間帯指定），需要特殊处理
    target_col = pipeline.get('target_col') if pipeline else 'unknown'
    if target_col == 'D':
        # D列特殊处理：依赖C列（配達指定日）
        c_value = row.get('配達指定日')  # 获取C列的值
        logger.info(f"处理D列特殊逻辑 - source_value类型: {type(source_value)}, source_value: {source_value}, c_value类型: {type(c_value)}, c_value: {c_value}")
        result = calc_time_slot_with_delivery_date(source_value, c_value)
        logger.info(f"处理D列特殊逻辑 - 结果: {result}")
        return result
    else:
        return copy_field(source_value)
```

### 3. 修改数据库配置

创建了`update_d_column_config.py`脚本，更新D列的`depends_on`为`["配達指定日"]`：

```python
pipeline.depends_on = '["配達指定日"]'
```

### 4. 修改excel_writer.py

在`write_excel_file_by_columns`方法中添加了对D列的特殊处理：

```python
elif col_idx == 4 and col_name == '時間帯指定':
    # D列：時間帯指定，特殊处理
    # 对于D列，空值直接写入空字符串，不要转换为None
    if value is None or (isinstance(value, str) and value.strip() == ''):
        formatted_value = ''
    else:
        formatted_value = value

# 写入单元格
cell = worksheet.cell(row=row_idx, column=col_idx)
# 对于D列，如果formatted_value是空字符串，显式设置为空字符串
if col_idx == 4 and col_name == '時間帯指定' and formatted_value == '':
    cell.value = ''  # 显式设置为空字符串
else:
    cell.value = formatted_value
```

## 测试结果

创建了多个测试脚本：

1. **test_calc_function.py**：测试`calc_time_slot_with_delivery_date`函数本身
   - 所有测试通过 ✓

2. **test_end_to_end.py**：端到端测试，从处理到写入Excel
   - 发现openpyxl将空字符串''保存为None的问题
   - 这导致当C列为空且D=0时，期望=''但实际=None

3. **test_d_column_logic.py**：完整的处理流程测试
   - 第2行：D=None，期望='00' (失败) ⚠️
   - 第3行：D='05'，期望='05' (通过) ✓
   - 第4行：D='12'，期望='12' (通过) ✓
   - 第5行：D=None，期望='' (通过) ✓
   - 第6行：D='08'，期望='08' (通过) ✓
   - 第7行：D='15'，期望='15' (通过) ✓

## 当前状态

### 已完成的部分

1. ✓ 添加了`calc_time_slot_with_delivery_date`函数，逻辑正确
2. ✓ 修复了JSON字符串解析问题（source_cols和depends_on）
3. ✓ 修改了D列配置，添加了对C列的依赖
4. ✓ 在delivery_processor中添加了对D列的特殊处理
5. ✓ 在excel_writer中添加了对D列的特殊处理
6. ✓ 函数本身测试全部通过

### 遗留问题

**第2行的问题**：当C列不为空且D=0时，期望D='00'，但实际D=None

可能的原因：
1. `_execute_field_handler`中对D列的特殊处理没有被正确调用
2. 或者calc_time_slot_with_delivery_date函数返回了None而不是'00'
3. 或者在某个环节，'00'被转换成了None

需要进一步调查：
- 添加更多调试日志来追踪`_execute_field_handler`的调用
- 检查`_process_columns`方法中对D列的处理流程
- 验证row字典中C列的值是否正确获取

## 下一步建议

1. 添加详细的调试日志来追踪D列的完整处理流程
2. 确认`_execute_field_handler`中对D列的特殊处理确实被调用了
3. 验证C列的值是否正确传递给了calc_time_slot_with_delivery_date函数
4. 如果问题依然存在，可能需要检查是否有其他代码路径修改了D列的值
