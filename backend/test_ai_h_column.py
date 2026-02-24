"""测试AI处理H列（英文品名清理）"""
import sys
import os
import time

# 添加backend目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.services.deepseek_ai_service import DeepSeekAIService
from app.services.ai_rule_executor import AIRuleExecutor

def test_h_column_cleaning():
    """测试H列英文品名清理"""
    print("=" * 70)
    print("测试AI处理H列（英文品名清理）")
    print("=" * 70)

    # 从环境变量获取API Key
    from dotenv import load_dotenv
    load_dotenv()
    api_key = os.getenv('DEEPSEEK_API_KEY')

    if not api_key:
        print("[ERROR] 未找到DEEPSEEK_API_KEY环境变量")
        return

    print(f"\n使用API Key: {api_key[:20]}...")

    # 初始化AI服务和规则执行器
    ai_service = DeepSeekAIService(api_key=api_key)
    executor = AIRuleExecutor(ai_service=ai_service)

    # 测试数据：模拟Excel H列的英文品名
    test_data = [
        {"H": "AIRPLANE TOY (L码)"},
        {"H": "cotton t-shirt"},
        {"H": "T-SHIRT (XL) blue"},
        {"H": "polyster pants (M)"},
        {"H": "SHOES (Size 42)"},
        {"H": "BAG - LEATHER"},
        {"H": "watch (black) plastic"},
        {"H": "socks cotton (white)"},
        {"H": "DRESS (L) - floral"},
        {"H": "hat baseball cap (red)"}
    ]

    print(f"\n输入数据（{len(test_data)}条）：")
    for i, item in enumerate(test_data, 1):
        print(f"{i}. {item['H']}")

    # 测试批量处理（一列只调用一次API）
    print("\n" + "=" * 70)
    print("批量处理测试（一列只调用一次API）")
    print("=" * 70)

    start_time = time.time()

    try:
        results = executor.execute_batch(
            rule_ref='policy_ai_goods_en_clean',
            input_data_list=test_data,
            rule_params={}
        )

        elapsed_time = time.time() - start_time

        print(f"\n处理完成！耗时：{elapsed_time:.2f}秒")
        print("\n输出结果：")
        print("-" * 70)

        for i, (input_item, result) in enumerate(zip(test_data, results), 1):
            original = input_item['H']
            cleaned = result if result else "[ERROR]"
            print(f"{i}. 输入: {original}")
            print(f"   输出: {cleaned}")
            print()

        # 验证结果
        print("=" * 70)
        print("验证结果")
        print("=" * 70)

        success_count = 0
        for i, (input_item, result) in enumerate(zip(test_data, results), 1):
            original = input_item['H']
            if result and result != '':
                # 检查是否转大写
                is_upper = result.isupper()
                # 检查是否删除了括号内容
                has_brackets = '(' in result or ')' in result

                status = "[OK]" if is_upper and not has_brackets else "[WARN]"
                print(f"{i}. {status}")
                print(f"   输入: {original}")
                print(f"   输出: {result}")
                print(f"   大写: {'是' if is_upper else '否'}")
                print(f"   无括号: {'是' if not has_brackets else '否'}")
                print()

                if is_upper and not has_brackets:
                    success_count += 1

        print("=" * 70)
        print(f"总结: {success_count}/{len(test_data)} 条数据清理成功")
        print("=" * 70)

    except Exception as e:
        print(f"\n[ERROR] 批量处理失败: {str(e)}")
        import traceback
        traceback.print_exc()

def test_single_item():
    """测试单条数据处理"""
    print("\n\n" + "=" * 70)
    print("单条数据处理测试")
    print("=" * 70)

    # 从环境变量获取API Key
    from dotenv import load_dotenv
    load_dotenv()
    api_key = os.getenv('DEEPSEEK_API_KEY')

    ai_service = DeepSeekAIService(api_key=api_key)
    executor = AIRuleExecutor(ai_service=ai_service)

    test_item = {"H": "AIRPLANE TOY (L码)"}

    print(f"\n输入: {test_item['H']}")

    try:
        result = executor.execute(
            rule_ref='policy_ai_goods_en_clean',
            input_data=test_item,
            rule_params={}
        )

        print(f"输出: {result}")

    except Exception as e:
        print(f"[ERROR] 处理失败: {str(e)}")

if __name__ == "__main__":
    test_h_column_cleaning()
    test_single_item()
