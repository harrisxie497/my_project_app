"""测试D列的处理情况"""
import sys
import os
import json
from dotenv import load_dotenv

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text

def get_field_config(engine, file_type, target_col):
    """获取指定字段的配置"""
    conn = engine.connect()
    result = conn.execute(text("""
        SELECT *
        FROM field_pipelines
        WHERE file_type = :file_type
          AND target_col = :target_col
        LIMIT 1
    """), {"file_type": file_type, "target_col": target_col})

    row = result.fetchone()
    if not row:
        conn.close()
        return None

    columns = result.keys()
    config = {col: row[i] for i, col in enumerate(columns)}

    # 解析JSON字段
    for json_field in ['source_cols', 'rule_ref', 'rule_params_json', 'depends_on']:
        if config.get(json_field):
            try:
                config[json_field + '_parsed'] = json.loads(config[json_field])
            except:
                config[json_field + '_parsed'] = None

    conn.close()
    return config

def test_d_column():
    """测试D列处理"""
    print("=" * 80)
    print("测试D列的处理情况")
    print("=" * 80)

    # 初始化数据库连接
    load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))
    database_url = os.getenv('DATABASE_URL')
    engine = create_engine(database_url)

    # 获取D列配置
    print("\n1. 获取D列配置")
    print("-" * 80)
    config = get_field_config(engine, 'CUSTOMS', 'D')

    if not config:
        print("未找到D列的配置")
        return

    print("D列完整配置：")
    for key, value in config.items():
        if '_parsed' in key:
            continue
        print(f"  {key:25} = {value}")

    print("\n解析后的JSON字段：")
    print(f"  source_cols_parsed     = {config.get('source_cols_parsed')}")
    print(f"  rule_ref_parsed        = {config.get('rule_ref_parsed')}")
    print(f"  depends_on_parsed     = {config.get('depends_on_parsed')}")
    print(f"  rule_params_json_parsed= {config.get('rule_params_json_parsed')}")

    # 获取规则定义
    if config.get('rule_ref_parsed'):
        rule_ref = config['rule_ref_parsed'][0] if config['rule_ref_parsed'] else None
        print("\n2. 获取规则定义")
        print("-" * 80)

        conn = engine.connect()
        result = conn.execute(text("""
            SELECT * FROM rule_definitions
            WHERE rule_ref = :rule_ref
        """), {"rule_ref": rule_ref})

        row = result.fetchone()
        if row:
            columns = result.keys()
            rule_config = {col: row[i] for i, col in enumerate(columns)}

            print(f"规则引用: {rule_config.get('rule_ref')}")
            print(f"规则类型: {rule_config.get('rule_type')}")
            print(f"执行器类型: {rule_config.get('executor_type')}")
            print(f"是否启用: {rule_config.get('enabled')}")

            schema_json = rule_config.get('schema_json')
            if schema_json:
                try:
                    schema = json.loads(schema_json)
                    print(f"\nSchema配置：")
                    print(f"  描述: {schema.get('desc')}")
                    print(f"  处理器: {schema.get('handler')}")
                    print(f"  可配置参数: {json.dumps(schema.get('configurable_params', {}), indent=4, ensure_ascii=False)}")
                except Exception as e:
                    print(f"  解析schema_json失败: {e}")

        conn.close()

    # 准备测试数据
    print("\n3. 准备测试数据")
    print("-" * 80)

    # 先读取真实的Excel文件，看看D列的实际数据
    from app.services.excel_reader import read_excel_file

    excel_file = "downloaded_original_t_cabb44e4.xlsx"
    if os.path.exists(excel_file):
        result = read_excel_file(excel_file)

        # 从column_data中查找D列和C列
        d_values = None
        c_values = None

        for col in result.get('column_data', []):
            if col.get('head') == 'D':
                d_values = col.get('data', [])
            elif col.get('head') == 'C':
                c_values = col.get('data', [])

        if d_values:
            print(f"D列数据行数: {len(d_values)}")
            print(f"\nD列前10行数据（跳过表头）：")
            for i in range(1, min(11, len(d_values))):
                value = d_values[i] if i < len(d_values) else ""
                print(f"  {i}: {value}")

            if c_values:
                print(f"\nC列数据行数: {len(c_values)}")
                print(f"\nC列前10行数据（跳过表头）：")
                for i in range(1, min(11, len(c_values))):
                    value = c_values[i] if i < len(c_values) else ""
                    print(f"  {i}: {value}")

                # 验证D列和C列是否一致
                print(f"\n验证D列与C列的一致性（前10行）：")
                for i in range(1, min(11, min(len(d_values), len(c_values)))):
                    d_val = d_values[i] if i < len(d_values) else ""
                    c_val = c_values[i] if i < len(c_values) else ""
                    is_match = d_val == c_val
                    status = "[OK]" if is_match else "[MISMATCH]"
                    print(f"  {i}: D={d_val}, C={c_val} {status}")
        else:
            print("未找到D列")

        # 查找D列
        d_col_index = None
        for col_name, col_idx in header.items():
            if col_name == 'D':
                d_col_index = col_idx
                break

        if d_col_index is not None:
            print(f"D列索引: {d_col_index}")
            print(f"\nD列前10行数据（跳过表头）：")
            for i in range(1, min(11, len(data))):
                value = data[i][d_col_index] if d_col_index < len(data[i]) else ""
                print(f"  {i}: {value}")
        else:
            print("未找到D列")
    else:
        print(f"Excel文件不存在: {excel_file}")
        print("\n使用模拟数据：")
        test_values = [
            "12345",
            "67890",
            "ABCDE12345",
            "123-456-789",
            "ABC DEF"
        ]
        for i, value in enumerate(test_values, 1):
            print(f"  {i}: {value}")

    print("\n" + "=" * 80)
    print("测试完成")
    print("=" * 80)

if __name__ == "__main__":
    test_d_column()
