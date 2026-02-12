import logging
import json
from typing import Dict, Any, List
import pymysql

logger = logging.getLogger(__name__)


class AIRuleExecutor:
    """AI规则执行器"""
    
    def __init__(self, ai_service):
        """
        初始化AI规则执行器
        
        输入：
            - ai_service: DeepSeek AI服务实例
        """
        self.ai_service = ai_service
        self.db_config = {
            'host': '172.18.207.224',
            'port': 3306,
            'user': 'app',
            'password': 'app123456',
            'database': 'demo',
            'charset': 'utf8mb4'
        }
        self.rule_batch_handlers = {
            'policy_ai_goods_en': self._handle_goods_en_batch,
            'policy_ai_material_en': self._handle_material_en_batch,
            'policy_ai_text_ja_clean': self._handle_text_ja_clean_batch,
            'policy_ai_text_dress_clean': self._handle_text_ja_address_clean_batch,
            'policy_translate_from_targetcol_en_upper': self._handle_translate_from_targetcol_en_upper_batch,
            'policy_translate_name_en_upper': self._handle_translate_upper_batch
        }
        logger.info("AI规则执行器初始化完成（触发重新加载）")
    
    def _get_prompt_from_db(self, rule_ref: str, target_col: str, input_count: int = 0) -> str:
        """
        从数据库读取提示词
        
        输入：
            - rule_ref: 规则引用
            - target_col: 目标列名
            - input_count: 输入数据数量
        
        输出：
            - 提示词（由三个部分组成：field_pipelines表中的prompt、rule_definitions表中的system_prompt、代码中的默认提示词）
        """
        try:
            connection = pymysql.connect(**self.db_config)
            cursor = connection.cursor()
            
            prompt_parts = []
            system_prompt = ''
            
            # 第一部分：从rule_definitions表读取system_prompt（优先使用）
            sql = """
            SELECT schema_json
            FROM rule_definitions
            WHERE rule_ref = %s
            """
            
            cursor.execute(sql, (rule_ref,))
            result = cursor.fetchone()
            
            if result and result[0]:
                schema_json = result[0]
                # 如果schema_json是字符串，则解析为字典
                if isinstance(schema_json, str):
                    try:
                        # 第一次解析
                        schema_json = json.loads(schema_json)
                        # 如果解析后仍然是字符串，则进行第二次解析
                        if isinstance(schema_json, str):
                            schema_json = json.loads(schema_json)
                    except json.JSONDecodeError as e:
                        logger.error(f"解析schema_json失败: {e}, schema_json: {schema_json[:500]}")
                        schema_json = {}
                # 确保schema_json是字典
                if not isinstance(schema_json, dict):
                    logger.error(f"schema_json不是字典类型: {type(schema_json)}, schema_json: {str(schema_json)[:500]}")
                    schema_json = {}
                # system_prompt在configurable_params中
                configurable_params = schema_json.get('configurable_params', {})
                system_prompt = configurable_params.get('system_prompt', '')
                if system_prompt:
                    prompt_parts.append(system_prompt)
                    logger.info(f"从rule_definitions表读取system_prompt - rule_ref: {rule_ref}, target_col: {target_col}, system_prompt: {system_prompt[:100]}...")
            
            # 第二部分：从field_pipelines表读取prompt（仅在rule_definitions中没有system_prompt时使用）
            if not system_prompt:
                sql = """
                SELECT rule_params_json
                FROM field_pipelines
                WHERE file_type = 'CUSTOMS' AND rule_ref = %s
                """
                
                cursor.execute(sql, (rule_ref,))
                result = cursor.fetchone()
                
                if result and result[0]:
                    rule_params_json = result[0]
                    # 如果rule_params_json是字符串，则解析为字典
                    if isinstance(rule_params_json, str):
                        try:
                            rule_params_json = json.loads(rule_params_json)
                        except json.JSONDecodeError as e:
                            logger.error(f"解析rule_params_json失败: {e}, rule_params_json: {rule_params_json[:500]}")
                            rule_params_json = {}
                    # 确保rule_params_json是字典
                    if not isinstance(rule_params_json, dict):
                        logger.error(f"rule_params_json不是字典类型: {type(rule_params_json)}, rule_params_json: {str(rule_params_json)[:500]}")
                        rule_params_json = {}
                    prompt = rule_params_json.get(rule_ref, {}).get('prompt', '')
                    if prompt:
                        prompt_parts.append(prompt)
                        logger.info(f"从field_pipelines表读取prompt - rule_ref: {rule_ref}, target_col: {target_col}, prompt: {prompt[:100]}...")
            
            # 第三部分：代码中的默认提示词（如果前两部分都没有）
            if not prompt_parts:
                default_prompt = self._get_default_prompt(rule_ref, target_col, input_count)
                if default_prompt:
                    prompt_parts.append(default_prompt)
                    logger.warning(f"使用默认提示词 - rule_ref: {rule_ref}, target_col: {target_col}")
            
            cursor.close()
            connection.close()
            
            # 组合三个部分的提示词
            if prompt_parts:
                combined_prompt = '\n\n'.join(prompt_parts)
                return combined_prompt
            else:
                return ''
            
        except Exception as e:
            logger.error(f"从数据库读取提示词失败：{str(e)}", exc_info=True)
            return ''
    
    def _get_default_prompt(self, rule_ref: str, target_col: str, input_count: int = 0) -> str:
        """
        获取默认提示词
        
        输入：
            - rule_ref: 规则引用
            - target_col: 目标列名
            - input_count: 输入数据数量
        
        输出：
            - 默认提示词
        """
        default_prompts = {
            'policy_ai_goods_en': f"""你是一个专业的日英翻译专家。请将以下日文品名进行整理并输出。

要求：
1. 先理解品名，如果有重叠，括号说明的部分都先去掉，然后翻译成英文，全面变成大写，需要翻译准确、专业
2. 不要包含特殊字符（/、\等）
5. 只返回翻译结果，不要包含序号（如"1."、"2."等）
6. 只返回翻译结果，不要包含其他文字
7. 输入有{input_count}个元素，输出必须保持{input_count}个元素，不要偷懒输出
9. 必须严格按顺序返回{input_count}个元素，不能多也不能少""",
            'policy_ai_material_en': f"""你是一个专业的日英翻译专家。请将以下日文材质进行整理并输出。

要求：
1. 先理解材质，如果有重叠，括号说明的部分都先去掉，然后翻译成英文，全面变成大写，翻译要准确、专业
2. 转换为标准材质代码（如：COTTON、POLYESTER等）
3. 每行一个翻译结果，按顺序对应
4. 只返回翻译结果，不要包含序号（如"1."、"2."等）
5. 只返回翻译结果，不要包含其他文字
6. 输入有{input_count}个元素，输出必须保持{input_count}个元素，不要偷懒输出
8. 必须严格按顺序返回{input_count}个元素，不能多也不能少""",
            'policy_ai_text_ja_clean': f"""你是一个日文数据处理专家。请清理以下日文收件人名。

要求：
1. 移除敬语和称谓（様、様、先生、様方等）
2. 标准化假名（平假名/片假名）
3. 如果不是标准的日本人名字（例如：公司名，地区名，大厦名），请虚构一个常见的日本名，包含名和姓都需要。
4. 每行一个清理结果，按顺序对应
5. 只返回清理后的名字，不要包含序号（如"1."、"2."等）
6. 只返回清理后的名字，不要包含其他文字
7. 输入有{input_count}个元素，输出必须保持{input_count}个元素，不要偷懒输出
8. 必须严格按顺序返回{input_count}个元素，不能多也不能少""",
            'policy_ai_text_dress_clean': f"""请将以下日文地址格式化，保持日文格式，不要翻译成英文。

要求：

4. 例如："大阪府大阪市中央区1-2-3" 应格式化为 "大阪府大阪市中央区1-2-3"
6. 门牌部分（如1-2-3）保持原格式，-两边都不需要有空格
8. 只返回格式化后的地址，每行一个，按顺序对应，不要包含JSON格式、序号或其他文字
9. 输入有{input_count}个元素，输出必须保持{input_count}个元素，不要偷懒输出
11. 必须严格按顺序返回{input_count}个元素，不能多也不能少""",
            'policy_translate_name_en_upper': f"""你是一个专业的日英翻译专家。请将以下日文翻译成英文。

要求：
1. 翻译要准确、专业
2. 每行一个翻译结果，按顺序对应
3. 只返回翻译结果，不要包含序号（如"1."、"2."等）
4. 只返回翻译结果，不要包含其他文字
5. 输入有{input_count}个元素，输出必须保持{input_count}个元素，不要偷懒输出
7. 必须严格按顺序返回{input_count}个元素，不能多也不能少""",
            'policy_translate_from_targetcol_en_upper': f"""你是一个日英翻译专家。请将以下日文翻译成英文。

要求：
1. 翻译要准确、专业
2. 每行一个翻译结果，按顺序对应
3. 只返回翻译结果，不要包含序号（如"1."、"2."等）
4. 只返回翻译结果，不要包含其他文字
5. 输入有{input_count}个元素，输出必须保持{input_count}个元素，不要偷懒输出
7. 必须严格按顺序返回{input_count}个元素，不能多也不能少""",
        }
        
        return default_prompts.get(rule_ref, '')
    
    def execute_batch(self, rule_ref: str, input_data_list: List[Dict[str, Any]], rule_params: Dict[str, Any]) -> List[Any]:
        """
        批量执行AI规则（一列一次调用）
        
        输入：
            - rule_ref: 规则引用
            - input_data_list: 输入数据列表（多行）
            - rule_params: 规则参数
        
        输出：
            - 处理结果列表
        """
        try:
            batch_handler = self.rule_batch_handlers.get(rule_ref)
            if batch_handler:
                logger.info(f"批量执行AI规则：{rule_ref}，数据量：{len(input_data_list)}")
                return batch_handler(input_data_list, rule_params)
            else:
                logger.warning(f"未知的批量AI规则：{rule_ref}")
                return [None] * len(input_data_list)
        except Exception as e:
            logger.error(f"批量执行AI规则失败：{rule_ref}，错误：{str(e)}", exc_info=True)
            return [None] * len(input_data_list)
    
    def _handle_text_ja_address_clean_batch(self, input_data_list: List[Dict[str, Any]], params: Dict[str, Any]) -> List[str]:
        """
        批量处理收件人地址清理和翻译
        
        输入：
            - input_data_list: 输入数据列表（多行）
            - params: 规则参数
        
        输出：
            - 翻译后的英文地址列表（大写）（List[str]）
        """
        logger.info("=" * 100)
        logger.info("开始批量处理收件人地址清理和翻译")
        logger.info("=" * 100)
        logger.info(f"输入数据列表长度: {len(input_data_list)}")
        
        # 从数据库中获取提示词
        target_col = params.get('target_col', 'Y')
        rule_ref = params.get('rule_ref', 'policy_ai_text_dress_clean')
        
        logger.info(f"target_col: {target_col}")
        logger.info(f"rule_ref: {rule_ref}")
        
        # 获取系统提示词
        system_prompt = self._get_prompt_from_db(rule_ref, target_col)
        
        logger.info(f"从数据库中获取的提示词: {system_prompt[:200]}...")
        
        # 构建批量处理的输入数据为JSON数组格式
        input_data_json = []
        for idx, input_data in enumerate(input_data_list):
            # 自动检测源列：找到第一个非空值作为地址
            address = ''
            for key, value in input_data.items():
                if value and str(value).strip():
                    address = str(value).strip()
                    break
            
            # 如果没有找到地址，使用默认值
            if not address:
                address = input_data.get('AE', '')
            
            # 添加调试日志
            logger.debug(f"输入数据[{idx}]: {input_data}, 提取的地址: {address}")
            
            input_data_json.append({
                "index": str(idx + 1),
                "context": address
            })
        
        # 用户提示词是JSON数组格式
        user_prompt = json.dumps(input_data_json, ensure_ascii=False)
        
        logger.info(f"调用AI - 用户提示词: {user_prompt[:200]}...")
        
        result = self.ai_service.chat(user_prompt, system_prompt)
        
        logger.info(f"调用AI - 用户提示词: {user_prompt[:200]}..., 输出数据: {result}")
        
        # 解析结果
        results = []
        
        # 尝试解析为JSON格式
        try:
            result = result.strip()
            if result.startswith('[') or result.startswith('["'):
                # JSON数组格式
                parsed_results = json.loads(result)
                if isinstance(parsed_results, list):
                    # 提取context字段的值
                    results = []
                    for item in parsed_results:
                        if isinstance(item, dict) and 'context' in item:
                            results.append(str(item['context']).strip()[:60])
                        elif isinstance(item, str):
                            results.append(item.strip()[:60])
                    # 如果提取的结果数量不足，用空值填充
                    while len(results) < len(parsed_results):
                        results.append('')
                else:
                    results = []
            else:
                # 按行分割格式
                lines = result.strip().split('\n')
                for i, line in enumerate(lines):
                    # 跳过空行和分隔线
                    stripped_line = line.strip()
                    if not stripped_line or stripped_line.startswith('===') or stripped_line.startswith('输入数据'):
                        continue
                    # 移除序号前缀（如"1. "）
                    if stripped_line and stripped_line[0].isdigit() and '.' in stripped_line[:10]:
                        stripped_line = stripped_line.split('. ', 1)[1] if '. ' in stripped_line else stripped_line
                    # 只添加非空的结果
                    if stripped_line:
                        results.append(stripped_line)
                    else:
                        # 如果解析后的结果为空，添加空值
                        results.append('')
        except Exception as e:
            logger.warning(f"解析结果失败: {e}")
            results = []
        
        # 确保结果数量匹配
        while len(results) < len(input_data_list):
            logger.warning(f"结果数量不足，当前: {len(results)}, 期望: {len(input_data_list)}, 添加空值")
            results.append('')
        
        # 如果结果数量超过输入数量，截断多余的
        if len(results) > len(input_data_list):
            logger.warning(f"结果数量过多，当前: {len(results)}, 期望: {len(input_data_list)}, 截断多余的")
            results = results[:len(input_data_list)]
        
        logger.info(f"解析后的结果数量: {len(results)}")
        logger.info(f"解析后的结果: {results}")
        
        return results
    
    def _handle_goods_en_batch(self, input_data_list: List[Dict[str, Any]], params: Dict[str, Any]) -> List[str]:
        """
        批量处理品名翻译
        
        输入：
            - input_data_list: [{"H": 日文品名}, ...]
            - params: 规则参数
        
        输出：
            - 英文品名列表（List[str]）
        """
        target_col = params.get('target_col', 'H')
        input_count = len(input_data_list)
        system_prompt = self._get_prompt_from_db('policy_ai_goods_en', target_col, input_count)
        
        if system_prompt:
            logger.info(f"使用数据库中的系统提示词 - rule_ref: policy_ai_goods_en, target_col: {target_col}")
        else:
            logger.warning(f"数据库中没有找到系统提示词，使用默认提示词 - rule_ref: policy_ai_goods_en, target_col: {target_col}")
        
        # 构建批量处理的输入数据为JSON数组格式
        input_data_json = []
        for idx, input_data in enumerate(input_data_list):
            input_data_json.append({
                "index": str(idx + 1),
                "context": input_data.get(target_col, '')
            })
        
        # 用户提示词是JSON数组格式
        user_prompt = json.dumps(input_data_json, ensure_ascii=False)
        
        logger.info(f"调用AI - 用户提示词: {user_prompt[:200]}...")
        
        result = self.ai_service.chat(user_prompt, system_prompt)
        
        logger.info(f"调用AI - 用户提示词: {user_prompt[:200]}..., 输出数据: {result}")
        
        # 解析结果
        results = []
        
        # 尝试解析为JSON格式
        try:
            result = result.strip()
            if result.startswith('[') or result.startswith('["'):
                # JSON数组格式
                parsed_results = json.loads(result)
                if isinstance(parsed_results, list):
                    # 提取context字段的值
                    results = []
                    for item in parsed_results:
                        if isinstance(item, dict) and 'context' in item:
                            results.append(str(item['context']).strip()[:60])
                        elif isinstance(item, str):
                            results.append(item.strip()[:60])
                    # 如果提取的结果数量不足，用空值填充
                    while len(results) < len(parsed_results):
                        results.append('')
                else:
                    results = []
            else:
                # 按行分割格式
                lines = result.strip().split('\n')
                for i, line in enumerate(lines):
                    # 移除序号（如"1. SHAKING TABLEWARE" -> "SHAKING TABLEWARE"）
                    line = line.strip()
                    if line and line[0].isdigit() and '.' in line:
                        # 移除序号部分
                        parts = line.split('.', 1)
                        if len(parts) > 1:
                            line = parts[1].strip()
                    line = line.replace('/', '').replace('\\', '').strip()
                    results.append(line[:60])
        except Exception as e:
            logger.error(f"解析AI返回结果失败：{str(e)}", exc_info=True)
            # 按行分割格式
            lines = result.strip().split('\n')
            for i, line in enumerate(lines):
                # 移除序号（如"1. SHAKING TABLEWARE" -> "SHAKING TABLEWARE"）
                line = line.strip()
                if line and line[0].isdigit() and '.' in line:
                    # 移除序号部分
                    parts = line.split('.', 1)
                    if len(parts) > 1:
                        line = parts[1].strip()
                line = line.replace('/', '').replace('\\', '').strip()
                results.append(line[:60])
        
        # 确保结果数量匹配
        while len(results) < len(input_data_list):
            logger.warning(f"结果数量不足，当前: {len(results)}, 期望: {len(input_data_list)}, 添加空值")
            results.append('')
        
        # 如果结果数量超过输入数量，截断多余的
        if len(results) > len(input_data_list):
            logger.warning(f"结果数量过多，当前: {len(results)}, 期望: {len(input_data_list)}, 截断多余的")
            results = results[:len(input_data_list)]
        
        logger.info(f"解析后的结果数量: {len(results)}")
        logger.info(f"解析后的结果: {results}")
        
        return results


    def _handle_material_en_batch(self, input_data_list: List[Dict[str, Any]], params: Dict[str, Any]) -> List[str]:
        """
        批量处理材质翻译
        
        输入：
            - input_data_list: [{"I": 日文材质}, ...]
            - params: 规则参数
        
        输出：
            - 英文材质列表（List[str]）
        """
        logger.info("=" * 100)
        logger.info("开始批量处理材质翻译")
        logger.info("=" * 100)
        logger.info(f"输入数据列表长度: {len(input_data_list)}")
        
        # 从数据库中获取提示词
        target_col = params.get('target_col', 'I')
        rule_ref = params.get('rule_ref', 'policy_ai_material_en')
        
        logger.info(f"target_col: {target_col}")
        logger.info(f"rule_ref: {rule_ref}")
        logger.info(f"params: {params}")
        
        # 获取系统提示词
        system_prompt = self._get_prompt_from_db(rule_ref, target_col)
        
        logger.info(f"从数据库中获取的提示词: {system_prompt[:200]}...")
        
        # 构建批量处理的输入数据为JSON数组格式
        input_data_json = []
        for idx, input_data in enumerate(input_data_list):
            input_data_json.append({
                "index": str(idx + 1),
                "context": input_data.get('I', '')
            })
        
        # 用户提示词是JSON数组格式
        user_prompt = json.dumps(input_data_json, ensure_ascii=False)
        
        logger.info(f"调用AI - 用户提示词: {user_prompt[:200]}...")
        
        result = self.ai_service.chat(user_prompt, system_prompt)
        
        logger.info(f"调用AI - 用户提示词: {user_prompt[:200]}..., 输出数据: {result}")
        
        # 解析结果
        results = []
        
        # 尝试解析为JSON格式
        try:
            result = result.strip()
            if result.startswith('[') or result.startswith('["'):
                # JSON数组格式
                parsed_results = json.loads(result)
                if isinstance(parsed_results, list):
                    # 提取context字段的值
                    results = []
                    for item in parsed_results:
                        if isinstance(item, dict) and 'context' in item:
                            results.append(str(item['context']).strip())
                        elif isinstance(item, str):
                            results.append(item.strip())
                    # 如果提取的结果数量不足，用空值填充
                    while len(results) < len(parsed_results):
                        results.append('')
                else:
                    results = []
            else:
                # 按行分割格式
                lines = result.strip().split('\n')
                for line in lines:
                    # 移除序号（如"1. ABS" -> "ABS"）
                    line = line.strip()
                    if line and line[0].isdigit() and '.' in line:
                        # 移除序号部分
                        parts = line.split('.', 1)
                        if len(parts) > 1:
                            line = parts[1].strip()
                    results.append(line.strip())
        except Exception as e:
            logger.error(f"解析AI返回结果失败：{str(e)}", exc_info=True)
            # 按行分割格式
            lines = result.strip().split('\n')
            for line in lines:
                # 移除序号（如"1. ABS" -> "ABS"）
                line = line.strip()
                if line and line[0].isdigit() and '.' in line:
                    # 移除序号部分
                    parts = line.split('.', 1)
                    if len(parts) > 1:
                        line = parts[1].strip()
                results.append(line.strip())
        
        # 确保结果数量匹配
        while len(results) < len(input_data_list):
            logger.warning(f"结果数量不足，当前: {len(results)}, 期望: {len(input_data_list)}, 添加空值")
            results.append('')
        
        # 如果结果数量超过输入数量，截断多余的
        if len(results) > len(input_data_list):
            logger.warning(f"结果数量过多，当前: {len(results)}, 期望: {len(input_data_list)}, 截断多余的")
            results = results[:len(input_data_list)]
        
        logger.info(f"解析后的结果数量: {len(results)}")
        logger.info(f"解析后的结果: {results}")
        
        return results


    def _handle_text_ja_clean_batch(self, input_data_list: List[Dict[str, Any]], params: Dict[str, Any]) -> List[str]:
        """
        批量处理收件人名清理
        
        输入：
            - input_data_list: [{"AD": 日文收件人名}, ...]
            - params: 规则参数
        
        输出：
            - 清理后的日文名列表（List[str]）
        """
        logger.info("=" * 100)
        logger.info("开始批量处理收件人名清理")
        logger.info("=" * 100)
        logger.info(f"输入数据列表长度: {len(input_data_list)}")
        
        # 从数据库中获取提示词
        target_col = params.get('target_col', 'X')
        rule_ref = params.get('rule_ref', 'policy_ai_text_ja_clean')
        
        logger.info(f"target_col: {target_col}")
        logger.info(f"rule_ref: {rule_ref}")
        
        # 获取系统提示词
        system_prompt = self._get_prompt_from_db(rule_ref, target_col)
        
        logger.info(f"从数据库中获取的提示词: {system_prompt[:200]}...")
        
        # 构建批量处理的输入数据为JSON数组格式
        input_data_json = []
        for idx, input_data in enumerate(input_data_list):
            input_data_json.append({
                "index": str(idx + 1),
                "context": input_data.get('AD', '')
            })
        
        # 用户提示词是JSON数组格式
        user_prompt = json.dumps(input_data_json, ensure_ascii=False)
        
        logger.info(f"调用AI - 用户提示词: {user_prompt[:200]}...")
        
        result = self.ai_service.chat(user_prompt, system_prompt)
        
        logger.info(f"调用AI - 用户提示词: {user_prompt[:200]}..., 输出数据: {result}")
        
        # 解析结果
        results = []
        
        # 尝试解析为JSON格式
        try:
            result = result.strip()
            if result.startswith('[') or result.startswith('["'):
                # JSON数组格式
                parsed_results = json.loads(result)
                if isinstance(parsed_results, list):
                    # 提取context字段的值
                    results = []
                    for item in parsed_results:
                        if isinstance(item, dict) and 'context' in item:
                            results.append(str(item['context']).strip()[:40])
                        elif isinstance(item, str):
                            results.append(item.strip()[:40])
                    # 如果提取的结果数量不足，用空值填充
                    while len(results) < len(parsed_results):
                        results.append('')
                else:
                    results = []
            else:
                # 按行分割格式
                lines = result.strip().split('\n')
                for line in lines:
                    # 移除序号（如"1. XXX" -> "XXX"）
                    line = line.strip()
                    if line and line[0].isdigit() and '.' in line:
                        # 移除序号部分
                        parts = line.split('.', 1)
                        if len(parts) > 1:
                            line = parts[1].strip()
                    results.append(line.strip()[:40])
        except Exception as e:
            logger.error(f"解析AI返回结果失败：{str(e)}", exc_info=True)
            # 按行分割格式
            lines = result.strip().split('\n')
            for line in lines:
                # 移除序号（如"1. XXX" -> "XXX"）
                line = line.strip()
                if line and line[0].isdigit() and '.' in line:
                    # 移除序号部分
                    parts = line.split('.', 1)
                    if len(parts) > 1:
                        line = parts[1].strip()
                results.append(line.strip()[:40])
        
        # 确保结果数量匹配
        while len(results) < len(input_data_list):
            logger.warning(f"结果数量不足，当前: {len(results)}, 期望: {len(input_data_list)}, 添加空值")
            results.append('')
        
        # 如果结果数量超过输入数量，截断多余的
        if len(results) > len(input_data_list):
            logger.warning(f"结果数量过多，当前: {len(results)}, 期望: {len(input_data_list)}, 截断多余的")
            results = results[:len(input_data_list)]
        
        logger.info(f"解析后的结果数量: {len(results)}")
        logger.info(f"解析后的结果: {results}")
        
        return results


    def _handle_translate_upper_batch(self, input_data_list: List[Dict[str, Any]], params: Dict[str, Any]) -> List[str]:
        """
        批量处理翻译并转大写

        输入：
            - input_data_list: [{"target_col": 目标列的值}, ...] 或 [{depends_on列: depends_on列的值}, ...]
            - params: 规则参数

        输出：
            - 英文翻译列表（大写）（List[str]）
        """
        logger.info("=" * 100)
        logger.info("开始批量处理翻译并转大写")
        logger.info("=" * 100)
        logger.info(f"输入数据列表长度: {len(input_data_list)}")
        
        # 从数据库中获取提示词
        target_col = params.get('target_col', 'J')
        rule_ref = params.get('rule_ref', 'policy_translate_name_en_upper')
        
        logger.info(f"target_col: {target_col}")
        logger.info(f"rule_ref: {rule_ref}")
        
        # 获取系统提示词
        system_prompt = self._get_prompt_from_db(rule_ref, target_col)
        
        logger.info(f"从数据库中获取的提示词: {system_prompt[:200]}...")
        
        # 内部再分批处理（每批50个），避免单次AI调用数据量过大
        internal_batch_size = 50
        all_results = []
        
        for batch_start in range(0, len(input_data_list), internal_batch_size):
            batch_end = min(batch_start + internal_batch_size, len(input_data_list))
            batch_input = input_data_list[batch_start:batch_end]
            
            logger.info(f"内部批次处理 - 批次: {batch_start//internal_batch_size + 1}, 处理: {len(batch_input)}个数据")
            
            # 构建批量处理的输入数据为JSON数组格式
            input_data_json = []
            for idx, input_data in enumerate(batch_input):
                # 获取输入值，优先使用depends_on列的值
                value = ''
                
                # 查找可能的依赖列名（X, Y等）
                for key in ['X', 'Y', 'target_col']:
                    if key in input_data and input_data[key]:
                        value = input_data[key]
                        break
                
                # 如果没有找到依赖列的值，则使用第一个非None的值
                if not value:
                    for key, val in input_data.items():
                        if val is not None and val != '':
                            value = val
                            break
                
                input_data_json.append({
                    "index": str(batch_start + idx + 1),
                    "context": value
                })
            
            # 用户提示词是JSON数组格式
            user_prompt = json.dumps(input_data_json, ensure_ascii=False)
            
            logger.info(f"调用AI - 用户提示词: {user_prompt[:200]}...")
            
            result = self.ai_service.chat(user_prompt, system_prompt)
            
            logger.info(f"调用AI - 用户提示词: {user_prompt[:200]}..., 输出数据: {result}")
            
            # 解析结果
            batch_results = []
            
            # 尝试解析为JSON格式
            try:
                result = result.strip()
                if result.startswith('[') or result.startswith('["'):
                    # JSON数组格式
                    parsed_results = json.loads(result)
                    if isinstance(parsed_results, list):
                        # 提取context字段的值
                        for item in parsed_results:
                            if isinstance(item, dict) and 'context' in item:
                                batch_results.append(str(item['context']).strip().upper())
                            elif isinstance(item, str):
                                batch_results.append(item.strip().upper())
                        # 如果提取的结果数量不足，用空值填充
                        while len(batch_results) < len(parsed_results):
                            batch_results.append('')
                    else:
                        batch_results = []
                else:
                    # 按行分割格式
                    lines = result.strip().split('\n')
                    for line in lines:
                        # 移除序号（如"1. XXX" -> "XXX"）
                        line = line.strip()
                        if line and line[0].isdigit() and '.' in line:
                            # 移除序号部分
                            parts = line.split('.', 1)
                            if len(parts) > 1:
                                line = parts[1].strip()
                        batch_results.append(line.strip().upper())
            except Exception as e:
                logger.error(f"解析AI返回结果失败：{str(e)}", exc_info=True)
                # 按行分割格式
                lines = result.strip().split('\n')
                for line in lines:
                    # 移除序号（如"1. XXX" -> "XXX"）
                    line = line.strip()
                    if line and line[0].isdigit() and '.' in line:
                        # 移除序号部分
                        parts = line.split('.', 1)
                        if len(parts) > 1:
                            line = parts[1].strip()
                    batch_results.append(line.strip().upper())
            
            # 确保批次结果数量匹配
            while len(batch_results) < len(batch_input):
                batch_results.append('')
            
            # 如果批次结果数量超过输入数量，截断多余的
            if len(batch_results) > len(batch_input):
                batch_results = batch_results[:len(batch_input)]
            
            all_results.extend(batch_results)
            logger.info(f"内部批次处理完成 - 批次: {batch_start//internal_batch_size + 1}, 返回: {len(batch_results)}个结果")
        
        # 确保总结果数量匹配
        while len(all_results) < len(input_data_list):
            all_results.append('')
        
        # 如果总结果数量超过输入数量，截断多余的
        if len(all_results) > len(input_data_list):
            all_results = all_results[:len(input_data_list)]
        
        logger.info(f"解析后的结果数量: {len(all_results)}")
        logger.info(f"解析后的结果: {all_results}")
        
        return all_results
    
    def _handle_translate_from_targetcol_en_upper_batch(self, input_data_list: List[Dict[str, Any]], params: Dict[str, Any]) -> List[str]:
        """
        批量处理从目标列翻译并转大写（用于K列：輸入者住所）

        输入：
            - input_data_list: [{"N": 日文地址}, ...]
            - params: 规则参数

        输出：
            - 英文翻译列表（大写）（List[str]）
        """
        logger.info("=" * 100)
        logger.info("开始批量处理从目标列翻译并转大写")
        logger.info("=" * 100)
        logger.info(f"输入数据列表长度: {len(input_data_list)}")
        
        # 从数据库中获取提示词
        target_col = params.get('target_col', 'K')
        rule_ref = params.get('rule_ref', 'policy_translate_from_targetcol_en_upper')
        
        logger.info(f"target_col: {target_col}")
        logger.info(f"rule_ref: {rule_ref}")
        
        # 获取系统提示词
        system_prompt = self._get_prompt_from_db(rule_ref, target_col)
        
        logger.info(f"从数据库中获取的提示词: {system_prompt[:200]}...")
        
        # 内部再分批处理（每批50个），避免单次AI调用数据量过大
        internal_batch_size = 50
        all_results = []
        
        for batch_start in range(0, len(input_data_list), internal_batch_size):
            batch_end = min(batch_start + internal_batch_size, len(input_data_list))
            batch_input = input_data_list[batch_start:batch_end]
            
            logger.info(f"内部批次处理 - 批次: {batch_start//internal_batch_size + 1}, 处理: {len(batch_input)}个数据")
            
            # 构建批量处理的输入数据为JSON数组格式
            input_data_json = []
            for idx, input_data in enumerate(batch_input):
                # 获取输入值，优先使用depends_on列的值
                value = ''
                
                # 查找可能的依赖列名（X, Y等）
                for key in ['X', 'Y', 'target_col']:
                    if key in input_data and input_data[key]:
                        value = input_data[key]
                        break
                
                # 如果没有找到依赖列的值，则使用第一个非None的值
                if not value:
                    for key, val in input_data.items():
                        if val is not None and val != '':
                            value = val
                            break
                
                input_data_json.append({
                    "index": str(batch_start + idx + 1),
                    "context": value
                })
            
            # 用户提示词是JSON数组格式
            user_prompt = json.dumps(input_data_json, ensure_ascii=False)
            
            logger.info(f"调用AI - 用户提示词: {user_prompt[:200]}...")
            
            result = self.ai_service.chat(user_prompt, system_prompt)
            
            logger.info(f"调用AI - 用户提示词: {user_prompt[:200]}..., 输出数据: {result}")
            
            # 解析结果
            batch_results = []
            
            # 尝试解析为JSON格式
            try:
                result = result.strip()
                if result.startswith('[') or result.startswith('["'):
                    # JSON数组格式
                    parsed_results = json.loads(result)
                    if isinstance(parsed_results, list):
                        # 提取context字段的值
                        for item in parsed_results:
                            if isinstance(item, dict) and 'context' in item:
                                batch_results.append(str(item['context']).strip().upper())
                            elif isinstance(item, str):
                                batch_results.append(item.strip().upper())
                        # 如果提取的结果数量不足，用空值填充
                        while len(batch_results) < len(parsed_results):
                            batch_results.append('')
                    else:
                        batch_results = []
                else:
                    # 按行分割格式
                    lines = result.strip().split('\n')
                    for line in lines:
                        # 移除序号（如"1. XXX" -> "XXX"）
                        line = line.strip()
                        if line and line[0].isdigit() and '.' in line:
                            # 移除序号部分
                            parts = line.split('.', 1)
                            if len(parts) > 1:
                                line = parts[1].strip()
                        batch_results.append(line.strip().upper())
            except Exception as e:
                logger.error(f"解析AI返回结果失败：{str(e)}", exc_info=True)
                # 按行分割格式
                lines = result.strip().split('\n')
                for line in lines:
                    # 移除序号（如"1. XXX" -> "XXX"）
                    line = line.strip()
                    if line and line[0].isdigit() and '.' in line:
                        # 移除序号部分
                        parts = line.split('.', 1)
                        if len(parts) > 1:
                            line = parts[1].strip()
                    batch_results.append(line.strip().upper())
            
            # 确保批次结果数量匹配
            while len(batch_results) < len(batch_input):
                logger.warning(f"结果数量不足，当前: {len(batch_results)}, 期望: {len(batch_input)}, 添加空值")
                batch_results.append('')
            
            # 如果批次结果数量超过输入数量，截断多余的
            if len(batch_results) > len(batch_input):
                logger.warning(f"结果数量过多，当前: {len(batch_results)}, 期望: {len(batch_input)}, 截断多余的")
                batch_results = batch_results[:len(batch_input)]
            
            all_results.extend(batch_results)
            logger.info(f"内部批次处理完成 - 批次: {batch_start//internal_batch_size + 1}, 返回: {len(batch_results)}个结果")
        
        # 确保总结果数量匹配
        while len(all_results) < len(input_data_list):
            all_results.append('')
        
        # 如果总结果数量超过输入数量，截断多余的
        if len(all_results) > len(input_data_list):
            all_results = all_results[:len(input_data_list)]
        
        logger.info(f"解析后的结果数量: {len(all_results)}")
        logger.info(f"解析后的结果: {all_results}")
        
        return all_results


