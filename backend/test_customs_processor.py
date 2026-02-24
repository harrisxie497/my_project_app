import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.excel_reader import read_excel_file
from app.services.excel_writer import write_excel_file
from app.services.header_processor import process_header_row
from app.services.field_handlers import (
    copy_field,
    set_constant,
    generate_sequence,
    copy_equal_to,
    calc_invoice_price_fx_round
)
from app.services.deepseek_ai_service import DeepSeekAIService
from app.services.ai_rule_executor import AIRuleExecutor
from app.services.exchange_rate_service import ExchangeRateService
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MockExchangeRateService:
    """模拟汇率服务，用于测试"""
    
    def get_rate(self, from_currency: str, to_currency: str = "JPY") -> float:
        logger.info(f"模拟获取汇率：{from_currency} -> {to_currency}")
        
        if from_currency == "USD":
            return 150.0
        elif from_currency == "EUR":
            return 160.0
        elif from_currency == "GBP":
            return 190.0
        elif from_currency == "CNY":
            return 20.0
        else:
            return 1.0


class MockDeepSeekAIService:
    """模拟DeepSeek AI服务，用于测试"""
    
    def chat(self, prompt: str, system_prompt: str = None) -> str:
        logger.info(f"模拟DeepSeek API调用，提示词长度：{len(prompt)}")
        
        if "重量" in prompt:
            return "1.5"
        elif "品名" in prompt and "翻译" in prompt:
            return "T-SHIRT"
        elif "材质" in prompt and "翻译" in prompt:
            return "COTTON"
        elif "收件人名" in prompt and "清理" in prompt:
            return "山田太郎"
        elif "翻译" in prompt:
            return "TANAKA"
        else:
            return prompt


def create_test_data_file():
    """创建测试数据文件"""
    logger.info("创建测试数据文件")
    
    test_data = [
        ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"],
        ["1", "2", "3", "4", "5", "6", "7", "8", "9"],
        ["10", "20", "30", "40", "50", "60", "70", "80", "90", "100"]
    ]
    
    write_excel_file("test_data.xlsx", ["列A", "列B", "列C"], test_data)
    logger.info("测试数据文件创建完成")


def test_excel_reader():
    """测试Excel读取器"""
    logger.info("=" * 50)
    logger.info("测试1：Excel读取器")
    logger.info("=" * 50)
    
    try:
        result = read_excel_file("test_data.xlsx")
        
        logger.info(f"表头：{result['headers']}")
        logger.info(f"数据行数：{len(result['data'])}")
        
        if len(result['data']) > 0:
            logger.info(f"第一行数据：{result['data'][0]}")
        
        print("✅ Excel读取器测试通过")
        return True
        
    except Exception as e:
        logger.error(f"❌ Excel读取器测试失败：{str(e)}")
        return False


def test_excel_writer():
    """测试Excel写入器"""
    logger.info("=" * 50)
    logger.info("测试2：Excel写入器")
    logger.info("=" * 50)
    
    try:
        test_headers = ["A", "B", "C"]
        test_data = [
            ["1", "2", "3"],
            ["4", "5", "6"]
        ]
        
        write_excel_file("test_output.xlsx", test_headers, test_data)
        
        print("✅ Excel写入器测试通过")
        return True
        
    except Exception as e:
        logger.error(f"❌ Excel写入器测试失败：{str(e)}")
        return False


def test_header_processor():
    """测试表头处理器"""
    logger.info("=" * 50)
    logger.info("测试3：表头处理器")
    logger.info("=" * 50)
    
    try:
        from openpyxl import Workbook
        
        workbook = Workbook()
        worksheet = workbook.active
        
        header_params = {
            "mawb_no": "16003279161",
            "flight_no": "CX509",
            "arrival_date": "20251210"
        }
        
        process_header_row(worksheet, header_params)
        
        print("✅ 表头处理器测试通过")
        return True
        
    except Exception as e:
        logger.error(f"❌ 表头处理器测试失败：{str(e)}")
        return False


def test_field_handlers():
    """测试字段处理函数"""
    logger.info("=" * 50)
    logger.info("测试4：字段处理函数")
    logger.info("=" * 50)
    
    try:
        print("测试 copy_field...")
        assert copy_field("test") == "test"
        
        print("测试 set_constant...")
        assert set_constant("") == ""
        assert set_constant("test") == "test"
        
        print("测试 generate_sequence...")
        assert generate_sequence(0) == 1
        assert generate_sequence(9) == 10
        
        print("测试 copy_equal_to...")
        assert copy_equal_to("test", "test") == "test"
        assert copy_equal_to("test", "other") == "other"
        
        print("测试 calc_invoice_price_fx_round...")
        mock_exchange_service = MockExchangeRateService()
        result = calc_invoice_price_fx_round(100.0, "USD", mock_exchange_service)
        assert result == 15000
        
        print("✅ 字段处理函数测试通过")
        return True
        
    except Exception as e:
        logger.error(f"❌ 字段处理函数测试失败：{str(e)}")
        return False


