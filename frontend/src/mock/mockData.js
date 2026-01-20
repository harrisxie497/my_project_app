// Mock数据配置

// 任务列表mock数据
export const mockTasks = [
  { id: "t_001", file_type: "customs", unique_code: "UC001", flight_no: "NH123", declare_date: "2026-01-20", status: "success", created_at: "2026-01-20T01:02:03Z" },
  { id: "t_002", file_type: "delivery", unique_code: "UC002", flight_no: "", declare_date: "", status: "failed", created_at: "2026-01-20T02:10:11Z" },
  { id: "t_003", file_type: "customs", unique_code: "UC003", flight_no: "JL777", declare_date: "2026-01-19", status: "processing", created_at: "2026-01-20T03:33:09Z" },
  { id: "t_004", file_type: "customs", unique_code: "UC004", flight_no: "CA987", declare_date: "2026-01-18", status: "success", created_at: "2026-01-19T10:20:30Z" },
  { id: "t_005", file_type: "delivery", unique_code: "UC005", flight_no: "", declare_date: "", status: "queued", created_at: "2026-01-20T15:45:00Z" }
];

// 任务详情mock数据
export const mockTaskDetail = {
  id: "t_001",
  file_type: "customs",
  unique_code: "UC001",
  flight_no: "NH123",
  declare_date: "2026-01-20",
  status: "success",
  created_at: "2026-01-20T01:02:03Z",
  files: [
    { name: "原始文件.xlsx", type: "original", url: "/mock/files/original.xlsx" },
    { name: "结果文件.xlsx", type: "result", url: "/mock/files/result.xlsx" },
    { name: "对比文件.xlsx", type: "diff", url: "/mock/files/diff.xlsx" },
    { name: "变化统计.xlsx", type: "stats", url: "/mock/files/stats.xlsx" }
  ],
  logs: [
    { time: "2026-01-20T01:02:03Z", message: "任务创建成功", level: "info" },
    { time: "2026-01-20T01:02:05Z", message: "开始处理", level: "info" },
    { time: "2026-01-20T01:03:10Z", message: "模板映射完成", level: "info" },
    { time: "2026-01-20T01:04:25Z", message: "字段映射完成", level: "info" },
    { time: "2026-01-20T01:05:40Z", message: "AI处理完成", level: "info" },
    { time: "2026-01-20T01:06:55Z", message: "样式应用完成", level: "info" },
    { time: "2026-01-20T01:07:00Z", message: "任务处理成功", level: "success" }
  ]
};

// 规则表mock数据
export const mockRuleTables = [
  { id: "rt_1", code: "MAP_CUSTOMS", file_type: "customs", rule_stage: "MAP", enabled: true, description: "原始→最终字段映射（清关）" },
  { id: "rt_2", code: "PROCESS_CUSTOMS", file_type: "customs", rule_stage: "PROCESS", enabled: true, description: "最终文件字段校验/修正/生成（清关）" },
  { id: "rt_3", code: "MAP_DELIVERY", file_type: "delivery", rule_stage: "MAP", enabled: true, description: "原始→最终字段映射（派送）" },
  { id: "rt_4", code: "PROCESS_DELIVERY", file_type: "delivery", rule_stage: "PROCESS", enabled: true, description: "最终文件字段校验/修正/生成（派送）" },
  { id: "rt_5", code: "RULE_FIX_CUSTOMS", file_type: "customs", rule_stage: "RULE_FIX", enabled: true, description: "规则修正（清关）" },
  { id: "rt_6", code: "CALC_CUSTOMS", file_type: "customs", rule_stage: "CALC", enabled: true, description: "字段计算（清关）" }
];

// 模板映射mock数据
export const mockTemplateMappings = [
  { id: "tm_1", mapping_code: "CUSTOMS_V1", file_type: "customs", sheet_match_mode: "name", sheet_match_value: "Sheet1", column_bindings_json: '{"A":"product_name","B":"product_code"}', enabled: true },
  { id: "tm_2", mapping_code: "DELIVERY_V1", file_type: "delivery", sheet_match_mode: "index", sheet_match_value: "0", column_bindings_json: '{"A":"order_no","B":"customer_name"}', enabled: true },
  { id: "tm_3", mapping_code: "CUSTOMS_V2", file_type: "customs", sheet_match_mode: "name", sheet_match_value: "Main", column_bindings_json: '{"A":"product_name","B":"product_code","C":"quantity"}', enabled: false }
];

// AI能力配置mock数据
export const mockAICapabilities = [
  { id: "aic_1", file_type: "customs", target_column: "B", capability_code: "JP_NAME_FILL", depends_on: "B,C,D,E", on_fail: "block", enabled: true },
  { id: "aic_2", file_type: "customs", target_column: "F", capability_code: "JP_PRODUCT_DESC_FILL", depends_on: "C,D,E", on_fail: "block", enabled: true },
  { id: "aic_3", file_type: "delivery", target_column: "D", capability_code: "JP_ADDRESS_FILL", depends_on: "C", on_fail: "skip", enabled: true },
  { id: "aic_4", file_type: "customs", target_column: "H", capability_code: "JP_CATEGORY_FILL", depends_on: "E,F", on_fail: "block", enabled: false }
];
