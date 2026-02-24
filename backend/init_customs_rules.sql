INSERT INTO rule_definitions (rule_ref, rule_type, executor_type, schema_json) 
VALUES 
/* ======================= 
    CONST 
    ======================= */ 
( 
   'const_value', 
   'CONST', 
   'program', 
   '{"type":"object","properties":{"value":{"type":["string","null"],"default":"","description":"constant output value; default empty string if omitted"},"null_strategy":{"type":"string","enum":["EMPTY_STRING","KEEP_NULL"],"default":"EMPTY_STRING"},"trim":{"type":"boolean","default":true}},"required":[]}' 
 ), 
 
/* ======================= 
    CALC - program 
    ======================= */ 
( DEEPSEEK_API_KEY: str = "your_deepseek_api_key_here"
EXCHANGE_RATE_API_KEY: str = "your_exchange_rate_api_key_here"
   'seq_from_1', 
   'CALC', 
   'program', 
   '{"type":"object","properties":{"start":{"type":"integer","default":1},"step":{"type":"integer","default":1}},"required":[]}' 
 ), 
( 
   'lookup_platform_code_with_default', 
   'CALC', 
   'program', 
   '{"type":"object","properties":{"mapping_source":{"type":"string","enum":["json","db","config"],"default":"db"},"default_code":{"type":"string","description":"code used when mapping not found"},"not_found_strategy":{"type":"string","enum":["use_default","error"],"default":"use_default"},"trim":{"type":"boolean","default":true}},"required":["default_code"]}' 
 ), 
( 
   'map_platform_name_from_code_with_default', 
   'CALC', 
   'program', 
   '{"type":"object","properties":{"mapping_source":{"type":"string","enum":["json","db","config"],"default":"db"},"default_name":{"type":"string","description":"name used when mapping not found"},"not_found_strategy":{"type":"string","enum":["use_default","error"],"default":"use_default"},"trim":{"type":"boolean","default":true}},"required":["default_name"]}' 
 ), 
 
/* ======================= 
    DEFAULT（空值兜底）- program 
    说明：rule_type 没用你枚举（没有 DEFAULT），这里放在 FORMAT 里实现 DEFAULT 语义 
    ======================= */ 
( 
   'default_if_empty', 
   'FORMAT', 
   'program', 
   '{"type":"object","properties":{"default_value":{"type":"string","description":"value used when input is empty"},"empty_values":{"type":"array","items":{"type":["string","null"]},"default":["",null]},"trim":{"type":"boolean","default":true}},"required":["default_value"]}' 
 ), 
 
/* ======================= 
    FORMAT - program 
    ======================= */ 
( 
   'remove_dash', 
   'FORMAT', 
   'program', 
   '{"type":"object","properties":{"chars":{"type":"array","items":{"type":"string"},"default":["-"]},"trim":{"type":"boolean","default":false}},"required":[]}' 
 ), 
( 
   'remove_brackets', 
   'FORMAT', 
   'program', 
   '{"type":"object","properties":{"chars":{"type":"array","items":{"type":"string"},"default":["(",")","（","）"]},"trim":{"type":"boolean","default":false}},"required":[]}' 
 ), 
 
/* ======================= 
    AI - ai 
    ======================= */ 
( 
   'ai_weight_infer', 
   'AI', 
   'ai', 
   '{"type":"object","properties":{"input_keys":{"type":"array","items":{"type":"string"},"default":["F","H","I"]},"unit":{"type":"string","enum":["kg"],"default":"kg"},"fallback":{"type":"string","enum":["error","keep_original","zero"],"default":"keep_original"},"max_weight":{"type":"number","default":50},"audit":{"type":"boolean","default":true}},"required":[]}' 
 ), 
( 
   'ai_goods_name_en', 
   'AI', 
   'ai', 
   '{"type":"object","properties":{"language_from":{"type":"string","default":"ja"},"language_to":{"type":"string","default":"en"},"max_length":{"type":"integer","default":60},"forbidden_chars":{"type":"array","items":{"type":"string"},"default":["/","\\\\"]},"audit":{"type":"boolean","default":true}},"required":[]}' 
 ), 
( 
   'ai_material_translate_and_map', 
   'AI', 
   'ai', 
   '{"type":"object","properties":{"language_from":{"type":"string","default":"ja"},"language_to":{"type":"string","default":"en"},"material_map_source":{"type":"string","enum":["builtin","db"],"default":"builtin"},"unknown_strategy":{"type":"string","enum":["keep","error"],"default":"keep"},"audit":{"type":"boolean","default":true}},"required":[]}' 
 ), 
( 
   'ai_receiver_name_clean_ja', 
   'AI', 
   'ai', 
   '{"type":"object","properties":{"remove_titles":{"type":"boolean","default":true},"normalize_kana":{"type":"boolean","default":true},"max_length":{"type":"integer","default":40},"audit":{"type":"boolean","default":true}},"required":[]}' 
 ), 
( 
   'ai_receiver_address_compose_ja', 
   'AI', 
   'ai', 
   '{"type":"object","properties":{"format":{"type":"string","enum":["jp_standard","intl"],"default":"jp_standard"},"max_length":{"type":"integer","default":200},"fallback":{"type":"string","enum":["error","keep_original","empty"],"default":"keep_original"},"audit":{"type":"boolean","default":true}},"required":[]}' 
 );
