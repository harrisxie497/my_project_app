# API接口测试报告

**测试时间**: 2026-01-25_16-00-18

**测试总数**: 45
**成功数**: 0
**失败数**: 45

## 详细测试结果

### other

#### ❌ 失败 GET /health
**摘要**: Health Check
**操作ID**: health_check_health_get
**命令**: `curl -X GET "http://127.0.0.1:8000/health" -H "accept: application/json"`
**退出码**: 1
**输出**:
```
Invoke-WebRequest : 找不到接受实际参数“cu
rl -X GET http://127.0.0.1:8000/health -H 
accept: application/json”的位置形式参数。
所在位置 行:1 字符: 1
+ curl --% curl -X GET http://127.0.0.1:80
00/health -H accept: applicat ...
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : InvalidArgu 
   ment: (:) [Invoke-WebRequest]，Paramet 
   erBindingException
    + FullyQualifiedErrorId : PositionalP 
   arameterNotFound,Microsoft.PowerShell  
  .Commands.InvokeWebRequestCommand
 

```

#### ❌ 失败 GET /
**摘要**: Root
**操作ID**: root__get
**命令**: `curl -X GET "http://127.0.0.1:8000/" -H "accept: application/json"`
**退出码**: 1
**输出**:
```
Invoke-WebRequest : 找不到接受实际参数“cu
rl -X GET http://127.0.0.1:8000/ -H accept
: application/json”的位置形式参数。
所在位置 行:1 字符: 1
+ curl --% curl -X GET http://127.0.0.1:80
00/ -H accept: application/js ...
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : InvalidArgu 
   ment: (:) [Invoke-WebRequest]，Paramet 
   erBindingException
    + FullyQualifiedErrorId : PositionalP 
   arameterNotFound,Microsoft.PowerShell  
  .Commands.InvokeWebRequestCommand
 

```

### v1

#### ❌ 失败 POST /api/v1/auth/login
**摘要**: Login
**操作ID**: login_api_v1_auth_login_post
**命令**: `curl -X POST "http://127.0.0.1:8000/api/v1/auth/login" -H "accept: application/json" -H "Content-Type: application/json" -d "{}"`
**退出码**: 1
**输出**:
```
Invoke-WebRequest : 找不到接受实际参数“cu
rl -X POST http://127.0.0.1:8000/api/v1/au
th/login -H accept: application/json -H Co
ntent-Type: application/json -d {}”的位置
形式参数。
所在位置 行:1 字符: 1
+ curl --% curl -X POST http://127.0.0.1:8
000/api/v1/auth/login -H acce ...
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : InvalidArgu 
   ment: (:) [Invoke-WebRequest]，Paramet 
   erBindingException
    + FullyQualifiedErrorId : PositionalP 
   arameterNotFound,Microsoft.PowerShell  
  .Commands.InvokeWebRequestCommand
 

```

#### ❌ 失败 GET /api/v1/auth/me
**摘要**: Get Me
**操作ID**: get_me_api_v1_auth_me_get
**命令**: `curl -X GET "http://127.0.0.1:8000/api/v1/auth/me" -H "accept: application/json"`
**退出码**: 1
**输出**:
```
Invoke-WebRequest : 找不到接受实际参数“cu
rl -X GET http://127.0.0.1:8000/api/v1/aut
h/me -H accept: application/json”的位置形
式参数。
所在位置 行:1 字符: 1
+ curl --% curl -X GET http://127.0.0.1:80
00/api/v1/auth/me -H accept:  ...
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : InvalidArgu 
   ment: (:) [Invoke-WebRequest]，Paramet 
   erBindingException
    + FullyQualifiedErrorId : PositionalP 
   arameterNotFound,Microsoft.PowerShell  
  .Commands.InvokeWebRequestCommand
 

```

#### ❌ 失败 POST /api/v1/auth/logout
**摘要**: Logout
**操作ID**: logout_api_v1_auth_logout_post
**命令**: `curl -X POST "http://127.0.0.1:8000/api/v1/auth/logout" -H "accept: application/json" -H "Content-Type: application/json"`
**退出码**: 1
**输出**:
```
Invoke-WebRequest : 找不到接受实际参数“cu
rl -X POST http://127.0.0.1:8000/api/v1/au
th/logout -H accept: application/json -H C
ontent-Type: application/json”的位置形式
参数。
所在位置 行:1 字符: 1
+ curl --% curl -X POST http://127.0.0.1:8
000/api/v1/auth/logout -H acc ...
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : InvalidArgu 
   ment: (:) [Invoke-WebRequest]，Paramet 
   erBindingException
    + FullyQualifiedErrorId : PositionalP 
   arameterNotFound,Microsoft.PowerShell  
  .Commands.InvokeWebRequestCommand
 

```

#### ❌ 失败 POST /api/v1/tasks
**摘要**: Create Task
**操作ID**: create_task_api_v1_tasks_post
**命令**: `curl -X POST "http://127.0.0.1:8000/api/v1/tasks" -H "accept: application/json" -H "Content-Type: application/json" -d "{}"`
**退出码**: 1
**输出**:
```
Invoke-WebRequest : 找不到接受实际参数“cu
rl -X POST http://127.0.0.1:8000/api/v1/ta
sks -H accept: application/json -H Content
-Type: application/json -d {}”的位置形式
参数。
所在位置 行:1 字符: 1
+ curl --% curl -X POST http://127.0.0.1:8
000/api/v1/tasks -H accept: a ...
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : InvalidArgu 
   ment: (:) [Invoke-WebRequest]，Paramet 
   erBindingException
    + FullyQualifiedErrorId : PositionalP 
   arameterNotFound,Microsoft.PowerShell  
  .Commands.InvokeWebRequestCommand
 

```

