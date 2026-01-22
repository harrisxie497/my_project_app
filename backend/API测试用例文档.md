# API测试用例文档

## 项目信息
- 项目名称：日本清关Excel自动生成系统
- 测试环境：本地开发环境
- 测试时间：2026-01-21
- API基础URL：http://localhost:8000/api/v1

## 测试准备

### 测试用户信息
- 用户名：admin
- 密码：admin123
- 角色：admin

### 测试文件
- 准备一个测试用的Excel文件（.xlsx格式），用于任务创建接口测试

## 认证相关测试用例

### 1. 登录接口测试

#### 测试用例1：正确用户名密码登录

| 测试项 | 内容 |
| --- | --- |
| 测试用例编号 | AUTH-001 |
| 测试用例名称 | 正确用户名密码登录 |
| 测试目的 | 验证使用正确的用户名和密码能够成功登录系统 |
| 请求URL | /api/v1/auth/login |
| 请求方法 | POST |
| 请求头 | Content-Type: application/x-www-form-urlencoded |
| 请求体 | username=admin&password=admin123 |
| 预期响应 | 200 OK，返回包含access_token的响应 |
| 实际响应 | - |
| 测试结果 | - |
| 备注 | - |

**CURL命令：**
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123"
```

#### 测试用例2：错误用户名登录

| 测试项 | 内容 |
| --- | --- |
| 测试用例编号 | AUTH-002 |
| 测试用例名称 | 错误用户名登录 |
| 测试目的 | 验证使用错误的用户名无法登录系统 |
| 请求URL | /api/v1/auth/login |
| 请求方法 | POST |
| 请求头 | Content-Type: application/x-www-form-urlencoded |
| 请求体 | username=wronguser&password=admin123 |
| 预期响应 | 401 Unauthorized，返回错误信息 |
| 实际响应 | - |
| 测试结果 | - |
| 备注 | - |

**CURL命令：**
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=wronguser&password=admin123"
```

#### 测试用例3：错误密码登录

| 测试项 | 内容 |
| --- | --- |
| 测试用例编号 | AUTH-003 |
| 测试用例名称 | 错误密码登录 |
| 测试目的 | 验证使用错误的密码无法登录系统 |
| 请求URL | /api/v1/auth/login |
| 请求方法 | POST |
| 请求头 | Content-Type: application/x-www-form-urlencoded |
| 请求体 | username=admin&password=wrongpassword |
| 预期响应 | 401 Unauthorized，返回错误信息 |
| 实际响应 | - |
| 测试结果 | - |
| 备注 | - |

**CURL命令：**
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=wrongpassword"
```

### 2. 获取当前用户信息

#### 测试用例4：获取当前用户信息

| 测试项 | 内容 |
| --- | --- |
| 测试用例编号 | AUTH-004 |
| 测试用例名称 | 获取当前用户信息 |
| 测试目的 | 验证已登录用户能够获取自己的信息 |
| 请求URL | /api/v1/auth/me |
| 请求方法 | GET |
| 请求头 | Authorization: Bearer {access_token} |
| 请求体 | 无 |
| 预期响应 | 200 OK，返回当前用户信息 |
| 实际响应 | - |
| 测试结果 | - |
| 备注 | 需先获取access_token |

**CURL命令：**
```bash
curl -X GET "http://localhost:8000/api/v1/auth/me" \
  -H "Authorization: Bearer {access_token}"
```

### 3. 登出接口测试

#### 测试用例5：登出系统

| 测试项 | 内容 |
| --- | --- |
| 测试用例编号 | AUTH-005 |
| 测试用例名称 | 登出系统 |
| 测试目的 | 验证用户能够成功登出系统 |
| 请求URL | /api/v1/auth/logout |
| 请求方法 | POST |
| 请求头 | Authorization: Bearer {access_token} |
| 请求体 | 无 |
| 预期响应 | 200 OK，返回成功信息 |
| 实际响应 | - |
| 测试结果 | - |
| 备注 | 需先获取access_token |

**CURL命令：**
```bash
curl -X POST "http://localhost:8000/api/v1/auth/logout" \
  -H "Authorization: Bearer {access_token}"
```

## 任务相关测试用例

### 1. 创建任务测试

#### 测试用例6：创建普通任务

| 测试项 | 内容 |
| --- | --- |
| 测试用例编号 | TASK-001 |
| 测试用例名称 | 创建普通任务 |
| 测试目的 | 验证用户能够成功创建任务 |
| 请求URL | /api/v1/tasks/ |
| 请求方法 | POST |
| 请求头 | Authorization: Bearer {access_token}, Content-Type: multipart/form-data |
| 请求体 | file_type=normal&unique_code=test001&file=@test.xlsx |
| 预期响应 | 200 OK，返回任务ID和状态 |
| 实际响应 | - |
| 测试结果 | - |
| 备注 | 需先获取access_token，准备test.xlsx文件 |

**CURL命令：**
```bash
curl -X POST "http://localhost:8000/api/v1/tasks/" \
  -H "Authorization: Bearer {access_token}" \
  -F "file_type=normal" \
  -F "unique_code=test001" \
  -F "file=@test.xlsx"
