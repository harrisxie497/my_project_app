import logging
import re
from datetime import datetime
from typing import Any, Optional, Dict

logger = logging.getLogger(__name__)


# ==================== 旧方法（向后兼容） ====================

def copy_field(source_value: Any) -> Any:
    """
    复制字段值（旧方法，向后兼容）
    
    输入：
        - source_value: 源字段值
    
    输出：
        - 目标字段值
    """
    return source_value


def set_constant(value: str = "") -> str:
    """
    设置常量值（旧方法，向后兼容）
    
    输入：
        - value: 常量值（默认：空字符串）
    
    输出：
        - 常量值
    """
    return assign_const(value)


def generate_sequence(row_index: int) -> int:
    """
    生成序号（旧方法，向后兼容）
    
    输入：
        - row_index: 行索引（从0开始）
    
    输出：
        - 序号（从1开始）
    """
    return calc_seq_from_1(row_index)


def copy_equal_to(source_value: Any, target_value: Any) -> Any:
    """
    复制等于目标值（DEFAULT类型：如果源值为空，则返回默认值；否则返回源值）

    输入：
        - source_value: 源字段值
        - target_value: 默认值（从rule_params_json中获取）

    输出：
        - 如果源值为空，返回默认值；否则返回源值
    """
    try:
        logger.info(f"copy_equal_to调用 - source_value: {repr(source_value)}, target_value: {repr(target_value)}")
        
        # 如果源值为空，则返回默认值
        if source_value is None or (isinstance(source_value, str) and source_value.strip() == ''):
            logger.info(f"源值为空，返回默认值：{target_value}")
            return target_value
        
        logger.info(f"源值不为空，返回源值：{source_value}")
        return source_value
    
    except Exception as e:
        logger.error(f"复制等于目标值失败：{str(e)}", exc_info=True)
        raise


def calc_time_slot_with_delivery_date(d_value: Any, c_value: Any) -> str:
    """
    根据C列（配達指定日）的值来处理D列（時間帯指定）的值

    逻辑：
    1. C列不为空时：
       - D列本身有值 → 保持不变，值的范围为00-99范围的2位格式，如果是0变成00
    2. C列为空时：
       - D列本身有值 → 保持不变，如果是值是0则置空

    输入：
        - d_value: D列（時間帯指定）的原始值
        - c_value: C列（配達指定日）的值

    输出：
        - 处理后的D列值
    """
    logger.debug(f"calc_time_slot_with_delivery_date - d_value: {d_value}, c_value: {c_value}")

    # 如果D列为空，直接返回空
    if d_value is None or (isinstance(d_value, str) and d_value.strip() == ''):
        return ''

    # 转换D值为数字
    try:
        if isinstance(d_value, str):
            d_num = int(d_value.strip())
        else:
            d_num = int(d_value)
    except (ValueError, TypeError):
        # 如果无法转换为数字，保持原值
        return str(d_value) if d_value is not None else ''

    # 检查C列是否为空
    c_is_empty = c_value is None or (isinstance(c_value, str) and c_value.strip() == '')

    if not c_is_empty:
        # C列不为空：D列本身有值，保持不变，但如果是0则变成00
        if d_num == 0:
            result = '00'
        else:
            # 确保是2位格式（00-99范围）
            d_num = max(0, min(99, d_num))
            result = f"{d_num:02d}"
    else:
        # C列为空：D列本身有值
        # 如果D列为0，返回空字符串；否则格式化为2位数
        if d_num == 0:
            result = ''
        else:
            d_num = max(0, min(99, d_num))
            result = f"{d_num:02d}"

    logger.debug(f"calc_time_slot_with_delivery_date - c_is_empty: {c_is_empty}, d_num: {d_num}, result: {result}")
    return result


# ==================== assign ====================

def assign_const(value: str = "") -> str:
    """
    设置常量值
    
    输入：
        - value: 常量值（默认：空字符串）
    
    输出：
        - 常量值
    """
    return value


# ==================== calc ====================

def calc_seq_from_1(row_index: int, step: int = 1, start: int = 1) -> int:
    """
    生成连续递增序号（从 start 开始，步长 step）
    
    输入：
        - row_index: 行索引（从0开始）
        - step: 步长（默认 1）
        - start: 起始值（默认 1）
    
    输出：
        - 序号
    """
    return start + row_index * step