#### ❌ 失败 GET /api/v1/tasks
**摘要**: Get Tasks
**操作ID**: get_tasks_api_v1_tasks_get
**命令**: `curl -X GET "http://127.0.0.1:8000/api/v1/tasks" -H "accept: application/json"`
**退出码**: 1
**输出**:
```
Invoke-WebRequest : 找不到接受实际参数“cu
rl -X GET http://127.0.0.1:8000/api/v1/tas
ks -H accept: application/json”的位置形式
参数。
所在位置 行:1 字符: 1
+ curl --% curl -X GET http://127.0.0.1:80
00/api/v1/tasks -H accept: ap ...
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : InvalidArgu 
   ment: (:) [Invoke-WebRequest]，Paramet 
   erBindingException
    + FullyQualifiedErrorId : PositionalP 
   arameterNotFound,Microsoft.PowerShell  
  .Commands.InvokeWebRequestCommand
 

```

#### ❌ 失败 POST /api/v1/tasks/{task_id}/run
**摘要**: Run Task
**操作ID**: run_task_api_v1_tasks__task_id__run_post
**命令**: `curl -X POST "http://127.0.0.1:8000/api/v1/tasks/{task_id}/run" -H "accept: application/json" -H "Content-Type: application/json"`
**退出码**: 1
**输出**:
```
Invoke-WebRequest : 找不到接受实际参数“cu
rl -X POST http://127.0.0.1:8000/api/v1/ta
sks/{task_id}/run -H accept: application/j
son -H Content-Type: application/json”的
位置形式参数。
所在位置 行:1 字符: 1
+ curl --% curl -X POST http://127.0.0.1:8
000/api/v1/tasks/{task_id}/ru ...
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : InvalidArgu 
   ment: (:) [Invoke-WebRequest]，Paramet 
   erBindingException
    + FullyQualifiedErrorId : PositionalP 
   arameterNotFound,Microsoft.PowerShell  
  .Commands.InvokeWebRequestCommand
 

```

#### ❌ 失败 GET /api/v1/tasks/{task_id}
**摘要**: Get Task Detail
**操作ID**: get_task_detail_api_v1_tasks__task_id__get
**命令**: `curl -X GET "http://127.0.0.1:8000/api/v1/tasks/{task_id}" -H "accept: application/json"`
**退出码**: 1
**输出**:
```
Invoke-WebRequest : 找不到接受实际参数“cu
rl -X GET http://127.0.0.1:8000/api/v1/tas
ks/{task_id} -H accept: application/json”
的位置形式参数。
所在位置 行:1 字符: 1
+ curl --% curl -X GET http://127.0.0.1:80
00/api/v1/tasks/{task_id} -H  ...
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : InvalidArgu 
   ment: (:) [Invoke-WebRequest]，Paramet 
   erBindingException
    + FullyQualifiedErrorId : PositionalP 
   arameterNotFound,Microsoft.PowerShell  
  .Commands.InvokeWebRequestCommand
 

```

#### ❌ 失败 GET /api/v1/tasks/{task_id}/files/{file_kind}
**摘要**: Download Task File
**操作ID**: download_task_file_api_v1_tasks__task_id__files__file_kind__get
**命令**: `curl -X GET "http://127.0.0.1:8000/api/v1/tasks/{task_id}/files/{file_kind}" -H "accept: application/json"`
**退出码**: 1
**输出**:
```
Invoke-WebRequest : 找不到接受实际参数“cu
rl -X GET http://127.0.0.1:8000/api/v1/tas
ks/{task_id}/files/{file_kind} -H accept: 
application/json”的位置形式参数。
所在位置 行:1 字符: 1
+ curl --% curl -X GET http://127.0.0.1:80
00/api/v1/tasks/{task_id}/fil ...
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : InvalidArgu 
   ment: (:) [Invoke-WebRequest]，Paramet 
   erBindingException
    + FullyQualifiedErrorId : PositionalP 
   arameterNotFound,Microsoft.PowerShell  
  .Commands.InvokeWebRequestCommand
 

```

#### ❌ 失败 GET /api/v1/users/
**摘要**: Get Users
**操作ID**: get_users_api_v1_users__get
**命令**: `curl -X GET "http://127.0.0.1:8000/api/v1/users/" -H "accept: application/json"`
**退出码**: 1
**输出**:
```
Invoke-WebRequest : 找不到接受实际参数“cu
rl -X GET http://127.0.0.1:8000/api/v1/use
rs/ -H accept: application/json”的位置形
式参数。
所在位置 行:1 字符: 1
+ curl --% curl -X GET http://127.0.0.1:80
00/api/v1/users/ -H accept: a ...
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : InvalidArgu 
   ment: (:) [Invoke-WebRequest]，Paramet 
   erBindingException
    + FullyQualifiedErrorId : PositionalP 
   arameterNotFound,Microsoft.PowerShell  
  .Commands.InvokeWebRequestCommand
 

```

#### ❌ 失败 POST /api/v1/users/
**摘要**: Create User
**操作ID**: create_user_api_v1_users__post
**命令**: `curl -X POST "http://127.0.0.1:8000/api/v1/users/" -H "accept: application/json" -H "Content-Type: application/json" -d "{}"`
**退出码**: 1
**输出**:
```
Invoke-WebRequest : 找不到接受实际参数“cu
rl -X POST http://127.0.0.1:8000/api/v1/us
ers/ -H accept: application/json -H Conten
t-Type: application/json -d {}”的位置形式
参数。
所在位置 行:1 字符: 1
+ curl --% curl -X POST http://127.0.0.1:8
000/api/v1/users/ -H accept:  ...
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : InvalidArgu 
   ment: (:) [Invoke-WebRequest]，Paramet 
   erBindingException
    + FullyQualifiedErrorId : PositionalP 
   arameterNotFound,Microsoft.PowerShell  
  .Commands.InvokeWebRequestCommand
 

```

