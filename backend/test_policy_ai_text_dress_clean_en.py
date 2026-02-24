"""测试policy_ai_text_dress_clean（翻译日本地址为英文）"""
import sys
import os
import json
from dotenv import load_dotenv

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text
from app.services.deepseek_ai_service import DeepSeekAIService

def test_address_translation():
    """测试日本地址翻译为英文"""

    print("=" * 80)
    print("测试 policy_ai_text_dress_clean（日本地址翻译为英文）")
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

    conn = engine.connect()
    result = conn.execute(text("""
        SELECT schema_json
        FROM rule_definitions
        WHERE rule_ref = 'policy_ai_text_dress_clean'
    """))

    row = result.fetchone()
    if not row:
        print("未找到规则配置")
        conn.close()
        return

    schema = json.loads(row[0])
    conn.close()

    print(f"描述: {schema.get('desc')}")
    print(f"处理器: {schema.get('handler')}")

    system_prompt = schema.get('configurable_params', {}).get('system_prompt', '')
    print(f"系统提示词长度: {len(system_prompt)} 字符")

    # 准备测试数据
    print("\n2. 准备测试数据")
    print("-" * 80)

    test_data = [
        "東京都渋谷区渋谷1-2-3",
        "愛知県名古屋市中区1-2-3",
        "大阪府大阪市中央区1-2-3",
        "福岡県福岡市博多区1-2-3"
    ]

    print("测试数据：")
    for i, address in enumerate(test_data, 1):
        print(f"  {i}. {address}")

    # 执行处理
    print("\n3. 执行AI处理（翻译为英文）")
    print("-" * 80)

    import time
    start_time = time.time()

    # 构建输入文本
    items_text = []
    for idx, address in enumerate(test_data):
        items_text.append(f"{idx+1}. {address}")

    user_prompt = f"""{schema.get('desc', '')}

{chr(10).join(items_text)}

要求：
1. 将日本地址翻译成英文（罗马大写）
2. 顺序：都道府县 → 市/区 → 町/地区 → 丁目/番地
3. 中间不需要标点符号，可以加入空格
4. 门牌部分（如1-10-101）不能有空格，-两边都不需要有空格
5. 翻译结果需全部大写
6. 只返回结果，不要包含其他文字"""

    try:
        result = ai_service.chat(user_prompt, system_prompt=system_prompt)

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
            is_upper = output_addr.isupper()
            no_brackets = '(' not in output_addr and ')' not in output_addr
            # 检查是否是英文（罗马字母）
            is_roman = all(c.upper() in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 -' for c in output_addr.replace(' ', ''))

            status = "[OK]" if is_upper and no_brackets and is_roman else "[WARN]"
            print(f"{i}. {status}")
            print(f"   输入: {input_addr}")
            print(f"   输出: {output_addr}")
            print(f"   全大写: {'是' if is_upper else '否'}")
            print(f"   无括号: {'是' if no_brackets else '否'}")
            print(f"   罗马字母: {'是' if is_roman else '否'}")
            print()

            if is_upper and no_brackets and is_roman:
                success_count += 1

        print("=" * 80)
        print(f"总结: {success_count}/{len(test_data)} 条数据翻译成功")
        print("=" * 80)

    except Exception as e:
        print(f"[ERROR] 处理失败: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_address_translation()
