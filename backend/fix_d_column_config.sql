-- 修复D列的配置，将source_cols从空数组改为['C']

UPDATE field_pipelines
SET source_cols = '["C"]'
WHERE target_col = 'D'
  AND file_type = 'CUSTOMS'
  AND map_op = 'COPY'
  AND field_type = 'CALC'
  AND rule_ref = '["policy_copy_equal_to"]'
  AND enabled = 1;
