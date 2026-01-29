-- 初始化D列（时间帯指定）配置的SQL脚本
-- 使用方法：sqlite3 app.db < init_d_column_config.sql

-- 1. 先检查是否存在规则表，如果不存在则创建
INSERT OR IGNORE INTO rule_tables (id, code, name, file_type, rule_stage, enabled, description, created_at, updated_at)
VALUES (
    'delivery-process-rule-table',
    'delivery-process-rule',
    '派送文件处理规则表',
    'DELIVERY',
    'PROCESS',
    1,
    '派送文件处理阶段的规则表',
    datetime('now'),
    datetime('now')
);

-- 2. 插入D列的规则项
INSERT OR REPLACE INTO rule_items (
    id,
    rule_table_id,
    enabled,
    order_no,
    target_column,
    target_field_name,
    map_op,
    source_column,
    field_type,
    process_depends_on,
    process_rules_json,
    executor,
    on_fail,
    note,
    created_at,
    updated_at
) VALUES (
    'd-column-rule-item',
    'delivery-process-rule-table',
    1,
    3,
    'D',
    '時間帯指定',
    'COPY',
    'D',
    'FORMAT',
    'C,D',
    '{"transformation_type": "conditional_expr", "target_col": "D", "rules": [{"when": "C != '''''' && (D == 0 || D == ''''0'''')", "set": "00"}, {"when": "C == '''''' && (D == 0 || D == ''''0'''')", "set": ""}], "else": "KEEP"}',
    'program',
    'BLOCK',
    'D列条件表达式规则配置',
    datetime('now'),
    datetime('now')
);

-- 3. 验证插入结果
SELECT * FROM rule_items WHERE target_column = 'D';