def calc_invoice_price_fx_round(original_price: float, currency_code: str, exchange_rates: Dict[str, float] = None, regex: str = r'^\d+$') -> int:
    """
    计算インボイス価格（汇率换算）
    
    输入：
        - original_price: 原始文件中R列的值（外币价格）
        - currency_code: Q列的通货代码（如：USD、EUR等）
        - exchange_rates: 汇率字典（可选，如果不提供则使用exchange_rate_service）
        - regex: 输出校验正则表达式（例如整数：^\d+$）
    
    输出：
        - 日元价格（取整）（int）
    """
    try:
        logger.info(f"计算汇率换算：{original_price} {currency_code} -> JPY")
        
        # 如果提供了汇率字典，则从字典中获取汇率
        if exchange_rates is not None:
            exchange_rate = exchange_rates.get(currency_code, 1.0)
            logger.info(f"使用预获取的汇率：{currency_code} -> JPY = {exchange_rate}")
        else:
            # 向后兼容：如果没有提供汇率字典，则使用exchange_rate_service
            from app.services.exchange_rate_service import ExchangeRateService
            exchange_rate_service = ExchangeRateService(api_key="")
            exchange_rate = exchange_rate_service.get_rate(currency_code, 'JPY')
        
        jpy_price = original_price * exchange_rate
        jpy_price = int(round(jpy_price))
        
        if not re.match(regex, str(jpy_price)):
            raise ValueError(f"计算结果不符合正则验证：{jpy_price}")
        
        logger.info(f"计算完成：{jpy_price} JPY")
        return jpy_price
        
    except Exception as e:
        logger.error(f"计算汇率换算失败：{str(e)}", exc_info=True)
        raise


# ==================== format ====================

def format_date_to_yyyy_mm_dd(date_value: Any, input_formats: Optional[list] = None, required: bool = False) -> Optional[str]:
    """
    配達指定日：格式化为 YYYY-MM-DD
    
    输入：
        - date_value: 日期值
        - input_formats: 可选：允许的输入日期格式列表（不配则后台自动识别）
        - required: 是否必填（默认 false）
    
    输出：
        - 格式化后的日期字符串（YYYY-MM-DD）
    """
    if date_value is None:
        if required:
            raise ValueError("日期为必填项")
        return None
    
    try:
        from datetime import datetime
        
        # 如果已经是字符串，尝试解析
        if isinstance(date_value, str):
            date_value = date_value.strip()
            if not date_value:
                if required:
                    raise ValueError("日期为必填项")
                return None
            
            # 尝试多种格式
            if input_formats:
                for fmt in input_formats:
                    try:
                        dt = datetime.strptime(date_value, fmt)
                        return dt.strftime('%Y-%m-%d')
                    except ValueError:
                        continue
            
            # 自动识别常见格式
            common_formats = [
                '%Y-%m-%d',
                '%Y/%m/%d',
                '%Y%m%d',
                '%Y年%m月%d日',
                '%d/%m/%Y',
                '%d-%m-%Y',
            ]
            
            for fmt in common_formats:
                try:
                    dt = datetime.strptime(date_value, fmt)
                    return dt.strftime('%Y-%m-%d')
                except ValueError:
                    continue
            
            raise ValueError(f"无法解析日期格式：{date_value}")
        
        # 如果是datetime对象
        elif isinstance(date_value, datetime):
            return date_value.strftime('%Y-%m-%d')
        
        else:
            raise ValueError(f"不支持的日期类型：{type(date_value)}")
    
    except Exception as e:
        logger.error(f"格式化日期失败：{str(e)}", exc_info=True)
        raise


def format_delivery_time_slot_conditional(
    source_value: Any,
    date_target_value: Any,
    zero_value: str = "0",
    when_date_empty_zero_to: str = "",
    when_date_present_zero_to: str = "00",
    range_regex_when_date_present: str = r'^\d{2}$'
) -> Optional[str]:
    """
    時間帯指定：C非空→范围00-99且0→00；C为空→原值保持，若为0则置空
    
    输入：
        - source_value: 源值（D列）
        - date_target_value: 依赖的日期列值（C列）
        - zero_value: 被视为0的取值（默认 "0"）
        - when_date_empty_zero_to: C为空且D=0时替换值（默认 ""）
        - when_date_present_zero_to: C非空且D=0时替换值（默认 "00"）
        - range_regex_when_date_present: C非空时的范围验证正则（默认 ^\d{2}$ 且 00-99 由后台校验）
    
    输出：
        - 处理后的值
    """
    try:
        # 检查是否为0
        is_zero = str(source_value) == zero_value if source_value is not None else False
        
        # C列为空
        if date_target_value is None or (isinstance(date_target_value, str) and date_target_value.strip() == ''):
            if is_zero:
                return when_date_empty_zero_to
            return source_value
        
        # C列非空
        if is_zero:
            return when_date_present_zero_to
        
        # 验证范围
        if not re.match(range_regex_when_date_present, str(source_value)):
            raise ValueError(f"值不符合范围验证：{source_value}")
        
        # 验证00-99范围
        try:
            value_int = int(source_value)
            if not (0 <= value_int <= 99):
                raise ValueError(f"值超出00-99范围：{source_value}")
        except ValueError:
            raise ValueError(f"值不是有效的数字：{source_value}")
        
        return source_value
    
    except Exception as e:
        logger.error(f"格式化时间槽失败：{str(e)}", exc_info=True)
        raise


