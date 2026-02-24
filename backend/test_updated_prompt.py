"""测试更新后的系统提示词"""
import sys
import os
import json
from dotenv import load_dotenv

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text
from app.services.deepseek_ai_service import DeepSeekAIService

def test_updated_prompt():
    """测试更新后的提示词"""

    print("=" * 80)
    print("测试更新后的 policy_ai_text_dress_clean")
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
        SELECT schema_json, updated_at
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

    print(f"更新时间: {row[1]}")
    print(f"系统提示词长度: {len(system_prompt)} 字符")

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

    user_prompt = f"""请将以下日本地址翻译成英文（罗马大写）：

{chr(10).join(items_text)}"""

    try:
        result = ai_service.chat(user_prompt, system_prompt=system_prompt)

        elapsed_time = time.time() - start_time
        print(f"处理完成！耗时: {elapsed_time:.2f}秒")

        print(f"\n原始AI响应：")
        print(result)
        print()

        # 解析结果
        lines = result.strip().split('\n')
        results = []
        for line in lines:
            line = line.strip()
            # 移除可能的JSON符号和序号
            line = line.strip('[]{}"\'')
            # 移除行号（如 "1. "）
            if '. ' in line and len(line.split('. ', 1)) > 1:
                parts = line.split('. ', 1)
                if len(parts) > 1:
                    line = parts[1].strip()
            if line and not line.isdigit():
                results.append(line)

        # 确保结果数量匹配
        while len(results) < len(test_data):
            results.append('')
        results = results[:len(test_data)]

        print("4. 解析后的输出结果")
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
        accuracy_issues = []

        for i, (input_addr, output_addr) in enumerate(zip(test_data, results), 1):
            is_upper = output_addr.isupper() if output_addr else False
            no_brackets = '(' not in output_addr and ')' not in output_addr if output_addr else False
            # 检查是否包含关键地址层级（如KEN、SHI、KU）
            has_all_levels = True
            if i == 1:  # 愛知県名古屋市中区
                has_all_levels = 'KEN' in output_addr and 'SHI' in output_addr and 'KU' in output_addr
            elif i == 2:  # 東京都渋谷区渋谷
                has_all_levels = 'TO' in output_addr and 'KU' in output_addr
            elif i == 3:  # 大阪府大阪市中央区
                has_all_levels = 'FU' in output_addr and 'SHI' in output_addr and 'KU' in output_addr

            status = "[OK]" if output_addr and is_upper and no_brackets and has_all_levels else "[WARN]"
            print(f"{i}. {status}")
            print(f"   输入: {input_addr}")
            print(f"   输出: {output_addr}")
            if output_addr:
                print(f"   全大写: {'是' if is_upper else '否'}")
                print(f"   无括号: {'是' if no_brackets else '否'}")
                print(f"   层级完整: {'是' if has_all_levels else '否'}")

                if not has_all_levels:
                    accuracy_issues.append(f"第{i}行: 缺少地址层级")
            print()

            if output_addr and is_upper and no_brackets and has_all_levels:
                success_count += 1

        print("=" * 80)
        print(f"总结: {success_count}/{len(test_data)} 条数据翻译成功")
        if accuracy_issues:
            print("\n准确性问题:")
            for issue in accuracy_issues:
                print(f"  - {issue}")
        print("=" * 80)

    except Exception as e:
        print(f"[ERROR] 处理失败: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_updated_prompt()
