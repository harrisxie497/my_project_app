# API设计文档

## 1. 概述

### 1.1 文档目的

本文档基于《日本清关 / 派送 Excel 自动处理系统》PRD v1.0，详细描述系统的API设计，包括所有表的增删查改操作，为开发人员提供明确的接口规范。

### 1.2 术语定义

| 术语 | 解释 |
| --- | --- |
| API | Application Programming Interface，应用程序编程接口 |
| JWT | JSON Web Token，用于身份验证的令牌 |
| CRUD | Create, Read, Update, Delete，增删查改操作 |
| REST | Representational State Transfer，一种软件架构风格 |
| HTTP | HyperText Transfer Protocol，超文本传输协议 |

### 1.3 API基础信息

| 项目 | 描述 |
| --- | --- |
| API版本 | v1.0 |
| 基础URL | http://localhost:8000/api/v1 |
| 认证方式 | JWT Token |
| 数据格式 | JSON |
| 错误处理 | 统一错误响应格式 |

## 2. 认证机制

### 2.1 JWT认证流程

1. 用户通过登录接口获取JWT Token
2. 后续请求在请求头中携带Token：`Authorization: Bearer {token}`
3. 服务器验证Token有效性，验证通过则处理请求，否则返回401错误

### 2.2 权限控制

| 角色 | 权限 |
| --- | --- |
| 管理员 | 所有API权限 |
| 操作员 | 任务相关API权限 |

## 3. 响应格式

### 3.1 成功响应

```json
{
  "ok": true,
  "data": {},
  "error": null
}
```

### 3.2 错误响应

```json
{
  "ok": false,
  "data": null,
  "error": {
    "code": "错误码",
    "message": "错误信息",
    "detail": "详细错误信息"
  }
}
```

## 4. API列表

### 4.1 认证相关API

| API路径 | 请求方法 | 功能描述 | 认证要求 | 权限要求 |
| --- | --- | --- | --- | --- |
| /auth/login | POST | 用户登录 | 无 | 无 |
| /auth/me | GET | 获取当前用户信息 | 需要 | 所有角色 |
| /auth/logout | POST | 用户登出 | 需要 | 所有角色 |

### 4.2 任务管理API

| API路径 | 请求方法 | 功能描述 | 认证要求 | 权限要求 |
| --- | --- | --- | --- | --- |
| /tasks | GET | 获取任务列表 | 需要 | 所有角色 |
| /tasks | POST | 创建任务 | 需要 | 所有角色 |
| /tasks/{id} | GET | 获取任务详情 | 需要 | 所有角色 |
| /tasks/{id} | PUT | 更新任务信息 | 需要 | 管理员 |
| /tasks/{id} | DELETE | 删除任务 | 需要 | 管理员 |
| /tasks/{id}/run | POST | 运行任务 | 需要 | 所有角色 |
| /tasks/{id}/files/{file_kind} | GET | 下载任务文件 | 需要 | 所有角色 |
| /tasks/{id}/stats | GET | 获取任务对比统计 | 需要 | 所有角色 |

### 4.3 规则表管理API

| API路径 | 请求方法 | 功能描述 | 认证要求 | 权限要求 |
| --- | --- | --- | --- | --- |
| /rule-tables | GET | 获取规则表列表 | 需要 | 管理员 |
| /rule-tables | POST | 创建规则表 | 需要 | 管理员 |
| /rule-tables/{id} | GET | 获取规则表详情 | 需要 | 管理员 |
| /rule-tables/{id} | PUT | 更新规则表 | 需要 | 管理员 |
| /rule-tables/{id} | DELETE | 删除规则表 | 需要 | 管理员 |
| /rule-tables/{id}/enable | PUT | 启用规则表 | 需要 | 管理员 |
| /rule-tables/{id}/disable | PUT | 禁用规则表 | 需要 | 管理员 |
| /admin/rule-tables | GET | 管理员获取规则表列表 | 需要 | 管理员 |
| /admin/rule-tables | POST | 管理员创建规则表 | 需要 | 管理员 |
| /admin/rule-tables/{rule_table_id} | PUT | 管理员更新规则表 | 需要 | 管理员 |

