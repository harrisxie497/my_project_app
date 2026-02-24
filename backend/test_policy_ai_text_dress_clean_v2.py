"""测试policy_ai_text_dress_clean（使用数据库中的完整system_prompt）"""
import sys
import os
import json
from dotenv import load_dotenv

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text
from app.services.deepseek_ai_service import DeepSeekAIService

def test_with_full_system_prompt():
    """使用完整的system_prompt测试"""

    print("=" * 80)
    print("测试 policy_ai_text_dress_clean（使用完整system_prompt）")
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
    system_prompt = schema.get('configurable_params', {}).get('system_prompt', '')
    conn.close()

    print(f"描述: {schema.get('desc')}")
    print(f"处理器: {schema.get('handler')}")
    print(f"系统提示词: {system_prompt[:200]}...")

    # 准备测试数据
    print("\n2. 准备测试数据")
    print("-" * 80)

    test_data = [
        "愛知県名古屋市中区1-2-3",
        "東京都渋谷区渋谷1-2-3",
        "大阪府大阪市中央区1-2-3"
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

    user_prompt = f"""请处理以下日本地址：

{chr(10).join(items_text)}

要求：
1. 将日本地址翻译成英文（罗马大写）
2. 顺序：都道府县 → 市/区 → 町/地区 → 丁目/番地
3. 中间不需要标点符号，可以加入空格
4. 门牌部分（如1-10-101）不能有空格，-两边都不需要有空格
5. 翻译结果需全部大写
6. 每行一个地址，按顺序对应
7. 只返回结果，不要包含其他文字、JSON格式或序号"""

    try:
        result = ai_service.chat(user_prompt, system_prompt=system_prompt)

        elapsed_time = time.time() - start_time
        print(f"处理完成！耗时: {elapsed_time:.2f}秒")

        print(f"\n原始AI响应：")
        print(result)

        # 解析结果
        lines = result.strip().split('\n')
        # 过滤掉空行和可能包含序号的行
        results = []
        for line in lines:
            line = line.strip()
            # 移除可能的JSON符号和序号
            line = line.strip('[]{}"\'')
            # 移除行号（如 "1. "）
            if '. ' in line:
                parts = line.split('. ', 1)
                if len(parts) > 1:
                    line = parts[1].strip()
            if line and not line.isdigit():
                results.append(line)

        # 确保结果数量匹配
        while len(results) < len(test_data):
            results.append('')
        results = results[:len(test_data)]

        print("\n4. 解析后的输出结果")
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
            is_upper = output_addr.isupper() if output_addr else False
            no_brackets = '(' not in output_addr and ')' not in output_addr if output_addr else False

            status = "[OK]" if output_addr and is_upper and no_brackets else "[WARN]"
            print(f"{i}. {status}")
            print(f"   输入: {input_addr}")
            print(f"   输出: {output_addr}")
            if output_addr:
                print(f"   全大写: {'是' if is_upper else '否'}")
                print(f"   无括号: {'是' if no_brackets else '否'}")
            print()

            if output_addr and is_upper and no_brackets:
                success_count += 1

        print("=" * 80)
        print(f"总结: {success_count}/{len(test_data)} 条数据翻译成功")
        print("=" * 80)

    except Exception as e:
        print(f"[ERROR] 处理失败: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_with_full_system_prompt()
