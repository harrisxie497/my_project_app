"""
新的_process_field方法实现，基于rule_definitions中的handler方法
"""

from app.services import field_handlers
import logging

logger = logging.getLogger(__name__)


def process_field_v2(
    map_op: str,
    source_cols: list,
    field_type: str,
    rule_ref: list,
    row: dict,
    pipeline: dict,
    exchange_rate_service=None,
    ai_service=None,
    current_time=None
) -> any:
    """
    处理单个字段（新版本）

    输入:
        - map_op: 映射操作类型
        - source_cols: 源列列表
        - field_type: 字段类型
        - rule_ref: 规则引用列表
        - row: 当前行数据
        - pipeline: 字段处理配置
        - exchange_rate_service: 汇率服务实例
        - ai_service: AI服务实例
        - current_time: 当前时间（用于AI上下文）

    输出:
        - 处理后的值
    """
    logger.debug(f"开始处理字段 - map_op: {map_op}, source_cols: {source_cols}, field_type: {field_type}, rule_ref: {rule_ref}")

    # 获取规则参数
    rule_params_json = pipeline.get('rule_params_json', {})
    rule_ref_key = rule_ref[0] if rule_ref else None

    if not rule_ref_key:
        logger.warning(f"缺少rule_ref，无法处理字段")
        return None

    # 获取规则参数
    rule_params = rule_params_json.get(rule_ref_key, {})
    
    # 根据handler方法调用对应的handler
    if rule_ref_key == 'policy_const':
        # assign.const
        const_value = rule_params.get('value', '')
        return field_handlers.assign_const(const_value)
    
    elif rule_ref_key == 'policy_seq_from_1':
        # calc.seq_from_1
        step = rule_params.get('step', 1)
        start = rule_params.get('start', 1)
        row_index = row.get('_row_index', 0)
        return field_handlers.calc_seq_from_1(row_index, step, start)
    
    elif rule_ref_key == 'policy_calc_invoice_price_fx_round':
        # calc.invoice_price_fx_round
        regex = rule_params.get('regex', r'^\d+$')
        original_price = row.get('V', 0)
        currency_code = row.get('Q', 'JPY')
        return field_handlers.calc_invoice_price_fx_round(original_price, currency_code, exchange_rate_service, regex)
    
    elif rule_ref_key == 'policy_copy_regex':
        # normalize.copy_then_regex
        regex = rule_params.get('regex', '')
        required = rule_params.get('required', False)
        remove_dash = rule_params.get('remove_dash', False)
        remove_leading_trailing_spaces = rule_params.get('remove_leading_trailing_spaces', False)
        remove_middle_spaces = rule_params.get('remove_middle_spaces', False)
        add_prefix_zero = rule_params.get('add_prefix_zero', False)
        source_col = source_cols[0] if source_cols else None
        source_value = row.get(source_col) if source_col else None
        return field_handlers.normalize_copy_then_regex(
            source_value, 
            regex, 
            required, 
            remove_dash, 
            remove_leading_trailing_spaces, 
            remove_middle_spaces,
            add_prefix_zero
        )
    
    elif rule_ref_key == 'policy_copy_optional_decimal':
        # normalize.copy_optional_decimal
        regex = rule_params.get('regex', '')
        allow_null = rule_params.get('allow_null', True)
        source_col = source_cols[0] if source_cols else None
        source_value = row.get(source_col) if source_col else None
        return field_handlers.normalize_copy_optional_decimal(source_value, regex, allow_null)

    elif rule_ref_key == 'policy_copy_one_decimal':
        # normalize.copy_one_decimal
        allow_null = rule_params.get('allow_null', True)
        source_col = source_cols[0] if source_cols else None
        source_value = row.get(source_col) if source_col else None
        return field_handlers.normalize_copy_one_decimal(source_value, allow_null)

    elif rule_ref_key == 'policy_default_copy':
        # normalize.copy_default_if_empty
        default_value = rule_params.get('default_value', '')
        remove_dash = rule_params.get('remove_dash', False)
        source_col = source_cols[0] if source_cols else None
        source_value = row.get(source_col) if source_col else None
        return field_handlers.normalize_copy_default_if_empty(source_value, default_value, remove_dash)
    
    elif rule_ref_key == 'policy_copy_equal_to':
        # validate.copy_then_equal_to_target_col
        equal_to_target_col = rule_params.get('equal_to_target_col', '')
        source_value = row.get(source_cols[0]) if source_cols else None
        target_value = row.get(equal_to_target_col)
        return field_handlers.validate_copy_then_equal_to_target_col(source_value, target_value, equal_to_target_col)
    
    elif rule_ref_key == 'policy_format_date_yyyy_mm_dd':
        # format.date_to_yyyy_mm_dd
        input_formats = rule_params.get('input_formats', None)
        required = rule_params.get('required', False)
        source_col = source_cols[0] if source_cols else None
        source_value = row.get(source_col) if source_col else None
        return field_handlers.format_date_to_yyyy_mm_dd(source_value, input_formats, required)
    
    elif rule_ref_key == 'policy_time_slot_conditional':
        # format.delivery_time_slot_conditional
        zero_value = rule_params.get('zero_value', '0')
        when_date_empty_zero_to = rule_params.get('when_date_empty_zero_to', '')
        when_date_present_zero_to = rule_params.get('when_date_present_zero_to', '00')
        range_regex_when_date_present = rule_params.get('range_regex_when_date_present', r'^\d{2}$')
        date_target_col = rule_params.get('date_target_col', 'C')
        
        source_value = row.get(source_cols[0]) if source_cols else None
        date_target_value = row.get(date_target_col)
        return field_handlers.format_delivery_time_slot_conditional(
            source_value, date_target_value, zero_value,
            when_date_empty_zero_to, when_date_present_zero_to, range_regex_when_date_present
        )
    
    elif rule_ref_key == 'policy_required_input':
        # validate.required_input
        required = rule_params.get('required', True)
        error_message = rule_params.get('error_message', None)
        source_col = source_cols[0] if source_cols else None
        source_value = row.get(source_col) if source_col else None
        return field_handlers.validate_required_input(source_value, required, error_message)
    

    elif rule_ref_key == 'policy_ai_goods_en':
        # ai.goods_name_en
        system_prompt = rule_params.get('system_prompt', None)
        input_data = {col: row.get(col) for col in source_cols}
        return field_handlers.ai_goods_name_en(input_data, ai_service, current_time, system_prompt)

    elif rule_ref_key == 'policy_ai_material_en':
        # ai.material_translate_and_substitute
        system_prompt = rule_params.get('system_prompt', None)
        input_data = {col: row.get(col) for col in source_cols}
        return field_handlers.ai_material_translate_and_substitute(input_data, ai_service, current_time, system_prompt)

    elif rule_ref_key == 'policy_ai_text_ja_clean':
        # ai.ja_name_clean
        system_prompt = rule_params.get('system_prompt', None)
        input_data = {col: row.get(col) for col in source_cols}
        return field_handlers.ai_ja_name_clean(input_data, ai_service, current_time, system_prompt)

    elif rule_ref_key == 'policy_ai_text_dress_clean':
        # ai.ja_address_clean
        system_prompt = rule_params.get('system_prompt', None)
        input_data = {col: row.get(col) for col in source_cols}
        return field_handlers.ai_ja_address_clean(input_data, ai_service, current_time, system_prompt)

    elif rule_ref_key == 'policy_translate_from_targetcol_en_upper':
        # ai.translate_from_targetcol_to_en_upper
        system_prompt = rule_params.get('system_prompt', None)
        depends_on = pipeline.get('depends_on', [])
        input_data = {col: row.get(col) for col in depends_on}
        return field_handlers.ai_translate_from_targetcol_to_en_upper(input_data, ai_service, current_time, system_prompt)
    
    else:
        logger.warning(f"未知的规则：{rule_ref_key}")
        return None


if __name__ == "__main__":
    # 测试代码
    print("process_field_v2 方法已实现")
