下面是基于当前冻结版 PRD（单文件任务、MAP+PROCESS、template_mappings、ai_field_capabilities、登录即可、无下载鉴权、含操作日志）的 **FastAPI 接口设计文档（API Spec）**。
风格：偏工程可落地，便于前后端对齐、直接开工。

---

# FastAPI 接口设计文档（API Spec v1.0）

## 0. 约定

### 0.1 Base

* Base URL：`/api/v1`

### 0.2 鉴权

* 仅要求**登录**，不做下载额外鉴权
* 推荐：JWT（Access Token）或 Session Cookie（二选一）
* 本文以 **JWT Bearer Token** 表达：

  * Header：`Authorization: Bearer <token>`

### 0.3 通用响应结构（建议）

成功：

```json
{ "ok": true, "data": { } }
```

失败：

```json
{
  "ok": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "xxx",
    "detail": { }
  }
}
```

### 0.4 枚举

* `file_type`: `customs` | `delivery`
* `task_status`: `queued` | `processing` | `success` | `failed`
* `rule_stage`: `MAP` | `PROCESS`
* `map_op`: `COPY` | `DROP` | `DERIVE`
* `field_type`: `RULE_FIX` | `CALC` | `AI`
* `executor`: `program` | `ai` | `other_program`
* `on_fail`: `block`

---

## 1. Auth（登录）

### 1.1 登录

**POST** `/auth/login`

Request:

```json
{ "username": "admin", "password": "xxx" }
```

Response:

```json
{
  "ok": true,
  "data": {
    "access_token": "jwt...",
    "token_type": "bearer",
    "user": {
      "id": "u_123",
      "username": "admin",
      "display_name": "Admin",
      "role": "admin"
    }
  }
}
```

错误：

* `AUTH_FAILED`

> 写日志：`AUTH_LOGIN_SUCCESS` / `AUTH_LOGIN_FAILED`

---

### 1.2 获取当前用户

**GET** `/auth/me`

Response:

```json
{
  "ok": true,
  "data": {
    "id": "u_123",
    "username": "admin",
    "display_name": "Admin",
    "role": "admin",
    "enabled": true,
    "last_login_at": "2026-01-20T12:00:00Z"
  }
}
```

---

### 1.3 登出（可选）

**POST** `/auth/logout`

Response:

```json
{ "ok": true, "data": {} }
```

> JWT 模式下通常是前端删除 token；后端可选实现 token blacklist。

---

## 2. Tasks（任务：上传→处理→下载）

> 一期：一次只能上传 1 个 Excel → 创建 1 个 task

### 2.1 创建任务（上传文件）

**POST** `/tasks`

* Content-Type: `multipart/form-data`

Form fields:

* `file_type`: `customs|delivery`
* `unique_code`: string
* `flight_no`: string（customs 必填）
* `declare_date`: `YYYY-MM-DD`（customs 必填）
* `file`: `.xlsx` 文件（必填）

Response:

```json
{
  "ok": true,
  "data": {
    "task_id": "t_001",
    "status": "queued"
  }
}
```

验证失败：

* `VALIDATION_ERROR`

  * customs 缺 flight_no/declare_date
  * 文件不是 xlsx
  * 多文件上传（若发生）直接报错

> 写日志：`TASK_CREATED`

---

### 2.2 触发处理（同步/异步二选一）

推荐：异步（后台队列/线程），前端轮询状态。

**POST** `/tasks/{task_id}/run`

Response:

```json
{
  "ok": true,
  "data": { "task_id": "t_001", "status": "processing" }
}
```

错误：

* `TASK_NOT_FOUND`
* `TASK_INVALID_STATE`（success/failed 不允许重复 run，一期可禁止）

> 一期也可以在创建任务时自动 run，则该接口可选。

---

### 2.3 查询任务列表

**GET** `/tasks`

Query params（可选）：

* `file_type`
* `status`
* `unique_code`
* `created_at_from`（ISO）
* `created_at_to`（ISO）
* `page`（default 1）
* `page_size`（default 20, max 100）

Response:

