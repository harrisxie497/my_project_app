# 任务处理流程文档

## 整体流程

```
1. 读取Excel文件 (excel_reader.py)
   ↓
2. 获取field_pipelines配置 (customs_processor.py)
   ↓
3. 按order_num排序处理列
   ↓
4. 对每一列，根据配置调用相应的处理函数
   ↓
5. 输出处理后的列数据
   ↓
6. 写入Excel文件 (excel_writer.py)
```

## 详细流程

### 1. 读取Excel文件 (excel_reader.py)

**输入**:
- file_path: Excel文件路径
- file_type: 文件类型 (CUSTOMS/DELIVERY)
- file_role: 文件角色 (SOURCE/TARGET)

**输出**:
```python
{
    'data_row_count': 124,  # 数据行数
    'column_data': [  # 列数据列表
        {
            'source_cols': 'A',  # 源列名
            'head': '列标题',  # 列标题
            'data': [...],  # 列数据列表
            'len': 124  # 数据长度
        },
        ...
    ]
}
```

### 2. 获取field_pipelines配置 (customs_processor.py)

**输入**:
- file_type: 文件类型 (CUSTOMS/DELIVERY)
- db_session: 数据库会话

**输出**:
```python
[
    {
        'target_col': 'A',  # 目标列名
        'target_header': '列标题',  # 目标列标题
        'map_op': 'COPY',  # 映射操作类型
        'source_cols': ['A'],  # 源列列表
        'field_type': 'COPY',  # 字段类型
        'rule_ref': ['policy_copy_regex'],  # 规则引用
        'rule_params_json': {  # 规则参数
            'policy_copy_regex': {
                'regex': '^\\d+$',
                'required': True,
                'remove_dash': False
            }
        },
        'depends_on': [],  # 依赖列
        'order_num': 10  # 处理顺序
    },
    ...
]
```

### 3. 按order_num排序处理列

**输入**:
- field_pipelines: 字段处理配置列表
- column_data: 原始列数据
- data_row_count: 数据行数

**输出**:
```python
[
    {
        'target_col': 'A',  # 目标列名
        'head': '列标题',  # 目标列标题
        'data': [...],  # 处理后的列数据
        'len': 124  # 数据长度
    },
    ...
]
```

### 4. 每一列处理函数

根据map_op、field_type、rule_ref等配置，调用相应的处理函数。

#### 4.1 COPY操作

**输入**:
- source_value: 源值
- rule_params: 规则参数

**处理函数**:
- `normalize.copy_then_regex`: 复制源值→可选去"-"→按正则校验
- `normalize.copy_optional_decimal`: 复制源值：可配置是否允许为空；非空时按正则校验
- `normalize.copy_default_if_empty`: 复制源值；为空则使用默认值兜底

**输出**:
- 处理后的值

#### 4.2 CONST操作

**输入**:
- rule_params: 规则参数

**处理函数**:
- `assign.const`: 设置常量值

**输出**:
- 常量值

#### 4.3 CALC操作

**输入**:
- row_index: 行索引
- rule_params: 规则参数

**处理函数**:
- `calc.seq_from_1`: 生成连续递增序号（从 start 开始，步长 step）
- `calc.invoice_price_fx_round`: 计算インボイス価格（汇率换算）

**输出**:
- 计算后的值

#### 4.4 AI操作（批量处理）

**输入**:
- input_data_list: 输入数据列表（多行）
- rule_params: 规则参数

**处理函数**:
- `ai.goods_name_en`: 品名：去括号备注→英译→大写→去冗余
- `ai.material_translate_and_substitute`: 材质：去括号备注→英译大写→材质替换表置换
- `ai.ja_name_clean`: 收件人名（日文）清洗：去括号备注，输出更像常见日本名字
- `ai.decimal_fix`: 重量：按品名/材质/原重量进行合理修正，输出两位小数

**输出**:
- 处理后的值列表

#### 4.5 FORMAT操作

**输入**:
- source_value: 源值
- rule_params: 规则参数

**处理函数**:
- `format.date_to_yyyy_mm_dd`: 配達指定日：格式化为 YYYY-MM-DD
- `format.delivery_time_slot_conditional`: 時間帯指定：C非空→范围00-99且0→00；C为空→原值保持

**输出**:
- 格式化后的值

#### 4.6 VALIDATE操作

**输入**:
- source_value: 源值
- target_value: 目标列值
- rule_params: 规则参数

**处理函数**:
- `validate.copy_then_equal_to_target_col`: 复制源值后校验：与指定目标列完全一致
- `validate.required_input`: 外部输入列必填校验

**输出**:
- 校验后的值

### 5. 写入Excel文件 (excel_writer.py)

**输入**:
- file_path: 输出文件路径
- column_data: 处理后的列数据

**输出**:
- 写入的Excel文件

## 处理函数详细说明

### 1. assign.const

**输入**:
```python
{
    'value': 'DIDA'  # 常量值
}
```

**输出**:
```python
'DIDA'
```

### 2. calc.seq_from_1

**输入**:
```python
{
    'row_index': 0,  # 行索引（从0开始）
    'step': 1,  # 步长（默认 1）
    'start': 1  # 起始值（默认 1）
}
```