### 4.4 规则项管理API

| API路径 | 请求方法 | 功能描述 | 认证要求 | 权限要求 |
| --- | --- | --- | --- | --- |
| /rule-items | GET | 获取规则项列表 | 需要 | 管理员 |
| /rule-items | POST | 创建规则项 | 需要 | 管理员 |
| /rule-items/{id} | GET | 获取规则项详情 | 需要 | 管理员 |
| /rule-items/{id} | PUT | 更新规则项 | 需要 | 管理员 |
| /rule-items/{id} | DELETE | 删除规则项 | 需要 | 管理员 |
| /rule-items/{id}/enable | PUT | 启用规则项 | 需要 | 管理员 |
| /rule-items/{id}/disable | PUT | 禁用规则项 | 需要 | 管理员 |
| /rule-tables/{rule_table_id}/rule-items | GET | 获取指定规则表的规则项 | 需要 | 管理员 |
| /admin/rule-tables/{rule_table_id}/items | GET | 管理员获取规则表的规则项 | 需要 | 管理员 |
| /admin/rule-tables/{rule_table_id}/items | POST | 管理员创建规则项 | 需要 | 管理员 |
| /admin/rule-items/{rule_item_id} | PUT | 管理员更新规则项 | 需要 | 管理员 |
| /admin/rule-items/{rule_item_id} | DELETE | 管理员删除规则项 | 需要 | 管理员 |
| /admin/rules/import | POST | 规则导入 | 需要 | 管理员 |

### 4.5 模板映射管理API

| API路径 | 请求方法 | 功能描述 | 认证要求 | 权限要求 |
| --- | --- | --- | --- | --- |
| /template-mappings | GET | 获取模板映射列表 | 需要 | 管理员 |
| /template-mappings | POST | 创建模板映射 | 需要 | 管理员 |
| /template-mappings/{id} | GET | 获取模板映射详情 | 需要 | 管理员 |
| /template-mappings/{id} | PUT | 更新模板映射 | 需要 | 管理员 |
| /template-mappings/{id} | DELETE | 删除模板映射 | 需要 | 管理员 |
| /template-mappings/{id}/enable | PUT | 启用模板映射 | 需要 | 管理员 |
| /template-mappings/{id}/disable | PUT | 禁用模板映射 | 需要 | 管理员 |
| /admin/template-mappings | GET | 管理员获取模板映射列表 | 需要 | 管理员 |
| /admin/template-mappings | POST | 管理员创建模板映射 | 需要 | 管理员 |
| /admin/template-mappings/{id} | PUT | 管理员更新模板映射 | 需要 | 管理员 |
| /admin/template-mappings/{id}/validate | POST | 模板映射自检 | 需要 | 管理员 |

### 4.6 AI字段能力管理API

| API路径 | 请求方法 | 功能描述 | 认证要求 | 权限要求 |
| --- | --- | --- | --- | --- |
| /ai-capabilities | GET | 获取AI字段能力列表 | 需要 | 管理员 |
| /ai-capabilities | POST | 创建AI字段能力 | 需要 | 管理员 |
| /ai-capabilities/{id} | GET | 获取AI字段能力详情 | 需要 | 管理员 |
| /ai-capabilities/{id} | PUT | 更新AI字段能力 | 需要 | 管理员 |
| /ai-capabilities/{id} | DELETE | 删除AI字段能力 | 需要 | 管理员 |
| /ai-capabilities/{id}/enable | PUT | 启用AI字段能力 | 需要 | 管理员 |
| /ai-capabilities/{id}/disable | PUT | 禁用AI字段能力 | 需要 | 管理员 |
| /admin/ai-capabilities | GET | 管理员获取AI字段能力列表 | 需要 | 管理员 |
| /admin/ai-capabilities | POST | 管理员创建AI字段能力 | 需要 | 管理员 |
| /admin/ai-capabilities/{id} | PUT | 管理员更新AI字段能力 | 需要 | 管理员 |