```json
{
  "ok": true,
  "data": {
    "items": [
      {
        "id": "t_001",
        "file_type": "customs",
        "unique_code": "UC001",
        "flight_no": "NH123",
        "declare_date": "2026-01-20",
        "status": "success",
        "created_at": "2026-01-20T01:02:03Z",
        "started_at": "2026-01-20T01:02:05Z",
        "finished_at": "2026-01-20T01:02:20Z"
      }
    ],
    "page": 1,
    "page_size": 20,
    "total": 123
  }
}
```

---

### 2.4 查询任务详情

**GET** `/tasks/{task_id}`

Response:

```json
{
  "ok": true,
  "data": {
    "id": "t_001",
    "created_by_user_id": "u_123",
    "file_type": "customs",
    "unique_code": "UC001",
    "flight_no": "NH123",
    "declare_date": "2026-01-20",
    "status": "success",
    "progress_stage": "done",
    "progress_message": "ok",
    "error": null,
    "stats": {
      "total_rows": 120,
      "fixed_count": 86,
      "filled_count": 42,
      "fx_changed_rows": 120,
      "llm_filled_count": 15
    },
    "files": {
      "original": { "file_name": "in.xlsx", "download_url": "/api/v1/tasks/t_001/files/original" },
      "result": { "file_name": "out.xlsx", "download_url": "/api/v1/tasks/t_001/files/result" },
      "diff": { "file_name": "diff.xlsx", "download_url": "/api/v1/tasks/t_001/files/diff" }
    },
    "created_at": "2026-01-20T01:02:03Z",
    "started_at": "2026-01-20T01:02:05Z",
    "finished_at": "2026-01-20T01:02:20Z"
  }
}
```

失败态示例：

```json
{
  "ok": true,
  "data": {
    "id": "t_002",
    "status": "failed",
    "error": {
      "code": "RULE_VALIDATION_FAILED",
      "message": "字段A不符合12位数字要求",
      "detail": { "sheet": "Sheet1", "row": 23, "col": "A" }
    }
  }
}
```

---

### 2.5 下载任务文件（不做额外鉴权，仅要求登录）

**GET** `/tasks/{task_id}/files/{file_kind}`

* `file_kind`: `original` | `result` | `diff`

Response:

* `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet` 二进制流

错误：

* `TASK_NOT_FOUND`
* `FILE_NOT_READY`（processing/failed 时）
* `FILE_NOT_FOUND`

> 可选写日志：`FILE_DOWNLOADED`

---

### 2.6 获取对比统计（可选，如果前端要单独拿）

**GET** `/tasks/{task_id}/stats`

Response:

```json
{ "ok": true, "data": { "total_rows": 120, "fixed_count": 86, "filled_count": 42 } }
```

---

## 3. Rules（规则表与规则项）— 管理员

> 管理员权限：`role=admin`

### 3.1 rule_tables 列表

**GET** `/admin/rule-tables`

Query（可选）：

* `file_type`
* `rule_stage`
* `enabled`

Response:

```json
{
  "ok": true,
  "data": [
    { "id": "rt_1", "code": "MAP_CUSTOMS", "file_type": "customs", "rule_stage": "MAP", "enabled": true }
  ]
}
```

---

### 3.2 创建 rule_table

**POST** `/admin/rule-tables`

Request:

```json
{
  "code": "MAP_CUSTOMS",
  "name": "清关字段映射规则",
  "file_type": "customs",
  "rule_stage": "MAP",
  "enabled": true,
  "description": "原始→最终字段映射"
}
```

Response:

```json
{ "ok": true, "data": { "id": "rt_1" } }
```

---

### 3.3 更新 rule_table

**PUT** `/admin/rule-tables/{rule_table_id}`

Request:

```json
{ "name": "xxx", "enabled": true, "description": "..." }
```

---

### 3.4 rule_items 列表（按表）

**GET** `/admin/rule-tables/{rule_table_id}/items`

Query：

* `enabled`
* `target_column`（可选）

Response:

```json
{
  "ok": true,
  "data": [
    {
      "id": "ri_1",
      "enabled": true,
      "order_no": 10,
      "target_column": "A",
      "target_field_name": "お客様管理番号",
      "map_op": "COPY",
      "source_column": "A",
      "field_type": null,
      "executor": null,
      "note": "示例"
    }
  ]
}
```

---

### 3.5 创建 rule_item

**POST** `/admin/rule-tables/{rule_table_id}/items`

Request（MAP 示例）：