#### ❌ 失败 GET /api/v1/users/{id}
**摘要**: Get User
**操作ID**: get_user_api_v1_users__id__get
**命令**: `curl -X GET "http://127.0.0.1:8000/api/v1/users/{id}" -H "accept: application/json"`
**退出码**: 1
**输出**:
```
Invoke-WebRequest : 找不到接受实际参数“cu
rl -X GET http://127.0.0.1:8000/api/v1/use
rs/{id} -H accept: application/json”的位
置形式参数。
所在位置 行:1 字符: 1
+ curl --% curl -X GET http://127.0.0.1:80
00/api/v1/users/{id} -H accep ...
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : InvalidArgu 
   ment: (:) [Invoke-WebRequest]，Paramet 
   erBindingException
    + FullyQualifiedErrorId : PositionalP 
   arameterNotFound,Microsoft.PowerShell  
  .Commands.InvokeWebRequestCommand
 

```

#### ❌ 失败 PUT /api/v1/users/{id}
**摘要**: Update User
**操作ID**: update_user_api_v1_users__id__put
**命令**: `curl -X PUT "http://127.0.0.1:8000/api/v1/users/{id}" -H "accept: application/json" -H "Content-Type: application/json" -d "{}"`
**退出码**: 1
**输出**:
```
Invoke-WebRequest : 找不到接受实际参数“cu
rl -X PUT http://127.0.0.1:8000/api/v1/use
rs/{id} -H accept: application/json -H Con
tent-Type: application/json -d {}”的位置
形式参数。
所在位置 行:1 字符: 1
+ curl --% curl -X PUT http://127.0.0.1:80
00/api/v1/users/{id} -H accep ...
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : InvalidArgu 
   ment: (:) [Invoke-WebRequest]，Paramet 
   erBindingException
    + FullyQualifiedErrorId : PositionalP 
   arameterNotFound,Microsoft.PowerShell  
  .Commands.InvokeWebRequestCommand
 

```

#### ❌ 失败 DELETE /api/v1/users/{id}
**摘要**: Delete User
**操作ID**: delete_user_api_v1_users__id__delete
**命令**: `curl -X DELETE "http://127.0.0.1:8000/api/v1/users/{id}" -H "accept: application/json"`
**退出码**: 1
**输出**:
```
Invoke-WebRequest : 找不到接受实际参数“cu
rl -X DELETE http://127.0.0.1:8000/api/v1/
users/{id} -H accept: application/json”的
位置形式参数。
所在位置 行:1 字符: 1
+ curl --% curl -X DELETE http://127.0.0.1
:8000/api/v1/users/{id} -H ac ...
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : InvalidArgu 
   ment: (:) [Invoke-WebRequest]，Paramet 
   erBindingException
    + FullyQualifiedErrorId : PositionalP 
   arameterNotFound,Microsoft.PowerShell  
  .Commands.InvokeWebRequestCommand
 

```

#### ❌ 失败 PUT /api/v1/users/{id}/enable
**摘要**: Enable User
**操作ID**: enable_user_api_v1_users__id__enable_put
**命令**: `curl -X PUT "http://127.0.0.1:8000/api/v1/users/{id}/enable" -H "accept: application/json" -H "Content-Type: application/json"`
**退出码**: 1
**输出**:
```
Invoke-WebRequest : 找不到接受实际参数“cu
rl -X PUT http://127.0.0.1:8000/api/v1/use
rs/{id}/enable -H accept: application/json
 -H Content-Type: application/json”的位置
形式参数。
所在位置 行:1 字符: 1
+ curl --% curl -X PUT http://127.0.0.1:80
00/api/v1/users/{id}/enable - ...
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : InvalidArgu 
   ment: (:) [Invoke-WebRequest]，Paramet 
   erBindingException
    + FullyQualifiedErrorId : PositionalP 
   arameterNotFound,Microsoft.PowerShell  
  .Commands.InvokeWebRequestCommand
 

```

#### ❌ 失败 PUT /api/v1/users/{id}/disable
**摘要**: Disable User
**操作ID**: disable_user_api_v1_users__id__disable_put
**命令**: `curl -X PUT "http://127.0.0.1:8000/api/v1/users/{id}/disable" -H "accept: application/json" -H "Content-Type: application/json"`
**退出码**: 1
**输出**:
```
Invoke-WebRequest : 找不到接受实际参数“cu
rl -X PUT http://127.0.0.1:8000/api/v1/use
rs/{id}/disable -H accept: application/jso
n -H Content-Type: application/json”的位
置形式参数。
所在位置 行:1 字符: 1
+ curl --% curl -X PUT http://127.0.0.1:80
00/api/v1/users/{id}/disable  ...
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : InvalidArgu 
   ment: (:) [Invoke-WebRequest]，Paramet 
   erBindingException
    + FullyQualifiedErrorId : PositionalP 
   arameterNotFound,Microsoft.PowerShell  
  .Commands.InvokeWebRequestCommand
 

```

#### ❌ 失败 GET /api/v1/operation-logs
**摘要**: Get Operation Logs
**操作ID**: get_operation_logs_api_v1_operation_logs_get
**命令**: `curl -X GET "http://127.0.0.1:8000/api/v1/operation-logs" -H "accept: application/json"`
**退出码**: 1
**输出**:
```
Invoke-WebRequest : 找不到接受实际参数“cu
rl -X GET http://127.0.0.1:8000/api/v1/ope
ration-logs -H accept: application/json”
的位置形式参数。
所在位置 行:1 字符: 1
+ curl --% curl -X GET http://127.0.0.1:80
00/api/v1/operation-logs -H a ...
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : InvalidArgu 
   ment: (:) [Invoke-WebRequest]，Paramet 
   erBindingException
    + FullyQualifiedErrorId : PositionalP 
   arameterNotFound,Microsoft.PowerShell  
  .Commands.InvokeWebRequestCommand
 

```