# ==================== normalize ====================

def normalize_copy_then_regex(
    source_value: Any,
    regex: str,
    required: bool = False,
    remove_dash: bool = False,
    remove_leading_trailing_spaces: bool = False,
    remove_middle_spaces: bool = False
) -> Any:
    """
    复制源值→可选去"-"→可选去前后空格→可选去中间空格→按正则校验（可配置是否必填）
    
    输入：
        - source_value: 源值
        - regex: 正则表达式（必填）
        - required: 是否必填
        - remove_dash: 是否移除连接符"-"
        - remove_leading_trailing_spaces: 是否去除前后空格
        - remove_middle_spaces: 是否去除中间空格
    
    输出：
        - 处理后的值
    """
    try:
        # 处理None值
        if source_value is None:
            if required:
                raise ValueError("值为必填项")
            return None
        
        # 转换为字符串
        source_value = str(source_value)
        
        # 移除横杠
        if remove_dash:
            source_value = source_value.replace('-', '')
        
        # 去除前后空格
        if remove_leading_trailing_spaces:
            source_value = source_value.strip()
        
        # 去除中间空格
        if remove_middle_spaces:
            source_value = source_value.replace(' ', '')
        
        # 验证regex
        if not re.match(regex, source_value):
            raise ValueError(f"值不匹配正则表达式：{regex}")
        
        return source_value
    
    except Exception as e:
        logger.error(f"正则校验失败：{str(e)}", exc_info=True)
        raise


def normalize_copy_optional_decimal(
    source_value: Any,
    regex: str,
    allow_null: bool = True
) -> Any:
    """
    复制源值：可配置是否允许为空；非空时按正则校验（用于两位小数等）
    
    输入：
        - source_value: 源值
        - regex: 非空时的正则表达式（如 ^\d+\.\d{2}$）
        - allow_null: 是否允许为空（默认 true）
    
    输出：
        - 处理后的值
    """
    try:
        # 处理None值
        if source_value is None:
            if not allow_null:
                raise ValueError("值不允许为空")
            return None
        
        # 验证regex
        if not re.match(regex, str(source_value)):
            raise ValueError(f"值不匹配正则表达式：{regex}")
        
        return source_value
    
    except Exception as e:
        logger.error(f"可选小数校验失败：{str(e)}", exc_info=True)
        raise


def normalize_copy_one_decimal(
    source_value: Any,
    allow_null: bool = True
) -> Any:
    """
    复制源值：保留1位小数，去掉非数字和小数点的字符

    输入：
        - source_value: 源值
        - allow_null: 是否允许为空（默认 true）

    输出：
        - 处理后的值（保留1位小数）
        - None/空字符串/无效值返回空字符串 ""
    """
    try:
        # 处理None值或空字符串 - 返回空字符串
        if source_value is None or (isinstance(source_value, str) and str(source_value).strip() == ''):
            return ""

        # 转换为字符串并去掉非数字和小数点的字符
        value_str = str(source_value)
        # 只保留数字和小数点
        cleaned_value = re.sub(r'[^\d.]', '', value_str)

        # 尝试转换为float并保留1位小数
        try:
            float_value = float(cleaned_value)
            # 四舍五入保留1位小数
            rounded_value = round(float_value, 1)
            # 格式化为字符串，确保保留1位小数（即使小数位是0）
            result = f"{rounded_value:.1f}"
            return result
        except ValueError:
            # 如果无法转换为float，返回空字符串
            return ""

    except Exception as e:
        logger.error(f"保留1位小数处理失败：{str(e)}", exc_info=True)
        return ""


