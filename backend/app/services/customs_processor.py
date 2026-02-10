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
    normalize_copy_one_decimal
)
from app.services.deepseek_ai_service import DeepSeekAIService
from app.services.ai_rule_executor import AIRuleExecutor
from app.services.exchange_rate_service import ExchangeRateService
import logging

logger = logging.getLogger(__name__)

class CustomsProcessor(BaseProcessor):
    """清关文件处理器，处理清关文件的生成"""
    
    def __init__(self, task_dir: str, db_session=None, file_type=None, header_params: dict = None):
        """
        初始化清关文件处理器
        
        输入:
            - task_dir: 任务文件存储目录
            - db_session: 数据库会话对象
            - file_type: 文件类型（默认: CUSTOMS）
            - header_params: 表头参数（如: mawb_no, flight_no, arrival_date）
        """
        super().__init__(task_dir, db_session, file_type)
        self.header_params = header_params or {}
        self.ai_service = None
        self.ai_rule_executor = None
        self.exchange_rate_service = None
        logger.info(f"清关文件处理器初始化完成，header_params: {header_params}")
    
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
    
    def process(self) -> Dict[str, Any]:
        """
        执行文件处理流程
        
        输出:
            - 处理结果统计信息
        """
        try:
            logger.info("=" * 100)
            logger.info("开始处理清关文件")
            logger.info("=" * 100)
            logger.info(f"处理输入 - 目录: {self.task_dir}, header_params: {self.header_params}")
            
            # 如果file_definitions为None，则从数据库中读取
            if self.file_definitions is None:
                logger.info(f"file_definitions为None，开始加载file_definitions")
                self.file_definitions = self._load_file_definitions()
                logger.info(f"加载file_definitions完成 - file_definitions: {self.file_definitions}")
                logger.info(f"加载file_definitions完成 - 键: {list(self.file_definitions.keys()) if self.file_definitions else 'None'}")
            else:
                logger.info(f"file_definitions不为None - file_definitions: {self.file_definitions}")
            
            # 1. 解析原始文件
            logger.info("-" * 100)
            logger.info("步骤1: 解析原始文件")
            logger.info("-" * 100)
            workbook, sheet, first_row, column_data, data_row_count = self._parse_original_file()
            logger.info(f"解析原始文件完成 - 第一行: {len(first_row)}, 列数: {len(column_data)}, 数据行数: {data_row_count}")
            logger.info(f"解析原始文件完成 - 第一行数据: {first_row}")
            logger.info(f"解析原始文件完成 - 列数据: {column_data}")
            
            # 2. 处理表头行（B1、E1、H1等）
            logger.info("-" * 100)
            logger.info("步骤2: 处理表头行")
            logger.info("-" * 100)
            special_first_row = self._process_header_row(sheet, first_row)
            logger.info(f"处理表头行完成 - 特殊第一行: {special_first_row}")
            
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
            
            logger.info("=" * 100)
            logger.info("文件处理完成，结果: {stats}")
            logger.info("=" * 100)
            return stats
            
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
            file_type='CUSTOMS',
            file_role='SOURCE'
        )
        return result["worksheet"].parent, result["worksheet"], result["first_row"], result["column_data"], result["data_row_count"]
    
    def _build_column_index(self, data: List[List[Any]]) -> Dict[str, int]:
        """
        构建列索引，将列名映射到列索引
        
        输入:
            - data: 数据列表
        输出:
            - 列索引字典 {列名: 列索引}
        """
        logger.info("构建列索引")
        column_index = {}
        
        if data and len(data) > 0:
            header_row = data[0]
            for idx, cell_value in enumerate(header_row):
                if cell_value:
                    # 去除可能的"列"字样，只保留字母部分
                    col_name = str(cell_value).replace("列", "").strip()
                    # 确保列名不为空
                    if col_name:
                        column_index[col_name] = idx
        
        logger.info(f"列索引: {column_index}")
        return column_index
    
    def _process_header_row(self, sheet, first_row: List[Any]) -> List[str]:
        """
        处理表头行（B1、E1、H1），返回特殊第一行数据
        
        输入:
            - sheet: 工作表对象（已废弃，保留参数兼容性）
            - first_row: 第一行数据列表
        
        输出:
            - 特殊第一行数据列表
        """
        logger.info("=" * 100)
        logger.info("开始处理表头行")
        logger.info("=" * 100)
        logger.info(f"处理表头行输入 - first_row: {first_row}")
        logger.info(f"处理表头行输入 - header_params: {self.header_params}")
        
        # 优先使用header_params中的值，如果没有则从first_row中提取
        mawb_no = self.header_params.get('mawb_no', '')
        flight_no = self.header_params.get('flight_no', '')
        arrival_date = self.header_params.get('arrival_date', '')
        
        # 如果header_params中没有值，尝试从first_row中提取
        if not mawb_no and len(first_row) > 1:
            mawb_no = first_row[1]
            # 移除前缀（如果存在）
            if isinstance(mawb_no, str) and mawb_no.startswith('MAWB NO：'):
                mawb_no = mawb_no.replace('MAWB NO：', '').strip()
        
        if not flight_no and len(first_row) > 4:
            flight_no = first_row[4]
            # 移除前缀（如果存在）
            if isinstance(flight_no, str) and flight_no.startswith('FLIGHT NO：'):
                flight_no = flight_no.replace('FLIGHT NO：', '').strip()
        
        if not arrival_date and len(first_row) > 7:
            arrival_date = first_row[7]
            # 移除前缀（如果存在）
            if isinstance(arrival_date, str) and arrival_date.startswith('ARRIVAL DATE'):
                arrival_date = arrival_date.replace('ARRIVAL DATE', '').strip()
        
        logger.info(f"最终使用的值 - mawb_no: {mawb_no}, flight_no: {flight_no}, arrival_date: {arrival_date}")
        
        # 构建header_params
        header_params = {
            'mawb_no': mawb_no,
            'flight_no': flight_no,
            'arrival_date': arrival_date
        }
        
        # 使用process_header_row函数生成特殊第一行
        # 默认8列（A-H），后续会根据实际列数扩展
        special_first_row = process_header_row(header_params, total_columns=8)
        
        logger.info(f"特殊第一行生成完成: {special_first_row}")
        logger.info("=" * 100)
        logger.info("表头行处理完成")
        logger.info("=" * 100)
        
        return special_first_row
    
    def _process_columns(self, column_data: List[Dict[str, Any]], data_row_count: int = None) -> Dict[str, List[Any]]:
        """
        按列处理数据
        
        输入:
            - column_data: 按列组织的数据列表 [{"head": "会员编号", "data": ["DIDA", "DIDA"], "len": 126}, ...]
            - data_row_count: 数据行数（从Excel文件中读取到的数据行数）
        
        输出:
            - 处理后的列数据列表 [{"head": "会员编号", "data": ["DIDA", "DIDA"], "len": 126}, ...]
        """
        logger.info("=" * 100)
        logger.info("开始按列处理数据")
        logger.info("=" * 100)
        logger.info(f"按列处理输入 - 列数: {len(column_data)}, 数据行数: {data_row_count}")
        logger.info(f"按列处理输入 - column_data: {column_data}")
        
        field_pipelines = self._get_field_pipelines()
        rule_definitions = self._get_rule_definitions()
        logger.info(f"按列处理配置 - 字段处理配置数量: {len(field_pipelines)}, 规则定义数量: {len(rule_definitions)}")
        logger.info(f"按列处理配置 - field_pipelines: {field_pipelines}")
        
        ai_service = self._get_ai_service()
        ai_rule_executor = AIRuleExecutor(ai_service)
        exchange_rate_service = self._get_exchange_rate_service()
        
        processed_column_data = []
        processed_columns = set()
        processed_column_data_map = {}  # 存储已处理过的列数据，用于depends_on访问
        
        for pipeline in field_pipelines:
            target_col = pipeline.get('target_col')
            if not target_col:
                logger.warning(f"字段配置缺少target_col，跳过处理 - pipeline: {pipeline}")
                continue
            
            target_header = pipeline.get('target_header')
            map_op = pipeline.get('map_op')
            source_cols = pipeline.get('source_cols', [])
            field_type = pipeline.get('field_type')
            rule_ref = pipeline.get('rule_ref', [])
            depends_on = pipeline.get('depends_on', [])
            
            logger.info(f"处理列配置 - 列名: {target_col}, map_op: {map_op}, source_cols: {source_cols}, field_type: {field_type}, rule_ref: {rule_ref}, depends_on: {depends_on}")
            
            if not self._check_dependencies(depends_on, processed_columns):
                logger.warning(f"字段 {target_col} 的依赖未满足，跳过处理")
                logger.debug(f"字段依赖检查失败 - 字段: {target_col}, 依赖: {depends_on}, 已处理列: {processed_columns}")
                continue
            
            logger.info(f"开始处理列 - 列名: {target_col}, map_op: {map_op}")
            
            processed_values = []
            source_column_data = None
            
            # 从column_data中查找源列数据
            if source_cols:
                logger.debug(f"查找源列 - source_cols[0]: {repr(source_cols[0])}")
                for col in column_data:
                    col_source_cols = col.get('source_cols')
                    logger.debug(f"  检查列 - col_source_cols: {repr(col_source_cols)}, 是否匹配: {col_source_cols == source_cols[0]}")
                    if col_source_cols == source_cols[0]:
                        source_column_data = col.get('data')
                        logger.debug(f"  找到匹配列 - col_source_cols: {repr(col_source_cols)}")
                        break
            
            # 限制处理行数到data_row_count
            if source_column_data and data_row_count:
                source_column_data = source_column_data[:data_row_count]
            
            logger.info(f"源列数据 - 列名: {target_col}, 源列: {source_cols}, 源数据长度: {len(source_column_data) if source_column_data else 0}")
            
            # 处理数据
            if source_column_data:
                # 有源列数据，逐行处理
                # 构建所有列的索引，方便查找
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

                # 构建最终的column_data_map：表头名称 -> 数据
                column_data_map = {}
                for header, col_letter in header_to_col_letter.items():
                    if col_letter in col_letter_to_data:
                        column_data_map[header] = col_letter_to_data[col_letter]
                
                # 检查是否是AI规则，如果是则批量处理
                is_ai_rule = map_op == 'NONE' and field_type == 'AI' and ai_rule_executor and len(rule_ref) > 0
                
                if is_ai_rule:
                    # AI规则：批量处理（直接分批处理，每批20个）
                    logger.info(f"AI规则批量处理 - 列名: {target_col}, 数据量: {len(source_column_data)}")
                    
                    # 构建批量输入数据
                    input_data_list = []
                    for row_idx in range(len(source_column_data)):
                        row = {}
                        if source_cols:
                            for col in source_cols:
                                # 使用col_letter_to_data获取列数据（按列字母映射）
                                row[col] = col_letter_to_data.get(col, [])[row_idx] if col in col_letter_to_data else None
                        
                        # 添加依赖列的值（从已处理的数据中获取）
                        if depends_on:
                            for dep_col in depends_on:
                                if dep_col in processed_column_data_map:
                                    row[dep_col] = processed_column_data_map.get(dep_col, [])[row_idx]
                        
                        input_data_list.append(row)
                    
                    # 批量执行AI规则（直接分批处理，每批20个）
                    rule_ref_key = rule_ref[0]
                    rule_params = self._get_rule_params(pipeline, rule_ref_key)
                    
                    # 将数据分成小批次（每批20个）
                    batch_size = 20
                    all_processed_values = []
                    
                    for batch_start in range(0, len(input_data_list), batch_size):
                        batch_end = min(batch_start + batch_size, len(input_data_list))
                        batch_input = input_data_list[batch_start:batch_end]
                        batch_result = ai_rule_executor.execute_batch(rule_ref_key, batch_input, rule_params)
                        all_processed_values.extend(batch_result)
                        logger.info(f"批次{batch_start//batch_size + 1}: 处理{len(batch_input)}个数据，返回{len(batch_result)}个结果")
                    
                    processed_values = all_processed_values
                    logger.info(f"AI批量处理完成 - 列: {target_col}, 总共返回{len(processed_values)}个结果")
                else:
                    # 非AI规则：逐行处理
                    # 如果source_column_data为None，则使用data_row_count
                    loop_count = len(source_column_data) if source_column_data else data_row_count
                    for row_idx in range(loop_count):
                        # 构建row字典，包含所有源列和依赖列的值
                        row = {}
                        if source_cols:
                            for col in source_cols:
                                # 使用col_letter_to_data获取列数据（按列字母映射）
                                row[col] = col_letter_to_data.get(col, [])[row_idx] if col in col_letter_to_data else None
                        
                        # 添加依赖列的值（从已处理的数据中获取）
                        if depends_on:
                            for dep_col in depends_on:
                                if dep_col in processed_column_data_map:
                                    row[dep_col] = processed_column_data_map.get(dep_col, [])[row_idx]
                        
                        processed_value = self._process_field(
                            map_op, source_cols, field_type, rule_ref, row, None, pipeline, ai_rule_executor
                        )
                        processed_values.append(processed_value)
                        logger.debug(f"生成值 - 列: {target_col}, 行号: {row_idx}, 处理值: {processed_value}")
            elif map_op in ['CONST', 'CALC', 'NONE'] or field_type in ['CONST', 'CALC', 'AI']:
                # 没有源列数据，但需要生成固定值或序号
                # 检查是否是AI规则，如果是则批量处理
                is_ai_rule = map_op == 'NONE' and field_type == 'AI' and ai_rule_executor and len(rule_ref) > 0
                
                if is_ai_rule and data_row_count:
                    # AI规则：批量处理
                    logger.info(f"AI规则批量处理 - 列名: {target_col}, 数据量: {data_row_count}")
                    
                    # 构建批量输入数据
                    input_data_list = []
                    for row_idx in range(data_row_count):
                        row = {}
                        
                        # 添加依赖列的值（从已处理的数据中获取）
                        if depends_on:
                            for dep_col in depends_on:
                                if dep_col in processed_column_data_map:
                                    row[dep_col] = processed_column_data_map.get(dep_col, [])[row_idx]
                        
                        input_data_list.append(row)
                    
                    # 批量执行AI规则
                    rule_ref_key = rule_ref[0]
                    rule_params = self._get_rule_params(pipeline, rule_ref_key)
                    processed_values = ai_rule_executor.execute_batch(rule_ref_key, input_data_list, rule_params)
                    
                    logger.debug(f"AI批量处理完成 - 列: {target_col}, 结果数量: {len(processed_values)}")
                    logger.info(f"AI批量处理返回值 - 列: {target_col}, 返回值: {processed_values}")
                elif data_row_count:
                    # 非AI规则：逐行处理
                    for row_idx in range(1, data_row_count + 1):
                        row = {}
                        row['_row_index'] = row_idx - 1
                        
                        # 添加依赖列的值（从已处理的数据中获取）
                        if depends_on:
                            for dep_col in depends_on:
                                if dep_col in processed_column_data_map:
                                    dep_data = processed_column_data_map.get(dep_col, [])
                                    if dep_data and row_idx - 1 < len(dep_data):
                                        row[dep_col] = dep_data[row_idx - 1]
                        
                        processed_value = self._process_field(
                            map_op, source_cols, field_type, rule_ref, row, None, pipeline, ai_rule_executor
                        )
                        processed_values.append(processed_value)
                        logger.debug(f"生成值 - 列: {target_col}, 行号: {row_idx}, 处理值: {processed_value}")
            else:
                logger.warning(f"源列数据不存在 - 列: {target_col}, 源列: {source_cols}")
            
            processed_column_data.append({
                "target_col": target_col,
                "head": target_header,
                "data": processed_values,
                "len": len(processed_values),
                "order_num": pipeline.get('order_num', 999)
            })
            processed_column_data_map[target_col] = processed_values
            processed_columns.add(target_col)
            logger.info(f"处理列完成 - 列名: {target_col}, 数据行数: {len(processed_values)}")
            logger.info("-" * 100)
        
        # 将所有None值替换为空字符串""
        for col in processed_column_data:
            data = col.get('data', [])
            col['data'] = ['' if v is None else v for v in data]
            logger.debug(f"列 {col.get('target_col')} - 替换None值为空字符串")
        
        logger.info("=" * 100)
        logger.info(f"按列处理完成，处理了 {len(processed_column_data)} 列")
        logger.info(f"按列处理输出 - 处理列数: {len(processed_column_data)}, 已处理列: {processed_columns}")
        logger.info("=" * 100)
        return processed_column_data
    
    def _map_fields(self, data: List[List[Any]], column_index: Dict[str, int]) -> List[Dict[str, Any]]:
        """
        MAP阶段: 字段映射，将原始字段映射到目标字段
        
        输入:
            - data: 数据列表
            - column_index: 列索引字典
        
        输出:
            - 映射后的数据列表
        """
        logger.info("开始MAP阶段: 字段映射")
        logger.debug(f"MAP阶段输入 - 数据行数: {len(data)}, 列索引: {column_index}")
        mapped_data = []
        
        # 跳过第一行（表头行），从第二行开始处理数据
        for row_idx, row in enumerate(data[1:], start=2):
            mapped_row = {}
            for col_name, col_idx in column_index.items():
                if col_idx < len(row):
                    mapped_row[col_name] = row[col_idx]
            mapped_data.append(mapped_row)
        
        logger.info(f"MAP阶段完成，处理了 {len(mapped_data)} 行数据")
        logger.debug(f"MAP阶段输出 - 映射数据行数: {len(mapped_data)}, 第一行示例: {mapped_data[0] if mapped_data else None}")
        return mapped_data
    
    def _process_fields(self, mapped_data: List[Dict[str, Any]], column_index: Dict[str, int]) -> List[Dict[str, Any]]:
        """
        PROCESS阶段: 字段处理，应用规则进行验证、转换和计算
        
        输入:
            - mapped_data: 映射后的数据列表
            - column_index: 列索引字典
        
        输出:
            - 处理后的数据列表
        """
        logger.info("开始PROCESS阶段: 字段处理")
        logger.debug(f"PROCESS阶段输入 - 映射数据行数: {len(mapped_data)}, 列索引: {column_index}")
        
        field_pipelines = self._get_field_pipelines()
        rule_definitions = self._get_rule_definitions()
        logger.debug(f"PROCESS阶段配置 - 字段处理配置数量: {len(field_pipelines)}, 规则定义数量: {len(rule_definitions)}")
        
        ai_service = self._get_ai_service()
        ai_rule_executor = AIRuleExecutor(ai_service)
        exchange_rate_service = self._get_exchange_rate_service()
        
        processed_data = []
        processed_fields = set()
        
        for row_idx, row in enumerate(mapped_data, start=1):
            processed_row = row.copy()
            
            for pipeline in field_pipelines:
                target_col = pipeline.get('target_col')
                if not target_col:
                    logger.warning(f"字段配置缺少target_col，跳过处理 - pipeline: {pipeline}")
                    continue
                
                map_op = pipeline.get('map_op')
                source_cols = pipeline.get('source_cols', [])
                field_type = pipeline.get('field_type')
                rule_ref = pipeline.get('rule_ref', [])
                depends_on = pipeline.get('depends_on', [])
                
                if not self._check_dependencies(depends_on, processed_fields):
                    logger.warning(f"字段 {target_col} 的依赖未满足，跳过处理")
                    logger.debug(f"字段依赖检查失败 - 字段: {target_col}, 依赖: {depends_on}, 已处理字段: {processed_fields}")
                    continue
                
                logger.debug(f"开始处理字段 - 行号: {row_idx}, 字段: {target_col}, map_op: {map_op}")
                
                value = self._process_field(
                    map_op, source_cols, field_type, rule_ref, row, column_index, pipeline, ai_rule_executor
                )
                
                processed_row[target_col] = value
                processed_fields.add(target_col)
                logger.debug(f"处理字段完成 - 行号: {row_idx}, 字段: {target_col}, 值: {value}")
            
            processed_data.append(processed_row)
            logger.debug(f"处理行完成 - 行号: {row_idx}, 已处理字段: {processed_fields}")
        
        logger.info(f"PROCESS阶段完成，处理了 {len(processed_data)} 行数据")
        logger.debug(f"PROCESS阶段输出 - 处理数据行数: {len(processed_data)}, 已处理字段: {processed_fields}")
        return processed_data
    
    def _check_dependencies(self, depends_on: List[str], processed_fields: set) -> bool:
        """
        检查字段依赖关系
        
        输入:
            - depends_on: 依赖字段列表
            - processed_fields: 已处理字段集合
        
        输出:
            - 是否满足依赖关系
        """
        for dep_field in depends_on:
            if dep_field not in processed_fields:
                return False
        return True
    
    def _process_field(self, map_op: str, source_cols: List[str], field_type: str, 
                   rule_ref: List[str], row: Dict[str, Any], column_index: Dict[str, int],
                   pipeline: Dict[str, Any] = None, ai_rule_executor=None) -> Any:
        """
        处理单个字段
        
        输入:
            - map_op: 映射操作类型
            - source_cols: 源列列表
            - field_type: 字段类型
            - rule_ref: 规则引用列表
            - row: 当前行数据
            - column_index: 列索引字典
            - pipeline: 字段处理配置（包含const_value等）
            - ai_rule_executor: AI规则执行器
        
        输出:
            - 处理后的值
        """
        logger.debug(f"开始处理字段 - map_op: {map_op}, source_cols: {source_cols}, field_type: {field_type}, rule_ref: {rule_ref}")
        
        if map_op == 'CONST':
            # 获取rule_params_json的value即可
            const_value = ''
            if pipeline:
                rule_params_json = pipeline.get('rule_params_json', {})
                
                # 如果rule_params_json是字符串，则解析为字典
                if isinstance(rule_params_json, str):
                    import json
                    try:
                        rule_params_json = json.loads(rule_params_json)
                    except json.JSONDecodeError:
                        logger.error(f"解析rule_params_json失败: {rule_params_json}")
                        rule_params_json = {}
                
                if 'policy_const' in rule_params_json:
                    const_value = rule_params_json['policy_const'].get('value', '')
            result = set_constant(const_value)
            logger.debug(f"CONST操作 - rule_params_json: {pipeline.get('rule_params_json') if pipeline else None}, const_value: {const_value}, 结果: {result}")
            return result
        
        elif map_op == 'COPY':
            # 获取source_cols的列的值，然后依据rule_params_json进行检查修正格式化即可
            source_col = source_cols[0] if source_cols else None
            source_value = row.get(source_col) if source_col else None
            
            if field_type == 'COPY':
                # field_type为COPY时：获取source_cols的列的值，然后依据rule_params_json进行检查修正格式化即可
                if len(rule_ref) > 0 and 'policy_copy_optional_text' in rule_ref:
                    # policy_copy_optional_text: 允许null
                    rule_params = self._get_rule_params(pipeline, 'policy_copy_optional_text')
                    allow_null = rule_params.get('allow_null', True)
                    if source_value is None and not allow_null:
                        logger.debug(f"COPY操作 - policy_copy_optional_text - 源值为空且不允许null，返回None")
                        return None
                    result = copy_field(source_value)
                    logger.debug(f"COPY操作 - policy_copy_optional_text - 源列: {source_col}, 源值: {source_value}, 结果: {result}")
                    return result
                else:
                    result = copy_field(source_value)
                    logger.debug(f"COPY操作 - 源列: {source_col}, 源值: {source_value}, 结果: {result}")
                    return result
            
            elif field_type == 'FORMAT':
                # field_type为FORMAT时：获取source_cols的列的值，然后依据rule_params_json进行检查修正格式化即可
                if len(rule_ref) > 0:
                    if 'policy_copy_regex' in rule_ref:
                        # policy_copy_regex: 根据regex进行验证
                        rule_params = self._get_rule_params(pipeline, 'policy_copy_regex')
                        regex = rule_params.get('regex', '')
                        required = rule_params.get('required', False)
                        remove_dash = rule_params.get('remove_dash', False)
                        remove_leading_trailing_spaces = rule_params.get('remove_leading_trailing_spaces', False)
                        remove_middle_spaces = rule_params.get('remove_middle_spaces', False)
                        
                        # 处理源值
                        if source_value is None:
                            if required:
                                logger.debug(f"COPY操作 - policy_copy_regex - 源值为空且必填，返回None")
                                return None
                            result = None
                        else:
                            # 移除横杠
                            if remove_dash and isinstance(source_value, str):
                                source_value = source_value.replace('-', '')
                            
                            # 去除前后空格
                            if remove_leading_trailing_spaces and isinstance(source_value, str):
                                source_value = source_value.strip()
                            
                            # 去除中间空格
                            if remove_middle_spaces and isinstance(source_value, str):
                                source_value = source_value.replace(' ', '')
                            
                            # 验证regex
                            import re
                            if regex and not re.match(regex, str(source_value)):
                                logger.debug(f"COPY操作 - policy_copy_regex - 源值不匹配regex: {regex}")
                                return None
                            
                            result = source_value
                            logger.debug(f"COPY操作 - policy_copy_regex - 源列: {source_col}, 源值: {source_value}, 结果: {result}")
                            return result
                    
                    elif 'policy_copy_optional_decimal' in rule_ref:
                        # policy_copy_optional_decimal: 允许null的小数
                        rule_params = self._get_rule_params(pipeline, 'policy_copy_optional_decimal')
                        regex = rule_params.get('regex', '')
                        allow_null = rule_params.get('allow_null', True)
                        
                        # 处理源值
                        if source_value is None:
                            if not allow_null:
                                logger.debug(f"COPY操作 - policy_copy_optional_decimal - 源值为空且不允许null，返回None")
                                return None
                            # U列中的NONE请直接置空
                            result = None
                            logger.debug(f"COPY操作 - policy_copy_optional_decimal - 源值为NONE，直接置空")
                        else:
                            # 验证regex
                            import re
                            if regex and not re.match(regex, str(source_value)):
                                logger.debug(f"COPY操作 - policy_copy_optional_decimal - 源值不匹配regex: {regex}")
                                return None
                            
                            result = source_value
                            logger.debug(f"COPY操作 - policy_copy_optional_decimal - 源列: {source_col}, 源值: {source_value}, 结果: {result}")
                            return result
                
                result = copy_field(source_value)
                logger.debug(f"COPY操作 - field_type=FORMAT - 源列: {source_col}, 源值: {source_value}, 结果: {result}")
                return result
            
            elif field_type == 'DEFAULT':
                # field_type为DEFAULT时：获取source_cols的列的值，然后依据rule_params_json进行检查修正格式化即可
                if len(rule_ref) > 0 and 'policy_default_copy' in rule_ref:
                    # policy_default_copy: 如果为空则使用default_value
                    rule_params = self._get_rule_params(pipeline, 'policy_default_copy')
                    remove_dash = rule_params.get('remove_dash', False)
                    default_value = rule_params.get('default_value', '')
                    
                    # 处理源值
                    if source_value is None or (isinstance(source_value, str) and source_value.strip() == ''):
                        result = default_value
                        logger.debug(f"COPY操作 - policy_default_copy - 源值为空，使用默认值: {default_value}")
                    else:
                        # 移除横杠
                        if remove_dash and isinstance(source_value, str):
                            source_value = source_value.replace('-', '')
                        result = source_value
                        logger.debug(f"COPY操作 - policy_default_copy - 源列: {source_col}, 源值: {source_value}, 结果: {result}")
                    return result
                
                result = copy_field(source_value)
                logger.debug(f"COPY操作 - field_type=DEFAULT - 源列: {source_col}, 源值: {source_value}, 结果: {result}")
                return result
            
            elif field_type == 'CALC':
                # field_type为CALC时：获取source_cols的列的值，获取depends_on列的值，然后依据rule_params_json中的进行修正处理
                if len(rule_ref) > 0 and 'policy_copy_equal_to' in rule_ref:
                    # policy_copy_equal_to: 如果为空则复制equal_to_target_col的值
                    rule_params = pipeline.get('rule_params_json', {}).get('policy_copy_equal_to', {}) if pipeline else {}
                    equal_to_target_col = rule_params.get('equal_to_target_col', '')
                    
                    # 处理源值
                    if source_value is None or (isinstance(source_value, str) and source_value.strip() == ''):
                        # 复制equal_to_target_col的值
                        target_value = row.get(equal_to_target_col)
                        result = target_value
                        logger.debug(f"COPY操作 - policy_copy_equal_to - 源值为空，复制equal_to_target_col: {equal_to_target_col}, 值: {target_value}")
                    else:
                        result = source_value
                        logger.debug(f"COPY操作 - policy_copy_equal_to - 源列: {source_col}, 源值: {source_value}, 结果: {result}")
                    return result
                
                if len(rule_ref) > 0 and 'policy_copy_one_decimal' in rule_ref:
                    # policy_copy_one_decimal: 保留1位小数
                    rule_params = pipeline.get('rule_params_json', {}).get('policy_copy_one_decimal', {}) if pipeline else {}
                    allow_null = rule_params.get('allow_null', True)
                    result = normalize_copy_one_decimal(source_value, allow_null)
                    logger.debug(f"COPY操作 - policy_copy_one_decimal - 源列: {source_col}, 源值: {source_value}, 结果: {result}")
                    return result
                
                result = copy_field(source_value)
                logger.debug(f"COPY操作 - field_type=CALC - 源列: {source_col}, 源值: {source_value}, 结果: {result}")
                return result
            
            result = copy_field(source_value)
            logger.debug(f"COPY操作 - 源列: {source_col}, 源值: {source_value}, 结果: {result}")
            return result
        
        elif map_op == 'CALC' or field_type == 'CALC':
            # map_op为NONE时，field_type为CALC时，然后依据rule_params_json进行对应的计算
            logger.debug(f"CALC操作 - rule_ref: {rule_ref}")
            
            if 'seq_from_1' in rule_ref or 'policy_seq_from_1' in rule_ref:
                # policy_seq_from_1: 从start开始，每次增加step
                rule_params = pipeline.get('rule_params_json', {}).get('policy_seq_from_1', {}) if pipeline else {}
                start = rule_params.get('start', 1)
                step = rule_params.get('step', 1)
                row_index = row.get('_row_index', 0)
                result = start + row_index * step
                logger.debug(f"policy_seq_from_1计算 - 行索引: {row_index}, start: {start}, step: {step}, 结果: {result}")
                return result
            
            elif 'calc_invoice_price_fx_round' in rule_ref or 'policy_calc_invoice_price_fx_round' in rule_ref:
                # policy_calc_invoice_price_fx_round: 计算发票价格并四舍五入
                rule_params = pipeline.get('rule_params_json', {}).get('policy_calc_invoice_price_fx_round', {}) if pipeline else {}
                regex = rule_params.get('regex', '')
                
                # 获取源值
                original_price = row.get('X', 0)
                currency_code = row.get('V', 'JPY')
                
                # 验证regex
                if regex:
                    import re
                    if not re.match(regex, str(original_price)):
                        logger.debug(f"policy_calc_invoice_price_fx_round - 原价不匹配regex: {regex}")
                        return None
                
                # 计算汇率转换
                exchange_rate_service = self._get_exchange_rate_service()
                result = calc_invoice_price_fx_round(original_price, currency_code, exchange_rate_service)
                logger.debug(f"policy_calc_invoice_price_fx_round计算 - 原价: {original_price}, 货币: {currency_code}, 结果: {result}")
                return result
            
            logger.warning(f"未知的CALC规则 - rule_ref: {rule_ref}")
            return None
        
        elif map_op == 'NONE' and field_type == 'AI' and ai_rule_executor:
            # map_op为NONE时，field_type为AI时，获取source_cols的列的值，获取depends_on列的值，然后依据rule_params_json进行对应的AI输出
            logger.debug(f"AI操作 - rule_ref: {rule_ref}")
            
            if len(rule_ref) > 0:
                rule_ref_key = rule_ref[0]
                rule_params = pipeline.get('rule_params_json', {}).get(rule_ref_key, {}) if pipeline else {}
                
                # 构建input_data，包含source_cols和depends_on的值
                input_data = {}
                if source_cols:
                    for col in source_cols:
                        input_data[col] = row.get(col)
                
                # 获取depends_on的值
                depends_on = pipeline.get('depends_on', [])
                if depends_on:
                    for dep_col in depends_on:
                        input_data[dep_col] = row.get(dep_col)
                
                result = ai_rule_executor.execute(rule_ref_key, input_data, rule_params)
                logger.debug(f"AI操作 - rule_ref: {rule_ref_key}, input_data: {input_data}, 结果: {result}")
                return result
            
            logger.warning(f"AI操作缺少rule_ref - rule_ref: {rule_ref}")
            return None
        
        elif map_op == 'NONE':
            logger.debug(f"NONE操作 - 返回None")
            return None
        
        else:
            logger.warning(f"未知的map_op类型 - map_op: {map_op}")
            return None
    
    def _generate_result_file(self, processed_column_data: List[Dict[str, Any]], special_first_row: List[str] = None):
        """
        生成结果文件
        
        输入:
            - processed_column_data: 处理后的列数据列表 [{"head": "会员编号", "data": ["DIDA", "DIDA"], "len": 126}, ...]
            - special_first_row: 特殊第一行数据（可选）
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
        logger.info(f"检查file_definitions - file_definitions: {self.file_definitions}, 类型: {type(self.file_definitions)}")
        if self.file_definitions:
            # 检查大小写不敏感的键
            for key in self.file_definitions:
                logger.info(f"检查键 - key: {key}, key.upper(): {key.upper()}, 是否等于'OUTPUT': {key.upper() == 'OUTPUT'}")
                if key.upper() == 'OUTPUT':
                    output_file_def = self.file_definitions[key]
                    logger.info(f"找到output_file_def - output_file_def: {output_file_def}")
                    break
            else:
                logger.warning(f"file_definitions中没有找到OUTPUT键 - file_definitions: {self.file_definitions}")
        else:
            logger.warning(f"file_definitions为空 - file_definitions: {self.file_definitions}")
        
        logger.info(f"output_file_def状态 - 是否为None: {output_file_def is None}")
        
        # 从file_definitions的OUTPUT中获取列顺序
        logger.info(f"从file_definitions的OUTPUT中获取列顺序")
        
        if output_file_def:
            # 从file_definitions的OUTPUT中获取列顺序
            columns_json = output_file_def.get('columns_json', [])
            headers = [col.get('header', '') for col in columns_json]
            logger.info(f"从file_definitions的OUTPUT中获取列顺序: {headers}")
            logger.info(f"从file_definitions的OUTPUT中获取列顺序 - columns_json长度: {len(columns_json)}")
        else:
            # 如果没有file_definitions，则从field_pipelines中获取
            logger.info(f"file_definitions为空，从field_pipelines中获取列顺序")
            from app.models.field_pipeline import FieldPipeline
            
            field_pipelines = self.db_session.query(FieldPipeline).filter(
                FieldPipeline.file_type.like('%CUSTOMS%')
            ).order_by(FieldPipeline.order_num).all()
            
            headers = [fp.target_header for fp in field_pipelines]
            logger.info(f"从field_pipelines中获取列顺序: {headers}")
            logger.info(f"从field_pipelines中获取列顺序 - field_pipelines长度: {len(field_pipelines)}")
        
        logger.info(f"最终使用的表头顺序: {headers}, 长度: {len(headers)}")
        
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
            - processed_column_data: 处理后的列数据列表 [{"head": "会员编号", "data": ["DIDA", "DIDA"], "len": 126}, ...]
            - column_data: 原始的列数据列表 [{"head": "会员编号", "data": ["DIDA", "DIDA"], "len": 126}, ...]
        
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
                original_len = original_col.get('len', 0)
                
                for row_idx in range(min(processed_len, original_len)):
                    processed_value = processed_data[row_idx] if row_idx < len(processed_data) else None
                    original_value = original_data[row_idx] if row_idx < len(original_data) else None
                    
                    if processed_value is not None and original_value is not None:
                        if processed_value != original_value:
                            stats["fixed_count"] += 1
                            
                            if "ai_" in processed_head or "translate" in processed_head:
                                stats["llm_filled_count"] += 1
                    
                    if processed_value is not None and processed_value != "":
                        stats["filled_count"] += 1
        
        # 计算修改的行数
        changed_rows = set()
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
                original_len = original_col.get('len', 0)
                
                for row_idx in range(min(processed_len, original_len)):
                    processed_value = processed_data[row_idx] if row_idx < len(processed_data) else None
                    original_value = original_data[row_idx] if row_idx < len(original_data) else None
                    
                    if processed_value is not None and original_value is not None:
                        if processed_value != original_value:
                            changed_rows.add(row_idx)
        
        stats["fx_changed_rows"] = len(changed_rows)
        
        logger.info(f"统计信息: {stats}")
        logger.info("=" * 100)
        return stats
    
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
                FieldPipeline.file_type == 'CUSTOMS',
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
    
    def _get_rule_definitions(self) -> Dict[str, Any]:
        """
        获取规则定义
        
        输出:
            - 规则定义字典
        """
        logger.info("获取规则定义")
        
        if self.db_session:
            from app.models.rule_definition import RuleDefinition
            rules = self.db_session.query(RuleDefinition).all()
            
            result = {}
            for rule in rules:
                result[rule.rule_ref] = {
                    'rule_type': rule.rule_type,
                    'executor_type': rule.executor_type,
                    'schema_json': rule.schema_json
                }
            
            logger.info(f"获取到 {len(result)} 个规则定义")
            return result
        
        return {}
    
    def _get_ai_service(self) -> DeepSeekAIService:
        """
        获取AI服务实例
        
        输出:
            - DeepSeek AI服务实例
        """
        logger.info("获取AI服务实例")
        
        from app.core.config import settings
        
        api_key = getattr(settings, 'DEEPSEEK_API_KEY', '')
        base_url = getattr(settings, 'DEEPSEEK_API_URL', 'https://api.deepseek.com/v1')
        
        return DeepSeekAIService(api_key, base_url)
    
    def _get_exchange_rate_service(self) -> ExchangeRateService:
        """
        获取汇率服务实例
        
        输出:
            - 汇率服务实例
        """
        logger.info("获取汇率服务实例")
        
        from app.core.config import settings
        
        api_key = getattr(settings, 'EXCHANGE_RATE_API_KEY', '')
        base_url = getattr(settings, 'EXCHANGE_RATE_API_URL', 'https://v6.exchangerate-api.com/v6')
        
        return ExchangeRateService(api_key, base_url)
