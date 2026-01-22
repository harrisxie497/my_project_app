from sqlalchemy.orm import Session
from uuid import uuid4
from datetime import datetime
from app.models.operation_log import OperationLog
from app.models.user import User


def log_operation(
    db: Session,
    user_id: str,
    action: str,
    entity_type: str,
    entity_id: str = None,
    success: bool = True,
    message: str = "",
    detail_json: dict = None
):
    """
    记录操作日志
    
    :param db: 数据库会话
    :param user_id: 操作用户ID
    :param action: 操作类型
    :param entity_type: 操作实体类型
    :param entity_id: 操作实体ID（可选）
    :param success: 操作是否成功（默认True）
    :param message: 操作消息（默认空）
    :param detail_json: 详细信息（默认None）
    :return: None
    """
    operation_log = OperationLog(
        id=str(uuid4()),
        user_id=user_id,
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        success=success,
        message=message,
        detail_json=detail_json,
        created_at=datetime.utcnow()
    )
    
    db.add(operation_log)
    db.commit()
    db.refresh(operation_log)