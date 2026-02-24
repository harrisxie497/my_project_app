"""
修改F列的rule_params_json
"""

import pymysql
import logging
import json

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def update_f_column_rule_params_json():
    """修改F列的rule_params_json"""
    print("=" * 100)
    print("修改F列的rule_params_json")
    print("=" * 100)
    
    # 数据库连接配置
    db_config = {
        'host': '172.18.207.224',
        'port': 3306,
        'user': 'app',
        'password': 'app123456',
        'database': 'demo',
        'charset': 'utf8mb4'
    }
    
    try:
        # 连接数据库
        connection = pymysql.connect(**db_config)
        cursor = connection.cursor()
        
        # 修改F列的rule_params_json
        sql = """
        UPDATE field_pipelines
        SET rule_params_json = %s
        WHERE file_type = 'CUSTOMS' AND target_col = 'F'
        """
        
        # 新的rule_params_json
        new_rule_params_json = {
            "policy_copy_one_decimal": {
                "allow_null": True
            }
        }
        
        cursor.execute(sql, (json.dumps(new_rule_params_json),))
        connection.commit()
        
        print(f"\n✅ 修改成功！")
        print(f"新的rule_params_json: {json.dumps(new_rule_params_json, ensure_ascii=False, indent=2)}")
        
        # 查询修改后的rule_params_json
        sql = """
        SELECT target_col, target_header, map_op, source_cols, field_type, rule_ref, depends_on, rule_params_json, enabled
        FROM field_pipelines
        WHERE file_type = 'CUSTOMS' AND target_col = 'F'
        """
        
        cursor.execute(sql)
        results = cursor.fetchall()
        
        print(f"\n找到 {len(results)} 条记录")
        
        for row in results:
            target_col, target_header, map_op, source_cols, field_type, rule_ref, depends_on, rule_params_json, enabled = row
            
            print(f"\n{'=' * 100}")
            print(f"target_col: {target_col}")
            print(f"target_header: {target_header}")
            print(f"map_op: {map_op}")
            print(f"source_cols: {source_cols}")
            print(f"field_type: {field_type}")
            print(f"rule_ref: {rule_ref}")
            print(f"depends_on: {depends_on}")
            print(f"rule_params_json: {rule_params_json}")
            print(f"enabled: {enabled}")
        
        # 关闭连接
        cursor.close()
        connection.close()
        
        print("\n" + "=" * 100)
        print("修改完成！")
        print("=" * 100)
        
    except Exception as e:
        print(f"\n❌ 修改失败: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    update_f_column_rule_params_json()
