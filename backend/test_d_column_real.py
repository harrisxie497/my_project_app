"""测试D列的处理情况（使用真实数据）"""
import sys
import os
import json
from dotenv import load_dotenv

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text
from app.services.excel_reader import read_excel_file
from app.services.field_handlers import copy_equal_to

def test_d_column_processing():
    """测试D列的完整处理流程"""
    print("=" * 80)
    print("测试D列的处理情况（完整流程）")
    print("=" * 80)

    # 初始化数据库连接
    load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))
    database_url = os.getenv('DATABASE_URL')
    engine = create_engine(database_url)

    # 获取D列配置
    print("\n1. 获取D列配置")
    print("-" * 80)
    conn = engine.connect()
    result = conn.execute(text("""
        SELECT * FROM field_pipelines
        WHERE file_type = 'CUSTOMS' AND target_col = 'D'
        LIMIT 1
    """))

    row = result.fetchone()
    if not row:
        print("未找到D列配置")
        conn.close()
        return

    columns = result.keys()
    config = {col: row[i] for i, col in enumerate(columns)}
    conn.close()

    print(f"目标列: {config['target_col']} ({config['target_header']})")
    print(f"操作类型: {config['map_op']}")
    print(f"字段类型: {config['field_type']}")
    print(f"源列: {json.loads(config['source_cols'])}")
    print(f"依赖列: {json.loads(config['depends_on'])}")

    rule_ref = json.loads(config['rule_ref'])[0] if config['rule_ref'] else None
    rule_params = json.loads(config['rule_params_json'])

    print(f"规则: {rule_ref}")
    print(f"规则参数: {rule_params}")

    # 查找Excel文件
    print("\n2. 查找Excel文件")
    print("-" * 80)

    excel_files = [f for f in os.listdir('.') if f.endswith('.xlsx') and 'downloaded' in f.lower()]
    if not excel_files:
        excel_files = [f for f in os.listdir('.') if f.endswith('.xlsx') and 'test' in f.lower()]

    found_excel = False
    if excel_files:
        excel_file = excel_files[0]
        print(f"使用文件: {excel_file}")

        try:
            result = read_excel_file(excel_file)

            # 提取C列和D列的数据
            c_values = None
            d_values = None

            for col in result.get('column_data', []):
                if col.get('head') == 'C':
                    c_values = col.get('data', [])
                elif col.get('head') == 'D':
                    d_values = col.get('data', [])

            if c_values and d_values:
                found_excel = True
                print(f"C列行数: {len(c_values)}, D列行数: {len(d_values)}")

                # 构建测试数据（取前10行，跳过表头）
                test_data = []
                for i in range(1, min(11, min(len(c_values), len(d_values)))):
                    test_data.append({
                        "C": c_values[i] if i < len(c_values) else "",
                        "D": d_values[i] if i < len(d_values) else ""
                    })
        except Exception as e:
            print(f"读取Excel文件失败: {e}")

    if not found_excel:
        print("未找到合适的Excel文件，使用测试数据")
        test_data = [
            {"C": "12345", "D": "12345"},
            {"C": "67890", "D": "67890"},
            {"C": "ABCDE", "D": "ABCDE"},
            {"C": "123", "D": "456"},  # 不一致
            {"C": "XYZ", "D": "XYZ123"}  # 不一致
        ]
    else:
        excel_file = excel_files[0]
        print(f"使用文件: {excel_file}")

        result = read_excel_file(excel_file)

        # 提取C列和D列的数据
        c_values = None
        d_values = None

        for col in result.get('column_data', []):
            if col.get('head') == 'C':
                c_values = col.get('data', [])
            elif col.get('head') == 'D':
                d_values = col.get('data', [])

        if not c_values or not d_values:
            print("未找到C列或D列数据")
            return

        print(f"C列行数: {len(c_values)}, D列行数: {len(d_values)}")

        # 构建测试数据（取前10行，跳过表头）
        test_data = []
        for i in range(1, min(11, min(len(c_values), len(d_values)))):
            test_data.append({
                "C": c_values[i] if i < len(c_values) else "",
                "D": d_values[i] if i < len(d_values) else ""
            })

    # 执行处理
    print("\n3. 执行D列处理")
    print("-" * 80)
    print("输入数据 -> 输出结果")
    print("-" * 80)

    success_count = 0
    error_count = 0

    for i, data in enumerate(test_data, 1):
        c_value = data.get('C', '')
        d_value = data.get('D', '')

        print(f"\n{i}. C列: {c_value}")
        print(f"   D列: {d_value}")

        try:
            # 执行验证规则
            equal_to_col = rule_params.get(rule_ref, {}).get('equal_to_target_col', 'C')
            target_value = data.get(equal_to_col, '')

            # 复制D列的值，并验证是否与C列一致
            result = copy_equal_to(d_value, target_value)

            # 检查是否一致
            is_valid = d_value == target_value
            status = "[OK]" if is_valid else "[MISMATCH]"

            print(f"   验证结果: {result}")
            print(f"   状态: {status}")

            if is_valid:
                success_count += 1
            else:
                error_count += 1

        except Exception as e:
            print(f"   [ERROR] {str(e)}")
            error_count += 1

    # 总结
    print("\n" + "=" * 80)
    print("处理总结")
    print("=" * 80)
    print(f"总行数: {len(test_data)}")
    print(f"验证通过: {success_count}")
    print(f"验证失败: {error_count}")
    print(f"通过率: {success_count/len(test_data)*100:.1f}%")
    print("=" * 80)

if __name__ == "__main__":
    test_d_column_processing()
