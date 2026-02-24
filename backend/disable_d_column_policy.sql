-- 禁用D列的policy_copy_equal_to规则，避免无限循环

UPDATE field_pipelines
SET enabled = 0
WHERE target_col = 'D'
  AND file_type = 'CUSTOMS'
  AND map_op = 'COPY'
  AND field_type = 'CALC'
  AND rule_ref = '["policy_copy_equal_to"]'
  AND enabled = 1;