#### ❌ 失败 GET /api/v1/operation-logs/{id}
**摘要**: Get Operation Log
**操作ID**: get_operation_log_api_v1_operation_logs__id__get
**命令**: `curl -X GET "http://127.0.0.1:8000/api/v1/operation-logs/{id}" -H "accept: application/json"`
**退出码**: 1
**输出**:
```
Invoke-WebRequest : 找不到接受实际参数“cu
rl -X GET http://127.0.0.1:8000/api/v1/ope
ration-logs/{id} -H accept: application/js
on”的位置形式参数。
所在位置 行:1 字符: 1
+ curl --% curl -X GET http://127.0.0.1:80
00/api/v1/operation-logs/{id} ...
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : InvalidArgu 
   ment: (:) [Invoke-WebRequest]，Paramet 
   erBindingException
    + FullyQualifiedErrorId : PositionalP 
   arameterNotFound,Microsoft.PowerShell  
  .Commands.InvokeWebRequestCommand
 

```

#### ❌ 失败 GET /api/v1/operation-logs/user/{user_id}
**摘要**: Get Operation Logs By User
**操作ID**: get_operation_logs_by_user_api_v1_operation_logs_user__user_id__get
**命令**: `curl -X GET "http://127.0.0.1:8000/api/v1/operation-logs/user/{user_id}" -H "accept: application/json"`
**退出码**: 1
**输出**:
```
Invoke-WebRequest : 找不到接受实际参数“cu
rl -X GET http://127.0.0.1:8000/api/v1/ope
ration-logs/user/{user_id} -H accept: appl
ication/json”的位置形式参数。
所在位置 行:1 字符: 1
+ curl --% curl -X GET http://127.0.0.1:80
00/api/v1/operation-logs/user ...
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : InvalidArgu 
   ment: (:) [Invoke-WebRequest]，Paramet 
   erBindingException
    + FullyQualifiedErrorId : PositionalP 
   arameterNotFound,Microsoft.PowerShell  
  .Commands.InvokeWebRequestCommand
 

```

#### ❌ 失败 GET /api/v1/operation-logs/action/{action}
**摘要**: Get Operation Logs By Action
**操作ID**: get_operation_logs_by_action_api_v1_operation_logs_action__action__get
**命令**: `curl -X GET "http://127.0.0.1:8000/api/v1/operation-logs/action/{action}" -H "accept: application/json"`
**退出码**: 1
**输出**:
```
Invoke-WebRequest : 找不到接受实际参数“cu
rl -X GET http://127.0.0.1:8000/api/v1/ope
ration-logs/action/{action} -H accept: app
lication/json”的位置形式参数。
所在位置 行:1 字符: 1
+ curl --% curl -X GET http://127.0.0.1:80
00/api/v1/operation-logs/acti ...
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : InvalidArgu 
   ment: (:) [Invoke-WebRequest]，Paramet 
   erBindingException
    + FullyQualifiedErrorId : PositionalP 
   arameterNotFound,Microsoft.PowerShell  
  .Commands.InvokeWebRequestCommand
 

```

#### ❌ 失败 GET /api/v1/file-definitions/file-definitions/
**摘要**: Get File Definitions
**操作ID**: get_file_definitions_api_v1_file_definitions_file_definitions__get
**命令**: `curl -X GET "http://127.0.0.1:8000/api/v1/file-definitions/file-definitions/" -H "accept: application/json"`
**退出码**: 1
**输出**:
```
Invoke-WebRequest : 找不到接受实际参数“cu
rl -X GET http://127.0.0.1:8000/api/v1/fil
e-definitions/file-definitions/ -H accept:
 application/json”的位置形式参数。
所在位置 行:1 字符: 1
+ curl --% curl -X GET http://127.0.0.1:80
00/api/v1/file-definitions/fi ...
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : InvalidArgu 
   ment: (:) [Invoke-WebRequest]，Paramet 
   erBindingException
    + FullyQualifiedErrorId : PositionalP 
   arameterNotFound,Microsoft.PowerShell  
  .Commands.InvokeWebRequestCommand
 

```

#### ❌ 失败 POST /api/v1/file-definitions/file-definitions/
**摘要**: Create File Definition
**操作ID**: create_file_definition_api_v1_file_definitions_file_definitions__post
**命令**: `curl -X POST "http://127.0.0.1:8000/api/v1/file-definitions/file-definitions/" -H "accept: application/json" -H "Content-Type: application/json" -d "{}"`
**退出码**: 1
**输出**:
```
Invoke-WebRequest : 找不到接受实际参数“cu
rl -X POST http://127.0.0.1:8000/api/v1/fi
le-definitions/file-definitions/ -H accept
: application/json -H Content-Type: applic
ation/json -d {}”的位置形式参数。
所在位置 行:1 字符: 1
+ curl --% curl -X POST http://127.0.0.1:8
000/api/v1/file-definitions/f ...
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : InvalidArgu 
   ment: (:) [Invoke-WebRequest]，Paramet 
   erBindingException
    + FullyQualifiedErrorId : PositionalP 
   arameterNotFound,Microsoft.PowerShell  
  .Commands.InvokeWebRequestCommand
 

```

#### ❌ 失败 GET /api/v1/file-definitions/file-definitions/{id}
**摘要**: Get File Definition
**操作ID**: get_file_definition_api_v1_file_definitions_file_definitions__id__get
**命令**: `curl -X GET "http://127.0.0.1:8000/api/v1/file-definitions/file-definitions/{id}" -H "accept: application/json"`
**退出码**: 1
**输出**:
```
Invoke-WebRequest : 找不到接受实际参数“cu
rl -X GET http://127.0.0.1:8000/api/v1/fil
e-definitions/file-definitions/{id} -H acc
ept: application/json”的位置形式参数。
所在位置 行:1 字符: 1
+ curl --% curl -X GET http://127.0.0.1:80
00/api/v1/file-definitions/fi ...
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : InvalidArgu 
   ment: (:) [Invoke-WebRequest]，Paramet 
   erBindingException
    + FullyQualifiedErrorId : PositionalP 
   arameterNotFound,Microsoft.PowerShell  
  .Commands.InvokeWebRequestCommand
 

```

