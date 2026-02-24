"""
检查缺失的6个列的field_pipelines配置
"""

import pymysql
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def check_missing_columns():
    """检查缺失的6个列的field_pipelines配置"""
    print("=" * 100)
    print("检查缺失的6个列的field_pipelines配置")
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
        
        # 缺失的6个列
        missing_columns = [
            '收件人名（删）',
            '英文邮编录入(删)',
            '收件人地址(删)2',
            '輸入者住所（删）',
            '提取门牌(删)',
            '单价（删）'
        ]
        
        print(f"\n检查 {len(missing_columns)} 个缺失的列")
        
        for col_name in missing_columns:
            print(f"\n{'=' * 100}")
            print(f"列名: {col_name}")
            
            # 查询这个列的field_pipelines配置
            sql = """
            SELECT target_col, map_op, source_cols, field_type, rule_ref, depends_on, enabled
            FROM field_pipelines
            WHERE file_type = 'CUSTOMS'
              AND target_col = %s
            """
            
            cursor.execute(sql, (col_name,))
            results = cursor.fetchall()
            
            if results:
                for row in results:
                    target_col, map_op, source_cols, field_type, rule_ref, depends_on, enabled = row
                    
                    print(f"  target_col: {target_col}")
                    print(f"  map_op: {map_op}")
                    print(f"  source_cols: {source_cols}")
                    print(f"  field_type: {field_type}")
                    print(f"  rule_ref: {rule_ref}")
                    print(f"  depends_on: {depends_on}")
                    print(f"  enabled: {enabled}")
                    
                    if map_op not in ['NONE', 'DROP']:
                        print(f"  ⚠️ 警告：这个列没有被DROP！map_op = {map_op}")
            else:
                print(f"  ⚠️ 警告：没有找到这个列的field_pipelines配置")
        
        # 关闭连接
        cursor.close()
        connection.close()
        
        print("\n" + "=" * 100)
        print("检查完成！")
        print("=" * 100)
        
    except Exception as e:
        print(f"\n❌ 检查失败: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    check_missing_columns()