### 4.7 Excel配置管理API

| API路径 | 请求方法 | 功能描述 | 认证要求 | 权限要求 |
| --- | --- | --- | --- | --- |
| /admin/excel-configs/active | GET | 获取当前Excel配置 | 需要 | 管理员 |
| /admin/excel-configs/active | PUT | 更新Excel配置 | 需要 | 管理员 |

### 4.8 用户管理API

| API路径 | 请求方法 | 功能描述 | 认证要求 | 权限要求 |
| --- | --- | --- | --- | --- |
| /users | GET | 获取用户列表 | 需要 | 管理员 |
| /users | POST | 创建用户 | 需要 | 管理员 |
| /users/{id} | GET | 获取用户详情 | 需要 | 管理员 |
| /users/{id} | PUT | 更新用户信息 | 需要 | 管理员 |
| /users/{id} | DELETE | 删除用户 | 需要 | 管理员 |
| /users/{id}/enable | PUT | 启用用户 | 需要 | 管理员 |
| /users/{id}/disable | PUT | 禁用用户 | 需要 | 管理员 |
| /admin/users | GET | 管理员获取用户列表 | 需要 | 管理员 |
| /admin/users | POST | 管理员创建用户 | 需要 | 管理员 |
| /admin/users/{id} | PUT | 管理员启用/禁用用户 | 需要 | 管理员 |
| /admin/users/{id}/reset-password | POST | 管理员重置用户密码 | 需要 | 管理员 |

### 4.9 操作日志API

| API路径 | 请求方法 | 功能描述 | 认证要求 | 权限要求 |
| --- | --- | --- | --- | --- |
| /operation-logs | GET | 获取操作日志列表 | 需要 | 管理员 |
| /operation-logs/{id} | GET | 获取操作日志详情 | 需要 | 管理员 |
| /operation-logs/user/{user_id} | GET | 获取指定用户的操作日志 | 需要 | 管理员 |
| /operation-logs/action/{action} | GET | 获取指定操作的日志 | 需要 | 管理员 |
| /admin/operation-logs | GET | 管理员查询操作日志 | 需要 | 管理员 |

## 5. API详细设计

### 5.1 认证相关API

#### 5.1.1 登录接口

**请求URL**：/auth/login

**请求方法**：POST

**请求头**：
```
Content-Type: application/x-www-form-urlencoded
```

**请求参数**：

| 参数名 | 类型 | 必填 | 描述 |
| --- | --- | --- | --- |
| username | string | 是 | 用户名 |
| password | string | 是 | 密码 |

**响应示例**：
```json
{
  "ok": true,
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer",
    "user": {
      "id": "u_12345678",
      "username": "admin",
      "display_name": "管理员",
      "role": "admin",
      "enabled": true,
      "created_at": "2026-01-21T10:00:00",
      "updated_at": "2026-01-21T10:00:00",
      "last_login_at": "2026-01-21T10:00:00"
    }
  },
  "error": null
}
```

#### 5.1.2 获取当前用户信息

**请求URL**：/auth/me

**请求方法**：GET

**请求头**：
```
Authorization: Bearer {token}
```

**响应示例**：
```json
{
  "ok": true,
  "data": {
    "id": "u_12345678",
    "username": "admin",
    "display_name": "管理员",
    "role": "admin",
    "enabled": true,
    "created_at": "2026-01-21T10:00:00",
    "updated_at": "2026-01-21T10:00:00",
    "last_login_at": "2026-01-21T10:00:00"
  },
  "error": null
}
```

#### 5.1.3 登出接口

**请求URL**：/auth/logout

**请求方法**：POST

**请求头**：
```
Authorization: Bearer {token}
```

**响应示例**：
```json
{
  "ok": true,
  "data": {
    "message": "Successfully logged out"
  },
  "error": null
}
```

### 5.2 用户管理API

#### 5.2.1 获取用户列表

**请求URL**：/users

**请求方法**：GET

