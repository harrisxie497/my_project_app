import pymysql

def query_customs_config():
    connection = pymysql.connect(
        host='172.18.207.224',
        user='root',
        password='root123456',
        database='demo',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM field_pipelines WHERE file_type = 'CUSTOMS' ORDER BY `order`")
            records = cursor.fetchall()
            
            print("CUSTOMS 字段配置（按order排序）：")
            print("=" * 150)
            for record in records:
                print(f"列: {record['target_col']:5} | "
                      f"表头: {record['target_header']:20} | "
                      f"map_op: {record['map_op']:8} | "
                      f"source_cols: {str(record['source_cols']):30} | "
                      f"field_type: {record['field_type']:10} | "
                      f"rule_ref: {str(record['rule_ref']):40} | "
                      f"depends_on: {str(record['depends_on']):20}")
                
            print("\n\n重点查看 Q列 和 R列 的配置：")
            print("=" * 150)
            for record in records:
                if record['target_col'] in ['Q', 'R']:
                    print(f"\n列: {record['target_col']}")
                    print(f"  表头: {record['target_header']}")
                    print(f"  map_op: {record['map_op']}")
                    print(f"  source_cols: {record['source_cols']}")
                    print(f"  field_type: {record['field_type']}")
                    print(f"  rule_ref: {record['rule_ref']}")
                    print(f"  depends_on: {record['depends_on']}")
                    print(f"  rule_params_json: {record['rule_params_json']}")
                    
    except Exception as e:
        print(f"查询失败: {e}")
    finally:
        connection.close()

if __name__ == '__main__':
    query_customs_config()
