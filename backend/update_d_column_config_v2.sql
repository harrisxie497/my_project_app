-- 修改D列的配置，使用更宽松的条件

UPDATE field_pipelines
SET source_cols = '["D"]'
WHERE target_col = 'D'
  AND file_type = 'CUSTOMS'
  AND map_op = 'COPY'
  AND field_type = 'CALC'
  AND rule_ref LIKE '%policy_copy_equal_to%';