#### ❌ 失败 PUT /api/v1/file-definitions/file-definitions/{id}
**摘要**: Update File Definition
**操作ID**: update_file_definition_api_v1_file_definitions_file_definitions__id__put
**命令**: `curl -X PUT "http://127.0.0.1:8000/api/v1/file-definitions/file-definitions/{id}" -H "accept: application/json" -H "Content-Type: application/json" -d "{}"`
**退出码**: 1
**输出**:
```
Invoke-WebRequest : 找不到接受实际参数“cu
rl -X PUT http://127.0.0.1:8000/api/v1/fil
e-definitions/file-definitions/{id} -H acc
ept: application/json -H Content-Type: app
lication/json -d {}”的位置形式参数。
所在位置 行:1 字符: 1
+ curl --% curl -X PUT http://127.0.0.1:80
00/api/v1/file-definitions/fi ...
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : InvalidArgu 
   ment: (:) [Invoke-WebRequest]，Paramet 
   erBindingException
    + FullyQualifiedErrorId : PositionalP 
   arameterNotFound,Microsoft.PowerShell  
  .Commands.InvokeWebRequestCommand
 

```

#### ❌ 失败 DELETE /api/v1/file-definitions/file-definitions/{id}
**摘要**: Delete File Definition
**操作ID**: delete_file_definition_api_v1_file_definitions_file_definitions__id__delete
**命令**: `curl -X DELETE "http://127.0.0.1:8000/api/v1/file-definitions/file-definitions/{id}" -H "accept: application/json"`
**退出码**: 1
**输出**:
```
Invoke-WebRequest : 找不到接受实际参数“cu
rl -X DELETE http://127.0.0.1:8000/api/v1/
file-definitions/file-definitions/{id} -H 
accept: application/json”的位置形式参数。
所在位置 行:1 字符: 1
+ curl --% curl -X DELETE http://127.0.0.1
:8000/api/v1/file-definitions ...
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : InvalidArgu 
   ment: (:) [Invoke-WebRequest]，Paramet 
   erBindingException
    + FullyQualifiedErrorId : PositionalP 
   arameterNotFound,Microsoft.PowerShell  
  .Commands.InvokeWebRequestCommand
 

```

#### ❌ 失败 PATCH /api/v1/file-definitions/file-definitions/{id}/status
**摘要**: Update File Definition Status
**操作ID**: update_file_definition_status_api_v1_file_definitions_file_definitions__id__status_patch
**命令**: `curl -X PATCH "http://127.0.0.1:8000/api/v1/file-definitions/file-definitions/{id}/status" -H "accept: application/json" -H "Content-Type: application/json"`
**退出码**: 1
**输出**:
```
Invoke-WebRequest : 找不到接受实际参数“cu
rl -X PATCH http://127.0.0.1:8000/api/v1/f
ile-definitions/file-definitions/{id}/stat
us -H accept: application/json -H Content-
Type: application/json”的位置形式参数。
所在位置 行:1 字符: 1
+ curl --% curl -X PATCH http://127.0.0.1:
8000/api/v1/file-definitions/ ...
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : InvalidArgu 
   ment: (:) [Invoke-WebRequest]，Paramet 
   erBindingException
    + FullyQualifiedErrorId : PositionalP 
   arameterNotFound,Microsoft.PowerShell  
  .Commands.InvokeWebRequestCommand
 

```

#### ❌ 失败 GET /api/v1/field-pipelines/field-pipelines/
**摘要**: Get Field Pipelines
**操作ID**: get_field_pipelines_api_v1_field_pipelines_field_pipelines__get
**命令**: `curl -X GET "http://127.0.0.1:8000/api/v1/field-pipelines/field-pipelines/" -H "accept: application/json"`
**退出码**: 1
**输出**:
```
Invoke-WebRequest : 找不到接受实际参数“cu
rl -X GET http://127.0.0.1:8000/api/v1/fie
ld-pipelines/field-pipelines/ -H accept: a
pplication/json”的位置形式参数。
所在位置 行:1 字符: 1
+ curl --% curl -X GET http://127.0.0.1:80
00/api/v1/field-pipelines/fie ...
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : InvalidArgu 
   ment: (:) [Invoke-WebRequest]，Paramet 
   erBindingException
    + FullyQualifiedErrorId : PositionalP 
   arameterNotFound,Microsoft.PowerShell  
  .Commands.InvokeWebRequestCommand
 

```

#### ❌ 失败 POST /api/v1/field-pipelines/field-pipelines/
**摘要**: Create Field Pipeline
**操作ID**: create_field_pipeline_api_v1_field_pipelines_field_pipelines__post
**命令**: `curl -X POST "http://127.0.0.1:8000/api/v1/field-pipelines/field-pipelines/" -H "accept: application/json" -H "Content-Type: application/json" -d "{}"`
**退出码**: 1
**输出**:
```
Invoke-WebRequest : 找不到接受实际参数“cu
rl -X POST http://127.0.0.1:8000/api/v1/fi
eld-pipelines/field-pipelines/ -H accept: 
application/json -H Content-Type: applicat
ion/json -d {}”的位置形式参数。
所在位置 行:1 字符: 1
+ curl --% curl -X POST http://127.0.0.1:8
000/api/v1/field-pipelines/fi ...
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : InvalidArgu 
   ment: (:) [Invoke-WebRequest]，Paramet 
   erBindingException
    + FullyQualifiedErrorId : PositionalP 
   arameterNotFound,Microsoft.PowerShell  
  .Commands.InvokeWebRequestCommand
 

```

