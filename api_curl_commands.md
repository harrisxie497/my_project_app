# API接口测试命令

**生成时间**: 2026-01-25_16-01-08

**接口总数**: 45

## 详细接口列表

### other

#### GET /health
**摘要**: Health Check
**操作ID**: health_check_health_get
**curl命令**:
```bash
curl -X GET "http://127.0.0.1:8000/health" -H "accept: application/json"
```

#### GET /
**摘要**: Root
**操作ID**: root__get
**curl命令**:
```bash
curl -X GET "http://127.0.0.1:8000/" -H "accept: application/json"
```

### v1

#### POST /api/v1/auth/login
**摘要**: Login
**操作ID**: login_api_v1_auth_login_post
**curl命令**:
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/auth/login" -H "accept: application/json" -H "Content-Type: application/json" -d "{}"
```

#### GET /api/v1/auth/me
**摘要**: Get Me
**操作ID**: get_me_api_v1_auth_me_get
**curl命令**:
```bash
curl -X GET "http://127.0.0.1:8000/api/v1/auth/me" -H "accept: application/json"
```

#### POST /api/v1/auth/logout
**摘要**: Logout
**操作ID**: logout_api_v1_auth_logout_post
**curl命令**:
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/auth/logout" -H "accept: application/json" -H "Content-Type: application/json"
```

#### POST /api/v1/tasks
**摘要**: Create Task
**操作ID**: create_task_api_v1_tasks_post
**curl命令**:
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/tasks" -H "accept: application/json" -H "Content-Type: application/json" -d "{}"
```

#### GET /api/v1/tasks
**摘要**: Get Tasks
**操作ID**: get_tasks_api_v1_tasks_get
**curl命令**:
```bash
curl -X GET "http://127.0.0.1:8000/api/v1/tasks" -H "accept: application/json"
```

#### POST /api/v1/tasks/{task_id}/run
**摘要**: Run Task
**操作ID**: run_task_api_v1_tasks__task_id__run_post
**curl命令**:
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/tasks/{task_id}/run" -H "accept: application/json" -H "Content-Type: application/json"
```

#### GET /api/v1/tasks/{task_id}
**摘要**: Get Task Detail
**操作ID**: get_task_detail_api_v1_tasks__task_id__get
**curl命令**:
```bash
curl -X GET "http://127.0.0.1:8000/api/v1/tasks/{task_id}" -H "accept: application/json"
```

#### GET /api/v1/tasks/{task_id}/files/{file_kind}
**摘要**: Download Task File
**操作ID**: download_task_file_api_v1_tasks__task_id__files__file_kind__get
**curl命令**:
```bash
curl -X GET "http://127.0.0.1:8000/api/v1/tasks/{task_id}/files/{file_kind}" -H "accept: application/json"
```

#### GET /api/v1/users/
**摘要**: Get Users
**操作ID**: get_users_api_v1_users__get
**curl命令**:
```bash
curl -X GET "http://127.0.0.1:8000/api/v1/users/" -H "accept: application/json"
```

#### POST /api/v1/users/
**摘要**: Create User
**操作ID**: create_user_api_v1_users__post
**curl命令**:
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/users/" -H "accept: application/json" -H "Content-Type: application/json" -d "{}"
```

#### GET /api/v1/users/{id}
**摘要**: Get User
**操作ID**: get_user_api_v1_users__id__get
**curl命令**:
```bash
curl -X GET "http://127.0.0.1:8000/api/v1/users/{id}" -H "accept: application/json"
```

#### PUT /api/v1/users/{id}
**摘要**: Update User
**操作ID**: update_user_api_v1_users__id__put
**curl命令**:
```bash
curl -X PUT "http://127.0.0.1:8000/api/v1/users/{id}" -H "accept: application/json" -H "Content-Type: application/json" -d "{}"
```

#### DELETE /api/v1/users/{id}
**摘要**: Delete User
**操作ID**: delete_user_api_v1_users__id__delete
**curl命令**:
```bash
curl -X DELETE "http://127.0.0.1:8000/api/v1/users/{id}" -H "accept: application/json"
```

#### PUT /api/v1/users/{id}/enable
**摘要**: Enable User
**操作ID**: enable_user_api_v1_users__id__enable_put
**curl命令**:
```bash
curl -X PUT "http://127.0.0.1:8000/api/v1/users/{id}/enable" -H "accept: application/json" -H "Content-Type: application/json"
```

#### PUT /api/v1/users/{id}/disable
**摘要**: Disable User
**操作ID**: disable_user_api_v1_users__id__disable_put
**curl命令**:
```bash
curl -X PUT "http://127.0.0.1:8000/api/v1/users/{id}/disable" -H "accept: application/json" -H "Content-Type: application/json"
```

#### GET /api/v1/operation-logs
**摘要**: Get Operation Logs
**操作ID**: get_operation_logs_api_v1_operation_logs_get
**curl命令**:
```bash
curl -X GET "http://127.0.0.1:8000/api/v1/operation-logs" -H "accept: application/json"
```

#### GET /api/v1/operation-logs/{id}
**摘要**: Get Operation Log
**操作ID**: get_operation_log_api_v1_operation_logs__id__get
**curl命令**:
```bash
curl -X GET "http://127.0.0.1:8000/api/v1/operation-logs/{id}" -H "accept: application/json"
```

#### GET /api/v1/operation-logs/user/{user_id}
**摘要**: Get Operation Logs By User
**操作ID**: get_operation_logs_by_user_api_v1_operation_logs_user__user_id__get
**curl命令**:
```bash
curl -X GET "http://127.0.0.1:8000/api/v1/operation-logs/user/{user_id}" -H "accept: application/json"
```

#### GET /api/v1/operation-logs/action/{action}
**摘要**: Get Operation Logs By Action
**操作ID**: get_operation_logs_by_action_api_v1_operation_logs_action__action__get
**curl命令**:
```bash
curl -X GET "http://127.0.0.1:8000/api/v1/operation-logs/action/{action}" -H "accept: application/json"
```

#### GET /api/v1/file-definitions/file-definitions/
**摘要**: Get File Definitions
**操作ID**: get_file_definitions_api_v1_file_definitions_file_definitions__get
**curl命令**:
```bash
curl -X GET "http://127.0.0.1:8000/api/v1/file-definitions/file-definitions/" -H "accept: application/json"
```

#### POST /api/v1/file-definitions/file-definitions/
**摘要**: Create File Definition
**操作ID**: create_file_definition_api_v1_file_definitions_file_definitions__post
**curl命令**:
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/file-definitions/file-definitions/" -H "accept: application/json" -H "Content-Type: application/json" -d "{}"
```