```

#### 测试用例7：创建清关任务

| 测试项 | 内容 |
| --- | --- |
| 测试用例编号 | TASK-002 |
| 测试用例名称 | 创建清关任务 |
| 测试目的 | 验证用户能够成功创建清关类型任务 |
| 请求URL | /api/v1/tasks/ |
| 请求方法 | POST |
| 请求头 | Authorization: Bearer {access_token}, Content-Type: multipart/form-data |
| 请求体 | file_type=customs&unique_code=customs001&flight_no=CA1234&declare_date=2026-01-21&file=@test.xlsx |
| 预期响应 | 200 OK，返回任务ID和状态 |
| 实际响应 | - |
| 测试结果 | - |
| 备注 | 需先获取access_token，准备test.xlsx文件 |

**CURL命令：**
```bash
curl -X POST "http://localhost:8000/api/v1/tasks/" \
  -H "Authorization: Bearer {access_token}" \
  -F "file_type=customs" \
  -F "unique_code=customs001" \
  -F "flight_no=CA1234" \
  -F "declare_date=2026-01-21" \
  -F "file=@test.xlsx"
```

### 2. 运行任务测试

#### 测试用例8：运行任务

| 测试项 | 内容 |
| --- | --- |
| 测试用例编号 | TASK-003 |
| 测试用例名称 | 运行任务 |
| 测试目的 | 验证用户能够成功运行任务 |
| 请求URL | /api/v1/tasks/{task_id}/run |
| 请求方法 | POST |
| 请求头 | Authorization: Bearer {access_token} |
| 请求体 | 无 |
| 预期响应 | 200 OK，返回任务ID和状态 |
| 实际响应 | - |
| 测试结果 | - |
| 备注 | 需先获取access_token和有效的task_id |

**CURL命令：**
```bash
curl -X POST "http://localhost:8000/api/v1/tasks/{task_id}/run" \
  -H "Authorization: Bearer {access_token}"
```

### 3. 获取任务列表测试

#### 测试用例9：获取所有任务列表

| 测试项 | 内容 |
| --- | --- |
| 测试用例编号 | TASK-004 |
| 测试用例名称 | 获取所有任务列表 |
| 测试目的 | 验证用户能够成功获取所有任务列表 |
| 请求URL | /api/v1/tasks/ |
| 请求方法 | GET |
| 请求头 | Authorization: Bearer {access_token} |
| 请求体 | 无 |
| 预期响应 | 200 OK，返回任务列表 |
| 实际响应 | - |
| 测试结果 | - |
| 备注 | 需先获取access_token |

**CURL命令：**
```bash
curl -X GET "http://localhost:8000/api/v1/tasks/" \
  -H "Authorization: Bearer {access_token}"
```

#### 测试用例10：按文件类型过滤任务列表

| 测试项 | 内容 |
| --- | --- |
| 测试用例编号 | TASK-005 |
| 测试用例名称 | 按文件类型过滤任务列表 |
| 测试目的 | 验证用户能够按文件类型过滤任务列表 |
| 请求URL | /api/v1/tasks/?file_type=normal |
| 请求方法 | GET |
| 请求头 | Authorization: Bearer {access_token} |
| 请求体 | 无 |
| 预期响应 | 200 OK，返回指定文件类型的任务列表 |
| 实际响应 | - |
| 测试结果 | - |
| 备注 | 需先获取access_token |

**CURL命令：**
```bash
curl -X GET "http://localhost:8000/api/v1/tasks/?file_type=normal" \
  -H "Authorization: Bearer {access_token}"
```

#### 测试用例11：按状态过滤任务列表

| 测试项 | 内容 |
| --- | --- |
| 测试用例编号 | TASK-006 |
| 测试用例名称 | 按状态过滤任务列表 |
| 测试目的 | 验证用户能够按状态过滤任务列表 |
| 请求URL | /api/v1/tasks/?status=queued |
| 请求方法 | GET |
| 请求头 | Authorization: Bearer {access_token} |
| 请求体 | 无 |
| 预期响应 | 200 OK，返回指定状态的任务列表 |
| 实际响应 | - |
| 测试结果 | - |
| 备注 | 需先获取access_token |

**CURL命令：**
```bash
curl -X GET "http://localhost:8000/api/v1/tasks/?status=queued" \
  -H "Authorization: Bearer {access_token}"
