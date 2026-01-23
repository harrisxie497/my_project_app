下面我按你要求的顺序，**一步一步输出**：
**①需求文档 → ②设计文档 → ③函数设计文档**。
（全部基于你已导入的配置：`template_mappings / rule_tables / rule_items / ai_field_capabilities`，并且遵循“两步法 + 三维拆分”。）

---

# ① 需求文档（基于配置驱动的派送文件处理）

## 1. 背景与目标

系统需要支持“派送文件”Excel 的自动处理：用户上传源文件，系统按配置生成结果文件，包含字段映射、格式化、默认值填充、依赖计算、（未来）AI 加工，最后输出可下载的 Excel。

本期聚焦：**派送文件（delivery）——佐川指定时间带（Speedy sheet）**。

## 2. 术语定义

* **模板（Template）**：描述一类 Excel（sheet、表头行、数据行、目标列结构）
* **MAP（字段映射）**：目标文件每一列的值来自哪里（源列/常量/页面输入）
* **PROCESS（字段处理）**：目标文件每一列如何处理（FORMAT/DEFAULT/CALC 等）
* **三维拆分**

  * WHO：`executor_type`（program/ai）
  * WHAT：`field_type`（COPY/FORMAT/DEFAULT/CALC/RULE_FIX/AI）
  * HOW：`proc_rules.transformation_type`（format_and_default 等）

## 3. 业务流程（派送处理）

1. 操作员选择文件类型：**派送文件（delivery）**
2. 上传 Excel（源文件）
3. 输入页面参数：`article2_input`（对应 P 列）
4. 系统执行：

   * 模板识别与解析（template_mappings）
   * Step1：MAP（rule_tables.stage=MAP）
   * Step2：PROCESS（rule_tables.stage=PROCESS）
   * 输出 Excel（符合 target_schema_json）
5. 返回：

   * 结果文件（必选）
   * （后续可扩展）差异对比与统计（你一期里有这个诉求，但这里先按当前派送配置聚焦结果文件）

## 4. 本期支持范围（按已导入配置）

### 4.1 模板范围

* template_code：`TPL_DELIVERY_SAGAWA_SPEEDY_V1`
* file_type：delivery
* sheet：Speedy
* header_row：1
* data_start_row：2
* match_strategy：header_first
* target_schema：A–Y（R–Y 目标表头为空）

### 4.2 字段映射（MAP）

* A–O、Q：源同列 COPY
* P：来自页面输入 `article2_input`
* R–Y：置空，且目标表头为空字符串

### 4.3 字段处理（PROCESS）

* D（時間帯指定）：FORMAT + DEFAULT（依赖 C,D）
* J/K/M：DEFAULT 空值填充
* Q：CALC，空值时取 A
* P：校验必填（required=true）
* 其他列：COPY/NOOP

## 5. 错误处理与阻断

* MAP/PROCESS 任意规则执行失败 → **阻断**（on_fail=block）
* 必填输入缺失（如 article2_input） → 阻断并返回明确错误
* 源文件 sheet 缺失/表头不匹配 → 阻断并返回模板识别错误

## 6. 非功能需求

* 敏感数据：姓名/电话/地址/价格等 → 需要访问控制（已登录即可）
* 存储：原始文件与结果文件长期保存（挂载盘）
* 可审计：处理记录、使用的 template_code / rule_table_code、以及每列处理结果摘要可追踪

---

# ② 设计文档（配置驱动的处理引擎）

## 1. 总体架构

模块划分：

1. **Config Repository**：从 DB 读取模板与规则配置
2. **Excel Parser**：读取源文件（sheet、header、data）
3. **Mapping Engine（MAP）**：生成目标表初始值
4. **Processing Engine（PROCESS）**：按字段规则加工
5. **Excel Renderer**：写出目标文件（按 target_schema_json 控制列、表头、顺序）
6. **Audit & Storage**：落库记录、文件存储

## 2. 配置加载（DB → 内存对象）

* 输入：file_type=delivery，template_code=TPL_DELIVERY_SAGAWA_SPEEDY_V1
* 加载：

  * `template_mappings`：sheet、行号、target_schema_json
  * `rule_tables`：找到 MAP/PROCESS 对应 rule_table_code
  * `rule_items`：按 rule_table_code 拉取并按 order_no 排序
  * （可选）`ai_field_capabilities`：当 PROCESS 出现 AI 字段时再加载

## 3. 数据模型（运行时）

### 3.1 表格上下文

* `source_df`：源 sheet 数据（二维表）
* `target_df`：目标二维表（A–Y 列结构）
* `inputs`：页面输入参数（如 article2_input）
* `row_context`：行级字典（便于依赖计算）

### 3.2 目标列结构

来自 `target_schema_json`：

* 列集合：A–Y
* 表头：A–Q 有名；R–Y 空字符串
* 输出时必须严格按此结构写出

## 4. Step1：MAP 设计

每行（目标数据行）逐列执行映射：

* `COPY`：从源列取值（按 match_strategy header_first 定位源列）
* `DERIVE/INPUT_PARAM`：从 inputs 取值
* `DERIVE/CONST`：写固定值

