from fastapi import APIRouter
from app.api.routes import auth, tasks, rule_tables, rule_items, template_mappings, ai_capabilities, excel_configs, users, operation_logs

# 创建主API路由器
router = APIRouter(redirect_slashes=False)

# 创建管理员API路由器
admin_router = APIRouter(prefix="/admin", tags=["admin"], redirect_slashes=False)

# 包含认证路由
router.include_router(auth.router, prefix="/auth", tags=["auth"])

# 包含任务路由
router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])

# 包含规则表路由
router.include_router(rule_tables.router, prefix="/rule-tables", tags=["rule-tables"])
admin_router.include_router(rule_tables.admin_router, prefix="/rule-tables", tags=["admin-rule-tables"])

# 包含规则项路由
router.include_router(rule_items.router, prefix="/rule-items", tags=["rule-items"])
admin_router.include_router(rule_items.admin_router, prefix="/rules", tags=["admin-rules"])

# 包含模板映射路由
router.include_router(template_mappings.router, prefix="/template-mappings", tags=["template-mappings"])
admin_router.include_router(template_mappings.admin_router, prefix="/template-mappings", tags=["admin-template-mappings"])

# 包含AI字段能力路由
router.include_router(ai_capabilities.router, prefix="/ai-capabilities", tags=["ai-capabilities"])
admin_router.include_router(ai_capabilities.admin_router, prefix="/ai-capabilities", tags=["admin-ai-capabilities"])

# 包含Excel配置路由
router.include_router(excel_configs.router, prefix="/excel-configs", tags=["excel-configs"])
admin_router.include_router(excel_configs.admin_router, prefix="/excel-configs", tags=["admin-excel-configs"])

# 包含用户路由
router.include_router(users.router, prefix="/users", tags=["users"])
admin_router.include_router(users.admin_router, prefix="/users", tags=["admin-users"])

# 包含操作日志路由
router.include_router(operation_logs.router, prefix="/operation-logs", tags=["operation-logs"])
admin_router.include_router(operation_logs.admin_router, prefix="/operation-logs", tags=["admin-operation-logs"])

# 包含管理员路由到主路由
router.include_router(admin_router)
