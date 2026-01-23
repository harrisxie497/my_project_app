from typing import Dict, List, Any
from datetime import datetime
from app.services.base_processor import BaseProcessor
import logging

logger = logging.getLogger(__name__)

class CustomsProcessor(BaseProcessor):
    """清关文件处理器，处理清关文件的生成"""
    
    def _get_template_mapping(self) -> Dict[str, Dict[str, Any]]:
        """
        获取清关文件模板映射
        
        Returns:
            模板映射字典
        """
        logger.info("加载清关文件模板映射")
        return {
            "MAWB NO": {
                "source_field": "MAWB NO",
                "default_value": "16003270890"
            },
            "FLIGHT NO": {
                "source_field": "FLIGHT NO",
                "default_value": "CX596"
            },
            "ARRIVAL DATE": {
                "source_field": "ARRIVAL DATE",
                "default_value": datetime.now().strftime("%Y%m%d")
            }
        }
    
    def _get_processing_rules(self) -> List[Dict[str, Any]]:
        """
        获取清关文件处理规则
        
        Returns:
            处理规则列表
        """
        logger.info("加载清关文件处理规则")
        return [
            {
                "field_name": "MAWB NO",
                "transformation_type": "validate_required",
                "params": {"message": "MAWB NO 是必填字段"},
                "order_no": 1
            },
            {
                "field_name": "FLIGHT NO",
                "transformation_type": "validate_required",
                "params": {"message": "FLIGHT NO 是必填字段"},
                "order_no": 2
            },
            {
                "field_name": "ARRIVAL DATE",
                "transformation_type": "validate_required",
                "params": {"message": "ARRIVAL DATE 是必填字段"},
                "order_no": 3
            },
            {
                "field_name": "MAWB NO",
                "transformation_type": "uppercase",
                "order_no": 4
            },
            {
                "field_name": "FLIGHT NO",
                "transformation_type": "uppercase",
                "order_no": 5
            }
        ]