**输出**:
```python
1  # 第一行
2  # 第二行
3  # 第三行
...
```

### 3. calc.invoice_price_fx_round

**输入**:
```python
{
    'original_price': 100.0,  # 原始价格
    'currency_code': 'USD',  # 货币代码
    'exchange_rate_service': ExchangeRateService,  # 汇率服务
    'regex': '^\\d+$'  # 输出校验正则表达式
}
```

**输出**:
```python
15000  # 日元价格（取整）
```

### 4. normalize.copy_then_regex

**输入**:
```python
{
    'source_value': '123-456-7890',  # 源值
    'regex': '^\\d{10}$',  # 正则表达式（必填）
    'required': True,  # 是否必填
    'remove_dash': True  # 是否移除连接符"-"
}
```

**输出**:
```python
'1234567890'  # 移除横杠后的值
```

### 5. normalize.copy_optional_decimal

**输入**:
```python
{
    'source_value': '123.45',  # 源值
    'regex': '^\\d+\\.\\d{2}$',  # 非空时的正则表达式
    'allow_null': True  # 是否允许为空（默认 true）
}
```

**输出**:
```python
'123.45'  # 验证通过的小数
```

### 6. normalize.copy_default_if_empty

**输入**:
```python
{
    'source_value': '',  # 源值（空）
    'default_value': 'DIDA',  # 默认值（必填）
    'remove_dash': False  # 是否移除连接符"-"
}
```

**输出**:
```python
'DIDA'  # 使用默认值
```

### 7. format.date_to_yyyy_mm_dd

**输入**:
```python
{
    'date_value': '2025/02/06',  # 日期值
    'input_formats': None,  # 可选：允许的输入日期格式列表
    'required': False  # 是否必填（默认 false）
}
```

**输出**:
```python
'2025-02-06'  # 格式化后的日期
```

### 8. format.delivery_time_slot_conditional

**输入**:
```python
{
    'source_value': '0',  # 源值（D列）
    'date_target_value': '2025-02-06',  # 依赖的日期列值（C列）
    'zero_value': '0',  # 被视为0的取值（默认 "0"）
    'when_date_empty_zero_to': '',  # C为空且D=0时替换值（默认 ""）
    'when_date_present_zero_to': '00',  # C非空且D=0时替换值（默认 "00"）
    'range_regex_when_date_present': '^\\d{2}$'  # C非空时的范围验证正则
}
```

**输出**:
```python
'00'  # 处理后的值
```

### 9. validate.copy_then_equal_to_target_col

**输入**:
```python
{
    'source_value': '',  # 源值（空）
    'target_value': '123456',  # 目标列值（C列）
    'equal_to_target_col': 'C'  # 对齐的目标列
}
```

**输出**:
```python
'123456'  # 复制目标列的值
```

### 10. validate.required_input

**输入**:
```python
{
    'source_value': '',  # 源值
    'required': True,  # 是否必填（默认 true）
    'error_message': '值为必填项'  # 自定义错误提示（可选）
}
```

**输出**:
```python
ValueError('值为必填项')  # 如果值为空且必填
```

### 11. ai.goods_name_en（批量处理）

**输入**:
```python
[
    {'H': '日文品名1'},
    {'H': '日文品名2'},
    ...
]
```

**输出**:
```python
[
    'ENGLISH GOODS NAME 1',
    'ENGLISH GOODS NAME 2',
    ...
]
```

### 12. ai.material_translate_and_substitute（批量处理）

**输入**:
```python
[
    {'I': '日文材质1'},
    {'I': '日文材质2'},
    ...
]
```

**输出**:
```python
[
    'COTTON',
    'POLYESTER',
    ...
]
```

### 13. ai.ja_name_clean（批量处理）

**输入**:
```python
[
    {'AD': '日文收件人名1'},
    {'AD': '日文收件人名2'},
    ...
]
```

**输出**:
```python
[
    '清理后的日文名1',
    '清理后的日文名2',
    ...
]
```

### 14. ai.decimal_fix（批量处理）

**输入**:
```python
[
    {'F': '1.23', 'H': '品名1', 'I': '材质1'},
    {'F': '2.34', 'H': '品名2', 'I': '材质2'},
    ...
]
```

**输出**:
```python
[
    1.23,
    2.34,
    ...
]
```

## 总结

整个任务处理流程如下：

1. **读取Excel文件** → 获取原始数据
2. **获取field_pipelines配置** → 获取列处理配置
3. **按order_num排序处理列** → 按顺序处理列
4. **对每一列，根据配置调用相应的处理函数** → 处理列数据
   - COPY操作 → 复制源值并验证
   - CONST操作 → 设置常量值
   - CALC操作 → 计算值
   - AI操作（批量）→ 调用AI批量处理
   - FORMAT操作 → 格式化值
   - VALIDATE操作 → 验证值
5. **输出处理后的列数据** → 输出结果
6. **写入Excel文件** → 保存结果

**关键优化**:
- AI规则使用批量处理，一列只调用一次DeepSeek API，大大提高效率
- 按order_num排序处理列，确保处理顺序正确
- 支持依赖列，确保依赖列先处理
