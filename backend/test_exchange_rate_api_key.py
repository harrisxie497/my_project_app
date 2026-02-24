"""
测试脚本：测试汇率服务API KEY和真实汇率获取
"""
import sys
import os
import logging

# 添加项目路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.exchange_rate_service import ExchangeRateService
from app.core.config import settings

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def test_api_key_config():
    """
    测试API KEY配置
    """
    logger.info("=" * 100)
    logger.info("测试1: API KEY配置检查")
    logger.info("=" * 100)

    # 方法1: 从settings获取
    api_key_from_settings = getattr(settings, 'EXCHANGE_RATE_API_KEY', '')
    base_url_from_settings = getattr(settings, 'EXCHANGE_RATE_API_URL', 'https://v6.exchangerate-api.com/v6')

    logger.info(f"API URL (from settings): {base_url_from_settings}")
    logger.info(f"API KEY (from settings): {api_key_from_settings[:20]}..." if api_key_from_settings else "未配置")
    logger.info(f"API KEY 长度: {len(api_key_from_settings)}")

    # 方法2: 直接从环境变量读取
    import os
    api_key_from_env = os.getenv('EXCHANGE_RATE_API_KEY', '')
    base_url_from_env = os.getenv('EXCHANGE_RATE_API_URL', 'https://v6.exchangerate-api.com/v6')

    logger.info("")
    logger.info("直接从环境变量读取:")
    logger.info(f"  API URL (from env): {base_url_from_env}")
    logger.info(f"  API KEY (from env): {api_key_from_env[:20]}..." if api_key_from_env else "未配置")
    logger.info(f"  API KEY 长度: {len(api_key_from_env)}")

    # 优先使用环境变量的值
    api_key = api_key_from_env if api_key_from_env else api_key_from_settings
    base_url = base_url_from_env if base_url_from_env else base_url_from_settings

    logger.info("")
    logger.info(f"最终使用 - API URL: {base_url}")
    logger.info(f"最终使用 - API KEY: {api_key[:20]}..." if api_key else "未配置")

    if api_key:
        # 显示API KEY的部分信息（用于调试）
        masked_key = f"{api_key[:8]}...{api_key[-4:]}" if len(api_key) > 12 else "***"
        logger.info(f"API KEY (已脱敏): {masked_key}")
        logger.info(f"API KEY 长度: {len(api_key)}")
        logger.info("✓ API KEY已配置")
    else:
        logger.warning("✗ API KEY未配置")
        logger.info("请在.env文件中配置: EXCHANGE_RATE_API_KEY=your_api_key")

    return api_key, base_url


def test_exchange_rate_initialization(api_key, base_url):
    """
    测试汇率服务初始化
    """
    logger.info("")
    logger.info("=" * 100)
    logger.info("测试2: 汇率服务初始化")
    logger.info("=" * 100)

    if not api_key:
        logger.warning("跳过测试：API KEY未配置")
        return None

    try:
        # 初始化汇率服务
        logger.info("初始化汇率服务...")
        exchange_service = ExchangeRateService(api_key, base_url)
        
        logger.info("✓ 汇率服务初始化成功")
        logger.info(f"  - API URL: {exchange_service.base_url}")
        logger.info(f"  - 缓存时长: {exchange_service.cache_duration}")
        logger.info(f"  - 缓存状态: {'有缓存' if exchange_service.cache else '无缓存'}")
        
        return exchange_service
        
    except Exception as e:
        logger.error(f"✗ 汇率服务初始化失败: {str(e)}", exc_info=True)
        return None


def test_get_real_rates(exchange_service):
    """
    测试获取真实汇率
    """
    logger.info("")
    logger.info("=" * 100)
    logger.info("测试3: 获取真实汇率")
    logger.info("=" * 100)

    if not exchange_service:
        logger.warning("跳过测试：汇率服务未初始化")
        return False

    # 测试货币列表
    test_currencies = ['USD', 'EUR', 'CNY', 'JPY', 'GBP', 'AUD', 'CAD']
    
    results = {}
    
    for currency in test_currencies:
        if currency == 'JPY':
            logger.info(f"JPY -> JPY: 跳过 (汇率固定为1.0)")
            results['JPY'] = 1.0
            continue
        
        try:
            logger.info(f"获取汇率: {currency} -> JPY")
            rate = exchange_service.get_rate(currency, 'JPY')
            logger.info(f"✓ {currency} -> JPY: {rate}")
            results[currency] = rate
        except Exception as e:
            logger.error(f"✗ {currency} -> JPY: {str(e)}")
            results[currency] = None
    
    # 汇总结果
    logger.info("")
    logger.info("汇率获取结果汇总:")
    logger.info("-" * 100)
    
    success_count = 0
    for currency, rate in results.items():
        status = "✓" if rate is not None else "✗"
        rate_str = f"{rate:.4f}" if rate is not None else "失败"
        logger.info(f"  {status} {currency} -> JPY: {rate_str}")
        if rate is not None:
            success_count += 1
    
    logger.info("-" * 100)
    logger.info(f"成功: {success_count}/{len(test_currencies)}")
    
    return success_count == len(test_currencies)


