from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class RuleEngine:
    """规则引擎，负责执行规则处理"""
    
    def __init__(self, rule_definitions: Dict[str, Any]):
        """
        初始化规则引擎
        
        Args:
            rule_definitions: 规则定义配置
        """
        self.rule_definitions = rule_definitions
    
    def execute(self, value: Any, rule_ref: str, row: Dict[str, Any] = None) -> Any:
        """
        执行规则
        
        Args:
            value: 原始值
            rule_ref: 规则引用
            row: 当前行数据
            
        Returns:
            处理后的值
        """
        try:
            if rule_ref not in self.rule_definitions:
                logger.warning(f"规则不存在：{rule_ref}")
                return value
            
            rule = self.rule_definitions[rule_ref]
            if not rule.get('enabled', True):
                logger.debug(f"规则已禁用：{rule_ref}")
                return value
            
            return self._apply_rule(value, rule, row or {})
            
        except Exception as e:
            logger.error(f"执行规则失败：{str(e)}", exc_info=True)
            return value
    
    def _apply_rule(self, value: Any, rule: Dict[str, Any], row: Dict[str, Any]) -> Any:
        """
        应用规则
        
        Args:
            value: 原始值
            rule: 规则定义
            row: 当前行数据
            
        Returns:
            处理后的值
        """
        rule_type = rule.get('rule_type')
        schema_json = rule.get('schema_json', {})
        
        logger.debug(f"应用规则：{rule['rule_ref']}，类型：{rule_type}")
        
        if rule_type == 'FORMAT':
            return self._apply_format_rule(value, schema_json, row)
        elif rule_type == 'CALC':
            return self._apply_calc_rule(value, schema_json, row)
        elif rule_type == 'RULE_FIX':
            return self._apply_rule_fix(value, schema_json, row)
        elif rule_type == 'CONST':
            return self._apply_const_rule(value, schema_json)
        elif rule_type == 'AI':
            return self._apply_ai_rule(value, schema_json, row)
        else:
            logger.warning(f"未知规则类型：{rule_type}")
            return value
    
    def _apply_format_rule(self, value: Any, schema: Dict[str, Any], row: Dict[str, Any]) -> Any:
        """
        应用格式化规则
        
        Args:
            value: 原始值
            schema: 规则参数
            row: 当前行数据
            
        Returns:
            格式化后的值
        """
        if value is None:
            return value
        
        # 处理日期格式化
        if schema.get('output_format') == 'YYYY-MM-DD':
            return self._format_date(value, '%Y-%m-%d')
        
        # 处理条件格式化
        if 'when_d_equals' in schema:
            # 处理时间帯指定字段的条件逻辑
            c_value = row.get('配達指定日')
            d_value = value
            
            if d_value in ['0', 0]:
                if c_value not in [None, '']:
                    return '00'
                else:
                    return ''
        
        # 处理字符删除
        if 'remove_chars' in schema:
            chars_to_remove = schema['remove_chars']
            if isinstance(value, str):
                for char in chars_to_remove:
                    value = value.replace(char, '')
                return value
        
        return value
    
    def _apply_calc_rule(self, value: Any, schema: Dict[str, Any], row: Dict[str, Any]) -> Any:
        """
        应用计算规则
        
        Args:
            value: 原始值
            schema: 规则参数
            row: 当前行数据
            
        Returns:
            计算后的值
        """
        # 处理默认值逻辑
        if 'fallback_target_col' in schema:
            fallback_col = schema['fallback_target_col']
            if value in [None, '']:
                return row.get(fallback_col)
        
        # 处理序号生成
        if schema.get('type') == 'sequence':
            return row.get('_row_index', 1)
        
        # 处理简单计算
        if 'formula' in schema:
            formula = schema['formula']
            try:
                # 简单的公式计算（示例）
                return self._calculate_formula(formula, row)
            except Exception as e:
                logger.error(f"计算公式失败：{str(e)}")
                return value
        
        return value
    
    def _apply_rule_fix(self, value: Any, schema: Dict[str, Any], row: Dict[str, Any]) -> Any:
        """
        应用规则修复
        
        Args:
            value: 原始值
            schema: 规则参数
            row: 当前行数据
            
        Returns:
            修复后的值
        """
        # 处理必填验证
        if schema.get('block_on_fail'):
            if value in [None, '']:
                # 标记错误
                field_name = schema.get('field_name', 'unknown')
                error_message = schema.get('error_message', f'{field_name} 是必填字段')
                row[f"{field_name}_error"] = error_message
        
        return value
    
    def _apply_const_rule(self, value: Any, schema: Dict[str, Any]) -> Any:
        """
        应用常量规则
        
        Args:
            value: 原始值
            schema: 规则参数
            
        Returns:
            常量值
        """
        return schema.get('value', '')
    
    def _apply_ai_rule(self, value: Any, schema: Dict[str, Any], row: Dict[str, Any]) -> Any:
        """
        应用AI规则

        Args:
            value: 原始值
            schema: 规则参数（包含 handler 和 system_prompt）
            row: 当前行数据

        Returns:
            AI处理后的值
        """
        from datetime import datetime
        from app.services import field_handlers

        # 检查是否配置了 AI 服务
        ai_service = getattr(self, 'ai_service', None)
        current_time = getattr(self, 'current_time', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        # 获取系统提示词（从配置表读取）
        system_prompt = schema.get('system_prompt', None)
        logger.debug(f"AI规则 - system_prompt: {system_prompt}")

        # 根据 handler 调用对应的 AI 方法
        handler = schema.get('handler')
        if not handler:
            logger.warning(f"AI规则缺少handler参数")
            return value

        # 构建输入数据
        input_data = {**row, '_value': value}

        try:
            if handler == 'ai_goods_name_en':
                return field_handlers.ai_goods_name_en(input_data, ai_service, current_time, system_prompt)
            elif handler == 'ai_material_translate_and_substitute':
                return field_handlers.ai_material_translate_and_substitute(input_data, ai_service, current_time, system_prompt)
            elif handler == 'ai_ja_name_clean':
                return field_handlers.ai_ja_name_clean(input_data, ai_service, current_time, system_prompt)
            elif handler == 'ai_translate_from_targetcol_to_en_upper':
                return field_handlers.ai_translate_from_targetcol_to_en_upper(input_data, ai_service, current_time, system_prompt)
            elif handler == 'ai_ja_address_clean':
                return field_handlers.ai_ja_address_clean(input_data, ai_service, current_time, system_prompt)
            elif handler == 'ai_translate_name_en_upper':
                return field_handlers.ai_translate_name_en_upper(input_data, ai_service, current_time, system_prompt)
            else:
                logger.warning(f"未知的AI handler：{handler}")
                return value
        except Exception as e:
            logger.error(f"AI规则处理失败：{handler}, 错误：{str(e)}")
            return value
    
    def _format_date(self, date_value: Any, format_str: str) -> str:
        """
        格式化日期
        
        Args:
            date_value: 原始日期值
            format_str: 目标格式字符串
            
        Returns:
            格式化后的日期字符串
        """
        from datetime import datetime
        
        if isinstance(date_value, datetime):
            return date_value.strftime(format_str)
        elif isinstance(date_value, str):
            # 尝试解析字符串日期
            try:
                # 尝试不同的日期格式
                for fmt in ['%Y-%m-%d', '%Y/%m/%d', '%d/%m/%Y', '%d-%m-%Y']:
                    try:
                        date_obj = datetime.strptime(date_value, fmt)
                        return date_obj.strftime(format_str)
                    except ValueError:
                        continue
                return date_value
            except Exception:
                return date_value
        return str(date_value)
    
    def _calculate_formula(self, formula: str, row: Dict[str, Any]) -> Any:
        """
        计算公式
        
        Args:
            formula: 公式字符串
            row: 当前行数据
            
        Returns:
            计算结果
        """
        # 简单的公式计算实现
        # 示例：支持 {字段名} 引用字段值
        try:
            # 替换字段引用
            for field, value in row.items():
                if isinstance(value, (int, float)):
                    formula = formula.replace(f"{{{field}}}", str(value))
            
            # 执行计算
            return eval(formula)
        except Exception as e:
            logger.error(f"执行公式失败：{str(e)}")
            return None