**请求头**：
```
Authorization: Bearer {token}
```

**请求参数**：

| 参数名 | 类型 | 必填 | 描述 |
| --- | --- | --- | --- |
| page | integer | 否 | 页码，默认1 |
| page_size | integer | 否 | 每页条数，默认20 |
| username | string | 否 | 用户名搜索 |
| role | string | 否 | 角色过滤 |
| enabled | boolean | 否 | 是否启用过滤 |

**响应示例**：
```json
{
  "ok": true,
  "data": {
    "items": [
      {
        "id": "u_12345678",
        "username": "admin",
        "display_name": "管理员",
        "role": "admin",
        "enabled": true,
        "created_at": "2026-01-21T10:00:00",
        "updated_at": "2026-01-21T10:00:00",
        "last_login_at": "2026-01-21T10:00:00"
      }
    ],
    "page": 1,
    "page_size": 20,
    "total": 1
  },
  "error": null
}
```

#### 5.2.2 创建用户

**请求URL**：/users

**请求方法**：POST

**请求头**：
```
Authorization: Bearer {token}
Content-Type: application/json
```

**请求体**：
```json
{
  "username": "operator",
  "password": "operator123",
  "display_name": "操作员",
  "role": "operator",
  "enabled": true
}
```

**响应示例**：
```json
{
  "ok": true,
  "data": {
    "id": "u_87654321",
    "username": "operator",
    "display_name": "操作员",
    "role": "operator",
    "enabled": true,
    "created_at": "2026-01-21T10:00:00",
    "updated_at": "2026-01-21T10:00:00",
    "last_login_at": null
  },
  "error": null
}
```

### 5.3 任务管理API

#### 5.3.1 获取任务列表

**请求URL**：/tasks

**请求方法**：GET

**请求头**：
```
Authorization: Bearer {token}
```

**请求参数**：

| 参数名 | 类型 | 必填 | 描述 |
| --- | --- | --- | --- |
| page | integer | 否 | 页码，默认1 |
| page_size | integer | 否 | 每页条数，默认20 |
| file_type | string | 否 | 文件类型过滤 |
| status | string | 否 | 状态过滤 |
| unique_code | string | 否 | 唯一编码搜索 |
| created_by | string | 否 | 创建者ID过滤 |

**响应示例**：
```json
{
  "ok": true,
  "data": {
    "items": [
      {
        "id": "t_12345678",
        "file_type": "customs",
        "unique_code": "test_001",
        "status": "success",
        "created_at": "2026-01-21T10:00:00",
        "started_at": "2026-01-21T10:01:00",
        "finished_at": "2026-01-21T10:02:00",
        "created_by_user_id": "u_12345678"
      }
    ],
    "page": 1,
    "page_size": 20,
    "total": 1
  },
  "error": null
}
```

#### 5.3.2 创建任务

**请求URL**：/tasks

**请求方法**：POST

**请求头**：
```
Authorization: Bearer {token}
Content-Type: multipart/form-data
```

**请求体**：

表单数据，包含以下字段：

| 参数名 | 类型 | 必填 | 描述 |
| --- | --- | --- | --- |
| file_type | string | 是 | 文件类型（customs/delivery） |
| unique_code | string | 是 | 唯一编码 |
| flight_no | string | 是 | 航空号（仅清关文件） |
| declare_date | string | 是 | 报关日期（仅清关文件，格式：YYYY-MM-DD） |
| file | file | 是 | Excel文件（.xlsx格式） |

**响应示例**：
```json
{
  "ok": true,
  "data": {
    "task_id": "t_12345678",
    "status": "queued"
  },
  "error": null
}
```

**验证失败响应**：
```json
{
  "ok": false,
  "data": null,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "customs文件缺少flight_no或declare_date",
    "detail": {}
  }
}
```

#### 5.3.3 运行任务

**请求URL**：/tasks/{id}/run

**请求方法**：POST

**请求头**：
```
Authorization: Bearer {token}
```

