-- 更新电话号码的正则表达式

-- 更新輸入者電話番号列的正则表达式
UPDATE field_pipelines
SET rule_params_json = JSON_SET(rule_params_json, '$.policy_copy_regex.regex', '^0\\d{9,11}$')
WHERE target_header = '輸入者電話番号'
  AND file_type LIKE '%CUSTOMS%';

-- 更新收件人电话列的正则表达式
UPDATE field_pipelines
SET rule_params_json = JSON_SET(rule_params_json, '$.policy_copy_regex.regex', '^0\\d{9,11}$')
WHERE target_header = '收件人电话'
  AND file_type LIKE '%CUSTOMS%';
