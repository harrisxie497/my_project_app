import logging
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
        self.rule_handlers = {
            'policy_ai_decimal_fix': self._handle_decimal_fix,
            'policy_ai_goods_en': self._handle_goods_en,
            'policy_ai_material_en': self._handle_material_en,
            'policy_ai_text_ja_clean': self._handle_text_ja_clean,
            'policy_ai_text_dress_clean': self._handle_text_ja_address_clean,
            'policy_translate_from_targetcol_en_upper': self._handle_translate_upper,
            'policy_ai_goods_en_clean': self._handle_goods_en_clean
        }
        self.rule_batch_handlers = {
            'policy_ai_decimal_fix': self._handle_decimal_fix_batch,
            'policy_ai_goods_en': self._handle_goods_en_batch,
            'policy_ai_material_en': self._handle_material_en_batch,
            'policy_ai_text_ja_clean': self._handle_text_ja_clean_batch,
            'policy_ai_text_dress_clean': self._handle_text_ja_address_clean_batch,
            'policy_translate_from_targetcol_en_upper': self._handle_translate_upper_batch,
            'policy_ai_goods_en_clean': self._handle_goods_en_clean_batch
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
                    import json
                    schema_json = json.loads(schema_json)
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
                WHERE file_type = 'CUSTOMS' AND target_col = %s
                """
                
                cursor.execute(sql, (target_col,))
                result = cursor.fetchone()
                
                if result and result[0]:
                    rule_params_json = result[0]
                    # 如果rule_params_json是字符串，则解析为字典
                    if isinstance(rule_params_json, str):
                        import json
                        rule_params_json = json.loads(rule_params_json)
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
            'policy_ai_goods_en': f"""你是一个专业的日英翻译专家。请将以下日文品名翻译成英文。

要求：
1. 翻译要准确、专业
2. 不要包含特殊字符（/、\等）
3. 长度不超过60个字符
4. 每行一个翻译结果，按顺序对应
5. 只返回翻译结果，不要包含序号（如"1."、"2."等）
6. 只返回翻译结果，不要包含其他文字
7. 输入有{input_count}个元素，输出必须保持{input_count}个元素，不要偷懒输出
8. 如果某个元素无法翻译，请返回空字符串，不要跳过该元素
9. 必须严格按顺序返回{input_count}个元素，不能多也不能少""",
            'policy_ai_material_en': f"""你是一个专业的日英翻译专家。请将以下日文材质翻译成英文。

要求：
1. 翻译要准确、专业
2. 转换为标准材质代码（如：COTTON、POLYESTER等）
3. 每行一个翻译结果，按顺序对应
4. 只返回翻译结果，不要包含序号（如"1."、"2."等）
5. 只返回翻译结果，不要包含其他文字
6. 输入有{input_count}个元素，输出必须保持{input_count}个元素，不要偷懒输出
7. 如果某个元素无法翻译，请返回空字符串，不要跳过该元素
8. 必须严格按顺序返回{input_count}个元素，不能多也不能少""",
            'policy_ai_text_ja_clean': f"""你是一个日文数据处理专家。请清理以下日文收件人名。

要求：
1. 移除敬语和称谓（様、様、先生、様方等）
2. 标准化假名（平假名/片假名）
3. 长度不超过40个字符
4. 每行一个清理结果，按顺序对应
5. 只返回清理后的名字，不要包含序号（如"1."、"2."等）
6. 只返回清理后的名字，不要包含其他文字
7. 输入有{input_count}个元素，输出必须保持{input_count}个元素，不要偷懒输出
8. 如果某个元素无法清理，请返回空字符串，不要跳过该元素
9. 必须严格按顺序返回{input_count}个元素，不能多也不能少""",
            'policy_ai_text_dress_clean': f"""请将以下日文地址格式化，保持日文格式，不要翻译成英文。

要求：
1. 地址层级完整：都道府县 → 市/区 → 町/地区 → 丁目/番地
2. 例如："愛知県名古屋市中区1-2-3" 应格式化为 "愛知県名古屋市中区1-2-3"
3. 例如："東京都渋谷区渋谷1-2-3" 应格式化为 "東京都渋谷区渋谷1-2-3"
4. 例如："大阪府大阪市中央区1-2-3" 应格式化为 "大阪府大阪市中央区1-2-3"
5. 中间不需要加标点符号，只加入空格分隔各层级
6. 门牌部分（如1-2-3）保持原格式，-两边都不需要有空格
7. 保持日文格式，不要翻译成英文（罗马字）
8. 只返回格式化后的地址，每行一个，按顺序对应，不要包含JSON格式、序号或其他文字
9. 输入有{input_count}个元素，输出必须保持{input_count}个元素，不要偷懒输出
10. 如果某个元素无法格式化，请返回空字符串，不要跳过该元素
11. 必须严格按顺序返回{input_count}个元素，不能多也不能少""",
            'policy_translate_from_targetcol_en_upper': f"""你是一个专业的日英翻译专家。请将以下日文翻译成英文。

要求：
1. 翻译要准确、专业
2. 每行一个翻译结果，按顺序对应
3. 只返回翻译结果，不要包含序号（如"1."、"2."等）
4. 只返回翻译结果，不要包含其他文字
5. 输入有{input_count}个元素，输出必须保持{input_count}个元素，不要偷懒输出
6. 如果某个元素无法翻译，请返回空字符串，不要跳过该元素
7. 必须严格按顺序返回{input_count}个元素，不能多也不能少""",
            'policy_ai_goods_en_clean': f"""你是一个英文数据清洗专家。请清理以下英文品名。

要求：
1. 输入的数组顺序保持不变
2. 删除括号内冗余内容（如"AIRPLANE TOY (L码)"→"AIRPLANE TOY"）
3. 英文名称统一大写（"cotton t-shirt"→"COTTON T-SHIRT"）
4. 每行一个清理结果，按顺序对应
5. 只返回清理结果，不要包含其他文字
6. 输入有{input_count}个元素，输出必须保持{input_count}个元素，不要偷懒输出
7. 如果某个元素无法清理，请返回空字符串，不要跳过该元素
8. 必须严格按顺序返回{input_count}个元素，不能多也不能少"""
        }
        
        return default_prompts.get(rule_ref, '')
    
    def execute(self, rule_ref: str, input_data: Dict[str, Any], rule_params: Dict[str, Any]) -> Any:
        """
        执行AI规则（单行）
        
        输入：
            - rule_ref: 规则引用
            - input_data: 输入数据
            - rule_params: 规则参数
        
        输出：
            - 处理结果
        """
        try:
            handler = self.rule_handlers.get(rule_ref)
            if handler:
                logger.info(f"执行AI规则：{rule_ref}")
                return handler(input_data, rule_params)
            else:
                logger.warning(f"未知的AI规则：{rule_ref}")
                return None
        except Exception as e:
            logger.error(f"执行AI规则失败：{rule_ref}，错误：{str(e)}", exc_info=True)
            return None
    
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
    
    def _handle_decimal_fix(self, input_data: Dict[str, Any], params: Dict[str, Any]) -> float:
        """
        处理重量小数修复
        
        输入：
            - input_data: {"F": 原始重量, "H": 品名, "I": 材质}
            - params: 规则参数
        
        输出：
            - 修复后的重量值（float）
        """
        prompt = f"""你是一个物流数据处理专家。请分析以下货物信息，修复重量数据的小数点问题。
货物重量：{input_data.get('F', '')}
品名：{input_data.get('H', '')}
材质：{input_data.get('I', '')}

请只返回修复后的重量数值，不要包含单位或其他文字。"""
        
        result = self.ai_service.chat(prompt)
        return float(result.strip())
    
    def _handle_goods_en(self, input_data: Dict[str, Any], params: Dict[str, Any]) -> str:
        """
        处理品名翻译
        
        输入：
            - input_data: {"H": 日文品名}
            - params: 规则参数
        
        输出：
            - 英文品名（str）
        """
        prompt = f"""你是一个专业的日英翻译专家。请将以下日文品名翻译成英文。
日文品名：{input_data.get('H', '')}

要求：
1. 翻译要准确、专业
2. 不要包含特殊字符（/、\等）
3. 长度不超过60个字符
4. 只返回翻译结果，不要包含其他文字"""
        
        result = self.ai_service.chat(prompt)
        result = result.replace('/', '').replace('\\', '')
        return result[:60]
    
    def _handle_material_en(self, input_data: Dict[str, Any], params: Dict[str, Any]) -> str:
        """
        处理材质翻译
        
        输入：
            - input_data: {"I": 日文材质}
            - params: 规则参数
        
        输出：
            - 英文材质（str）
        """
        prompt = f"""你是一个专业的日英翻译专家。请将以下日文材质翻译成英文。
日文材质：{input_data.get('I', '')}

要求：
1. 翻译要准确、专业
2. 转换为标准材质代码（如：COTTON、POLYESTER等）
3. 只返回翻译结果，不要包含其他文字"""
        
        result = self.ai_service.chat(prompt)
        return result.strip()
    
    def _handle_text_ja_clean(self, input_data: Dict[str, Any], params: Dict[str, Any]) -> str:
        """
        处理收件人名清理
        
        输入：
            - input_data: {"AD": 日文收件人名}
            - params: 规则参数
        
        输出：
            - 清理后的日文名（str）
        """
        prompt = f"""你是一个日文数据处理专家。请清理以下日文收件人名。
日文收件人名：{input_data.get('AD', '')}

要求：
1. 移除敬语和称谓（様、様、先生、様方等）
2. 标准化假名（平假名/片假名）
3. 长度不超过40个字符
4. 只返回清理后的名字，不要包含其他文字"""
        
        result = self.ai_service.chat(prompt)
        return result[:40]
    
    def _handle_translate_upper(self, input_data: Dict[str, Any], params: Dict[str, Any]) -> str:
        """
        处理翻译并转大写
        
        输入：
            - input_data: {"target_col": 目标列的值}
            - params: 规则参数
        
        输出：
            - 英文翻译（大写）（str）
        """
        target_value = input_data.get('target_col', '')
        prompt = f"""你是一个专业的日英翻译专家。请将以下日文翻译成英文。
日文内容：{target_value}

要求：
1. 翻译要准确、专业
2. 只返回翻译结果，不要包含其他文字"""
        
        result = self.ai_service.chat(prompt)
        return result[:40]
    
    def _handle_text_ja_address_clean(self, input_data: Dict[str, Any], params: Dict[str, Any]) -> str:
        """
        处理收件人地址清理和翻译
        
        输入：
            - input_data: 输入数据字典（包含源列数据，如 AE=收件人地址）
            - params: 规则参数
        
        输出：
            - 翻译后的英文地址（大写）（str）
        """
        address = input_data.get('AE', '')
        
        if not address:
            return ''
        
        system_prompt = params.get('system_prompt', None)
        prompt = f"""请将以下日文地址翻译成英文（罗马字）。
日文地址：{address}

要求：
1. 地址层级完整：都道府县 → 市/区 → 町/地区 → 丁目/番地
2. 例如："愛知県名古屋市中区1-2-3" 应翻译为 "AICHI KEN NAGOYA SHI NAKA KU 1-2-3"
3. 例如："東京 都渋谷区渋谷1-2-3" 应翻译为 "TOKYO TO SHIBUYA KU 1-2-3"
4. 例如："大阪府大阪市中央区1-2-3" 应翻译为 "OSAKA FU OSAKA SHI CHUO KU 1-2-3"
5. 中间不需要加标点符号，只加入空格分隔各层级
6. 门牌部分（如1-2-3）保持原格式，-两边都不需要有空格
7. 翻译结果需全部大写（全罗马大写）
8. 只返回翻译后的地址，不要包含其他文字"""
        
        result = self.ai_service.chat(prompt, system_prompt)
        return result.upper()
    
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
        
        # 获取组合后的提示词
        prompt = self._get_prompt_from_db(rule_ref, target_col)
        
        logger.info(f"从数据库中获取的提示词: {prompt[:200]}...")
        
        # 构建批量处理的输入数据
        items_text = []
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
            
            items_text.append(f"{idx+1}. {address}")
        
        # 替换提示词中的{输入数据}占位符
        input_data_str = '\n'.join(items_text)
        prompt = prompt.replace('{输入数据}', input_data_str)
        prompt = prompt.replace('{input_count}', str(len(input_data_list)))
        
        logger.info("=" * 100)
        logger.info("调用AI的输入数据:")
        logger.info("=" * 100)
        logger.info(f"{input_data_str}")
        logger.info("=" * 100)
        logger.info(f"调用AI的提示词:")
        logger.info("=" * 100)
        logger.info(f"{prompt}")
        logger.info("=" * 100)
        
        result = self.ai_service.chat(prompt)
        
        logger.info("=" * 100)
        logger.info("AI返回的输出数据:")
        logger.info("=" * 100)
        logger.info(f"{result}")
        logger.info("=" * 100)
        
        # 解析结果
        lines = result.strip().split('\n')
        results = []
        
        for i, line in enumerate(lines):
            try:
                stripped_line = line.strip()
                # 跳过空行和序号行
                if not stripped_line or stripped_line.startswith('===') or stripped_line.startswith('输入数据'):
                    continue
                # 移除序号前缀（如"1. "）
                if stripped_line and stripped_line[0].isdigit() and '. ' in stripped_line[:10]:
                    stripped_line = stripped_line.split('. ', 1)[1] if '. ' in stripped_line else stripped_line
                results.append(stripped_line)
            except Exception as e:
                logger.warning(f"解析第{i+1}行失败: {line}, 错误: {e}")
                results.append('')
        
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
    
    def _handle_goods_en_clean(self, input_data: Dict[str, Any], params: Dict[str, Any]) -> str:
        """
        处理英文品名清理

        输入：
            - input_data: {"H": 英文品名}
            - params: 规则参数

        输出：
            - 清理后的英文品名（str）
        """
        prompt = f"""你是一个英文数据清洗专家。请清理以下英文品名。
英文品名：{input_data.get('H', '')}

要求：
1. 删除括号内冗余内容（如"AIRPLANE TOY (L码)"→"AIRPLANE TOY"）
2. 英文名称统一大写（"cotton t-shirt"→"COTTON T-SHIRT"）
3. 只返回清理结果，不要包含其他文字"""

        result = self.ai_service.chat(prompt)
        return result.strip()

    def _handle_decimal_fix_batch(self, input_data_list: List[Dict[str, Any]], params: Dict[str, Any]) -> List[float]:
        """
        批量处理重量小数修复
        
        输入：
            - input_data_list: [{"F": 原始重量, "H": 品名, "I": 材质}, ...]
            - params: 规则参数
        
        输出：
            - 修复后的重量值列表（List[float]）
        """
        # 构建批量处理的prompt
        items_text = []
        for idx, input_data in enumerate(input_data_list):
            items_text.append(f"{idx+1}. 重量：{input_data.get('F', '')}，品名：{input_data.get('H', '')}，材质：{input_data.get('I', '')}")
        
        prompt = f"""你是一个物流数据处理专家。请分析以下货物信息，修复重量数据的小数点问题。

{chr(10).join(items_text)}

请只返回修复后的重量数值，每行一个数字，不要包含单位或其他文字。"""
        
        result = self.ai_service.chat(prompt)
        
        # 解析结果
        results = []
        lines = result.strip().split('\n')
        for i, line in enumerate(lines):
            try:
                results.append(float(line.strip()))
            except ValueError:
                results.append(None)
        
        # 确保结果数量匹配
        while len(results) < len(input_data_list):
            results.append(None)
        
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
        
        # 构建批量处理的prompt
        items_text = []
        for idx, input_data in enumerate(input_data_list):
            items_text.append(f"{input_data.get(target_col, '')}")
        
        # 将输入数据格式化为数组
        input_array = f"[{', '.join([f'\"{item}\"' for item in items_text])}]"
        
        prompt = f"""请将以下日文品名翻译成英文。

输入数据：{input_array}"""
        
        logger.info("=" * 100)
        logger.info("调用AI的输入数据:")
        logger.info("=" * 100)
        logger.info(f"{input_array}")
        logger.info("=" * 100)
        logger.info(f"调用AI的提示词:")
        logger.info("=" * 100)
        logger.info(f"{prompt}")
        logger.info("=" * 100)
        
        result = self.ai_service.chat(prompt, system_prompt)
        
        logger.info("=" * 100)
        logger.info("AI返回的输出数据:")
        logger.info("=" * 100)
        logger.info(f"{result}")
        logger.info("=" * 100)
        
        # 解析结果
        results = []
        
        # 尝试解析为JSON格式
        import json
        try:
            result = result.strip()
            if result.startswith('[') or result.startswith('["'):
                # JSON数组格式
                results = json.loads(result)
                if isinstance(results, list):
                    results = [str(item).strip()[:60] for item in results]
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

    def _handle_goods_en_clean_batch(self, input_data_list: List[Dict[str, Any]], params: Dict[str, Any]) -> List[str]:
        """
        批量处理英文品名清理

        输入：
            - input_data_list: [{"H": 英文品名}, ...]
            - params: 规则参数

        输出：
            - 清理后的英文品名列表（List[str]）
        """
        # 构建批量处理的prompt
        items_text = []
        for idx, input_data in enumerate(input_data_list):
            items_text.append(f"{idx+1}. {input_data.get('H', '')}")

        prompt = f"""你是一个英文数据清洗专家。请清理以下英文品名。

{chr(10).join(items_text)}

要求：
1. 输入的数组顺序保持不变
2. 删除括号内冗余内容（如"AIRPLANE TOY (L码)"→"AIRPLANE TOY"）
3. 英文名称统一大写（"cotton t-shirt"→"COTTON T-SHIRT"）
4. 每行一个清理结果，按顺序对应
5. 只返回清理结果，不要包含序号（如"1."、"2."等）
6. 只返回清理结果，不要包含其他文字"""

        result = self.ai_service.chat(prompt)

        # 解析结果
        results = []
        lines = result.strip().split('\n')
        for line in lines:
            # 移除序号（如"1. XXX" -> "XXX"）
            line = line.strip()
            if line and line[0].isdigit() and '.' in line:
                # 移除序号部分
                parts = line.split('.', 1)
                if len(parts) > 1:
                    line = parts[1].strip()
            results.append(line.strip())

        # 确保结果数量匹配
        while len(results) < len(input_data_list):
            results.append('')

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
        # 构建批量处理的prompt
        items_text = []
        for idx, input_data in enumerate(input_data_list):
            items_text.append(f"{idx+1}. {input_data.get('I', '')}")
        
        prompt = f"""你是一个专业的日英翻译专家。请将以下日文材质翻译成英文。

{chr(10).join(items_text)}

要求：
1. 翻译要准确、专业
2. 转换为标准材质代码（如：COTTON、POLYESTER等）
3. 每行一个翻译结果，按顺序对应
4. 只返回翻译结果，不要包含序号（如"1."、"2."等）
5. 只返回翻译结果，不要包含其他文字
6. 输入有{len(input_data_list)}个元素，输出必须保持{len(input_data_list)}个元素，不要偷懒输出
7. 如果某个元素无法翻译，请返回空字符串，不要跳过该元素
8. 必须严格按顺序返回{len(input_data_list)}个元素，不能多也不能少"""
        
        result = self.ai_service.chat(prompt)
        
        # 解析结果
        results = []
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
            results.append('')

        return results

    def _handle_goods_en_clean_batch(self, input_data_list: List[Dict[str, Any]], params: Dict[str, Any]) -> List[str]:
        """
        批量处理英文品名清理

        输入：
            - input_data_list: [{"H": 英文品名}, ...]
            - params: 规则参数

        输出：
            - 清理后的英文品名列表（List[str]）
        """
        # 构建批量处理的prompt
        items_text = []
        for idx, input_data in enumerate(input_data_list):
            items_text.append(f"{idx+1}. {input_data.get('H', '')}")

        prompt = f"""你是一个英文数据清洗专家。请清理以下英文品名。

{chr(10).join(items_text)}

要求：
1. 输入的数组顺序保持不变
2. 删除括号内冗余内容（如"AIRPLANE TOY (L码)"→"AIRPLANE TOY"）
3. 英文名称统一大写（"cotton t-shirt"→"COTTON T-SHIRT"）
4. 每行一个清理结果，按顺序对应
5. 只返回清理结果，不要包含其他文字
6. 输入有{len(input_data_list)}个元素，输出必须保持{len(input_data_list)}个元素，不要偷懒输出
7. 如果某个元素无法清理，请返回空字符串，不要跳过该元素
8. 必须严格按顺序返回{len(input_data_list)}个元素，不能多也不能少"""

        result = self.ai_service.chat(prompt)

        # 解析结果
        results = []
        lines = result.strip().split('\n')
        for line in lines:
            results.append(line.strip())

        # 确保结果数量匹配
        while len(results) < len(input_data_list):
            results.append('')

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
        # 构建批量处理的prompt
        items_text = []
        for idx, input_data in enumerate(input_data_list):
            items_text.append(f"{idx+1}. {input_data.get('AD', '')}")
        
        prompt = f"""你是一个日文数据处理专家。请清理以下日文收件人名。

{chr(10).join(items_text)}

要求：
1. 移除敬语和称谓（様、様、先生、様方等）
2. 标准化假名（平假名/片假名）
3. 长度不超过40个字符
4. 每行一个清理结果，按顺序对应
5. 只返回清理后的名字，不要包含序号（如"1."、"2."等）
6. 只返回清理后的名字，不要包含其他文字
7. 输入有{len(input_data_list)}个元素，输出必须保持{len(input_data_list)}个元素，不要偷懒输出
8. 如果某个元素无法清理，请返回空字符串，不要跳过该元素
9. 必须严格按顺序返回{len(input_data_list)}个元素，不能多也不能少"""
        
        result = self.ai_service.chat(prompt)
        
        # 解析结果
        results = []
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
            results.append('')

        return results

    def _handle_goods_en_clean_batch(self, input_data_list: List[Dict[str, Any]], params: Dict[str, Any]) -> List[str]:
        """
        批量处理英文品名清理

        输入：
            - input_data_list: [{"H": 英文品名}, ...]
            - params: 规则参数

        输出：
            - 清理后的英文品名列表（List[str]）
        """
        # 构建批量处理的prompt
        items_text = []
        for idx, input_data in enumerate(input_data_list):
            items_text.append(f"{idx+1}. {input_data.get('H', '')}")

        prompt = f"""你是一个英文数据清洗专家。请清理以下英文品名。

{chr(10).join(items_text)}

要求：
1. 输入的数组顺序保持不变
2. 删除括号内冗余内容（如"AIRPLANE TOY (L码)"→"AIRPLANE TOY"）
3. 英文名称统一大写（"cotton t-shirt"→"COTTON T-SHIRT"）
4. 每行一个清理结果，按顺序对应
5. 只返回清理结果，不要包含其他文字"""

        result = self.ai_service.chat(prompt)

        # 解析结果
        results = []
        lines = result.strip().split('\n')
        for line in lines:
            results.append(line.strip())

        # 确保结果数量匹配
        while len(results) < len(input_data_list):
            results.append('')

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
        target_col = params.get('target_col', 'K')
        rule_ref = params.get('rule_ref', 'policy_translate_from_targetcol_en_upper')
        
        logger.info(f"target_col: {target_col}")
        logger.info(f"rule_ref: {rule_ref}")
        
        # 获取组合后的提示词
        prompt = self._get_prompt_from_db(rule_ref, target_col)
        
        logger.info(f"从数据库中获取的提示词: {prompt[:200]}...")
        
        # 构建批量处理的输入数据
        items_text = []
        for idx, input_data in enumerate(input_data_list):
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
            
            items_text.append(f"{idx+1}. {value}")
        
        # 替换提示词中的{输入数据}占位符
        input_data_str = '\n'.join(items_text)
        prompt = prompt.replace('{输入数据}', input_data_str)
        prompt = prompt.replace('{input_count}', str(len(input_data_list)))
        
        logger.info("=" * 100)
        logger.info("调用AI的输入数据:")
        logger.info("=" * 100)
        logger.info(f"{input_data_str}")
        logger.info("=" * 100)
        logger.info(f"调用AI的提示词:")
        logger.info("=" * 100)
        logger.info(f"{prompt}")
        logger.info("=" * 100)
        
        result = self.ai_service.chat(prompt)
        
        logger.info("=" * 100)
        logger.info("AI返回的输出数据:")
        logger.info("=" * 100)
        logger.info(f"{result}")
        logger.info("=" * 100)
        
        # 解析结果
        lines = result.strip().split('\n')
        results = []
        for line in lines:
            # 移除序号（如"1. XXX" -> "XXX"）
            line = line.strip()
            if line and line[0].isdigit() and '.' in line:
                # 移除序号部分
                parts = line.split('.', 1)
                if len(parts) > 1:
                    line = parts[1].strip()
            results.append(line.strip().upper())
        
        # 确保结果数量匹配
        while len(results) < len(input_data_list):
            results.append('')
        
        logger.info(f"解析后的结果数量: {len(results)}")
        logger.info(f"解析后的结果: {results}")
        
        return results

    def _handle_goods_en_clean_batch(self, input_data_list: List[Dict[str, Any]], params: Dict[str, Any]) -> List[str]:
        """
        批量处理英文品名清理

        输入：
            - input_data_list: [{"H": 英文品名}, ...]
            - params: 规则参数

        输出：
            - 清理后的英文品名列表（List[str]）
        """
        # 构建批量处理的prompt
        items_text = []
        for idx, input_data in enumerate(input_data_list):
            items_text.append(f"{idx+1}. {input_data.get('H', '')}")

        prompt = f"""你是一个英文数据清洗专家。请清理以下英文品名。

{chr(10).join(items_text)}

要求：
1. 输入的数组顺序保持不变
2. 删除括号内冗余内容（如"AIRPLANE TOY (L码)"→"AIRPLANE TOY"）
3. 英文名称统一大写（"cotton t-shirt"→"COTTON T-SHIRT"）
4. 每行一个清理结果，按顺序对应
5. 只返回清理结果，不要包含其他文字"""

        result = self.ai_service.chat(prompt)

        # 解析结果
        results = []
        lines = result.strip().split('\n')
        for line in lines:
            results.append(line.strip())

        # 确保结果数量匹配
        while len(results) < len(input_data_list):
            results.append('')

        return results

    def _handle_goods_en_clean_batch(self, input_data_list: List[Dict[str, Any]], params: Dict[str, Any]) -> List[str]:
        """
        批量处理英文品名清理

        输入：
            - input_data_list: [{"H": 英文品名}, ...]
            - params: 规则参数

        输出：
            - 清理后的英文品名列表（List[str]）
        """
        # 构建批量处理的prompt
        items_text = []
        for idx, input_data in enumerate(input_data_list):
            items_text.append(f"{idx+1}. {input_data.get('H', '')}")

        prompt = f"""你是一个英文数据清洗专家。请清理以下英文品名。

{chr(10).join(items_text)}

要求：
1. 输入的数组顺序保持不变
2. 删除括号内冗余内容（如"AIRPLANE TOY (L码)"→"AIRPLANE TOY"）
3. 英文名称统一大写（"cotton t-shirt"→"COTTON T-SHIRT"）
4. 每行一个清理结果，按顺序对应
5. 只返回清理结果，不要包含其他文字"""

        result = self.ai_service.chat(prompt)

        # 解析结果
        results = []
        lines = result.strip().split('\n')
        for line in lines:
            results.append(line.strip())

        # 确保结果数量匹配
        while len(results) < len(input_data_list):
            results.append('')

        return results

