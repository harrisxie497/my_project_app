from typing import Dict, Any, Optional
import logging
from app.services.delivery_processor import DeliveryProcessor
from app.services.customs_processor import CustomsProcessor

logger = logging.getLogger(__name__)

class FileProcessor:
    """文件处理服务工厂类，根据文件类型创建相应的处理器实例"""
    
    def __init__(self, task_dir: str, file_type: str, db_session: Optional[Any] = None):
        """
        初始化文件处理器
        
        Args:
            task_dir: 任务文件存储目录
            file_type: 文件类型（delivery/customs）
            db_session: 数据库会话对象，用于从数据库读取配置
        """
        self.task_dir = task_dir
        self.file_type = file_type
        
        # 根据文件类型创建相应的处理器实例，并传递数据库会话
        if file_type == "delivery":
            self.processor = DeliveryProcessor(task_dir, db_session, file_type)
        elif file_type == "customs":
            self.processor = CustomsProcessor(task_dir, db_session, file_type)
        else:
            raise ValueError(f"不支持的文件类型：{file_type}")
        
    def process(self) -> Dict[str, Any]:
        """
        执行文件处理流程
        
        Returns:
            处理结果统计信息
        """
        logger.info(f"使用{self.processor.__class__.__name__}处理文件，类型：{self.file_type}")
        return self.processor.process()
