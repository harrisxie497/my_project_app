from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger(__name__)

class FieldProcessor:
    """字段处理器，负责处理字段映射和转换"""
    
    def __init__(self, field_pipelines: List[Dict[str, Any]], rule_engine: Optional[Any] = None):
        """
        初始化字段处理器
        
        Args:
            field_pipelines: 字段处理配置列表
            rule_engine: 规则引擎实例
        """
        self.field_pipelines = field_pipelines
        self.rule_engine = rule_engine
        self.processed_fields = set()
    
    def process_fields(self, row: Dict[str, Any], source_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        处理一行数据的所有字段
        
        Args:
            row: 当前行数据，用于存储处理结果
            source_data: 源数据，用于复制数据
            
        Returns:
            处理后的行数据
        """
        try:
            # 按order排序字段处理配置
            sorted_pipelines = sorted(self.field_pipelines, key=lambda x: x.get('order', 999))
            
            self.processed_fields.clear()
            
            for pipeline in sorted_pipelines:
                target_col = pipeline.get('target_col')
                if not target_col:
                    logger.warning("字段配置缺少target_col")
                    continue
                
                # 处理依赖关系
                if not self._check_dependencies(pipeline, row):
                    logger.warning(f"字段 {target_col} 的依赖未满足，跳过处理")
                    continue
                
                # 处理字段
                processed_value = self._process_field(pipeline, row, source_data)
                row[target_col] = processed_value
                self.processed_fields.add(target_col)
            
            return row
            
        except Exception as e:
            logger.error(f"处理字段失败：{str(e)}", exc_info=True)
            return row
    
    def _check_dependencies(self, pipeline: Dict[str, Any], row: Dict[str, Any]) -> bool:
        """
        检查字段依赖关系
        
        Args:
            pipeline: 字段处理配置
            row: 当前行数据
            
        Returns:
            是否满足依赖关系
        """
        depends_on = pipeline.get('depends_on', [])
        if not depends_on:
            return True
        
        # 确保所有依赖的字段都已处理
        for dep_field in depends_on:
            if dep_field not in self.processed_fields:
                return False
        
        return True
    
    def _process_field(self, pipeline: Dict[str, Any], row: Dict[str, Any], source_data: Dict[str, Any]) -> Any:
        """
        处理单个字段
        
        Args:
            pipeline: 字段处理配置
            row: 当前行数据
            source_data: 源数据
            
        Returns:
            处理后的值
        """
        map_op = pipeline.get('map_op', 'COPY')
        source_cols = pipeline.get('source_cols', [])
        field_type = pipeline.get('field_type')
        rule_refs = pipeline.get('rule_ref', [])
        
        logger.debug(f"处理字段：{pipeline['target_col']}，操作：{map_op}，类型：{field_type}")
        
        # 执行映射操作
        value = self._execute_map_op(map_op, source_cols, source_data, pipeline)
        
        # 应用规则
        if rule_refs and self.rule_engine:
            for rule_ref in rule_refs:
                value = self.rule_engine.execute(value, rule_ref, row)
        
        return value
    
    def _execute_map_op(self, map_op: str, source_cols: List[str], source_data: Dict[str, Any], pipeline: Dict[str, Any]) -> Any:
        """
        执行映射操作
        
        Args:
            map_op: 映射操作类型
            source_cols: 源列列表
            source_data: 源数据
            pipeline: 字段处理配置
            
        Returns:
            映射后的值
        """
        if map_op == 'COPY':
            # 从源列复制数据
            if source_cols:
                # 取第一个源列的值
                source_col = source_cols[0]
                return source_data.get(source_col)
            return None
        
        elif map_op == 'CONST':
            # 设置固定值
            return pipeline.get('const_value', '')
        
        elif map_op == 'INPUT':
            # 人工输入值（暂时返回空，后续可集成前端输入）
            return ''
        
        elif map_op == 'NONE':
            # 无操作
            return None
        
        else:
            logger.warning(f"未知的映射操作：{map_op}")
            return None
    
    def validate_pipelines(self, pipelines: List[Dict[str, Any]]) -> List[str]:
        """
        验证字段处理配置
        
        Args:
            pipelines: 字段处理配置列表
            
        Returns:
            错误信息列表
        """
        errors = []
        
        for i, pipeline in enumerate(pipelines):
            # 检查必填字段
            if not pipeline.get('target_col'):
                errors.append(f"配置 {i+1}：缺少target_col")
            
            if not pipeline.get('map_op'):
                errors.append(f"配置 {i+1}：缺少map_op")
            
            if not pipeline.get('field_type'):
                errors.append(f"配置 {i+1}：缺少field_type")
            
            # 检查依赖关系
            depends_on = pipeline.get('depends_on', [])
            target_col = pipeline.get('target_col')
            
            if target_col in depends_on:
                errors.append(f"配置 {i+1}：字段 {target_col} 不能依赖自身")
        
        return errors