#### ❌ 失败 GET /api/v1/field-pipelines/field-pipelines/{id}
**摘要**: Get Field Pipeline
**操作ID**: get_field_pipeline_api_v1_field_pipelines_field_pipelines__id__get
**命令**: `curl -X GET "http://127.0.0.1:8000/api/v1/field-pipelines/field-pipelines/{id}" -H "accept: application/json"`
**退出码**: 1
**输出**:
```
Invoke-WebRequest : 找不到接受实际参数“cu
rl -X GET http://127.0.0.1:8000/api/v1/fie
ld-pipelines/field-pipelines/{id} -H accep
t: application/json”的位置形式参数。
所在位置 行:1 字符: 1
+ curl --% curl -X GET http://127.0.0.1:80
00/api/v1/field-pipelines/fie ...
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : InvalidArgu 
   ment: (:) [Invoke-WebRequest]，Paramet 
   erBindingException
    + FullyQualifiedErrorId : PositionalP 
   arameterNotFound,Microsoft.PowerShell  
  .Commands.InvokeWebRequestCommand
 

```

#### ❌ 失败 PUT /api/v1/field-pipelines/field-pipelines/{id}
**摘要**: Update Field Pipeline
**操作ID**: update_field_pipeline_api_v1_field_pipelines_field_pipelines__id__put
**命令**: `curl -X PUT "http://127.0.0.1:8000/api/v1/field-pipelines/field-pipelines/{id}" -H "accept: application/json" -H "Content-Type: application/json" -d "{}"`
**退出码**: 1
**输出**:
```
Invoke-WebRequest : 找不到接受实际参数“cu
rl -X PUT http://127.0.0.1:8000/api/v1/fie
ld-pipelines/field-pipelines/{id} -H accep
t: application/json -H Content-Type: appli
cation/json -d {}”的位置形式参数。
所在位置 行:1 字符: 1
+ curl --% curl -X PUT http://127.0.0.1:80
00/api/v1/field-pipelines/fie ...
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : InvalidArgu 
   ment: (:) [Invoke-WebRequest]，Paramet 
   erBindingException
    + FullyQualifiedErrorId : PositionalP 
   arameterNotFound,Microsoft.PowerShell  
  .Commands.InvokeWebRequestCommand
 

```

#### ❌ 失败 DELETE /api/v1/field-pipelines/field-pipelines/{id}
**摘要**: Delete Field Pipeline
**操作ID**: delete_field_pipeline_api_v1_field_pipelines_field_pipelines__id__delete
**命令**: `curl -X DELETE "http://127.0.0.1:8000/api/v1/field-pipelines/field-pipelines/{id}" -H "accept: application/json"`
**退出码**: 1
**输出**:
```
Invoke-WebRequest : 找不到接受实际参数“cu
rl -X DELETE http://127.0.0.1:8000/api/v1/
field-pipelines/field-pipelines/{id} -H ac
cept: application/json”的位置形式参数。
所在位置 行:1 字符: 1
+ curl --% curl -X DELETE http://127.0.0.1
:8000/api/v1/field-pipelines/ ...
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : InvalidArgu 
   ment: (:) [Invoke-WebRequest]，Paramet 
   erBindingException
    + FullyQualifiedErrorId : PositionalP 
   arameterNotFound,Microsoft.PowerShell  
  .Commands.InvokeWebRequestCommand
 

```

#### ❌ 失败 PATCH /api/v1/field-pipelines/field-pipelines/{id}/status
**摘要**: Update Field Pipeline Status
**操作ID**: update_field_pipeline_status_api_v1_field_pipelines_field_pipelines__id__status_patch
**命令**: `curl -X PATCH "http://127.0.0.1:8000/api/v1/field-pipelines/field-pipelines/{id}/status" -H "accept: application/json" -H "Content-Type: application/json"`
**退出码**: 1
**输出**:
```
Invoke-WebRequest : 找不到接受实际参数“cu
rl -X PATCH http://127.0.0.1:8000/api/v1/f
ield-pipelines/field-pipelines/{id}/status
 -H accept: application/json -H Content-Ty
pe: application/json”的位置形式参数。
所在位置 行:1 字符: 1
+ curl --% curl -X PATCH http://127.0.0.1:
8000/api/v1/field-pipelines/f ...
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : InvalidArgu 
   ment: (:) [Invoke-WebRequest]，Paramet 
   erBindingException
    + FullyQualifiedErrorId : PositionalP 
   arameterNotFound,Microsoft.PowerShell  
  .Commands.InvokeWebRequestCommand
 

```

#### ❌ 失败 GET /api/v1/field-pipelines/field-pipelines/execution-order/{file_type}
**摘要**: Get Execution Order
**操作ID**: get_execution_order_api_v1_field_pipelines_field_pipelines_execution_order__file_type__get
**命令**: `curl -X GET "http://127.0.0.1:8000/api/v1/field-pipelines/field-pipelines/execution-order/{file_type}" -H "accept: application/json"`
**退出码**: 1
**输出**:
```
Invoke-WebRequest : 找不到接受实际参数“cu
rl -X GET http://127.0.0.1:8000/api/v1/fie
ld-pipelines/field-pipelines/execution-ord
er/{file_type} -H accept: application/json
”的位置形式参数。
所在位置 行:1 字符: 1
+ curl --% curl -X GET http://127.0.0.1:80
00/api/v1/field-pipelines/fie ...
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : InvalidArgu 
   ment: (:) [Invoke-WebRequest]，Paramet 
   erBindingException
    + FullyQualifiedErrorId : PositionalP 
   arameterNotFound,Microsoft.PowerShell  
  .Commands.InvokeWebRequestCommand
 

```