```

### 4. 获取任务详情测试

#### 测试用例12：获取任务详情

| 测试项 | 内容 |
| --- | --- |
| 测试用例编号 | TASK-007 |
| 测试用例名称 | 获取任务详情 |
| 测试目的 | 验证用户能够成功获取任务详情 |
| 请求URL | /api/v1/tasks/{task_id} |
| 请求方法 | GET |
| 请求头 | Authorization: Bearer {access_token} |
| 请求体 | 无 |
| 预期响应 | 200 OK，返回任务详情 |
| 实际响应 | - |
| 测试结果 | - |
| 备注 | 需先获取access_token和有效的task_id |

**CURL命令：**
```bash
curl -X GET "http://localhost:8000/api/v1/tasks/{task_id}" \
  -H "Authorization: Bearer {access_token}"
```

### 5. 下载任务文件测试

#### 测试用例13：下载原始文件

| 测试项 | 内容 |
| --- | --- |
| 测试用例编号 | TASK-008 |
| 测试用例名称 | 下载原始文件 |
| 测试目的 | 验证用户能够成功下载任务的原始文件 |
| 请求URL | /api/v1/tasks/{task_id}/files/original |
| 请求方法 | GET |
| 请求头 | Authorization: Bearer {access_token} |
| 请求体 | 无 |
| 预期响应 | 200 OK，返回文件内容 |
| 实际响应 | - |
| 测试结果 | - |
| 备注 | 需先获取access_token和有效的task_id |

**CURL命令：**
```bash
curl -X GET "http://localhost:8000/api/v1/tasks/{task_id}/files/original" \
  -H "Authorization: Bearer {access_token}" \
  -o original.xlsx
```

#### 测试用例14：下载结果文件

| 测试项 | 内容 |
| --- | --- |
| 测试用例编号 | TASK-009 |
| 测试用例名称 | 下载结果文件 |
| 测试目的 | 验证用户能够成功下载任务的结果文件 |
| 请求URL | /api/v1/tasks/{task_id}/files/result |
| 请求方法 | GET |
| 请求头 | Authorization: Bearer {access_token} |
| 请求体 | 无 |
| 预期响应 | 200 OK，返回文件内容（任务完成后） |
| 实际响应 | - |
| 测试结果 | - |
| 备注 | 需先获取access_token和有效的task_id，任务需已完成 |

**CURL命令：**
```bash
curl -X GET "http://localhost:8000/api/v1/tasks/{task_id}/files/result" \
  -H "Authorization: Bearer {access_token}" \
  -o result.xlsx
```

## 健康检查测试

### 测试用例15：健康检查

| 测试项 | 内容 |
| --- | --- |
| 测试用例编号 | SYS-001 |
| 测试用例名称 | 健康检查 |
| 测试目的 | 验证系统服务是否正常运行 |
| 请求URL | /health |
| 请求方法 | GET |
| 请求头 | 无 |
| 请求体 | 无 |
| 预期响应 | 200 OK，返回系统状态信息 |
| 实际响应 | - |
| 测试结果 | - |
| 备注 | - |

**CURL命令：**
```bash
curl -X GET "http://localhost:8000/health"
```

## 测试结果统计

| 测试模块 | 测试用例数 | 通过数 | 失败数 | 通过率 |
| --- | --- | --- | --- | --- |
| 认证相关 | 5 | - | - | - |
| 任务相关 | 9 | - | - | - |
| 系统相关 | 1 | - | - | - |
| 总计 | 15 | - | - | - |

## 测试总结

### 测试发现的问题

| 问题编号 | 问题描述 | 严重程度 | 修复建议 |
| --- | --- | --- | --- |
| - | - | - | - |

### 测试结论

- [ ] 所有测试用例通过
- [ ] 大部分测试用例通过，存在少量问题
- [ ] 存在较多问题，需要进一步修复

### 建议

- 建议在生产环境部署前，确保所有测试用例通过
- 建议添加更多边界条件测试用例
- 建议定期运行测试用例，确保系统稳定性

## 附录

### 状态码说明

| 状态码 | 说明 |
| --- | --- |
| 200 | 请求成功 |
| 400 | 请求参数错误 |
| 401 | 未授权，需要登录 |
| 403 | 禁止访问，权限不足 |
| 404 | 资源不存在 |
| 500 | 服务器内部错误 |

### 文件类型说明

| 文件类型 | 说明 |
| --- | --- |
| normal | 普通文件 |
| customs | 清关文件 |

### 任务状态说明

| 状态 | 说明 |
| --- | --- |
| queued | 排队中 |
| processing | 处理中 |
| success | 成功 |
| failed | 失败 |

### 响应格式说明

所有API响应均采用统一格式：

```json
{
  "data": { /* 响应数据 */ },
  "message": "success",
  "code": 0
}
```

- data：响应的具体数据
- message：响应消息，成功时为"success"，失败时为错误信息
- code：响应码，成功时为0，失败时为错误码

## 版本历史

| 版本 | 日期 | 更新内容 | 更新人 |
| --- | --- | --- | --- |
| v1.0 | 2026-01-21 | 初始版本 | AI Assistant |