def normalize_copy_default_if_empty(
    source_value: Any,
    default_value: str,
    remove_dash: bool = False
) -> str:
    """
    复制源值；为空则使用默认值兜底（可选先去"-"）
    
    输入：
        - source_value: 源值
        - default_value: 默认值（必填）
        - remove_dash: 是否移除连接符"-"
    
    输出：
        - 处理后的值
    """
    try:
        # 处理None值或空字符串
        if source_value is None or (isinstance(source_value, str) and source_value.strip() == ''):
            return default_value
        
        # 移除横杠
        if remove_dash and isinstance(source_value, str):
            source_value = source_value.replace('-', '')
        
        return source_value
    
    except Exception as e:
        logger.error(f"默认值处理失败：{str(e)}", exc_info=True)
        raise


# ==================== validate ====================

def validate_copy_then_equal_to_target_col(
    source_value: Any,
    target_value: Any,
    equal_to_target_col: str
) -> Any:
    """
    复制源值后校验：与指定目标列完全一致（跨列一致性）
    
    输入：
        - source_value: 源值
        - target_value: 目标列值
        - equal_to_target_col: 对齐的目标列（如 C）
    
    输出：
        - 如果源值为空，则复制目标列值；否则返回源值
    """
    try:
        # 如果源值为空，则复制目标列值
        if source_value is None or (isinstance(source_value, str) and source_value.strip() == ''):
            logger.debug(f"源值为空，复制目标列 {equal_to_target_col} 的值：{target_value}")
            return target_value
        
        return source_value
    
    except Exception as e:
        logger.error(f"复制等于目标列失败：{str(e)}", exc_info=True)
        raise


def validate_required_input(
    source_value: Any,
    required: bool = True,
    error_message: Optional[str] = None
) -> Any:
    """
    外部输入列必填校验（用于 map_op=INPUT）

    输入：
        - source_value: 源值
        - required: 是否必填（默认 true）
        - error_message: 自定义错误提示（可选）

    输出：
        - 源值

    异常：
        - ValueError: 当 required=True 且值为 None 或空字符串时
    """
    if required:
        # 检查 None 或空字符串
        if source_value is None:
            error_msg = error_message or "值为必填项"
            raise ValueError(error_msg)

        # 字符串类型检查是否为空白
        if isinstance(source_value, str) and source_value.strip() == '':
            error_msg = error_message or "值为必填项"
            raise ValueError(error_msg)

    return source_value


# ==================== AI ====================

def ai_goods_name_en(
    input_data: Dict[str, Any],
    ai_service = None,
    current_time: Optional[str] = None,
    system_prompt: Optional[str] = None
) -> str:
    """
    品名：去括号备注→英译→大写→去冗余（后台固定流程）

    输入：
        - input_data: 输入数据字典（包含源列数据，如 H=品名）
        - ai_service: AI服务实例
        - current_time: 当前时间（用于AI上下文）
        - system_prompt: 系统提示词（从配置表读取）

    输出：
        - 处理后的品名（英文大写）
    """
    if not ai_service:
        logger.warning("ai_goods_name_en: AI服务未提供，返回原值")
        return str(input_data.get('H', ''))

    # 用户提示词 - 基于输入数据动态构建
    user_prompt = f"""
日文品名：{input_data.get('H', '')}"""

    try:
        result = ai_service.chat(user_prompt, system_prompt)
        result = result.replace('/', '').replace('\\', '')
        return result[:60].upper()
    except Exception as e:
        logger.error(f"ai_goods_name_en 调用AI失败：{str(e)}")
        return str(input_data.get('H', ''))


def ai_material_translate_and_substitute(
    input_data: Dict[str, Any],
    ai_service = None,
    current_time: Optional[str] = None,
    system_prompt: Optional[str] = None
) -> str:
    """
    材质：去括号备注→英译大写→材质替换表置换（后台固定流程）

    输入：
        - input_data: 输入数据字典（包含源列数据，如 I=材质）
        - ai_service: AI服务实例
        - current_time: 当前时间（用于AI上下文）
        - system_prompt: 系统提示词（从配置表读取）

    输出：
        - 处理后的材质（英文大写）
    """
    if not ai_service:
        logger.warning("ai_material_translate_and_substitute: AI服务未提供，返回原值")
        return str(input_data.get('I', ''))

    # 用户提示词 - 基于输入数据动态构建
    user_prompt = f"""
日文材质：{input_data.get('I', '')}"""

    try:
        result = ai_service.chat(user_prompt, system_prompt)
        return result.strip().upper()
    except Exception as e:
        logger.error(f"ai_material_translate_and_substitute 调用AI失败：{str(e)}")
        return str(input_data.get('I', ''))