#### ❌ 失败 GET /api/v1/rule-definitions/rule-definitions/
**摘要**: Get Rule Definitions
**操作ID**: get_rule_definitions_api_v1_rule_definitions_rule_definitions__get
**命令**: `curl -X GET "http://127.0.0.1:8000/api/v1/rule-definitions/rule-definitions/" -H "accept: application/json"`
**退出码**: 1
**输出**:
```
Invoke-WebRequest : 找不到接受实际参数“cu
rl -X GET http://127.0.0.1:8000/api/v1/rul
e-definitions/rule-definitions/ -H accept:
 application/json”的位置形式参数。
所在位置 行:1 字符: 1
+ curl --% curl -X GET http://127.0.0.1:80
00/api/v1/rule-definitions/ru ...
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : InvalidArgu 
   ment: (:) [Invoke-WebRequest]，Paramet 
   erBindingException
    + FullyQualifiedErrorId : PositionalP 
   arameterNotFound,Microsoft.PowerShell  
  .Commands.InvokeWebRequestCommand
 

```

#### ❌ 失败 POST /api/v1/rule-definitions/rule-definitions/
**摘要**: Create Rule Definition
**操作ID**: create_rule_definition_api_v1_rule_definitions_rule_definitions__post
**命令**: `curl -X POST "http://127.0.0.1:8000/api/v1/rule-definitions/rule-definitions/" -H "accept: application/json" -H "Content-Type: application/json" -d "{}"`
**退出码**: 1
**输出**:
```
Invoke-WebRequest : 找不到接受实际参数“cu
rl -X POST http://127.0.0.1:8000/api/v1/ru
le-definitions/rule-definitions/ -H accept
: application/json -H Content-Type: applic
ation/json -d {}”的位置形式参数。
所在位置 行:1 字符: 1
+ curl --% curl -X POST http://127.0.0.1:8
000/api/v1/rule-definitions/r ...
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : InvalidArgu 
   ment: (:) [Invoke-WebRequest]，Paramet 
   erBindingException
    + FullyQualifiedErrorId : PositionalP 
   arameterNotFound,Microsoft.PowerShell  
  .Commands.InvokeWebRequestCommand
 

```

#### ❌ 失败 GET /api/v1/rule-definitions/rule-definitions/{rule_ref}
**摘要**: Get Rule Definition
**操作ID**: get_rule_definition_api_v1_rule_definitions_rule_definitions__rule_ref__get
**命令**: `curl -X GET "http://127.0.0.1:8000/api/v1/rule-definitions/rule-definitions/{rule_ref}" -H "accept: application/json"`
**退出码**: 1
**输出**:
```
Invoke-WebRequest : 找不到接受实际参数“cu
rl -X GET http://127.0.0.1:8000/api/v1/rul
e-definitions/rule-definitions/{rule_ref} 
-H accept: application/json”的位置形式参
数。
所在位置 行:1 字符: 1
+ curl --% curl -X GET http://127.0.0.1:80
00/api/v1/rule-definitions/ru ...
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : InvalidArgu 
   ment: (:) [Invoke-WebRequest]，Paramet 
   erBindingException
    + FullyQualifiedErrorId : PositionalP 
   arameterNotFound,Microsoft.PowerShell  
  .Commands.InvokeWebRequestCommand
 

```

#### ❌ 失败 PUT /api/v1/rule-definitions/rule-definitions/{rule_ref}
**摘要**: Update Rule Definition
**操作ID**: update_rule_definition_api_v1_rule_definitions_rule_definitions__rule_ref__put
**命令**: `curl -X PUT "http://127.0.0.1:8000/api/v1/rule-definitions/rule-definitions/{rule_ref}" -H "accept: application/json" -H "Content-Type: application/json" -d "{}"`
**退出码**: 1
**输出**:
```
Invoke-WebRequest : 找不到接受实际参数“cu
rl -X PUT http://127.0.0.1:8000/api/v1/rul
e-definitions/rule-definitions/{rule_ref} 
-H accept: application/json -H Content-Typ
e: application/json -d {}”的位置形式参数
。
所在位置 行:1 字符: 1
+ curl --% curl -X PUT http://127.0.0.1:80
00/api/v1/rule-definitions/ru ...
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : InvalidArgu 
   ment: (:) [Invoke-WebRequest]，Paramet 
   erBindingException
    + FullyQualifiedErrorId : PositionalP 
   arameterNotFound,Microsoft.PowerShell  
  .Commands.InvokeWebRequestCommand
 

```

#### ❌ 失败 DELETE /api/v1/rule-definitions/rule-definitions/{rule_ref}
**摘要**: Delete Rule Definition
**操作ID**: delete_rule_definition_api_v1_rule_definitions_rule_definitions__rule_ref__delete
**命令**: `curl -X DELETE "http://127.0.0.1:8000/api/v1/rule-definitions/rule-definitions/{rule_ref}" -H "accept: application/json"`
**退出码**: 1
**输出**:
```
Invoke-WebRequest : 找不到接受实际参数“cu
rl -X DELETE http://127.0.0.1:8000/api/v1/
rule-definitions/rule-definitions/{rule_re
f} -H accept: application/json”的位置形式
参数。
所在位置 行:1 字符: 1
+ curl --% curl -X DELETE http://127.0.0.1
:8000/api/v1/rule-definitions ...
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : InvalidArgu 
   ment: (:) [Invoke-WebRequest]，Paramet 
   erBindingException
    + FullyQualifiedErrorId : PositionalP 
   arameterNotFound,Microsoft.PowerShell  
  .Commands.InvokeWebRequestCommand
 

```

