"""
测试脚本：使用真实的API KEY测试汇率服务
"""
import sys
import os
import logging

# 添加项目路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dotenv import load_dotenv
from app.services.exchange_rate_service import ExchangeRateService
from app.services.field_handlers import calc_invoice_price_fx_round

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """
    主函数：测试真实API
    """
    logger.info("=" * 100)
    logger.info("使用真实API KEY测试汇率服务")
    logger.info("=" * 100)

    # 加载.env文件
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    load_dotenv(env_path)

    # 读取配置
    api_key = os.getenv('EXCHANGE_RATE_API_KEY', '')
    base_url = os.getenv('EXCHANGE_RATE_API_URL', 'https://v6.exchangerate-api.com/v6')

    logger.info(f"API URL: {base_url}")
    logger.info(f"API KEY (已脱敏): {api_key[:8]}...{api_key[-4:]}" if len(api_key) > 12 else "***")

    if not api_key:
        logger.error("API KEY未配置")
        return

    try:
        # 初始化汇率服务
        logger.info("")
        logger.info("初始化汇率服务...")
        exchange_service = ExchangeRateService(api_key, base_url)
        logger.info("✓ 汇率服务初始化成功")

        # 测试获取汇率
        logger.info("")
        logger.info("=" * 100)
        logger.info("测试1: 获取真实汇率")
        logger.info("=" * 100)

        test_currencies = ['USD', 'EUR', 'CNY']
        rates = {}

        for currency in test_currencies:
            try:
                logger.info(f"获取汇率: {currency} -> JPY")
                rate = exchange_service.get_rate(currency, 'JPY')
                logger.info(f"✓ {currency} -> JPY: {rate}")
                rates[currency] = rate
            except Exception as e:
                logger.error(f"✗ {currency} -> JPY: {str(e)}")
                rates[currency] = None

        # 测试缓存
        logger.info("")
        logger.info("测试缓存功能:")
        logger.info("第二次获取USD汇率（应该使用缓存）")
        rate_cached = exchange_service.get_rate('USD', 'JPY')
        logger.info(f"✓ USD -> JPY (缓存): {rate_cached}")

        # 测试计算
        logger.info("")
        logger.info("=" * 100)
        logger.info("测试2: 使用真实汇率计算")
        logger.info("=" * 100)

        test_cases = [
            (100.0, 'USD', '100美元'),
            (50.0, 'CNY', '50人民币'),
            (200.0, 'EUR', '200欧元'),
        ]

        for price, currency, desc in test_cases:
            if currency == 'EUR' and rates.get('EUR') is None:
                logger.warning(f"跳过{desc}: EUR汇率获取失败")
                continue

            logger.info(f"")
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

                if currency in rates and rates[currency] is not None:
                    expected = int(round(price * rates[currency]))
                    logger.info(f"  期望价格: {expected} JPY")

                    if jpy_price == expected:
                        logger.info(f"  ✓ 计算正确")
                    else:
                        logger.warning(f"  ✗ 计算不匹配")

            except Exception as e:
                logger.error(f"  ✗ 计算失败: {str(e)}")

        # 显示所有获取的汇率
        logger.info("")
        logger.info("=" * 100)
        logger.info("汇率汇总")
        logger.info("=" * 100)
        for currency, rate in rates.items():
            if rate is not None:
                logger.info(f"  {currency} -> JPY: {rate}")

        logger.info("")
        logger.info("=" * 100)
        logger.info("✓ 测试完成!")
        logger.info("=" * 100)

    except Exception as e:
        logger.error(f"测试失败: {str(e)}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
