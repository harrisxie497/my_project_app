from fastapi import APIRouter
from app.api.routes import auth, tasks, users, operation_logs, file_definitions, field_pipelines, rule_definitions, test_route, test_config, test_simple

# 创建主API路由器
router = APIRouter(redirect_slashes=False)

# 包含认证路由
router.include_router(auth.router, prefix="/auth", tags=["auth"])

# 包含任务路由
router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])

# 包含用户路由
router.include_router(users.router, prefix="/users", tags=["users"])

# 包含操作日志路由
router.include_router(operation_logs.router, prefix="/operation-logs", tags=["operation-logs"])

# 包含文件定义路由
router.include_router(file_definitions.router, prefix="/file-definitions", tags=["file-definitions"])

# 包含字段映射路由
router.include_router(field_pipelines.router, prefix="/field-pipelines", tags=["field-pipelines"])

# 包含规则定义路由
router.include_router(rule_definitions.router, prefix="/rule-definitions", tags=["rule-definitions"])

# 包含测试配置路由
router.include_router(test_config.router, prefix="/test-config", tags=["test-config"])

# 包含简单测试路由
router.include_router(test_simple.router, prefix="/test-simple", tags=["test-simple"])
