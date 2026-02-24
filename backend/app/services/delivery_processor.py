"""
DELIVERY文件处理器
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
from app.services.base_processor import BaseProcessor
from app.services.excel_reader import read_excel_file
from app.services.excel_writer import write_excel_file, write_excel_file_by_columns
from app.services.header_processor import process_header_row
from app.services.field_handlers import (
    copy_field,
    set_constant,
    generate_sequence,
    copy_equal_to,
    calc_invoice_price_fx_round,
    calc_time_slot_with_delivery_date
)
from app.services.deepseek_ai_service import DeepSeekAIService
from app.services.ai_rule_executor import AIRuleExecutor
import logging

logger = logging.getLogger(__name__)


class DeliveryProcessor(BaseProcessor):
    """DELIVERY文件处理器，处理DELIVERY文件的生成"""
    
    def __init__(self, task_dir: str, db_session=None, file_type=None, header_params: dict = None):
        """
        初始化DELIVERY文件处理器
        
        输入:
            - task_dir: 任务文件存储目录
            - db_session: 数据库会话对象
            - file_type: 文件类型（默认: DELIVERY）
            - header_params: 表头参数（如: mawb_no, flight_no, arrival_date）
        """
        super().__init__(task_dir, db_session, file_type)
        self.file_definitions = self._load_file_definitions()
        self.header_params = header_params or {}
        self.ai_service = None
        self.ai_rule_executor = None
        self.exchange_rate_service = None
        logger.info(f"DELIVERY文件处理器初始化完成，header_params: {header_params}")
    
    def _get_rule_params(self, pipeline: Dict[str, Any], rule_ref_key: str) -> Dict[str, Any]:
        """
        从pipeline中获取rule_params
        
        输入:
            - pipeline: 字段处理配置
            - rule_ref_key: 规则引用键
        
        输出:
            - 规则参数字典
        """
        import json
        
        if not pipeline:
            return {}
        
        rule_params_json = pipeline.get('rule_params_json', {})
        
        # 如果rule_params_json是字符串，则解析为字典
        if isinstance(rule_params_json, str):
            try:
                rule_params_json = json.loads(rule_params_json)
            except json.JSONDecodeError:
                logger.error(f"解析rule_params_json失败: {rule_params_json}")
                rule_params_json = {}
        
        return rule_params_json.get(rule_ref_key, {}) if rule_params_json else {}
    
    def process(self) -> Dict[str, Any]:
        """
        执行文件处理流程
        
        输出:
            - 处理结果统计信息
        """
        try:
            logger.info("=" * 100)
            logger.info("开始处理DELIVERY文件")
            logger.info("=" * 100)
            logger.info(f"处理输入 - 目录: {self.task_dir}, header_params: {self.header_params}")
            
            # 1. 解析原始文件
            logger.info("-" * 100)
            logger.info("步骤1: 解析原始文件")
            logger.info("-" * 100)
            workbook, sheet, first_row, column_data, data_row_count = self._parse_original_file()
            logger.info(f"解析原始文件完成 - 第一行: {len(first_row)}, 列数: {len(column_data)}, 数据行数: {data_row_count}")
            logger.info(f"解析原始文件完成 - 第一行数据: {first_row}")
            logger.info(f"解析原始文件完成 - 列数据: {column_data}")
            
            # 2. 处理表头行（DELIVERY不需要特殊第一行，CUSTOMS需要）
            logger.info("-" * 100)
            logger.info("步骤2: 处理表头行")
            logger.info("-" * 100)
            # DELIVERY类型不需要特殊第一行，表头在第1行，数据从第2行开始
            special_first_row = None
            logger.info(f"处理表头行完成 - 特殊第一行: {special_first_row} (DELIVERY类型不需要特殊第一行)")
            
            # 3. 按列处理数据
            logger.info("-" * 100)
            logger.info("步骤3: 按列处理数据")
            logger.info("-" * 100)
            processed_column_data = self._process_columns(column_data, data_row_count)
            logger.info(f"按列处理完成 - 处理列数: {len(processed_column_data)}")
            
            # 4. 生成结果文件
            logger.info("-" * 100)
            logger.info("步骤4: 生成结果文件")
            logger.info("-" * 100)
            self._generate_result_file(processed_column_data, special_first_row)
            logger.info(f"生成结果文件完成")
            
            # 5. 计算统计信息
            logger.info("-" * 100)
            logger.info("步骤5: 计算统计信息")
            logger.info("-" * 100)
            stats = self._calculate_stats(processed_column_data, column_data)
            logger.info(f"计算统计信息完成 - 统计信息: {stats}")
            
            # 返回结果，包含输出文件路径
            result = {
                'output_file': self.result_file_path,
                'stats': stats
            }
            
            logger.info("=" * 100)
            logger.info(f"文件处理完成 - 输出文件: {self.result_file_path}, 统计信息: {stats}")
            logger.info("=" * 100)
            return result
            
        except Exception as e:
            logger.error(f"文件处理失败: {str(e)}", exc_info=True)
            raise
    
    def _parse_original_file(self):
        """
        解析原始Excel文件
        
        输出:
            - (workbook, sheet, first_row, column_data, data_row_count): 工作簿、工作表对象、第一行数据、按列组织的数据和数据行数
        """
        logger.info(f"解析原始文件：{self.original_file_path}")
        result = read_excel_file(
            self.original_file_path,
            file_type='DELIVERY',
            file_role='SOURCE'
        )
        return result["worksheet"].parent, result["worksheet"], result["first_row"], result["column_data"], result["data_row_count"]
    
    def _process_header_row(self, sheet, first_row: List[Any]) -> List[str]:
        """
        处理表头行（B1、E1、H1等）
        
        输入:
            - sheet: 工作表对象
            - first_row: 第一行数据
            
        输出:
            - 特殊第一行数据
        """
        logger.info("处理表头行")
        
        # 优先使用header_params中的值，如果没有则从first_row中提取
        mawb_no = self.header_params.get('mawb_no', '')
        flight_no = self.header_params.get('flight_no', '')
        arrival_date = self.header_params.get('arrival_date', '')
        
        # 如果header_params中没有值，尝试从first_row中提取
        if not mawb_no and first_row:
            mawb_no = first_row[0] if len(first_row) > 0 else ''
        if not flight_no and first_row:
            flight_no = first_row[1] if len(first_row) > 1 else ''
        if not arrival_date and first_row:
            arrival_date = first_row[2] if len(first_row) > 2 else ''
        
        # 构建header_params
        header_params = {
            'mawb_no': mawb_no,
            'flight_no': flight_no,
            'arrival_date': arrival_date
        }
        
        # 使用process_header_row函数生成特殊第一行
        special_first_row = process_header_row(header_params, total_columns=8)
        
        logger.info(f"处理表头行输入 - header_params: {header_params}")
        logger.info(f"处理表头行输出 - 特殊第一行: {special_first_row}")
        
        return special_first_row
    
    def _process_columns(self, column_data: List[Dict[str, Any]], data_row_count: int) -> List[Dict[str, Any]]:
        """
        按列处理数据
        
        输入:
            - column_data: 按列组织的数据列表
            - data_row_count: 数据行数
            
        输出:
            - 处理后的列数据列表
        """
        logger.info("=" * 100)
        logger.info("开始按列处理数据")
        logger.info("=" * 100)
        logger.info(f"按列处理输入 - 列数: {len(column_data)}, 数据行数: {data_row_count}")
        logger.info(f"按列处理输入 - column_data: {column_data}")
        
        # 获取field_pipelines配置
        field_pipelines = self._get_field_pipelines()
        logger.info(f"按列处理配置 - 字段处理配置数量: {len(field_pipelines)}")
        logger.debug(f"按列处理配置 - field_pipelines: {field_pipelines}")
        
        # 初始化AI服务
        if not self.ai_service:
            from app.core.config import settings
            api_key = getattr(settings, 'DEEPSEEK_API_KEY', '')
            base_url = getattr(settings, 'DEEPSEEK_API_URL', 'https://api.deepseek.com/v1')
            self.ai_service = DeepSeekAIService(api_key, base_url)
            logger.info("AI服务初始化完成")
        
        # 初始化AI规则执行器
        if not self.ai_rule_executor:
            self.ai_rule_executor = AIRuleExecutor(self.ai_service)
            logger.info("AI规则执行器初始化完成")
        
        # 初始化汇率服务
        if not self.exchange_rate_service:
            from app.services.exchange_rate_service import ExchangeRateService
            self.exchange_rate_service = ExchangeRateService(self.db_session)
            logger.info("汇率服务初始化完成")
        
        # 初始化处理后的列数据
        processed_column_data = []
        
        # 构建列数据映射
        # 建立表头名称到列字母的映射，以及列字母到数据的映射
        header_to_col_letter = {}  # 表头 -> 列字母
        col_letter_to_data = {}    # 列字母 -> 数据
        for col in column_data:
            col_source_cols = col.get('source_cols')  # 列字母
            col_header = col.get('head')               # 表头名称
            if col_source_cols:
                col_letter_to_data[col_source_cols] = col.get('data')
                if col_header:
                    header_to_col_letter[col_header] = col_source_cols

        # 构建最终的column_data_map：表头名称 -> 数据，列字母 -> 数据
        column_data_map = {}
        # 通过表头名称映射
        for header, col_letter in header_to_col_letter.items():
            if col_letter in col_letter_to_data:
                column_data_map[header] = col_letter_to_data[col_letter]
        # 通过列字母映射（这样可以通过列字母直接获取数据）
        for col_letter, data in col_letter_to_data.items():
            column_data_map[col_letter] = data
        
        # 构建已处理列数据映射
        processed_column_data_map = {}
        
        # 遍历field_pipelines配置
        for pipeline in field_pipelines:
            target_col = pipeline.get('target_col')
            target_header = pipeline.get('target_header')
            map_op = pipeline.get('map_op')
            source_cols = pipeline.get('source_cols', [])
            # 确保source_cols是列表
            if isinstance(source_cols, str):
                import json
                try:
                    source_cols = json.loads(source_cols)
                except Exception as e:
                    logger.warning(f"解析source_cols JSON失败: {source_cols}, 错误: {e}")
                    source_cols = []
            field_type = pipeline.get('field_type')
            rule_ref = pipeline.get('rule_ref', [])
            depends_on = pipeline.get('depends_on', [])
            # 确保depends_on也是列表
            if isinstance(depends_on, str):
                import json
                try:
                    depends_on = json.loads(depends_on)
                except Exception as e:
                    logger.warning(f"解析depends_on JSON失败: {depends_on}, 错误: {e}")
                    depends_on = []
            order = pipeline.get('order', 0)
            enabled = pipeline.get('enabled', 1)
            
            logger.info("-" * 100)
            logger.info(f"处理列配置 - 列名: {target_col}, map_op: {map_op}, source_cols: {source_cols}, field_type: {field_type}, rule_ref: {rule_ref}, depends_on: {depends_on}")
            
            if target_col == 'D':
                logger.info(f"[DEBUG] D列处理 - map_op={map_op}, source_cols={source_cols}, depends_on={depends_on}")

            
            if not enabled:
                logger.info(f"列已禁用，跳过处理 - 列名: {target_col}")
                continue
            
            # 获取源列数据
            source_column_data = None
            if source_cols:
                source_column_data = column_data_map.get(source_cols[0], []) if source_cols else []
            
            # 检查是否是AI规则
            is_ai_rule = map_op == 'NONE' and field_type == 'AI' and self.ai_rule_executor and len(rule_ref) > 0
            
            if is_ai_rule:
                # AI规则：批量处理
                logger.info(f"AI规则批量处理 - 列名: {target_col}, 数据量: {len(source_column_data)}")
                
                # 构建批量输入数据
                input_data_list = []
                for row_idx in range(len(source_column_data)):
                    row = {}
                    if source_cols:
                        for col in source_cols:
                            row[col] = column_data_map.get(col, [])[row_idx] if col in column_data_map else None
                    
                    # 添加依赖列的值（从已处理的数据中获取）
                    if depends_on:
                        for dep_col in depends_on:
                            if dep_col in processed_column_data_map:
                                dep_data = processed_column_data_map.get(dep_col, [])
                                if row_idx < len(dep_data):
                                    row[dep_col] = dep_data[row_idx]
                                else:
                                    row[dep_col] = None
                    
                    input_data_list.append(row)
                
                # 批量执行AI规则
                rule_ref_key = rule_ref[0]
                rule_params = self._get_rule_params(pipeline, rule_ref_key)
                
                # 添加rule_ref和target_col到rule_params中
                rule_params['rule_ref'] = rule_ref_key
                rule_params['target_col'] = target_col
                
                processed_values = self.ai_rule_executor.execute_batch(rule_ref_key, input_data_list, rule_params)
                
                logger.debug(f"AI批量处理完成 - 列: {target_col}, 结果数量: {len(processed_values)}")
                
                # 添加到已处理列数据映射
                processed_column_data_map[target_col] = processed_values
                
                # 添加到处理后的列数据列表
                processed_column_data.append({
                    'head': target_header,
                    'data': processed_values,
                    'len': len(processed_values)
                })
            else:
                # 非AI规则：逐行处理
                # 如果source_column_data为None，则使用data_row_count
                loop_count = len(source_column_data) if source_column_data else data_row_count
                processed_values = []
                
                for row_idx in range(loop_count):
                    # 构建row字典，包含所有源列和依赖列的值
                    row = {}
                    if source_cols:
                        for col in source_cols:
                            col_data = column_data_map.get(col, [])
                            if row_idx < len(col_data):
                                row[col] = col_data[row_idx]
                                # 添加表头名称作为key（通过列字母查找表头）
                                for header, col_letter in header_to_col_letter.items():
                                    if col_letter == col:
                                        row[header] = col_data[row_idx]
                                        break
                            else:
                                row[col] = None
                                # 添加表头名称作为key
                                for header, col_letter in header_to_col_letter.items():
                                    if col_letter == col:
                                        row[header] = None
                                        break
                    
                    # 添加依赖列的值（从已处理的数据中获取）
                    if depends_on:
                        for dep_col in depends_on:
                            if dep_col in processed_column_data_map:
                                dep_data = processed_column_data_map.get(dep_col, [])
                                if row_idx < len(dep_data):
                                    row[dep_col] = dep_data[row_idx]
                                    # 添加表头名称作为key（通过列字母查找表头）
                                    for header, col_letter in header_to_col_letter.items():
                                        if col_letter == dep_col:
                                            row[header] = dep_data[row_idx]
                                            break
                                else:
                                    row[dep_col] = None
                                    # 添加表头名称作为key
                                    for header, col_letter in header_to_col_letter.items():
                                        if col_letter == dep_col:
                                            row[header] = None
                                            break
                            elif dep_col in column_data_map:
                                # 如果依赖列在原始数据中（尚未处理），从原始数据中获取
                                dep_data = column_data_map.get(dep_col, [])
                                if row_idx < len(dep_data):
                                    row[dep_col] = dep_data[row_idx]
                                    # 添加表头名称作为key（通过列字母查找表头）
                                    for header, col_letter in header_to_col_letter.items():
                                        if col_letter == dep_col:
                                            row[header] = dep_data[row_idx]
                                            break
                                else:
                                    row[dep_col] = None
                                    # 添加表头名称作为key
                                    for header, col_letter in header_to_col_letter.items():
                                        if col_letter == dep_col:
                                            row[header] = None
                                            break
                    
                    # 执行处理逻辑
                    processed_value = self._execute_field_handler(row, map_op, source_cols, field_type, rule_ref, pipeline)
                    processed_values.append(processed_value)
                
                # 添加到已处理列数据映射
                processed_column_data_map[target_col] = processed_values

                # 添加到处理后的列数据列表
                processed_column_data.append({
                    'head': target_header,
                    'data': processed_values,
                    'len': len(processed_values)
                })

            logger.info(f"处理列完成 - 列名: {target_col}, 数据行数: {len(processed_values)}")
            # 特殊日志：如果是D列，打印处理后的数据
            if target_col == 'D':
                logger.info(f"D列（時間帯指定）处理后的数据: {processed_values}")
            logger.info("-" * 100)
        
        logger.info("=" * 100)
        logger.info(f"按列处理完成，处理列数: {len(processed_column_data)}, 已处理列: {set(col['head'] for col in processed_column_data)}")
        logger.info("=" * 100)
        
        # 将所有None值替换为空字符串""
        for col in processed_column_data:
            data = col.get('data', [])
            col['data'] = ['' if v is None else v for v in data]
            logger.debug(f"列 {col.get('target_col')} - 替换None值为空字符串")
        logger.info("✅ 已将所有None值替换为空字符串")
        
        return processed_column_data
    
    def _execute_field_handler(self, row: Dict[str, Any], map_op: str, source_cols: List[str], field_type: str, rule_ref: List[str], pipeline: Dict[str, Any]) -> Any:
        """
        执行字段处理逻辑
        
        输入:
            - row: 当前行数据
            - map_op: 映射操作
            - source_cols: 源列列表
            - field_type: 字段类型
            - rule_ref: 规则引用列表
            - pipeline: 管道配置
            
        输出:
            - 处理后的值
        """
        try:
            # 获取源值
            source_value = None
            if source_cols:
                source_value = row.get(source_cols[0])
            
            # 获取规则参数
            rule_params = {}
            if pipeline:
                rule_params_json = pipeline.get('rule_params_json')
                
                # 如果rule_params_json是字符串，则解析为字典
                if isinstance(rule_params_json, str):
                    import json
                    try:
                        rule_params_json = json.loads(rule_params_json)
                    except json.JSONDecodeError:
                        logger.error(f"解析rule_params_json失败: {rule_params_json}")
                        rule_params_json = {}
                
                if rule_params_json:
                    if map_op == 'CONST':
                        # CONST操作直接使用rule_params_json
                        rule_params = rule_params_json
                    elif map_op == 'DEFAULT':
                        # DEFAULT操作：rule_params_json直接就是默认值
                        rule_params = rule_params_json
                    elif rule_ref and len(rule_ref) > 0:
                        # 其他操作从rule_params_json中获取对应规则的参数
                        rule_params = rule_params_json.get(rule_ref[0], {})
            
            # 根据map_op执行不同的处理逻辑
            if map_op == 'COPY':
                # 检查是否是D列（時間帯指定），需要特殊处理
                target_col = pipeline.get('target_col') if pipeline else 'unknown'
                logger.info(f"COPY操作 - target_col: {target_col}, field_type: {field_type}")
                
                if target_col == 'D':
                    # D列特殊处理：依赖C列（配達指定日）
                    c_value = row.get('配達指定日')  # 获取C列的值
                    logger.info(f"处理D列特殊逻辑 - source_value类型: {type(source_value)}, source_value: {source_value}, c_value类型: {type(c_value)}, c_value: {c_value}")
                    logger.info(f"处理D列特殊逻辑 - row字典内容: {row}")
                    logger.info(f"处理D列特殊逻辑 - row字典keys: {list(row.keys())}")
                    result = calc_time_slot_with_delivery_date(source_value, c_value)
                    logger.info(f"处理D列特殊逻辑 - 结果: {result}")
                    return result
                elif field_type == 'DEFAULT':
                    # DEFAULT类型：如果源值为空，则使用默认值；否则复制源值
                    logger.info(f"COPY+DEFAULT操作 - field_type: {field_type}, rule_params类型: {type(rule_params)}, rule_params值: {rule_params}")
                    default_value = ''
                    if isinstance(rule_params, dict):
                        # 直接从rule_params中提取default_value
                        default_value = rule_params.get('default_value', '')
                        logger.info(f"COPY+DEFAULT操作 - 从dict提取默认值: {default_value}")
                    elif isinstance(rule_params, str):
                        # rule_params可能是字符串，尝试解析
                        import json
                        try:
                            parsed_params = json.loads(rule_params)
                            default_value = parsed_params.get('default_value', '')
                            logger.info(f"COPY+DEFAULT操作 - 从字符串解析默认值: {default_value}")
                        except Exception as e:
                            logger.warning(f"COPY+DEFAULT操作 - 无法解析rule_params字符串: {rule_params}, 错误: {e}")
                    else:
                        logger.info(f"COPY+DEFAULT操作 - rule_params类型: {type(rule_params)}, 值: {rule_params}")
                    
                    return copy_equal_to(source_value, default_value)
                else:
                    return copy_field(source_value)
            elif map_op == 'CONST':
                logger.info(f"处理CONST操作 - target_col: {pipeline.get('target_col') if pipeline else 'unknown'}")
                
                # 从rule_params中提取value
                const_value = ''
                if isinstance(rule_params, dict) and 'policy_const' in rule_params:
                    const_value = rule_params['policy_const'].get('value', '')
                    logger.info(f"CONST操作 - 从dict提取常量值: {const_value}")
                elif isinstance(rule_params, str):
                    # rule_params可能是字符串，尝试解析
                    import json
                    try:
                        parsed_params = json.loads(rule_params)
                        if 'policy_const' in parsed_params:
                            const_value = parsed_params['policy_const'].get('value', '')
                            logger.info(f"CONST操作 - 从字符串解析常量值: {const_value}")
                    except Exception as e:
                        logger.warning(f"CONST操作 - 无法解析rule_params字符串: {rule_params}, 错误: {e}")
                else:
                    logger.info(f"CONST操作 - rule_params类型: {type(rule_params)}, 值: {rule_params}")
                
                # 检查是否是特殊标记，从header_params获取值
                logger.info(f"CONST操作 - 检查特殊标记: const_value='{const_value}', header_params={self.header_params}")
                
                if const_value == '{{unique_code}}':
                    const_value = self.header_params.get('mawb_no', '')
                    logger.info(f"CONST操作 - 使用unique_code作为常量值（原始）: {const_value}")
                    
                    # 格式化unique_code: "160-03270890" -> "160-0327 0890"
                    if const_value and len(const_value) >= 8:
                        old_value = const_value
                        const_value = const_value[:8] + ' ' + const_value[8:]
                        logger.info(f"CONST操作 - 格式化unique_code: '{old_value}' -> '{const_value}'")
                else:
                    logger.info(f"CONST操作 - 使用普通常量值: {const_value}")
                
                result = set_constant(const_value)
                logger.info(f"CONST操作 - 最终返回值: {result}")
                return result
            elif map_op == 'INPUT':
                return generate_sequence(row, rule_params)
            elif map_op == 'DEFAULT':
                # DEFAULT操作：从rule_params中提取default_value
                default_value = ''
                if isinstance(rule_params, dict) and 'policy_default_copy' in rule_params:
                    default_value = rule_params['policy_default_copy'].get('default_value', '')
                    logger.info(f"DEFAULT操作 - 从dict提取默认值: {default_value}")
                elif isinstance(rule_params, str):
                    # rule_params可能是字符串，尝试解析
                    import json
                    try:
                        parsed_params = json.loads(rule_params)
                        if 'policy_default_copy' in parsed_params:
                            default_value = parsed_params['policy_default_copy'].get('default_value', '')
                            logger.info(f"DEFAULT操作 - 从字符串解析默认值: {default_value}")
                    except Exception as e:
                        logger.warning(f"DEFAULT操作 - 无法解析rule_params字符串: {rule_params}, 错误: {e}")
                else:
                    logger.info(f"DEFAULT操作 - rule_params类型: {type(rule_params)}, 值: {rule_params}")
                
                return copy_equal_to(source_value, default_value)
            elif map_op == 'CALC':
                return calc_invoice_price_fx_round(row, rule_params, self.exchange_rate_service)
            else:
                logger.warning(f"未知的map_op: {map_op}")
                return source_value
        except Exception as e:
            logger.error(f"字段处理失败: {str(e)}", exc_info=True)
            return None
    
    def _generate_result_file(self, processed_column_data: List[Dict[str, Any]], special_first_row: List[str]):
        """
        生成结果文件
        
        输入:
            - processed_column_data: 处理后的列数据列表
            - special_first_row: 特殊第一行数据
        """
        logger.info("=" * 100)
        logger.info("生成结果文件")
        logger.info("=" * 100)
        logger.info(f"生成结果文件: {self.result_file_path}")
        logger.info(f"生成结果文件输入 - 列数: {len(processed_column_data)}, 特殊第一行: {special_first_row}")
        
        if not processed_column_data:
            logger.warning("处理数据为空，跳过生成结果文件")
            return
        
        # 从file_definitions中获取OUTPUT定义的columns_json，确保列顺序正确
        output_file_def = None
        logger.debug(f"检查file_definitions - file_definitions: {self.file_definitions}, 类型: {type(self.file_definitions)}")
        if self.file_definitions:
            # 检查大小写不敏感的键
            for key in self.file_definitions:
                logger.debug(f"检查键 - key: {key}, key.upper(): {key.upper()}, 是否等于'OUTPUT': {key.upper() == 'OUTPUT'}")
                if key.upper() == 'OUTPUT':
                    output_file_def = self.file_definitions[key]
                    logger.debug(f"找到output_file_def - output_file_def: {output_file_def}")
                    break
            else:
                logger.warning(f"file_definitions中没有找到OUTPUT键 - file_definitions: {self.file_definitions}")
        else:
            logger.warning(f"file_definitions为空 - file_definitions: {self.file_definitions}")
        
        if output_file_def:
            # 从file_definitions中获取列顺序
            columns_json = output_file_def.get('columns_json', [])
            headers = [col.get('header', '') for col in columns_json]
            logger.info(f"从file_definitions中获取列顺序: {headers}")
        else:
            # 如果没有file_definitions，则从processed_column_data中提取
            headers = [col['head'] for col in processed_column_data]
            logger.info(f"从processed_column_data中提取列顺序: {headers}")
        
        # 扩展special_first_row到与表头相同的列数
        if special_first_row and len(special_first_row) < len(headers):
            # 扩展稀疏列表到完整长度
            extended_special_row = list(special_first_row)
            extended_special_row.extend([''] * (len(headers) - len(extended_special_row)))
            special_first_row = extended_special_row
            logger.info(f"扩展特殊第一行 - 原长度: {len(special_first_row)}, 扩展到: {len(headers)}")
        
        # 构建列数据字典，按照file_definitions中定义的列顺序
        column_data_dict = {}
        if output_file_def:
            columns_json = output_file_def.get('columns_json', [])
            for col_def in columns_json:
                col_header = col_def.get('header', '')
                # 从processed_column_data中查找对应的数据
                for col in processed_column_data:
                    if col['head'] == col_header:
                        column_data_dict[col_header] = col['data']
                        break
        else:
            for col in processed_column_data:
                col_name = col['head']
                col_values = col['data']
                column_data_dict[col_name] = col_values
        
        # 使用按列写入的方式生成结果文件，包含特殊第一行
        write_excel_file_by_columns(
            self.result_file_path,
            headers,
            column_data_dict,
            special_first_row
        )
        
        logger.info("=" * 100)
        logger.info("生成结果文件完成")
        logger.info("=" * 100)
    
    def _calculate_stats(self, processed_column_data: List[Dict[str, Any]], column_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        计算处理结果统计信息
        
        输入:
            - processed_column_data: 处理后的列数据列表
            - column_data: 原始的列数据列表
            
        输出:
            - 统计信息字典
        """
        logger.info("=" * 100)
        logger.info("计算处理结果统计信息")
        logger.info("=" * 100)
        
        stats = {
            "total_rows": 0,
            "fixed_count": 0,
            "filled_count": 0,
            "fx_changed_rows": 0,
            "llm_filled_count": 0
        }
        
        # 计算总行数
        for col in processed_column_data:
            if 'len' in col:
                stats["total_rows"] = max(stats["total_rows"], col['len'])
        
        # 计算修改次数和填充次数
        for processed_col in processed_column_data:
            processed_head = processed_col.get('head', '')
            processed_data = processed_col.get('data', [])
            processed_len = processed_col.get('len', 0)
            
            # 查找原始列数据
            original_col = None
            for col in column_data:
                if col.get('head') == processed_head:
                    original_col = col
                    break
            
            if original_col:
                original_data = original_col.get('data', [])
                
                # 比较原始数据和处理后数据，统计修改次数
                for idx in range(min(processed_len, len(original_data))):
                    if processed_data[idx] != original_data[idx]:
                        stats["fixed_count"] += 1
                    elif processed_data[idx] is not None and original_data[idx] is None:
                        stats["filled_count"] += 1
        
        logger.info(f"计算统计信息完成 - 统计信息: {stats}")
        
        return stats
    
    def _load_file_definitions(self) -> Dict[str, Any]:
        """
        从数据库中读取file_definitions配置
        
        输出：
            - file_definitions配置字典
        """
        from app.models.file_definition import FileDefinition
        
        logger.info("加载file_definitions配置")
        logger.info(f"查询参数 - file_type: {self.file_type}")
        
        # 查询派送文件的文件定义
        file_definitions = self.db_session.query(FileDefinition).filter(
            FileDefinition.file_type == self.file_type
        ).all()
        
        logger.info(f"查询结果 - 找到{len(file_definitions)}个文件定义")
        
        # 构建配置字典
        configs = {}
        for fd in file_definitions:
            logger.info(f"处理文件定义 - file_role: {fd.file_role}, id: {fd.id}")
            configs[fd.file_role] = {
                "id": fd.id,
                "file_type": fd.file_type,
                "file_role": fd.file_role,
                "sheet_name": fd.sheet_name,
                "header_row": fd.header_row,
                "data_start_row": fd.data_start_row,
                "columns_json": fd.columns_json
            }
        
        logger.info(f"构建配置字典完成 - 键: {list(configs.keys())}")
        
        logger.info(f"加载了 {len(configs)} 个文件定义配置")
        return configs
    
    def _get_field_pipelines(self) -> List[Dict[str, Any]]:
        """
        获取字段处理配置
        
        输出:
            - 字段处理配置列表
        """
        logger.info("获取字段处理配置")
        
        if self.db_session:
            from app.models.field_pipeline import FieldPipeline
            pipelines = self.db_session.query(FieldPipeline).filter(
                FieldPipeline.file_type == 'DELIVERY',
                FieldPipeline.enabled == True
            ).order_by(FieldPipeline.order_num).all()
            
            result = []
            for pipeline in pipelines:
                result.append({
                    'target_col': pipeline.target_col,
                    'target_header': pipeline.target_header,
                    'map_op': pipeline.map_op,
                    'source_cols': pipeline.source_cols,
                    'field_type': pipeline.field_type,
                    'rule_ref': pipeline.rule_ref,
                    'rule_params_json': pipeline.rule_params_json,
                    'depends_on': pipeline.depends_on,
                    'order_num': pipeline.order_num
                })
            
            logger.info(f"获取到 {len(result)} 个字段处理配置")
            return result
        
        return []
