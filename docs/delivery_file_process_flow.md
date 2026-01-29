# 派单文件处理流程设计

## 一、流程概述

派单文件处理流程是指从用户上传源Excel文件开始，系统按照配置规则自动处理并生成结果Excel文件的完整过程。该流程遵循项目的核心设计原则：**源文件 → 配置规则 → 结果文件**。

## 二、核心组件

| 组件名称 | 职责 | 实现位置 |
|---------|------|----------|
| 文件上传服务 | 接收用户上传的源文件，存储到本地 | backend/app/services/file_processor.py |
| 文件解析器 | 解析Excel文件，提取sheet和数据 | backend/app/services/file_processor.py |
| 配置加载器 | 加载派单文件的配置规则 | backend/app/services/file_processor.py |
| 字段处理器 | 按照配置规则处理每个字段 | backend/app/services/base_processor.py |
| 规则执行器 | 执行具体的规则逻辑 | backend/app/services/delivery_processor.py |
| 结果生成器 | 生成结果Excel文件 | backend/app/services/file_processor.py |
| 任务管理器 | 管理整个处理流程的状态 | backend/app/models/task.py |

## 三、详细流程

### 1. 用户上传源文件

- **触发方式**：用户通过前端界面上传Excel文件
- **请求路径**：`POST /api/v1/tasks/upload`
- **处理逻辑**：
  - 接收文件并验证文件类型
  - 生成唯一任务ID
  - 创建任务记录，状态设为"pending"
  - 将文件存储到指定目录
  - 返回任务ID给前端

### 2. 任务初始化

- **触发方式**：文件上传完成后自动触发
- **处理逻辑**：
  - 更新任务状态为"processing"
  - 记录开始时间
  - 加载派单文件配置

### 3. 文件解析与验证

- **核心函数**：`parse_excel_file()`
- **处理逻辑**：
  - 使用openpyxl读取Excel文件
  - 根据`file_definitions`配置验证sheet名称、表头行、数据起始行
  - 解析数据并转换为内部数据结构
  - 验证数据完整性

### 4. 配置加载

- **核心函数**：`load_config()`
- **处理逻辑**：
  - 从数据库加载`file_definitions`配置
  - 从数据库加载`field_pipelines`配置
  - 从数据库加载`rule_definitions`配置
  - 按执行顺序排序`field_pipelines`

### 5. 字段处理（核心环节）

- **核心函数**：`process_fields()`
- **处理逻辑**：
  - 遍历所有字段映射（按执行顺序）
  - 对每个字段执行以下操作：
    1. **获取源数据**：根据`source_cols`从源数据中获取需要处理的字段值
    2. **应用映射操作**：根据`map_op`（COPY/CONST/INPUT）执行基本映射
    3. **应用字段类型处理**：根据`field_type`（COPY/FORMAT/DEFAULT/CALC/RULE_FIX/CONST）执行相应处理
    4. **应用规则**：按顺序执行`rule_ref`中引用的规则
    5. **处理依赖关系**：确保依赖的字段已被处理
    6. **存储处理结果**：将处理结果存储到结果数据结构中

### 6. 规则执行

- **核心函数**：`execute_rule()`
- **处理逻辑**：
  - 根据`rule_ref`查找对应的规则定义
  - 根据`rule_type`和`executor_type`选择合适的执行器
  - 传递参数并执行规则
  - 返回执行结果

### 7. 结果文件生成

- **核心函数**：`generate_result_file()`
- **处理逻辑**：
  - 创建新的Excel文件
  - 根据`file_definitions`配置设置sheet名称、表头
  - 将处理后的数据写入Excel文件
  - 保存文件到指定目录

### 8. 任务完成

- **处理逻辑**：
  - 更新任务状态为"completed"
  - 记录结束时间和处理结果
  - 生成下载链接
  - 发送通知给前端

## 四、关键数据结构

### 1. 任务对象