def test_rate_format_validation(exchange_service):
    """
    测试汇率格式验证
    """
    logger.info("")
    logger.info("=" * 100)
    logger.info("测试4: 汇率格式验证")
    logger.info("=" * 100)

    if not exchange_service:
        logger.warning("跳过测试：汇率服务未初始化")
        return False

    try:
        # 获取一个汇率
        logger.info("获取USD汇率用于格式验证...")
        rate = exchange_service.get_rate('USD', 'JPY')
        
        logger.info(f"汇率值: {rate}")
        logger.info(f"类型: {type(rate).__name__}")
        
        # 验证格式
        checks = {
            "是数字类型": isinstance(rate, (int, float)),
            "大于0": rate > 0,
            "是浮点数": isinstance(rate, float),
            "合理范围(1-1000)": 1 <= rate <= 1000
        }
        
        all_passed = True
        for check_name, check_result in checks.items():
            status = "✓" if check_result else "✗"
            logger.info(f"  {status} {check_name}")
            if not check_result:
                all_passed = False
        
        if all_passed:
            logger.info("✓ 汇率格式验证通过")
        else:
            logger.warning("✗ 汇率格式验证失败")
        
        return all_passed
        
    except Exception as e:
        logger.error(f"✗ 汇率格式验证失败: {str(e)}", exc_info=True)
        return False


def test_cache_functionality(exchange_service):
    """
    测试缓存功能
    """
    logger.info("")
    logger.info("=" * 100)
    logger.info("测试5: 缓存功能")
    logger.info("=" * 100)

    if not exchange_service:
        logger.warning("跳过测试：汇率服务未初始化")
        return False

    try:
        # 第一次获取
        logger.info("第一次获取USD汇率...")
        rate1 = exchange_service.get_rate('USD', 'JPY')
        logger.info(f"  结果: {rate1}")
        logger.info(f"  缓存大小: {len(exchange_service.cache)}")
        
        # 第二次获取（应该使用缓存）
        logger.info("")
        logger.info("第二次获取USD汇率（应该使用缓存）...")
        rate2 = exchange_service.get_rate('USD', 'JPY')
        logger.info(f"  结果: {rate2}")
        logger.info(f"  缓存大小: {len(exchange_service.cache)}")
        
        # 验证缓存
        if rate1 == rate2:
            logger.info("✓ 缓存功能正常")
            logger.info(f"  两次获取结果一致: {rate1}")
        else:
            logger.warning("✗ 缓存功能异常")
            logger.warning(f"  第一次: {rate1}, 第二次: {rate2}")
            return False
        
        # 检查缓存内容
        logger.info("")
        logger.info("缓存内容:")
        for cache_key, (cached_time, cached_rate) in exchange_service.cache.items():
            logger.info(f"  {cache_key}: {cached_rate} (时间: {cached_time})")
        
        return True
        
    except Exception as e:
        logger.error(f"✗ 缓存功能测试失败: {str(e)}", exc_info=True)
        return False


def test_calculation_with_real_rate(exchange_service):
    """
    测试使用真实汇率进行计算
    """
    logger.info("")
    logger.info("=" * 100)
    logger.info("测试6: 使用真实汇率计算")
    logger.info("=" * 100)

    if not exchange_service:
        logger.warning("跳过测试：汇率服务未初始化")
        return False

    try:
        from app.services.field_handlers import calc_invoice_price_fx_round

        # 测试数据
        test_cases = [
            (100.0, 'USD', '100美元'),
            (50.0, 'CNY', '50人民币'),
            (200.0, 'EUR', '200欧元'),
        ]

        all_success = True
        for price, currency, desc in test_cases:
            logger.info("")
            logger.info(f"计算: {desc}")
            logger.info(f"  原始价格: {price} {currency}")

            try:
                jpy_price = calc_invoice_price_fx_round(
                    original_price=price,
                    currency_code=currency,
                    exchange_rate_service=exchange_service,
                    regex=r'^\d+$'
                )

                logger.info(f"  日元价格: {jpy_price} JPY")
                logger.info("✓ 计算成功")

            except Exception as e:
                logger.error(f"✗ 计算失败: {str(e)}")
                all_success = False
        
        if all_success:
            logger.info("")
            logger.info("✓ 所有计算成功")
        
        return all_success
        
    except Exception as e:
        logger.error(f"✗ 计算测试失败: {str(e)}", exc_info=True)
        return False


def main():
    """
    主函数：执行所有测试
    """
    logger.info("=" * 100)
    logger.info("汇率服务API KEY测试")
    logger.info("=" * 100)

    try:
        # 测试1: API KEY配置
        api_key, base_url = test_api_key_config()

        # 测试2: 初始化
        exchange_service = test_exchange_rate_initialization(api_key, base_url)

        if exchange_service:
            # 测试3: 获取真实汇率
            test3_success = test_get_real_rates(exchange_service)
            
            # 测试4: 格式验证
            test4_success = test_rate_format_validation(exchange_service)
            
            # 测试5: 缓存功能
            test5_success = test_cache_functionality(exchange_service)
            
            # 测试6: 计算测试
            test6_success = test_calculation_with_real_rate(exchange_service)
            
            # 汇总结果
            logger.info("")
            logger.info("=" * 100)
            logger.info("测试结果汇总")
            logger.info("=" * 100)
            logger.info(f"测试1 (API KEY配置): {'✓ 通过' if api_key else '✗ 跳过'}")
            logger.info(f"测试2 (服务初始化): {'✓ 通过' if exchange_service else '✗ 失败'}")
            logger.info(f"测试3 (获取汇率): {'✓ 通过' if test3_success else '✗ 失败'}")
            logger.info(f"测试4 (格式验证): {'✓ 通过' if test4_success else '✗ 失败'}")
            logger.info(f"测试5 (缓存功能): {'✓ 通过' if test5_success else '✗ 失败'}")
            logger.info(f"测试6 (计算测试): {'✓ 通过' if test6_success else '✗ 失败'}")
        else:
            logger.info("")
            logger.info("=" * 100)
            logger.info("测试结果汇总")
            logger.info("=" * 100)
            logger.info("汇率服务未初始化，跳过后续测试")

        logger.info("")
        logger.info("=" * 100)
        logger.info("测试完成!")
        logger.info("=" * 100)

    except Exception as e:
        logger.error(f"测试失败: {str(e)}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
