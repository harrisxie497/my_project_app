from typing import Dict, List, Any, Optional
from datetime import datetime
from app.services.base_processor import BaseProcessor
import logging
from openpyxl import load_workbook
from openpyxl.worksheet.worksheet import Worksheet

logger = logging.getLogger(__name__)

class DeliveryProcessor(BaseProcessor):
    """派送文件处理器，处理派送文件的生成"""
    
    def _parse_original_file(self) -> tuple[Any, Worksheet]:
        """
        解析原始Excel文件，保留公式计算结果
        
        Returns:
            (workbook, sheet): 工作簿和工作表对象
        """
        logger.info(f"解析原始文件：{self.original_file_path}")
        workbook = load_workbook(self.original_file_path, data_only=True)  # data_only=True 读取公式计算结果
        sheet = workbook.active
        return workbook, sheet
    
    def _get_template_mapping(self) -> Dict[str, Dict[str, Any]]:
        """
        从数据库获取派送文件模板映射
        
        Returns:
            模板映射字典
        """
        logger.info("从数据库加载派送文件模板映射")
        
        # 如果没有数据库会话，返回默认映射
        if not self.db_session:
            logger.warning("没有数据库会话，使用默认模板映射")
            return self._get_default_template_mapping()
        
        try:
            from app.models.template_mapping import TemplateMapping
            from app.models.task import FileType
            
            # 查询启用的派送文件模板映射
            template_mapping = self.db_session.query(TemplateMapping).filter(
                TemplateMapping.file_type == FileType.DELIVERY,
                TemplateMapping.enabled == True
            ).first()
            
            if template_mapping:
                logger.info(f"找到了模板映射：{template_mapping.mapping_code}")
                # 解析列绑定JSON
                column_bindings = template_mapping.column_bindings_json
                
                # 构建模板映射字典
                template_mapping_dict = {}
                for binding in column_bindings:
                    target_field = binding.get("target_field")
                    source_field = binding.get("source_field")
                    default_value = binding.get("default_value")
                    
                    if target_field:
                        template_mapping_dict[target_field] = {
                            "source_field": source_field,
                            "default_value": default_value
                        }
                
                return template_mapping_dict
            else:
                logger.warning("没有找到启用的模板映射，使用默认映射")
                return self._get_default_template_mapping()
                
        except Exception as e:
            logger.error(f"从数据库加载模板映射失败：{str(e)}", exc_info=True)
            return self._get_default_template_mapping()
    
    def _get_default_template_mapping(self) -> Dict[str, Dict[str, Any]]:
        """
        获取默认的派送文件模板映射
        
        Returns:
            默认模板映射字典
        """
        logger.info("使用默认派送文件模板映射")
        return {
            "お客様管理番号": {
                "source_field": "お客様管理番号",
                "default_value": None
            },
            "佐川問合せ番号HAWB": {
                "source_field": "佐川問合せ番号HAWB",
                "default_value": None
            },
            "配達指定日": {
                "source_field": "配達指定日",
                "default_value": None
            },
            "時間帯指定": {
                "source_field": "時間帯指定",
                "default_value": None
            },
            "貨物個数": {
                "source_field": "貨物個数",
                "default_value": None
            },
            "お届け先人名": {
                "source_field": "お届け先人名",
                "default_value": None
            },
            "お届け先住所": {
                "source_field": "お届け先住所",
                "default_value": None
            },
            "お届け先電話": {
                "source_field": "お届け先電話",
                "default_value": None
            },
            "お届け先郵便": {
                "source_field": "お届け先郵便",
                "default_value": None
            },
            "依頼主": {
                "source_field": "依頼主",
                "default_value": None
            },
            "依頼主住所": {
                "source_field": "依頼主住所",
                "default_value": None
            },
            "依頼主郵便番号": {
                "source_field": "依頼主郵便番号",
                "default_value": None
            },
            "依頼主電話": {
                "source_field": "依頼主電話",
                "default_value": None
            },
            "佐川顧客コード（固定）": {
                "source_field": "佐川顧客コード（固定）",
                "default_value": None
            },
            "記事欄2（品名）": {
                "source_field": "記事欄2（品名）",
                "default_value": None
            },
            "記事欄2": {
                "source_field": "記事欄2",
                "default_value": "160-0327 9161"
            },
            "記事欄3": {
                "source_field": "記事欄3",
                "default_value": None
            }
        }
    
    def _process_fields(self, mapped_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        PROCESS阶段：从数据库读取规则并处理字段
        
        Args:
            mapped_data: 映射后的数据列表
        
        Returns:
            处理后的数据列表
        """
        logger.info("开始PROCESS阶段：字段处理")
        
        # 调用父类的_process_fields方法，使用规则引擎处理字段
        processed_data = super()._process_fields(mapped_data)
        
        # 额外的自定义处理
        for processed_row in processed_data:
            # 处理佐川問合せ番号HAWB字段，确保为字符串类型
            if processed_row["佐川問合せ番号HAWB"] is not None:
                processed_row["佐川問合せ番号HAWB"] = str(processed_row["佐川問合せ番号HAWB"])
        
        logger.info(f"PROCESS阶段完成，处理了 {len(processed_data)} 行数据")
        return processed_data
    
    def _get_processing_rules(self) -> List[Dict[str, Any]]:
        """
        从数据库获取派送文件处理规则
        
        Returns:
            处理规则列表
        """
        logger.info("从数据库加载派送文件处理规则")
        
        # 如果没有数据库会话，返回默认规则
        if not self.db_session:
            logger.warning("没有数据库会话，使用默认处理规则")
            return self._get_default_processing_rules()
        
        try:
            from app.models.rule_table import RuleTable
            from app.models.rule_item import RuleItem
            from app.models.task import FileType
            
            # 查询启用的派送文件处理阶段规则表
            rule_table = self.db_session.query(RuleTable).filter(
                RuleTable.file_type == FileType.DELIVERY,
                RuleTable.rule_stage == "PROCESS",
                RuleTable.enabled == True
            ).first()
            
            if rule_table:
                logger.info(f"找到了规则表：{rule_table.code}")
                
                # 查询规则表下的所有规则项
                rule_items = self.db_session.query(RuleItem).filter(
                    RuleItem.rule_table_id == rule_table.id,
                    RuleItem.enabled == True
                ).order_by(RuleItem.order_no).all()
                
                # 构建规则列表
                rules = []
                for item in rule_items:
                    rules.append({
                        "field_name": item.field_name,
                        "transformation_type": item.transformation_type,
                        "params": item.params_json,
                        "order_no": item.order_no
                    })
                
                return rules
            else:
                logger.warning("没有找到启用的处理规则表，使用默认规则")
                return self._get_default_processing_rules()
                
        except Exception as e:
            logger.error(f"从数据库加载处理规则失败：{str(e)}", exc_info=True)
            return self._get_default_processing_rules()
    
    def _get_default_processing_rules(self) -> List[Dict[str, Any]]:
        """
        获取默认的派送文件处理规则
        
        Returns:
            处理规则列表
        """
        logger.info("使用默认派送文件处理规则")
        return [
            {
                "field_name": "記事欄2",
                "transformation_type": "default_value",
                "params": {"value": "160-0327 9161"},
                "order_no": 1
            },
            {
                "field_name": "依頼主",
                "transformation_type": "default_value",
                "params": {"value": "DIDA"},
                "order_no": 2
            },
            {
                "field_name": "時間帯指定",
                "transformation_type": "conditional_expr",
                "params": {
                    "transformation_type": "conditional_expr",
                    "target_col": "時間帯指定",
                    "rules": [
                        {
                            "when": "C != '' && (D == 0 || D == '0')",
                            "set": "00"
                        },
                        {
                            "when": "C == '' && (D == 0 || D == '0')",
                            "set": ""
                        }
                    ],
                    "else": "KEEP"
                },
                "order_no": 3
            },
            {
                "field_name": "お届け先住所",
                "transformation_type": "trim",
                "params": {},
                "order_no": 4
            },
            {
                "field_name": "依頼主住所",
                "transformation_type": "trim",
                "params": {},
                "order_no": 5
            },
            {
                "field_name": "依頼主電話",
                "transformation_type": "default_value",
                "params": {"value": "0471377848"},
                "order_no": 6
            }
        ]