```json
{
  "enabled": true,
  "order_no": 10,
  "target_column": "A",
  "target_field_name": "お客様管理番号",
  "map_op": "COPY",
  "source_column": "A",
  "derive_type": null,
  "derive_depends_on": null,
  "derive_rule": null,
  "note": ""
}
```

Request（PROCESS 示例）：

```json
{
  "enabled": true,
  "order_no": 10,
  "target_column": "A",
  "target_field_name": "お客様管理番号",
  "field_type": "RULE_FIX",
  "process_depends_on": "",
  "process_rules_json": [
    { "name": "required" },
    { "name": "regex", "pattern": "^\\d{12}$" }
  ],
  "executor": "program",
  "on_fail": "block",
  "note": ""
}
```

后端校验（关键）：

* MAP 表必须填写 map_op
* PROCESS 表必须填写 field_type
* RULE_FIX 的 `process_depends_on` 必须为空
* CALC/AI 的 `process_depends_on` 必须非空
* 同一 rule_table 内 `target_column` 不允许重复（建议）

---

### 3.6 更新 / 删除 rule_item

**PUT** `/admin/rule-items/{rule_item_id}`

* 支持字段同创建

**DELETE** `/admin/rule-items/{rule_item_id}`

* 软删或 enabled=false（二选一，推荐 enabled=false）

---

### 3.7 规则导入（与你的 Excel 模板配套，强烈建议）

**POST** `/admin/rules/import`

* Content-Type: `multipart/form-data`
* file: `.xlsx`（导入模板）

Response:

```json
{
  "ok": true,
  "data": {
    "imported": { "rule_tables": 4, "rule_items": 120 },
    "updated": { "rule_tables": 0, "rule_items": 12 },
    "skipped": 3,
    "warnings": [ "PROCESS_CUSTOMS: target_column B duplicated, kept latest" ]
  }
}
```

失败：

* `IMPORT_FAILED`（返回行号、sheet、列名）

> 写日志：`RULE_UPDATED` / `CONFIG_UPDATED`（导入也算更新）

---

## 4. Template Mappings（模板映射）— 管理员

### 4.1 列表

**GET** `/admin/template-mappings`

Query：

* `file_type`
* `enabled`

Response:

```json
{
  "ok": true,
  "data": [
    {
      "id": "tm_1",
      "mapping_code": "TM_CUSTOMS_V1",
      "file_type": "customs",
      "source_template_code": "CUSTOMS_SRC_TPL_V1",
      "target_template_code": "CUSTOMS_RESULT_V1",
      "sheet_match_mode": "name",
      "sheet_match_value": "Sheet1",
      "enabled": true
    }
  ]
}
```

---

### 4.2 创建/更新

**POST** `/admin/template-mappings`
**PUT** `/admin/template-mappings/{id}`

Request：

```json
{
  "mapping_code": "TM_CUSTOMS_V1",
  "file_type": "customs",
  "source_template_code": "CUSTOMS_SRC_TPL_V1",
  "target_template_code": "CUSTOMS_RESULT_V1",
  "sheet_match_mode": "name",
  "sheet_match_value": "Sheet1",
  "column_bindings_json": {
    "bindings": [
      {
        "source_key": "order_no",
        "match": { "by": "header", "candidates": ["お客様管理番号","订单号"] },
        "fallback": { "by": "col", "value": "A" },
        "required": true
      }
    ]
  },
  "enabled": true,
  "note": ""
}
```

---

### 4.3 模板映射自检（强烈建议）

**POST** `/admin/template-mappings/{id}/validate`

作用：

* 校验 json 格式
* candidates 非空
* required 的 source_key 可解析

Response:

```json
{ "ok": true, "data": { "valid": true, "warnings": [] } }
```

---

## 5. AI Field Capabilities（AI 列能力配置）— 管理员

### 5.1 列表

**GET** `/admin/ai-capabilities`

Query：

* `file_type`
* `enabled`
* `target_column`

Response:

```json
{
  "ok": true,
  "data": [
    {
      "id": "aic_1",
      "file_type": "customs",
      "target_column": "B",
      "capability_code": "JP_NAME_FILL",
      "depends_on": ["B","C","D","E"],
      "on_fail": "block",
      "enabled": true
    }
  ]
}
```

---