def test_deepseek_ai_service():
    """测试DeepSeek AI服务"""
    logger.info("=" * 50)
    logger.info("测试5：DeepSeek AI服务")
    logger.info("=" * 50)
    
    try:
        ai_service = MockDeepSeekAIService()
        
        result = ai_service.chat("测试提示词")
        print(f"AI响应：{result}")
        
        assert result is not None
        assert isinstance(result, str)
        
        print("✅ DeepSeek AI服务测试通过")
        return True
        
    except Exception as e:
        logger.error(f"❌ DeepSeek AI服务测试失败：{str(e)}")
        return False


def test_exchange_rate_service():
    """测试汇率服务"""
    logger.info("=" * 50)
    logger.info("测试6：汇率服务")
    logger.info("=" * 50)
    
    try:
        exchange_service = MockExchangeRateService()
        
        rate = exchange_service.get_rate("USD", "JPY")
        print(f"USD -> JPY汇率：{rate}")
        assert rate == 150.0
        
        rate = exchange_service.get_rate("EUR", "JPY")
        print(f"EUR -> JPY汇率：{rate}")
        assert rate == 160.0
        
        rate = exchange_service.get_rate("GBP", "JPY")
        print(f"GBP -> JPY汇率：{rate}")
        assert rate == 190.0
        
        rate = exchange_service.get_rate("CNY", "JPY")
        print(f"CNY -> JPY汇率：{rate}")
        assert rate == 20.0
        
        print("✅ 汇率服务测试通过")
        return True
        
    except Exception as e:
        logger.error(f"❌ 汇率服务测试失败：{str(e)}")
        return False


def test_ai_rule_executor():
    """测试AI规则执行器"""
    logger.info("=" * 50)
    logger.info("测试7：AI规则执行器")
    logger.info("=" * 50)
    
    try:
        ai_service = MockDeepSeekAIService()
        executor = AIRuleExecutor(ai_service)
        
        print("测试 _handle_decimal_fix...")
        result = executor._handle_decimal_fix(
            {"F": "2.5", "H": "T恤", "I": "棉"},
            {}
        )
        print(f"结果：{result}")
        assert float(result) == 1.5
        
        print("测试 _handle_goods_en...")
        result = executor._handle_goods_en(
            {"H": "Tシャツ"},
            {}
        )
        print(f"结果：{result}")
        assert result == "T-SHIRT"
        
        print("测试 _handle_material_en...")
        result = executor._handle_material_en(
            {"I": "綿"},
            {}
        )
        print(f"结果：{result}")
        assert result == "COTTON"
        
        print("测试 _handle_text_ja_clean...")
        result = executor._handle_text_ja_clean(
            {"AD": "山田太郎様"},
            {}
        )
        print(f"结果：{result}")
        assert result == "山田太郎"
        
        print("测试 _handle_translate_upper...")
        result = executor._handle_translate_upper(
            {"target_col": "山田太郎"},
            {}
        )
        print(f"结果：{result}")
        assert result == "TANAKA"
        
        print("✅ AI规则执行器测试通过")
        return True
        
    except Exception as e:
        logger.error(f"❌ AI规则执行器测试失败：{str(e)}")
        return False


def run_all_tests():
    """运行所有测试"""
    logger.info("\n" + "=" * 50)
    logger.info("开始运行所有测试")
    logger.info("=" * 50 + "\n")
    
    tests = [
        ("Excel读取器", test_excel_reader),
        ("Excel写入器", test_excel_writer),
        ("表头处理器", test_header_processor),
        ("字段处理函数", test_field_handlers),
        ("DeepSeek AI服务", test_deepseek_ai_service),
        ("汇率服务", test_exchange_rate_service),
        ("AI规则执行器", test_ai_rule_executor),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        logger.info(f"\n运行测试：{test_name}")
        try:
            if test_func():
                passed += 1
                logger.info(f"✅ {test_name} 测试通过")
            else:
                failed += 1
                logger.error(f"❌ {test_name} 测试失败")
        except Exception as e:
            failed += 1
            logger.error(f"❌ {test_name} 测试异常：{str(e)}")
    
    logger.info("\n" + "=" * 50)
    logger.info("测试结果汇总")
    logger.info("=" * 50)
    logger.info(f"通过：{passed}/{len(tests)}")
    logger.info(f"失败：{failed}/{len(tests)}")
    logger.info(f"成功率：{passed/len(tests)*100:.2f}%")
    
    print("\n" + "=" * 50)
    print("测试结果汇总")
    print("=" * 50)
    print(f"通过：{passed}/{len(tests)}")
    print(f"失败：{failed}/{len(tests)}")
    print(f"成功率：{passed/len(tests)*100:.2f}%")
    print("=" * 50 + "\n")
    
    return passed == len(tests)


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
