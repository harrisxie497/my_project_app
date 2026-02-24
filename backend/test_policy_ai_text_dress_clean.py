"""测试policy_ai_text_dress_clean的处理功能"""
import sys
import os
import json
from dotenv import load_dotenv

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text
from app.services.deepseek_ai_service import DeepSeekAIService

def get_rule_config(engine, rule_ref):
    """获取规则配置"""
    conn = engine.connect()
    result = conn.execute(text("""
        SELECT schema_json
        FROM rule_definitions
        WHERE rule_ref = :rule_ref
    """), {"rule_ref": rule_ref})

    row = result.fetchone()
    if not row:
        conn.close()
        return None

    schema = json.loads(row[0])
    conn.close()

    return {
        'desc': schema.get('desc'),
        'handler': schema.get('handler'),
        'system_prompt': schema.get('configurable_params', {}).get('system_prompt')
    }

def test_policy_ai_text_dress_clean():
    """测试policy_ai_text_dress_clean"""

    print("=" * 80)
    print("测试 policy_ai_text_dress_clean 处理")
    print("=" * 80)

    # 初始化数据库连接
    load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))
    database_url = os.getenv('DATABASE_URL')
    engine = create_engine(database_url)

    # 初始化AI服务
    api_key = os.getenv('DEEPSEEK_API_KEY')
    ai_service = DeepSeekAIService(api_key=api_key)

    # 获取规则配置
    print("\n1. 获取规则配置")
    print("-" * 80)
    rule_config = get_rule_config(engine, 'policy_ai_text_dress_clean')

    if not rule_config:
        print("未找到规则配置")
        return

    print(f"描述: {rule_config.get('desc')}")
    print(f"处理器: {rule_config.get('handler')}")
    print(f"系统提示词: {rule_config.get('system_prompt')}")

    # 准备测试数据
    print("\n2. 准备测试数据")
    print("-" * 80)

    test_data = [
        "東京都渋谷区渋谷1-2-3（郵便局前）",
        "大阪府大阪市中央区1-2-3（2階）",
        "愛知県名古屋市中区1-2-3（ビル名）",
        "福岡県福岡市博多区1-2-3（電話番号あり）"
    ]

    print("测试数据：")
    for i, address in enumerate(test_data, 1):
        print(f"  {i}. {address}")

    # 执行处理
    print("\n3. 执行AI处理")
    print("-" * 80)

    import time
    start_time = time.time()

    # 构建输入文本
    items_text = []
    for idx, address in enumerate(test_data):
        items_text.append(f"{idx+1}. {address}")

    user_prompt = f"""{rule_config.get('desc', '')}

{chr(10).join(items_text)}

要求：
1. 输入的数组顺序保持不变
2. 去除括号内非地址部分（如"邮编备注"、"楼层备注"等）
3. 保留清晰的地址信息
4. 每行一个结果，按顺序对应
5. 只返回结果，不要包含其他文字"""

    try:
        result = ai_service.chat(user_prompt, system_prompt=rule_config.get('system_prompt'))

        elapsed_time = time.time() - start_time
        print(f"处理完成！耗时: {elapsed_time:.2f}秒")

        # 解析结果
        lines = result.strip().split('\n')
        results = [line.strip() for line in lines if line.strip()]

        print("\n4. 输出结果")
        print("-" * 80)

        for i, (input_addr, output_addr) in enumerate(zip(test_data, results), 1):
            print(f"{i}. 输入: {input_addr}")
            print(f"   输出: {output_addr}")
            print()

        # 验证结果
        print("=" * 80)
        print("验证结果")
        print("=" * 80)

        success_count = 0
        for i, (input_addr, output_addr) in enumerate(zip(test_data, results), 1):
            has_brackets = '(' in output_addr or ')' in output_addr or '（' in output_addr or '）' in output_addr

            status = "[OK]" if not has_brackets else "[WARN]"
            print(f"{i}. {status}")
            print(f"   输入: {input_addr}")
            print(f"   输出: {output_addr}")
            print(f"   无括号: {'是' if not has_brackets else '否'}")
            print()

            if not has_brackets:
                success_count += 1

        print("=" * 80)
        print(f"总结: {success_count}/{len(test_data)} 条数据清理成功")
        print("=" * 80)

    except Exception as e:
        print(f"[ERROR] 处理失败: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_policy_ai_text_dress_clean()
