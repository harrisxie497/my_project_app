from typing import Dict, List, Any, Optional
from datetime import datetime
import logging
import os
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)

class TaskExecutor:
    """任务执行器，负责协调整个任务执行流程"""
    
    def __init__(self, db_session: Session, task_id: str, file_type: str, header_params: dict = None):
        """
        初始化任务执行器
        
        Args:
            db_session: 数据库会话
            task_id: 任务ID
            file_type: 文件类型（DELIVERY/CUSTOMS）
            header_params: 表头参数（如: mawb_no, flight_no, arrival_date）
        """
        self.db_session = db_session
        self.task_id = task_id
        self.file_type = file_type
        self.file_definitions = None
        self.field_pipelines = None
        self.rule_definitions = None
        self.task_record = None
        self.header_params = header_params or {}
        logger.info(f"任务执行器初始化完成 - task_id: {task_id}, file_type: {file_type}, header_params: {header_params}")
    
    def execute(self, original_file_path: str, result_file_path: str) -> Dict[str, Any]:
        """
        执行任务
        
        Args:
            original_file_path: 原始文件路径
            result_file_path: 结果文件路径
            
        Returns:
            执行结果统计信息
        """
        try:
            logger.info(f"开始执行任务 {self.task_id}，文件类型：{self.file_type}")
            
            # 0. 加载任务记录
            self._load_task_record()
            
            # 1. 加载配置
            self._load_configurations()
            
            # 2. 初始化处理器
            processor = self._initialize_processor(original_file_path, result_file_path)
            
            # 3. 执行处理
            stats = processor.process()
            
            logger.info(f"任务执行完成，结果：{stats}")
            return stats
            
        except Exception as e:
            logger.error(f"任务执行失败：{str(e)}", exc_info=True)
            raise
    
    def _load_configurations(self):
        """
        加载配置信息
        """
        logger.info("加载配置信息")
        
        # 加载file_definitions
        self.file_definitions = self._load_file_definitions()
        
        # 加载field_pipelines
        self.field_pipelines = self._load_field_pipelines()
        
        # 加载rule_definitions
        self.rule_definitions = self._load_rule_definitions()
        
        logger.info("配置信息加载完成")
    
    def _load_task_record(self):
        """
        加载任务记录
        """
        from app.models.task import Task
        
        logger.info("加载任务记录")
        
        # 查询任务记录
        self.task_record = self.db_session.query(Task).filter(
            Task.id == self.task_id
        ).first()
        
        if not self.task_record:
            raise ValueError(f"任务不存在：{self.task_id}")
        
        logger.info(f"加载任务记录成功 - 任务ID: {self.task_id}, unique_code: {self.task_record.unique_code}, flight_no: {self.task_record.flight_no}, declare_date: {self.task_record.declare_date}")
    
    def _load_file_definitions(self) -> Dict[str, Any]:
        """
        加载文件定义配置
        """
        from app.models.file_definition import FileDefinition
        
        logger.info("加载file_definitions配置")
        
        # 查询派送文件的文件定义
        file_definitions = self.db_session.query(FileDefinition).filter(
            FileDefinition.file_type == self.file_type
        ).all()
        
        # 构建配置字典
        configs = {}
        for fd in file_definitions:
            configs[fd.file_role] = {
                "id": fd.id,
                "file_type": fd.file_type,
                "file_role": fd.file_role,
                "sheet_name": fd.sheet_name,
                "header_row": fd.header_row,
                "data_start_row": fd.data_start_row,
                "columns_json": fd.columns_json
            }
        
        logger.info(f"加载了 {len(configs)} 个文件定义配置")
        return configs
    
    def _load_field_pipelines(self) -> List[Dict[str, Any]]:
        """
        加载字段映射配置
        """
        from app.models.field_pipeline import FieldPipeline
        
        logger.info("加载field_pipelines配置")
        
        # 查询派送文件的字段映射
        field_pipelines = self.db_session.query(FieldPipeline).filter(
            FieldPipeline.file_type == self.file_type
        ).order_by(FieldPipeline.order_num).all()
        
        # 构建配置列表
        configs = []
        for fp in field_pipelines:
            configs.append({
                "id": fp.id,
                "file_type": fp.file_type,
                "target_col": fp.target_col,
                "target_header": fp.target_header,
                "map_op": fp.map_op,
                "source_cols": fp.source_cols,
                "field_type": fp.field_type,
                "rule_ref": fp.rule_ref,
                "depends_on": fp.depends_on,
                "order": fp.order_num,
                "enabled": fp.enabled
            })
        
        logger.info(f"加载了 {len(configs)} 个字段映射配置")
        return configs
    
    def _load_rule_definitions(self) -> Dict[str, Any]:
        """
        加载规则定义配置
        """
        from app.models.rule_definition import RuleDefinition
        
        logger.info("加载rule_definitions配置")
        
        # 查询所有规则定义
        rule_definitions = self.db_session.query(RuleDefinition).all()
        
        # 构建配置字典
        configs = {}
        for rd in rule_definitions:
            configs[rd.rule_ref] = {
                "rule_ref": rd.rule_ref,
                "rule_type": rd.rule_type,
                "executor_type": rd.executor_type,
                "schema_json": rd.schema_json,
                "enabled": rd.enabled
            }
        
        logger.info(f"加载了 {len(configs)} 个规则定义配置")
        return configs
    
    def _initialize_processor(self, original_file_path: str, result_file_path: str):
        """
        初始化处理器
        
        Args:
            original_file_path: 原始文件路径
            result_file_path: 结果文件路径
            
        Returns:
            处理器实例
        """
        if self.file_type == "CUSTOMS":
            from app.services.customs_processor import CustomsProcessor
            
            # 使用self.header_params
            header_params = self.header_params
            logger.info(f"使用header_params - header_params: {header_params}")
            
            processor = CustomsProcessor(
                task_dir=os.path.dirname(original_file_path),
                db_session=self.db_session,
                file_type='CUSTOMS',
                header_params=header_params
            )
            
            # 注入配置
            processor.file_definitions = self.file_definitions
            processor.field_pipelines = self.field_pipelines
            processor.rule_definitions = self.rule_definitions
            
            return processor
        elif self.file_type == "DELIVERY":
            from app.services.delivery_processor import DeliveryProcessor
            
            # 使用self.header_params
            header_params = self.header_params
            logger.info(f"使用header_params - header_params: {header_params}")
            
            processor = DeliveryProcessor(
                task_dir=os.path.dirname(original_file_path),
                db_session=self.db_session,
                file_type='DELIVERY',
                header_params=header_params
            )
            
            # 注入配置
            processor.file_definitions = self.file_definitions
            processor.field_pipelines = self.field_pipelines
            processor.rule_definitions = self.rule_definitions
            
            return processor
        else:
            raise ValueError(f"不支持的文件类型：{self.file_type}")