#### ❌ 失败 PATCH /api/v1/rule-definitions/rule-definitions/{rule_ref}/status
**摘要**: Update Rule Definition Status
**操作ID**: update_rule_definition_status_api_v1_rule_definitions_rule_definitions__rule_ref__status_patch
**命令**: `curl -X PATCH "http://127.0.0.1:8000/api/v1/rule-definitions/rule-definitions/{rule_ref}/status" -H "accept: application/json" -H "Content-Type: application/json"`
**退出码**: 1
**输出**:
```
Invoke-WebRequest : 找不到接受实际参数“cu
rl -X PATCH http://127.0.0.1:8000/api/v1/r
ule-definitions/rule-definitions/{rule_ref
}/status -H accept: application/json -H Co
ntent-Type: application/json”的位置形式参
数。
所在位置 行:1 字符: 1
+ curl --% curl -X PATCH http://127.0.0.1:
8000/api/v1/rule-definitions/ ...
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : InvalidArgu 
   ment: (:) [Invoke-WebRequest]，Paramet 
   erBindingException
    + FullyQualifiedErrorId : PositionalP 
   arameterNotFound,Microsoft.PowerShell  
  .Commands.InvokeWebRequestCommand
 

```

#### ❌ 失败 GET /api/v1/admin/users/
**摘要**: Admin Get Users
**操作ID**: admin_get_users_api_v1_admin_users__get
**命令**: `curl -X GET "http://127.0.0.1:8000/api/v1/admin/users/" -H "accept: application/json"`
**退出码**: 1
**输出**:
```
Invoke-WebRequest : 找不到接受实际参数“cu
rl -X GET http://127.0.0.1:8000/api/v1/adm
in/users/ -H accept: application/json”的
位置形式参数。
所在位置 行:1 字符: 1
+ curl --% curl -X GET http://127.0.0.1:80
00/api/v1/admin/users/ -H acc ...
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : InvalidArgu 
   ment: (:) [Invoke-WebRequest]，Paramet 
   erBindingException
    + FullyQualifiedErrorId : PositionalP 
   arameterNotFound,Microsoft.PowerShell  
  .Commands.InvokeWebRequestCommand
 

```

#### ❌ 失败 POST /api/v1/admin/users/
**摘要**: Admin Create User
**操作ID**: admin_create_user_api_v1_admin_users__post
**命令**: `curl -X POST "http://127.0.0.1:8000/api/v1/admin/users/" -H "accept: application/json" -H "Content-Type: application/json" -d "{}"`
**退出码**: 1
**输出**:
```
Invoke-WebRequest : 找不到接受实际参数“cu
rl -X POST http://127.0.0.1:8000/api/v1/ad
min/users/ -H accept: application/json -H 
Content-Type: application/json -d {}”的位
置形式参数。
所在位置 行:1 字符: 1
+ curl --% curl -X POST http://127.0.0.1:8
000/api/v1/admin/users/ -H ac ...
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : InvalidArgu 
   ment: (:) [Invoke-WebRequest]，Paramet 
   erBindingException
    + FullyQualifiedErrorId : PositionalP 
   arameterNotFound,Microsoft.PowerShell  
  .Commands.InvokeWebRequestCommand
 

```

#### ❌ 失败 PUT /api/v1/admin/users/{id}
**摘要**: Admin Enable Disable User
**操作ID**: admin_enable_disable_user_api_v1_admin_users__id__put
**命令**: `curl -X PUT "http://127.0.0.1:8000/api/v1/admin/users/{id}" -H "accept: application/json" -H "Content-Type: application/json"`
**退出码**: 1
**输出**:
```
Invoke-WebRequest : 找不到接受实际参数“cu
rl -X PUT http://127.0.0.1:8000/api/v1/adm
in/users/{id} -H accept: application/json 
-H Content-Type: application/json”的位置
形式参数。
所在位置 行:1 字符: 1
+ curl --% curl -X PUT http://127.0.0.1:80
00/api/v1/admin/users/{id} -H ...
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : InvalidArgu 
   ment: (:) [Invoke-WebRequest]，Paramet 
   erBindingException
    + FullyQualifiedErrorId : PositionalP 
   arameterNotFound,Microsoft.PowerShell  
  .Commands.InvokeWebRequestCommand
 

```

#### ❌ 失败 POST /api/v1/admin/users/{id}/reset-password
**摘要**: Admin Reset Password
**操作ID**: admin_reset_password_api_v1_admin_users__id__reset_password_post
**命令**: `curl -X POST "http://127.0.0.1:8000/api/v1/admin/users/{id}/reset-password" -H "accept: application/json" -H "Content-Type: application/json" -d "{}"`
**退出码**: 1
**输出**:
```
Invoke-WebRequest : 找不到接受实际参数“cu
rl -X POST http://127.0.0.1:8000/api/v1/ad
min/users/{id}/reset-password -H accept: a
pplication/json -H Content-Type: applicati
on/json -d {}”的位置形式参数。
所在位置 行:1 字符: 1
+ curl --% curl -X POST http://127.0.0.1:8
000/api/v1/admin/users/{id}/r ...
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : InvalidArgu 
   ment: (:) [Invoke-WebRequest]，Paramet 
   erBindingException
    + FullyQualifiedErrorId : PositionalP 
   arameterNotFound,Microsoft.PowerShell  
  .Commands.InvokeWebRequestCommand
 

```

#### ❌ 失败 GET /api/v1/admin/operation-logs
**摘要**: Admin Get Operation Logs
**操作ID**: admin_get_operation_logs_api_v1_admin_operation_logs_get
**命令**: `curl -X GET "http://127.0.0.1:8000/api/v1/admin/operation-logs" -H "accept: application/json"`
**退出码**: 1
**输出**:
```
Invoke-WebRequest : 找不到接受实际参数“cu
rl -X GET http://127.0.0.1:8000/api/v1/adm
in/operation-logs -H accept: application/j
son”的位置形式参数。
所在位置 行:1 字符: 1
+ curl --% curl -X GET http://127.0.0.1:80
00/api/v1/admin/operation-log ...
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : InvalidArgu 
   ment: (:) [Invoke-WebRequest]，Paramet 
   erBindingException
    + FullyQualifiedErrorId : PositionalP 
   arameterNotFound,Microsoft.PowerShell  
  .Commands.InvokeWebRequestCommand
 

```

