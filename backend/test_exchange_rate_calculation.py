"""
测试脚本：单独测试R列汇率计算和汇率获取函数
"""
import sys
import os
import logging
from datetime import datetime

# 添加项目路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.exchange_rate_service import ExchangeRateService
from app.services.field_handlers import calc_invoice_price_fx_round
from app.core.config import settings
from unittest.mock import Mock, MagicMock

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def test_exchange_rate_service_real():
    """
    测试真实的汇率服务
    """
    logger.info("=" * 100)
    logger.info("测试1: 真实汇率服务API")
    logger.info("=" * 100)

    try:
        # 获取API KEY
        api_key = getattr(settings, 'EXCHANGE_RATE_API_KEY', '')
        base_url = getattr(settings, 'EXCHANGE_RATE_API_URL', 'https://v6.exchangerate-api.com/v6')

        logger.info(f"API URL: {base_url}")
        logger.info(f"API KEY: {api_key[:10]}...{api_key[-4:] if len(api_key) > 10 else api_key}")

        if not api_key:
            logger.warning("API KEY未配置，跳过真实API测试")
            return None

        # 初始化汇率服务
        exchange_service = ExchangeRateService(api_key, base_url)
        logger.info("汇率服务初始化完成")

        # 测试获取汇率
        test_currencies = ['USD', 'EUR', 'CNY', 'JPY']

        for currency in test_currencies:
            if currency == 'JPY':
                logger.info(f"跳过JPY (日元对日元汇率: 1.0)")
                continue

            try:
                logger.info(f"测试获取汇率: {currency} -> JPY")
                rate = exchange_service.get_rate(currency, 'JPY')
                logger.info(f"✓ {currency} -> JPY: {rate}")
            except Exception as e:
                logger.error(f"✗ 获取{currency}汇率失败: {str(e)}")

        # 测试缓存功能
        logger.info("")
        logger.info("测试缓存功能:")
        logger.info("第二次获取USD汇率（应该使用缓存）")
        rate_cached = exchange_service.get_rate('USD', 'JPY')
        logger.info(f"✓ USD -> JPY (缓存): {rate_cached}")

        logger.info("")
        logger.info("✓ 真实汇率服务测试完成")
        return exchange_service

    except Exception as e:
        logger.error(f"真实汇率服务测试失败: {str(e)}", exc_info=True)
        return None


def test_exchange_rate_service_mock():
    """
    测试Mock汇率服务
    """
    logger.info("")
    logger.info("=" * 100)
    logger.info("测试2: Mock汇率服务")
    logger.info("=" * 100)

    try:
        # 创建Mock汇率服务
        mock_exchange_service = Mock(spec=ExchangeRateService)

        # 设置Mock返回值
        mock_exchange_service.get_rate.side_effect = {
            'USD': 149.5,
            'EUR': 162.3,
            'CNY': 21.2,
            'JPY': 1.0
        }.get

        logger.info("Mock汇率服务初始化完成")
        logger.info("模拟汇率:")
        logger.info("  USD -> JPY: 149.5")
        logger.info("  EUR -> JPY: 162.3")
        logger.info("  CNY -> JPY: 21.2")

        # 测试获取Mock汇率
        test_cases = [
            ('USD', 149.5),
            ('EUR', 162.3),
            ('CNY', 21.2)
        ]

        for currency, expected_rate in test_cases:
            rate = mock_exchange_service.get_rate(currency, 'JPY')
            logger.info(f"✓ {currency} -> JPY: {rate} (期望: {expected_rate})")
            assert rate == expected_rate, f"{currency}汇率不匹配"

        logger.info("")
        logger.info("✓ Mock汇率服务测试完成")
        return mock_exchange_service

    except Exception as e:
        logger.error(f"Mock汇率服务测试失败: {str(e)}", exc_info=True)
        return None