**响应示例**：
```json
{
  "ok": true,
  "data": {
    "task_id": "t_12345678",
    "status": "processing"
  },
  "error": null
}
```

**错误响应**：
```json
{
  "ok": false,
  "data": null,
  "error": {
    "code": "TASK_NOT_FOUND",
    "message": "任务不存在",
    "detail": {}
  }
}
```

#### 5.3.4 下载任务文件

**请求URL**：/tasks/{id}/files/{file_kind}

**请求方法**：GET

**请求头**：
```
Authorization: Bearer {token}
```

**路径参数**：

| 参数名 | 类型 | 描述 |
| --- | --- | --- |
| id | string | 任务ID |
| file_kind | string | 文件类型（original/result/diff） |

**响应**：
- 成功：返回`application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`二进制流
- 失败：返回错误JSON

**错误响应示例**：
```json
{
  "ok": false,
  "data": null,
  "error": {
    "code": "FILE_NOT_READY",
    "message": "文件未准备好",
    "detail": {}
  }
}
```

#### 5.3.5 获取任务对比统计

**请求URL**：/tasks/{id}/stats

**请求方法**：GET

**请求头**：
```
Authorization: Bearer {token}
```

**响应示例**：
```json
{
  "ok": true,
  "data": {
    "total_rows": 120,
    "fixed_count": 86,
    "filled_count": 42
  },
  "error": null
}
```

## 6. 管理员API详细设计

### 6.1 规则管理API

#### 6.1.1 管理员获取规则表列表

**请求URL**：/admin/rule-tables

**请求方法**：GET

**请求头**：
```
Authorization: Bearer {token}
```

**查询参数**：

| 参数名 | 类型 | 必填 | 描述 |
| --- | --- | --- | --- |
| file_type | string | 否 | 文件类型过滤 |
| rule_stage | string | 否 | 规则阶段过滤 |
| enabled | boolean | 否 | 是否启用过滤 |

**响应示例**：
```json
{
  "ok": true,
  "data": [
    {
      "id": "rt_1",
      "code": "MAP_CUSTOMS",
      "file_type": "customs",
      "rule_stage": "MAP",
      "enabled": true
    }
  ],
  "error": null
}
```

#### 6.1.2 管理员创建规则表

**请求URL**：/admin/rule-tables

**请求方法**：POST

**请求头**：
```
Authorization: Bearer {token}
Content-Type: application/json
```

**请求体**：
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

**响应示例**：
```json
{
  "ok": true,
  "data": {
    "id": "rt_1"
  },
  "error": null
}
```

#### 6.1.3 管理员获取规则项列表

**请求URL**：/admin/rule-tables/{rule_table_id}/items

**请求方法**：GET

**请求头**：
```
Authorization: Bearer {token}
```

**路径参数**：

| 参数名 | 类型 | 描述 |
| --- | --- | --- |
| rule_table_id | string | 规则表ID |

**查询参数**：

| 参数名 | 类型 | 必填 | 描述 |
| --- | --- | --- | --- |
| enabled | boolean | 否 | 是否启用过滤 |
| target_column | string | 否 | 目标列搜索 |

**响应示例**：
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
  ],
  "error": null
}
```

#### 6.1.4 管理员创建规则项

**请求URL**：/admin/rule-tables/{rule_table_id}/items

**请求方法**：POST

**请求头**：
```
Authorization: Bearer {token}
Content-Type: application/json
```

**路径参数**：

| 参数名 | 类型 | 描述 |
| --- | --- | --- |
| rule_table_id | string | 规则表ID |

**请求体（MAP规则示例）**：
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

**请求体（PROCESS规则示例）**：
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

**响应示例**：
```json
{
  "ok": true,
  "data": {
    "id": "ri_1"
  },
  "error": null
}
```

#### 6.1.5 规则导入

**请求URL**：/admin/rules/import

**请求方法**：POST

**请求头**：
```
Authorization: Bearer {token}
Content-Type: multipart/form-data
```

**请求体**：

| 参数名 | 类型 | 必填 | 描述 |
| --- | --- | --- | --- |
| file | file | 是 | Excel导入模板文件 |

**响应示例**：
```json
{
  "ok": true,
  "data": {
    "imported": { "rule_tables": 4, "rule_items": 120 },
    "updated": { "rule_tables": 0, "rule_items": 12 },
    "skipped": 3,
    "warnings": [ "PROCESS_CUSTOMS: target_column B duplicated, kept latest" ]
  },
  "error": null
}
```

### 6.2 模板映射管理API

#### 6.2.1 管理员获取模板映射列表

**请求URL**：/admin/template-mappings

**请求方法**：GET

**请求头**：
```
Authorization: Bearer {token}
```

**查询参数**：

| 参数名 | 类型 | 必填 | 描述 |
| --- | --- | --- | --- |
| file_type | string | 否 | 文件类型过滤 |
| enabled | boolean | 否 | 是否启用过滤 |

**响应示例**：
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
  ],
  "error": null
}
```