### 5.2 创建/更新

**POST** `/admin/ai-capabilities`
**PUT** `/admin/ai-capabilities/{id}`

Request:

```json
{
  "file_type": "customs",
  "target_column": "B",
  "target_field_name": "收件人姓名(日文)",
  "capability_code": "JP_NAME_FILL",
  "depends_on": ["B","C","D","E"],
  "prompt_template": "根据以下字段生成日文姓名：{B},{C},{D},{E}",
  "output_constraints_json": { "max_length": 30, "charset": "ja", "not_empty": true },
  "on_fail": "block",
  "enabled": true,
  "note": ""
}
```

后端校验：

* depends_on 非空（对 AI）
* prompt_template 必须可格式化（占位符字段存在）

---

## 6. ExcelConfig（输出样式配置）— 管理员（可选接口）

> PRD 中 ExcelConfig 存在，但当前重点是 rule_tables/rule_items/template_mappings/ai_capabilities。
> 这里给最小接口，后续可扩展样式规则。

### 6.1 获取当前配置

**GET** `/admin/excel-configs/active?file_type=customs`

Response:

```json
{
  "ok": true,
  "data": {
    "file_type": "customs",
    "default_font": "Meiryo",
    "date_format": "YYYY-MM-DD",
    "merge_ranges": ["A1:C1"],
    "style_rules": [
      { "target": { "type": "column", "value": "B" }, "style": { "fill_color": "#FFF2CC" } }
    ]
  }
}
```

### 6.2 更新配置

**PUT** `/admin/excel-configs/active`

Request 同上。

---

## 7. Users（管理员）

### 7.1 用户列表

**GET** `/admin/users`

### 7.2 创建用户

**POST** `/admin/users`

```json
{ "username": "op1", "display_name": "操作员1", "role": "operator", "password": "Init1234" }
```

### 7.3 启用/禁用

**PUT** `/admin/users/{id}`

```json
{ "enabled": false }
```

### 7.4 重置密码

**POST** `/admin/users/{id}/reset-password`

```json
{ "new_password": "New1234" }
```

---

## 8. Operation Logs（管理员）

### 8.1 查询日志

**GET** `/admin/operation-logs`

Query：

* `user_id`
* `action`
* `from`
* `to`
* `page/page_size`

Response：

```json
{
  "ok": true,
  "data": {
    "items": [
      {
        "id": "log_1",
        "user_id": "u_123",
        "action": "TASK_CREATED",
        "entity_type": "task",
        "entity_id": "t_001",
        "success": true,
        "message": "created",
        "created_at": "2026-01-20T01:02:03Z"
      }
    ],
    "page": 1,
    "page_size": 50,
    "total": 999
  }
}
```

---

# 9. 任务处理引擎对接口的依赖（实现提示）

任务运行 `POST /tasks/{id}/run` 内部应按顺序加载配置：

1. `template_mappings`：按 file_type 选 active mapping（或默认 mapping_code）
2. `rule_tables`：

   * stage=MAP
   * stage=PROCESS
3. 对于 PROCESS 中 `field_type=AI`：

   * 从 `ai_field_capabilities` 读取列级能力配置（capability_code、prompt、约束）
4. 应用 `excel_configs`（字体、合并、样式）

若任一步配置缺失：

* 任务失败（block），error_code 建议：

  * `CONFIG_MISSING`
  * `CONFIG_INVALID`
  * `RULE_CONFLICT`

---

# 10. 错误码建议（一期）

* `AUTH_FAILED`
* `VALIDATION_ERROR`
* `TASK_NOT_FOUND`
* `TASK_INVALID_STATE`
* `FILE_NOT_READY`
* `FILE_NOT_FOUND`
* `CONFIG_MISSING`
* `CONFIG_INVALID`
* `IMPORT_FAILED`
* `RULE_VALIDATION_FAILED`
* `INTERNAL_ERROR`

---

# 11. 版本与兼容

* v1.0：单文件任务、无下载鉴权、无用户隔离
* v1.x：可扩展批量、差异预览、规则版本

---

如果你希望我继续把这份 API Spec **落到一个 OpenAPI 3.1 YAML**（可直接给前端用、也可让 FastAPI 自动生成校验模型），我可以在下一步直接输出一份 `openapi.yaml` 草案。