```python
class Task:
    id: str
    user_id: str
    file_type: str  # DELIVERY/CUSTOMS
    status: str  # pending/processing/completed/failed
    source_file_path: str
    result_file_path: str
    error_message: str
    created_at: datetime
    updated_at: datetime
    started_at: datetime
    completed_at: datetime
```

### 2. 处理上下文

```python
class ProcessingContext:
    task_id: str
    file_type: str
    source_data: list[dict]  # 源数据，每个元素是一行数据
    result_data: list[dict]  # 结果数据，每个元素是一行数据
    config: dict  # 配置规则
    errors: list[str]  # 错误信息
    warnings: list[str]  # 警告信息
    current_row: int  # 当前处理的行号
    current_field: str  # 当前处理的字段
```

## 五、错误处理机制

1. **文件验证错误**：返回具体的验证失败原因，如sheet名称不匹配、表头行不正确等
2. **数据格式错误**：记录错误行号和字段，继续处理其他行
3. **规则执行错误**：根据`on_fail`配置决定是跳过还是终止处理
4. **系统错误**：记录详细错误日志，返回友好的错误信息给用户

## 六、日志记录

1. **任务日志**：记录任务的开始、结束时间和状态变化
2. **处理日志**：记录每个字段的处理过程和结果
3. **错误日志**：记录所有错误和警告信息
4. **性能日志**：记录每个步骤的执行时间，用于优化

## 七、流程时序图

```
用户 → 前端 → API → 任务创建 → 文件上传 → 文件解析 → 配置加载 → 字段处理 → 规则执行 → 结果生成 → 任务完成 → 前端通知 → 用户下载
```

## 八、实现计划

### 1. 第一阶段：核心组件实现
- 完成文件上传和解析功能
- 实现配置加载功能
- 实现基本的字段处理框架

### 2. 第二阶段：规则执行实现
- 实现各类规则的执行逻辑
- 支持依赖关系处理
- 实现错误处理和日志记录

### 3. 第三阶段：结果生成实现
- 实现结果Excel文件生成
- 支持多sheet处理
- 实现文件下载功能

### 4. 第四阶段：测试和优化
- 编写单元测试
- 进行集成测试
- 性能优化
- 完善错误处理

## 九、技术栈

- **文件处理**：openpyxl
- **配置管理**：SQLAlchemy + MySQL
- **规则执行**：Python函数 + 动态调用
- **API框架**：FastAPI
- **任务管理**：SQLAlchemy

## 十、扩展考虑

1. **支持多文件类型**：设计为可扩展架构，方便添加其他文件类型的处理
2. **支持并行处理**：考虑使用多线程或异步处理提高性能
3. **支持批量处理**：支持一次上传多个文件进行批量处理
4. **支持规则可视化配置**：未来可扩展为可视化配置界面
5. **支持版本回溯**：保存配置和结果的版本，支持回溯查看

## 十一、关键接口设计

| 接口路径 | 方法 | 功能 |
|---------|------|------|
| /api/v1/tasks/upload | POST | 上传源文件，创建任务 |
| /api/v1/tasks/{task_id} | GET | 获取任务状态 |
| /api/v1/tasks/{task_id}/files/{file_kind} | GET | 下载文件（源文件或结果文件） |
| /api/v1/tasks | GET | 获取任务列表 |
| /api/v1/tasks/{task_id}/cancel | POST | 取消任务 |

## 十二、预期效果

1. **自动化处理**：用户只需上传源文件，系统自动完成所有处理
2. **可配置性**：通过配置管理处理规则，无需修改代码
3. **可扩展性**：支持添加新的文件类型和处理规则
4. **可监控性**：实时监控任务状态，查看处理日志
5. **可追溯性**：保存完整的处理记录，支持回溯查看

以上流程设计遵循了项目的核心原则，实现了从源文件到结果文件的自动化处理，同时保持了良好的可扩展性和可维护性。