#### GET /api/v1/file-definitions/file-definitions/{id}
**摘要**: Get File Definition
**操作ID**: get_file_definition_api_v1_file_definitions_file_definitions__id__get
**curl命令**:
```bash
curl -X GET "http://127.0.0.1:8000/api/v1/file-definitions/file-definitions/{id}" -H "accept: application/json"
```

#### PUT /api/v1/file-definitions/file-definitions/{id}
**摘要**: Update File Definition
**操作ID**: update_file_definition_api_v1_file_definitions_file_definitions__id__put
**curl命令**:
```bash
curl -X PUT "http://127.0.0.1:8000/api/v1/file-definitions/file-definitions/{id}" -H "accept: application/json" -H "Content-Type: application/json" -d "{}"
```

#### DELETE /api/v1/file-definitions/file-definitions/{id}
**摘要**: Delete File Definition
**操作ID**: delete_file_definition_api_v1_file_definitions_file_definitions__id__delete
**curl命令**:
```bash
curl -X DELETE "http://127.0.0.1:8000/api/v1/file-definitions/file-definitions/{id}" -H "accept: application/json"
```

#### PATCH /api/v1/file-definitions/file-definitions/{id}/status
**摘要**: Update File Definition Status
**操作ID**: update_file_definition_status_api_v1_file_definitions_file_definitions__id__status_patch
**curl命令**:
```bash
curl -X PATCH "http://127.0.0.1:8000/api/v1/file-definitions/file-definitions/{id}/status" -H "accept: application/json" -H "Content-Type: application/json"
```

#### GET /api/v1/field-pipelines/field-pipelines/
**摘要**: Get Field Pipelines
**操作ID**: get_field_pipelines_api_v1_field_pipelines_field_pipelines__get
**curl命令**:
```bash
curl -X GET "http://127.0.0.1:8000/api/v1/field-pipelines/field-pipelines/" -H "accept: application/json"
```