def ai_ja_name_clean(
    input_data: Dict[str, Any],
    ai_service = None,
    current_time: Optional[str] = None,
    system_prompt: Optional[str] = None
) -> str:
    """
    收件人名（日文）清洗：去括号备注，输出更像常见日本名字（后台固定流程）

    输入：
        - input_data: 输入数据字典（包含源列数据，如 AD=收件人名, AE=收件人地址）
        - ai_service: AI服务实例
        - current_time: 当前时间（用于AI上下文）
        - system_prompt: 系统提示词（从配置表读取）

    输出：
        - 清洗后的收件人名
    """
    if not ai_service:
        logger.warning("ai_ja_name_clean: AI服务未提供，返回原值")
        return str(input_data.get('AD', ''))

    # 用户提示词 - 基于输入数据动态构建
    user_prompt = f"""
日文收件人名：{input_data.get('AD', '')}"""

    try:
        result = ai_service.chat(user_prompt, system_prompt)
        return result[:40]
    except Exception as e:
        logger.error(f"ai_ja_name_clean 调用AI失败：{str(e)}")
        return str(input_data.get('AD', ''))


def ai_translate_from_targetcol_to_en_upper(
    input_data: Dict[str, Any],
    ai_service = None,
    current_time: Optional[str] = None,
    system_prompt: Optional[str] = None
) -> str:
    """
    从目标列（X/Y）翻译为英文并大写（后台固定流程）

    输入：
        - input_data: 输入数据字典（包含源列数据，如 target_col=目标列值）
        - ai_service: AI服务实例
        - current_time: 当前时间（用于AI上下文）
        - system_prompt: 系统提示词（从配置表读取）

    输出：
        - 翻译后的英文（大写）
    """
    if not ai_service:
        logger.warning("ai_translate_from_targetcol_to_en_upper: AI服务未提供，返回原值")
        return str(input_data.get('target_col', ''))

    # 用户提示词 - 基于输入数据动态构建
    user_prompt = f"""
日文内容：{input_data.get('target_col', '')}"""

    try:
        result = ai_service.chat(user_prompt, system_prompt)
        return result.upper()
    except Exception as e:
        logger.error(f"ai_translate_from_targetcol_to_en_upper 调用AI失败：{str(e)}")
        return str(input_data.get('target_col', ''))

def ai_ja_address_clean(
    input_data: Dict[str, Any],
    ai_service = None,
    current_time: Optional[str] = None,
    system_prompt: Optional[str] = None
) -> str:
    """
    收件人地址（日文）清理和翻译：将日本地址精准翻译成英文（罗马字），确保语义准确无误
    
    输入：
        - input_data: 输入数据字典（包含源列数据，如 AE=收件人地址）
        - ai_service: AI服务实例
        - current_time: 当前时间（用于AI上下文）
        - system_prompt: 系统提示词（从配置表读取）
    
    输出：
        - 翻译后的英文地址（大写）
    """
    if not ai_service:
        logger.warning("ai_ja_address_clean: AI服务未提供，返回原值")
        return str(input_data.get('AE', ''))
    
    # 获取收件人地址
    address = input_data.get('AE', '')
    
    # 如果地址为空，返回空字符串
    if not address:
        return ''
    
    # 用户提示词 - 基于输入数据动态构建
    user_prompt = f"""
日文地址：{address}"""
    
    try:
        result = ai_service.chat(user_prompt, system_prompt)
        return result.upper()
    except Exception as e:
        logger.error(f"ai_ja_address_clean 调用AI失败：{str(e)}")
        return str(input_data.get('AE', ''))


def ai_translate_name_en_upper(
    input_data: Dict[str, Any],
    ai_service = None,
    current_time: Optional[str] = None,
    system_prompt: Optional[str] = None
) -> str:
    """
    日文人名翻译为英文并大写（后台固定流程）

    输入：
        - input_data: 输入数据字典（包含源列数据，如 target_col=目标列值）
        - ai_service: AI服务实例
        - current_time: 当前时间（用于AI上下文）
        - system_prompt: 系统提示词（从配置表读取）

    输出：
        - 翻译后的英文（大写）
    """
    if not ai_service:
        logger.warning("ai_translate_name_en_upper: AI服务未提供，返回原值")
        return str(input_data.get('target_col', ''))

    # 用户提示词 - 基于输入数据动态构建
    user_prompt = f"""
日文内容：{input_data.get('target_col', '')}"""

    try:
        result = ai_service.chat(user_prompt, system_prompt)
        return result.upper()
    except Exception as e:
        logger.error(f"ai_translate_name_en_upper 调用AI失败：{str(e)}")
        return str(input_data.get('target_col', ''))
