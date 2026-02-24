```sql
/* =========================================================
   rule_definitions（schema_json 极简：handler/desc/configurable_params）
   你要求的“可配置项”补齐版本：
   - policy_seq_from_1：开放 start/step
   - policy_copy_regex：开放 regex/remove_dash/required
   - policy_copy_optional_decimal：开放 allow_null/regex（可选 scale 也可开放，这里按你要求不强加）
   - policy_calc_invoice_price_fx_round：开放 regex（用于最终输出校验）
   其他：AI 只开放 system_prompt；固定值/跨列一致维持不变
   ========================================================= */

DELETE FROM rule_definitions
WHERE rule_ref IN (
  'policy_const',
  'policy_seq_from_1',
  'policy_copy_regex',
  'policy_copy_equal_to',
  'policy_copy_optional_decimal',
  'policy_copy_optional_text',
  'policy_default_copy',
  'policy_ai_decimal_fix',
  'policy_ai_goods_en',
  'policy_ai_material_en',
  'policy_ai_text_ja_clean',
  'policy_translate_from_targetcol_en_upper',
  'policy_calc_invoice_price_fx_round'
);

INSERT INTO rule_definitions (rule_ref, rule_type, executor_type, schema_json, enabled)
VALUES

/* ---------------- 固定值 ---------------- */
('policy_const','CONST','program',
 JSON_OBJECT(
   'handler','assign.const',
   'desc','输出固定值（含预留列置空）',
   'configurable_params', JSON_OBJECT(
     'value','固定值'
   )
 ),
 1),

/* ---------------- 序号 ---------------- */
('policy_seq_from_1','CALC','program',
 JSON_OBJECT(
   'handler','calc.seq_from_1',
   'desc','生成连续递增序号（从 start 开始，步长 step）',
   'configurable_params', JSON_OBJECT(
     'start','起始值（默认 1）',
     'step','步长（默认 1）'
   )
 ),
 1),

/* ---------------- COPY + regex ---------------- */
('policy_copy_regex','FORMAT','program',
 JSON_OBJECT(
   'handler','normalize.copy_then_regex',
   'desc','复制源值→可选去“-”→按正则校验（可配置是否必填）',
   'configurable_params', JSON_OBJECT(
     'regex','正则表达式（必填）',
     'remove_dash','是否移除连接符“-”',
     'required','是否必填'
   )
 ),
 1),

/* ---------------- COPY + 跨列一致 ---------------- */
('policy_copy_equal_to','CALC','program',
 JSON_OBJECT(
   'handler','validate.copy_then_equal_to_target_col',
   'desc','复制源值后校验：与指定目标列完全一致（跨列一致性）',
   'configurable_params', JSON_OBJECT(
     'equal_to_target_col','对齐的目标列（如 C）'
   )
 ),
 1),

/* ---------------- COPY 可空小数 ---------------- */
('policy_copy_optional_decimal','FORMAT','program',
 JSON_OBJECT(
   'handler','normalize.copy_optional_decimal',
   'desc','复制源值：可配置是否允许为空；非空时按正则校验（用于两位小数等）',
   'configurable_params', JSON_OBJECT(
     'allow_null','是否允许为空（默认 true）',
     'regex','非空时的正则表达式（如 ^\\d+\\.\\d{2}$ ）'
   )
 ),
 1),

/* ---------------- COPY 文本 ---------------- */
('policy_copy_optional_text','FORMAT','program',
 JSON_OBJECT(
   'handler','normalize.copy_optional_text',
   'desc','复制源文本：可配置是否允许为空（可选trim由后台实现）',
   'configurable_params', JSON_OBJECT(
     'allow_null','是否允许为空（默认 true）'
   )
 ),
 1),

/* ---------------- COPY + 空值兜底 ---------------- */
('policy_default_copy','FORMAT','program',
 JSON_OBJECT(
   'handler','normalize.copy_default_if_empty',
   'desc','复制源值；为空则使用默认值兜底（可选先去“-”）',
   'configurable_params', JSON_OBJECT(
     'default_value','默认值（必填）',
     'remove_dash','是否移除连接符“-”'
   )
 ),
 1),

/* ---------------- AI：只开放系统提示词 ---------------- */
('policy_ai_decimal_fix','AI','ai',
 JSON_OBJECT(
   'handler','ai.decimal_fix',
   'desc','重量：按品名/材质/原重量进行合理修正，输出两位小数（后台固定流程）',
   'configurable_params', JSON_OBJECT(
     'system_prompt','系统提示词'
   )
 ),
 1),

('policy_ai_goods_en','AI','ai',
 JSON_OBJECT(
   'handler','ai.goods_name_en',
   'desc','品名：去括号备注→英译→大写→去冗余（后台固定流程）',
   'configurable_params', JSON_OBJECT(
     'system_prompt','系统提示词'
   )
 ),
 1),

('policy_ai_material_en','AI','ai',
 JSON_OBJECT(
   'handler','ai.material_translate_and_substitute',
   'desc','材质：去括号备注→英译大写→材质替换表置换（后台固定流程）',
   'configurable_params', JSON_OBJECT(
     'system_prompt','系统提示词'
   )
 ),
 1),

('policy_ai_text_ja_clean','AI','ai',
 JSON_OBJECT(
   'handler','ai.ja_name_clean',
   'desc','收件人名（日文）清洗：去括号备注，输出更像常见日本名字（后台固定流程）',
   'configurable_params', JSON_OBJECT(
     'system_prompt','系统提示词'
   )
 ),
 1),

('policy_translate_from_targetcol_en_upper','AI','ai',
 JSON_OBJECT(
   'handler','ai.translate_from_targetcol_to_en_upper',
   'desc','从目标列（X/Y）翻译为英文并大写（后台固定流程）',
   'configurable_params', JSON_OBJECT(
     'system_prompt','系统提示词'
   )
 ),
 1),

/* ---------------- 汇率加工：开放输出 regex 校验 ---------------- */
('policy_calc_invoice_price_fx_round','CALC','program',
 JSON_OBJECT(
   'handler','calc.invoice_price_fx_round',
   'desc','インボイス価格：实时汇率×单价取整，并支持外部总价覆盖（后台实现）；可配置输出正则校验',
   'configurable_params', JSON_OBJECT(
     'regex','输出校验正则表达式（例如整数：^\\d+$）'
   )
 ),
 1);
```

