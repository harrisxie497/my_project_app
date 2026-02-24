# DELIVERY规则定义检查报告

## 检查日期
2026-02-07

## 检查内容
DELIVERY的FieldPipeline中引用的rule_definitions是否存在

## 检查结果

### ✅ FieldPipelines配置
DELIVERY共有17个FieldPipeline配置，所有配置都使用简单操作：

| 列 | 表头 | map_op | rule_ref | 说明 |
|-----|-------|---------|----------|------|
| A | お客様管理番号 | COPY | [] | 直接复制 |
| B | 佐川問合せ番号HAWB | COPY | [] | 直接复制 |
| C | 配達指定日 | COPY | [] | 直接复制 |
| D | 時間帯指定 | COPY | [] | 直接复制 |
| E | 貨物個数 | COPY | [] | 直接复制 |
| F | お届け先人名 | COPY | [] | 直接复制 |
| G | お届け先住所 | COPY | [] | 直接复制 |
| H | お届け先電話 | COPY | [] | 直接复制 |
| I | お届け先郵便 | COPY | [] | 直接复制 |
| J | 依頼主 | COPY | [] | 直接复制 |
| K | 依頼主住所 | COPY | [] | 直接复制 |
| L | 依頼主郵便番号 | COPY | [] | 直接复制 |
| M | 依頼主電話 | COPY | [] | 直接复制 |
| N | 佐川顧客コード（固定） | CONST | [] | 固定值 |
| O | 記事欄2（品名） | COPY | [] | 直接复制 |
| P | 記事欄2 | COPY | [] | 直接复制 |
| Q | 記事欄3 | COPY | [] | 直接复制 |

**关键发现：所有FieldPipeline的rule_ref都是空数组[]，没有引用任何规则**

### ✅ 规则引用检查
- **引用的规则总数**: 0
- **缺失的规则数**: 0
- **结论**: DELIVERY不需要引用任何规则定义

### 📊 数据库中的RuleDefinitions
数据库中共有17个启用的规则定义：

#### AI规则（6个）
| rule_ref | 类型 | 描述 |
|----------|------|------|
| policy_ai_decimal_fix | AI | 重量：按品名/材质/原重量进行合理修正，输出两位小数 |
| policy_ai_goods_en | AI | 品名：去括号备注→英译→大写→去冗余 |
| policy_ai_material_en | AI | 材质：去括号备注→英译大写→材质替换表置换 |
| policy_ai_text_dress_clean | AI | 收件人名（日文）清洗：去括号备注 |
| policy_ai_text_ja_clean | AI | 收件人名（日文）清洗：去括号备注 |
| policy_translate_from_targetcol_en_upper | AI | 从目标列（X/Y）翻译为英文并大写 |

#### 计算规则（3个）
| rule_ref | 类型 | 描述 |
|----------|------|------|
| policy_calc_invoice_price_fx_round | CALC | インボイス価格：实时汇率×单价取整 |
| policy_copy_equal_to | CALC | 复制源值后校验：与指定目标列完全一致 |
| policy_seq_from_1 | CALC | 生成连续递增序号（从 start 开始，步长 step） |

#### 格式化规则（6个）
| rule_ref | 类型 | 描述 |
|----------|------|------|
| policy_copy_one_decimal | FORMAT | 复制源值：保留1位小数 |
| policy_copy_optional_decimal | FORMAT | 复制源值：可配置是否允许为空 |
| policy_copy_regex | FORMAT | 复制源值→可选去"-"→按正则校验 |
| policy_default_copy | FORMAT | 复制源值；为空则使用默认值兜底 |
| **policy_format_date_yyyy_mm_dd** | FORMAT | **配達指定日：格式化为 YYYY-MM-DD** |
| **policy_time_slot_conditional** | FORMAT | **時間帯指定：C非空→范围00-99且0→00；C为空→原值保持，若为0则置空** |

#### 常量规则（1个）
| rule_ref | 类型 | 描述 |
|----------|------|------|
| policy_const | CONST | 输出固定值（含预留列置空） |

#### 校验规则（1个）
| rule_ref | 类型 | 描述 |
|----------|------|------|
| policy_required_input | RULE_FIX | 外部输入列必填校验 |

### 🔍 DELIVERY相关规则
通过规则描述，发现有2个规则与DELIVERY相关：

1. **policy_format_date_yyyy_mm_dd**
   - 类型: FORMAT
   - 描述: 配達指定日：格式化为 YYYY-MM-DD
   - 当前状态: 未被DELIVERY的FieldPipeline引用

2. **policy_time_slot_conditional**
   - 类型: FORMAT
   - 描述: 時間帯指定：C非空→范围00-99且0→00；C为空→原值保持，若为0则置空
   - 当前状态: 未被DELIVERY的FieldPipeline引用

## 总结

### ✅ 当前状态
- **无规则引用**: DELIVERY的所有17个FieldPipeline都没有引用任何规则
- **操作简单**: 所有列都使用简单的COPY或CONST操作
- **无需额外规则**: 当前的配置已经可以满足基本的DELIVERY文件处理需求

### 💡 可选优化建议

如果需要更复杂的处理，可以考虑使用以下规则：

1. **配達指定日格式化**
   - 当前: COPY（直接复制）
   - 建议: 使用 `policy_format_date_yyyy_mm_dd` 规则
   - 作用: 统一日期格式为 YYYY-MM-DD

2. **時間帯指定处理**
   - 当前: COPY（直接复制）
   - 建议: 使用 `policy_time_slot_conditional` 规则
   - 作用: 规范时间格式（00-99范围处理）

3. **電話号码格式化**
   - 当前: COPY（直接复制）
   - 可选: 创建或使用现有的电话号码格式化规则

### 📋 配置修改示例

如果需要使用规则，可以修改FieldPipeline配置：

**示例1: 配達指定日格式化**
```json
{
  "target_col": "C",
  "target_header": "配達指定日",
  "map_op": "FORMAT",
  "source_cols": ["配達指定日"],
  "rule_ref": ["policy_format_date_yyyy_mm_dd"],
  "field_type": "TEXT"
}
```

**示例2: 時間帯指定处理**
```json
{
  "target_col": "D",
  "target_header": "時間帯指定",
  "map_op": "FORMAT",
  "source_cols": ["時間帯指定"],
  "rule_ref": ["policy_time_slot_conditional"],
  "field_type": "TEXT"
}
```

## 结论

✅ **DELIVERY的FieldPipeline配置正确，无需引用任何规则**

- 所有17个FieldPipeline配置都是简单的COPY或CONST操作
- 数据库中有完整的规则定义可供使用（如果需要）
- 当前配置已满足基本的DELIVERY文件处理需求
- 如需更复杂的处理，可以按需添加规则引用

## 相关文件
- 检查脚本: `check_delivery_rule_definitions.py`
- 测试脚本: `test_delivery_task_with_mysql.py`
- 配置脚本: `init_delivery_pipelines.py`
