"""测试汇率服务"""
import sys
import os

# 添加backend目录到路径
backend_path = os.path.join(os.path.dirname(__file__), 'app')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.services.exchange_rate_service import ExchangeRateService

def main():
    """测试汇率服务"""
    print("=" * 60)
    print("测试汇率服务 (ExchangeRateService)")
    print("=" * 60)

    # 使用用户提供的API Key
    api_key = "c06e7281b839d210bd636db0"

    # 初始化汇率服务
    service = ExchangeRateService(api_key=api_key)

    # 测试1: USD -> JPY
    print("\n1. 测试 USD -> JPY")
    try:
        rate = service.get_rate("USD", "JPY")
        print(f"   [OK] 成功获取汇率: 1 USD = {rate} JPY")
        print(f"   计算示例: 100 USD = {100 * rate:.2f} JPY")
    except Exception as e:
        print(f"   [FAIL] 失败: {str(e)}")

    # 测试2: EUR -> JPY
    print("\n2. 测试 EUR -> JPY")
    try:
        rate = service.get_rate("EUR", "JPY")
        print(f"   [OK] 成功获取汇率: 1 EUR = {rate} JPY")
        print(f"   计算示例: 100 EUR = {100 * rate:.2f} JPY")
    except Exception as e:
        print(f"   [FAIL] 失败: {str(e)}")

    # 测试3: CNY -> JPY
    print("\n3. 测试 CNY -> JPY")
    try:
        rate = service.get_rate("CNY", "JPY")
        print(f"   [OK] 成功获取汇率: 1 CNY = {rate} JPY")
        print(f"   计算示例: 100 CNY = {100 * rate:.2f} JPY")
    except Exception as e:
        print(f"   [FAIL] 失败: {str(e)}")

    # 测试4: 缓存机制
    print("\n4. 测试缓存机制")
    try:
        import time
        print("   第一次调用 USD -> JPY...")
        rate1 = service.get_rate("USD", "JPY")
        print(f"   汇率: {rate1}")

        print("   第二次调用（应使用缓存）...")
        rate2 = service.get_rate("USD", "JPY")
        print(f"   汇率: {rate2}")

        if rate1 == rate2:
            print("   [OK] 缓存机制正常工作")
        else:
            print("   [WARN] 两次获取的汇率不同")
    except Exception as e:
        print(f"   [FAIL] 失败: {str(e)}")

    # 测试5: 汇率转换示例
    print("\n5. 汇率转换示例（模拟Excel中的R列计算）")
    try:
        # 假设R列值为100 USD
        amount_usd = 100.0
        rate = service.get_rate("USD", "JPY")
        amount_jpy = round(amount_usd * rate, 2)
        print(f"   {amount_usd} USD × {rate} = {amount_jpy} JPY")

        amount_eur = 50.0
        rate = service.get_rate("EUR", "JPY")
        amount_jpy = round(amount_eur * rate, 2)
        print(f"   {amount_eur} EUR × {rate} = {amount_jpy} JPY")

        amount_cny = 200.0
        rate = service.get_rate("CNY", "JPY")
        amount_jpy = round(amount_cny * rate, 2)
        print(f"   {amount_cny} CNY × {rate} = {amount_jpy} JPY")
    except Exception as e:
        print(f"   [FAIL] 失败: {str(e)}")

    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)

if __name__ == "__main__":
    main()