#### POST /api/v1/field-pipelines/field-pipelines/
**摘要**: Create Field Pipeline
**操作ID**: create_field_pipeline_api_v1_field_pipelines_field_pipelines__post
**curl命令**:
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/field-pipelines/field-pipelines/" -H "accept: application/json" -H "Content-Type: application/json" -d "{}"
```

#### GET /api/v1/field-pipelines/field-pipelines/{id}
**摘要**: Get Field Pipeline
**操作ID**: get_field_pipeline_api_v1_field_pipelines_field_pipelines__id__get
**curl命令**:
```bash
curl -X GET "http://127.0.0.1:8000/api/v1/field-pipelines/field-pipelines/{id}" -H "accept: application/json"
```

#### PUT /api/v1/field-pipelines/field-pipelines/{id}
**摘要**: Update Field Pipeline
**操作ID**: update_field_pipeline_api_v1_field_pipelines_field_pipelines__id__put
**curl命令**:
```bash
curl -X PUT "http://127.0.0.1:8000/api/v1/field-pipelines/field-pipelines/{id}" -H "accept: application/json" -H "Content-Type: application/json" -d "{}"
```

#### DELETE /api/v1/field-pipelines/field-pipelines/{id}
**摘要**: Delete Field Pipeline
**操作ID**: delete_field_pipeline_api_v1_field_pipelines_field_pipelines__id__delete
**curl命令**:
```bash
curl -X DELETE "http://127.0.0.1:8000/api/v1/field-pipelines/field-pipelines/{id}" -H "accept: application/json"
```

#### PATCH /api/v1/field-pipelines/field-pipelines/{id}/status
**摘要**: Update Field Pipeline Status
**操作ID**: update_field_pipeline_status_api_v1_field_pipelines_field_pipelines__id__status_patch
**curl命令**:
```bash
curl -X PATCH "http://127.0.0.1:8000/api/v1/field-pipelines/field-pipelines/{id}/status" -H "accept: application/json" -H "Content-Type: application/json"
```

#### GET /api/v1/field-pipelines/field-pipelines/execution-order/{file_type}
**摘要**: Get Execution Order
**操作ID**: get_execution_order_api_v1_field_pipelines_field_pipelines_execution_order__file_type__get
**curl命令**:
```bash
curl -X GET "http://127.0.0.1:8000/api/v1/field-pipelines/field-pipelines/execution-order/{file_type}" -H "accept: application/json"
```

#### GET /api/v1/rule-definitions/rule-definitions/
**摘要**: Get Rule Definitions
**操作ID**: get_rule_definitions_api_v1_rule_definitions_rule_definitions__get
**curl命令**:
```bash
curl -X GET "http://127.0.0.1:8000/api/v1/rule-definitions/rule-definitions/" -H "accept: application/json"
```

#### POST /api/v1/rule-definitions/rule-definitions/
**摘要**: Create Rule Definition
**操作ID**: create_rule_definition_api_v1_rule_definitions_rule_definitions__post
**curl命令**:
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/rule-definitions/rule-definitions/" -H "accept: application/json" -H "Content-Type: application/json" -d "{}"
```

#### GET /api/v1/rule-definitions/rule-definitions/{rule_ref}
**摘要**: Get Rule Definition
**操作ID**: get_rule_definition_api_v1_rule_definitions_rule_definitions__rule_ref__get
**curl命令**:
```bash
curl -X GET "http://127.0.0.1:8000/api/v1/rule-definitions/rule-definitions/{rule_ref}" -H "accept: application/json"
```

#### PUT /api/v1/rule-definitions/rule-definitions/{rule_ref}
**摘要**: Update Rule Definition
**操作ID**: update_rule_definition_api_v1_rule_definitions_rule_definitions__rule_ref__put
**curl命令**:
```bash
curl -X PUT "http://127.0.0.1:8000/api/v1/rule-definitions/rule-definitions/{rule_ref}" -H "accept: application/json" -H "Content-Type: application/json" -d "{}"
```

#### DELETE /api/v1/rule-definitions/rule-definitions/{rule_ref}
**摘要**: Delete Rule Definition
**操作ID**: delete_rule_definition_api_v1_rule_definitions_rule_definitions__rule_ref__delete
**curl命令**:
```bash
curl -X DELETE "http://127.0.0.1:8000/api/v1/rule-definitions/rule-definitions/{rule_ref}" -H "accept: application/json"
```

#### PATCH /api/v1/rule-definitions/rule-definitions/{rule_ref}/status
**摘要**: Update Rule Definition Status
**操作ID**: update_rule_definition_status_api_v1_rule_definitions_rule_definitions__rule_ref__status_patch
**curl命令**:
```bash
curl -X PATCH "http://127.0.0.1:8000/api/v1/rule-definitions/rule-definitions/{rule_ref}/status" -H "accept: application/json" -H "Content-Type: application/json"
```

#### GET /api/v1/admin/users/
**摘要**: Admin Get Users
**操作ID**: admin_get_users_api_v1_admin_users__get
**curl命令**:
```bash
curl -X GET "http://127.0.0.1:8000/api/v1/admin/users/" -H "accept: application/json"
```

#### POST /api/v1/admin/users/
**摘要**: Admin Create User
**操作ID**: admin_create_user_api_v1_admin_users__post
**curl命令**:
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/admin/users/" -H "accept: application/json" -H "Content-Type: application/json" -d "{}"
```

#### PUT /api/v1/admin/users/{id}
**摘要**: Admin Enable Disable User
**操作ID**: admin_enable_disable_user_api_v1_admin_users__id__put
**curl命令**:
```bash
curl -X PUT "http://127.0.0.1:8000/api/v1/admin/users/{id}" -H "accept: application/json" -H "Content-Type: application/json"
```

#### POST /api/v1/admin/users/{id}/reset-password
**摘要**: Admin Reset Password
**操作ID**: admin_reset_password_api_v1_admin_users__id__reset_password_post
**curl命令**:
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/admin/users/{id}/reset-password" -H "accept: application/json" -H "Content-Type: application/json" -d "{}"
```

#### GET /api/v1/admin/operation-logs
**摘要**: Admin Get Operation Logs
**操作ID**: admin_get_operation_logs_api_v1_admin_operation_logs_get
**curl命令**:
```bash
curl -X GET "http://127.0.0.1:8000/api/v1/admin/operation-logs" -H "accept: application/json"
```