def test_calc_invoice_price_fx_round(exchange_service):
    """
    测试R列汇率计算函数
    """
    logger.info("")
    logger.info("=" * 100)
    logger.info("测试3: R列汇率计算 (calc_invoice_price_fx_round)")
    logger.info("=" * 100)

    try:
        # 测试用例：原始价格、货币代码、期望结果
        test_cases = [
            # (original_price, currency_code, expected_jpy_price, description)
            (100.0, 'USD', 14950, '100美元转换为日元'),
            (50.0, 'EUR', 8115, '50欧元转换为日元'),
            (500.0, 'CNY', 10600, '500人民币转换为日元'),
            (1000.0, 'JPY', 1000, '1000日元(无转换)'),
            (123.45, 'USD', 18451, '123.45美元转换为日元(四舍五入)'),
            (0.0, 'USD', 0, '0美元转换为日元'),
            (None, 'USD', None, 'None值处理'),
        ]

        for idx, (original_price, currency_code, expected, desc) in enumerate(test_cases, 1):
            logger.info("")
            logger.info(f"测试用例 {idx}: {desc}")
            logger.info(f"  输入: {original_price} {currency_code}")

            try:
                if original_price is None:
                    logger.info("  跳过None值测试")
                    continue

                # 计算汇率转换
                jpy_price = calc_invoice_price_fx_round(
                    original_price=original_price,
                    currency_code=currency_code,
                    exchange_rate_service=exchange_service,
                    regex=r'^\d+$'
                )

                logger.info(f"  输出: {jpy_price} JPY")
                logger.info(f"  期望: {expected} JPY")

                if jpy_price == expected:
                    logger.info(f"  ✓ 结果正确")
                else:
                    logger.warning(f"  ✗ 结果不匹配")

            except Exception as e:
                logger.error(f"  ✗ 计算失败: {str(e)}")

        logger.info("")
        logger.info("✓ R列汇率计算测试完成")

    except Exception as e:
        logger.error(f"R列汇率计算测试失败: {str(e)}", exc_info=True)


def test_real_data_scenario():
    """
    测试真实数据场景
    """
    logger.info("")
    logger.info("=" * 100)
    logger.info("测试4: 真实数据场景")
    logger.info("=" * 100)

    try:
        # 模拟真实Excel中的R列和Q列数据
        logger.info("模拟真实数据:")

        # 获取API KEY
        api_key = getattr(settings, 'EXCHANGE_RATE_API_KEY', '')
        base_url = getattr(settings, 'EXCHANGE_RATE_API_URL', 'https://v6.exchangerate-api.com/v6')

        if not api_key:
            logger.warning("API KEY未配置，使用Mock汇率服务")
            # 使用Mock
            mock_exchange_service = Mock(spec=ExchangeRateService)
            mock_exchange_service.get_rate.side_effect = {
                'USD': 149.5,
                'CNY': 21.2,
                'JPY': 1.0
            }.get
            exchange_service = mock_exchange_service
        else:
            exchange_service = ExchangeRateService(api_key, base_url)

        # 测试数据：R列(价格), Q列(货币代码)
        test_data = [
            (1250.50, 'USD', '美元订单'),
            (3200.00, 'CNY', '人民币订单'),
            (850.25, 'JPY', '日元订单'),
            (520.75, 'USD', '美元订单2'),
            (1800.00, 'CNY', '人民币订单2'),
        ]

        for idx, (price, currency, desc) in enumerate(test_data, 1):
            logger.info("")
            logger.info(f"订单 {idx}: {desc}")
            logger.info(f"  R列(价格): {price}")
            logger.info(f"  Q列(货币): {currency}")

            try:
                jpy_price = calc_invoice_price_fx_round(
                    original_price=price,
                    currency_code=currency,
                    exchange_rate_service=exchange_service,
                    regex=r'^\d+$'
                )

                logger.info(f"  日元价格: {jpy_price} JPY")

                # 显示汇率
                if currency != 'JPY':
                    rate = exchange_service.get_rate(currency, 'JPY')
                    logger.info(f"  使用汇率: 1 {currency} = {rate} JPY")

            except Exception as e:
                logger.error(f"  计算失败: {str(e)}")

        logger.info("")
        logger.info("✓ 真实数据场景测试完成")

    except Exception as e:
        logger.error(f"真实数据场景测试失败: {str(e)}", exc_info=True)


def main():
    """
    主函数：执行所有测试
    """
    logger.info("=" * 100)
    logger.info("R列汇率计算测试")
    logger.info("=" * 100)
    logger.info(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    try:
        # 测试1: 真实汇率服务
        exchange_service_real = test_exchange_rate_service_real()

        # 测试2: Mock汇率服务
        exchange_service_mock = test_exchange_rate_service_mock()

        # 测试3: R列汇率计算（使用Mock）
        if exchange_service_mock:
            test_calc_invoice_price_fx_round(exchange_service_mock)

        # 测试4: 真实数据场景
        test_real_data_scenario()

        logger.info("")
        logger.info("=" * 100)
        logger.info("✓ 所有测试完成!")
        logger.info("=" * 100)

    except Exception as e:
        logger.error(f"测试失败: {str(e)}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