#### 6.2.2 管理员创建模板映射

**请求URL**：/admin/template-mappings

**请求方法**：POST

**请求头**：
```
Authorization: Bearer {token}
Content-Type: application/json
```

**请求体**：
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

**响应示例**：
```json
{
  "ok": true,
  "data": {
    "id": "tm_1"
  },
  "error": null
}
```

#### 6.2.3 模板映射自检

**请求URL**：/admin/template-mappings/{id}/validate

**请求方法**：POST

**请求头**：
```
Authorization: Bearer {token}
```

**路径参数**：

| 参数名 | 类型 | 描述 |
| --- | --- | --- |
| id | string | 模板映射ID |

**响应示例**：
```json
{
  "ok": true,
  "data": {
    "valid": true,
    "warnings": []
  },
  "error": null
}
```

### 6.3 AI字段能力管理API

#### 6.3.1 管理员获取AI字段能力列表

**请求URL**：/admin/ai-capabilities

**请求方法**：GET

**请求头**：
```
Authorization: Bearer {token}
```

**查询参数**：

| 参数名 | 类型 | 必填 | 描述 |
| --- | --- | --- | --- |
| file_type | string | 否 | 文件类型过滤 |
| enabled | boolean | 否 | 是否启用过滤 |
| target_column | string | 否 | 目标列搜索 |

**响应示例**：
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
  ],
  "error": null
}
```

#### 6.3.2 管理员创建AI字段能力

**请求URL**：/admin/ai-capabilities

**请求方法**：POST

**请求头**：
```
Authorization: Bearer {token}
Content-Type: application/json
```

**请求体**：
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

**响应示例**：
```json
{
  "ok": true,
  "data": {
    "id": "aic_1"
  },
  "error": null
}
```

### 6.4 Excel配置管理API

#### 6.4.1 获取当前Excel配置

**请求URL**：/admin/excel-configs/active

**请求方法**：GET

**请求头**：
```
Authorization: Bearer {token}
```

**查询参数**：

| 参数名 | 类型 | 必填 | 描述 |
| --- | --- | --- | --- |
| file_type | string | 是 | 文件类型 |

**响应示例**：
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
  },
  "error": null
}
```

#### 6.4.2 更新Excel配置

**请求URL**：/admin/excel-configs/active

**请求方法**：PUT

**请求头**：
```
Authorization: Bearer {token}
Content-Type: application/json
```

**请求体**：
```json
{
  "file_type": "customs",
  "default_font": "Meiryo",
  "date_format": "YYYY-MM-DD",
  "merge_ranges": ["A1:C1"],
  "style_rules": [
    { "target": { "type": "column", "value": "B" }, "style": { "fill_color": "#FFF2CC" } }
  ]
}
```