输出：填充好 `target_df` 的所有列（A–Y）

## 5. Step2：PROCESS 设计

按 `order_no` 顺序执行（同一 rule_table_code 内）：

* 路由依据：`field_type`（WHAT）+ `executor_type`（WHO）
* 具体策略：`proc_rules.transformation_type`（HOW）

### 5.1 本期内置 handlers（program）

* COPY：不处理
* DEFAULT：空值填充
* FORMAT：格式化（支持 format_and_default）
* CALC：依赖其他列计算（支持 if_empty_copy_from）
* RULE_FIX：预留
* AI：预留（由 executor_type=ai 调用模型）

### 5.2 本期关键规则落地

* D：format_and_default（依赖 C,D）
* J/K/M：default_value（when_empty）
* Q：default_value（if_empty_copy_from=A）
* P：required 校验（缺则 block）

## 6. 输出 Excel 设计

* 只写 `Speedy` 这个处理 sheet（其他 sheet 可按“原样 copy”规则复制；你之前提过多 sheet，但只有一个处理，这里可以同时支持）
* 按 `target_schema_json` 写表头与列顺序
* 数据从 `data_start_row` 起写入

## 7. 审计与存储设计（最小可用）

建议新增一张处理记录表（如果你已有可忽略）：

* job_id、user_id、file_type、template_code
* source_file_path、result_file_path
* used_rule_table_codes（MAP/PROCESS）
* status、error_message
* created_at

---

# ③ 函数设计文档（核心函数与输入输出）

下面给“后端引擎”建议函数级拆分（Python/FastAPI 里直接可用）。

## 1. 配置加载

### 1.1 `load_template_mapping(file_type: str, template_code: str) -> TemplateMapping`

* 入参：file_type, template_code
* 出参：模板对象（sheet、行号、target_schema_json、match_strategy）
* 异常：找不到模板/未启用 → raise

### 1.2 `load_rule_table_codes(file_type: str) -> (str map_code, str process_code)`

* 从 rule_tables 找 stage=MAP/PROCESS 的 code
* 异常：缺 MAP 或 PROCESS → raise

### 1.3 `load_rule_items(rule_table_code: str) -> list[RuleItem]`

* 返回按 order_no 排序后的 rule_items

---

## 2. Excel 解析与表头定位

### 2.1 `read_workbook(path: str) -> openpyxl.Workbook`

* 只负责打开

### 2.2 `parse_sheet_to_rows(wb, sheet_name: str, header_row: int, data_start_row: int) -> (list[str] headers, list[list[Any]] rows)`

* 输出 headers + 数据行

### 2.3 `build_source_column_index(headers: list[str]) -> dict[str, int]`

* header_first：表头名到列索引映射（支持 strip）

---

## 3. MAP 执行

### 3.1 `apply_mapping(rows, headers, map_items, inputs, match_strategy, target_schema) -> target_rows`

* 输入：源数据行、表头、MAP items、inputs、目标列结构
* 输出：目标数据行（list[dict] 或 list[list]）
* 规则：

  * COPY：取源列值
  * INPUT_PARAM：取 inputs[param]
  * CONST：固定值

---

## 4. PROCESS 执行

### 4.1 `apply_processing(target_rows, process_items, inputs) -> target_rows`

* 输入：目标数据行、PROCESS items、inputs
* 输出：加工后的目标数据行
* 按 field_type 分发：

#### 4.1.1 `handle_default(row, item)`

* when_empty → value

#### 4.1.2 `handle_calc(row, item)`

* if_empty_copy_from

#### 4.1.3 `handle_format(row, item)`

* transformation_type=format_and_default
* 支持依赖列条件判断（C 是否为空）

#### 4.1.4 `handle_required(row, item)`

* proc_rules.required=true 时校验

> 注意：你当前配置里把 P 的 required 放在 CALC 的 proc_rules 里，这里就按 “proc_rules.required” 做校验即可。

---

## 5. Excel 输出

### 5.1 `render_target_workbook(original_wb, target_sheet_name, target_schema, target_rows, header_row, data_start_row) -> openpyxl.Workbook`

* 可选：复制原始 workbook 的其他 sheet
* 对目标 sheet：

  * 写表头（按 target_schema）
  * 写数据

### 5.2 `save_workbook(wb, output_path: str) -> None`

---

## 6. 入口编排（一个函数跑完整流程）

### 6.1 `process_delivery_file(source_path: str, inputs: dict, template_code: str) -> result_path`

* 编排顺序：

  1. load template + rule tables + items
  2. read workbook + parse sheet
  3. apply mapping
  4. apply processing（遇到 block 抛错）
  5. render + save
  6. 记录审计
* 输出：结果文件路径

---

如果你确认这三份文档结构 OK，下一步我就可以把它**落成真实代码**（按你现有 FastAPI 项目结构）：

* `services/config_repo.py`
* `services/excel_engine.py`
* `services/rule_handlers/*.py`
* `routers/process_delivery.py`
  并且直接对接你已导入的 DB 配置。