**响应示例**：
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
  },
  "error": null
}
```

### 6.5 管理员用户管理API

#### 6.5.1 管理员获取用户列表

**请求URL**：/admin/users

**请求方法**：GET

**请求头**：
```
Authorization: Bearer {token}
```

**响应示例**：
```json
{
  "ok": true,
  "data": [
    {
      "id": "u_1",
      "username": "admin",
      "display_name": "管理员",
      "role": "admin",
      "enabled": true
    }
  ],
  "error": null
}
```

#### 6.5.2 管理员创建用户

**请求URL**：/admin/users

**请求方法**：POST

**请求头**：
```
Authorization: Bearer {token}
Content-Type: application/json
```

**请求体**：
```json
{
  "username": "op1",
  "display_name": "操作员1",
  "role": "operator",
  "password": "Init1234"
}
```

**响应示例**：
```json
{
  "ok": true,
  "data": {
    "id": "u_2"
  },
  "error": null
}
```

#### 6.5.3 管理员启用/禁用用户

**请求URL**：/admin/users/{id}

**请求方法**：PUT

**请求头**：
```
Authorization: Bearer {token}
Content-Type: application/json
```

**路径参数**：

| 参数名 | 类型 | 描述 |
| --- | --- | --- |
| id | string | 用户ID |

**请求体**：
```json
{
  "enabled": false
}
```

**响应示例**：
```json
{
  "ok": true,
  "data": {
    "id": "u_2",
    "enabled": false
  },
  "error": null
}
```

#### 6.5.4 管理员重置用户密码

**请求URL**：/admin/users/{id}/reset-password

**请求方法**：POST

**请求头**：
```
Authorization: Bearer {token}
Content-Type: application/json
```

**路径参数**：

| 参数名 | 类型 | 描述 |
| --- | --- | --- |
| id | string | 用户ID |

**请求体**：
```json
{
  "new_password": "New1234"
}
```

**响应示例**：
```json
{
  "ok": true,
  "data": {
    "message": "密码重置成功"
  },
  "error": null
}
```

### 6.6 管理员操作日志API

#### 6.6.1 管理员查询操作日志

**请求URL**：/admin/operation-logs

**请求方法**：GET

**请求头**：
```
Authorization: Bearer {token}
```

**查询参数**：

| 参数名 | 类型 | 必填 | 描述 |
| --- | --- | --- | --- |
| user_id | string | 否 | 用户ID过滤 |
| action | string | 否 | 操作类型过滤 |
| from | string | 否 | 开始时间（ISO格式） |
| to | string | 否 | 结束时间（ISO格式） |
| page | integer | 否 | 页码，默认1 |
| page_size | integer | 否 | 每页条数，默认20 |

**响应示例**：
```json
{
  "ok": true,
  "data": {
    "items": [
      {
        "id": "log_1",
        "user_id": "u_1",
        "action": "TASK_CREATED",
        "entity_type": "task",
        "entity_id": "t_001",
        "success": true,
        "message": "created",
        "detail_json": {
          "username": "admin"
        },
        "created_at": "2026-01-20T01:02:03Z"
      }
    ],
    "page": 1,
    "page_size": 50,
    "total": 999
  },
  "error": null
}
```

## 7. 任务处理引擎对接口的依赖

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

## 8. 错误码设计

| 错误码 | 含义 | HTTP状态码 |
| --- | --- | --- |
| 0 | 成功 | 200 |
| 1000 | 请求参数错误 | 400 |
| 1001 | 资源不存在 | 404 |
| 1002 | 权限不足 | 403 |
| 1003 | 认证失败 | 401 |
| 1004 | 资源已存在 | 409 |
| 1005 | 服务器内部错误 | 500 |
| 2000 | 文件上传失败 | 400 |
| 2001 | 文件格式错误 | 400 |
| 2002 | 任务执行失败 | 500 |
| 3000 | 规则执行失败 | 500 |
| 3001 | 规则配置错误 | 400 |
| 4000 | AI服务调用失败 | 500 |
| AUTH_FAILED | 认证失败 | 401 |
| VALIDATION_ERROR | 验证错误 | 400 |
| TASK_NOT_FOUND | 任务不存在 | 404 |
| TASK_INVALID_STATE | 任务状态无效 | 400 |
| FILE_NOT_READY | 文件未准备好 | 400 |
| FILE_NOT_FOUND | 文件不存在 | 404 |
| CONFIG_MISSING | 配置缺失 | 500 |
| CONFIG_INVALID | 配置无效 | 500 |
| IMPORT_FAILED | 导入失败 | 500 |
| RULE_VALIDATION_FAILED | 规则验证失败 | 500 |
| INTERNAL_ERROR | 内部错误 | 500 |

## 9. 安全设计

1. **认证与授权**：使用JWT进行身份验证，实现基于角色的权限控制
2. **数据加密**：敏感数据（如密码）存储时进行加密
3. **输入验证**：所有API请求参数进行严格验证
4. **防止SQL注入**：使用ORM框架，避免直接拼接SQL语句
5. **防止XSS攻击**：对输出到前端的数据进行转义
6. **文件上传安全**：限制文件类型和大小，进行病毒扫描
7. **日志安全**：操作日志中不记录敏感信息
8. **API限流**：对API请求进行限流，防止恶意请求

## 10. 性能设计

1. **分页查询**：所有列表查询支持分页，避免一次性返回大量数据
2. **缓存机制**：对频繁访问的数据进行缓存
3. **异步处理**：耗时操作（如文件处理）使用异步方式处理
4. **数据库索引**：对查询频繁的字段建立索引
5. **连接池**：使用数据库连接池，提高数据库访问效率
6. **负载均衡**：支持多实例部署，实现负载均衡

## 11. 部署与监控

### 11.1 部署方式

1. **容器化部署**：使用Docker进行容器化部署
2. **微服务架构**：支持微服务架构，便于扩展
3. **CI/CD**：实现持续集成和持续部署

### 11.2 监控与日志

1. **API监控**：监控API调用次数、响应时间、错误率等
2. **系统监控**：监控服务器CPU、内存、磁盘等资源使用情况
3. **日志收集**：集中收集和分析系统日志
4. **告警机制**：设置告警规则，及时发现和处理问题

## 12. 版本控制

| 版本 | 日期 | 作者 | 描述 |
| --- | --- | --- | --- |
| v1.0 | 2026-01-21 | AI Assistant | 初始版本，包含所有表的CRUD API |
| v1.1 | 2026-01-21 | AI Assistant | 合并APIV1.0版本，增加管理员API和详细设计 |
| v1.2 | 2026-01-22 | AI Assistant | 合并两个API设计文档，统一文档结构 |

## 13. 附录

### 13.1 数据类型定义

| 类型 | 描述 |
| --- | --- |
| string | 字符串类型 |
| integer | 整数类型 |
| number | 数字类型（包括整数和小数） |
| boolean | 布尔类型（true/false） |
| array | 数组类型 |
| object | 对象类型 |
| file | 文件类型 |

### 13.2 HTTP方法定义

| 方法 | 描述 |
| --- | --- |
| GET | 获取资源 |
| POST | 创建资源 |
| PUT | 更新资源 |
| DELETE | 删除资源 |
| PATCH | 部分更新资源 |

### 13.3 状态码定义

| 状态码 | 描述 |
| --- | --- |
| 200 | 请求成功 |
| 201 | 资源创建成功 |
| 204 | 请求成功，无返回内容 |
| 400 | 请求参数错误 |
| 401 | 未授权，需要登录 |
| 403 | 禁止访问，权限不足 |
| 404 | 资源不存在 |
| 405 | 不支持的HTTP方法 |
| 409 | 资源冲突 |
| 500 | 服务器内部错误 |
| 501 | 未实现的功能 |
| 503 | 服务不可用 |

### 13.4 枚举定义

| 枚举名 | 枚举值 |
| --- | --- |
| file_type | `customs` \| `delivery` |
| task_status | `queued` \| `processing` \| `success` \| `failed` |
| rule_stage | `MAP` \| `PROCESS` |
| map_op | `COPY` \| `DROP` \| `DERIVE` |
| field_type | `RULE_FIX` \| `CALC` \| `AI` |
| executor | `program` \| `ai` \| `other_program` |
| on_fail | `block`