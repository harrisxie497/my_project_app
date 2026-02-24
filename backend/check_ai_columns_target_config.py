import pymysql
import json

def check_ai_columns_in_target_config():
    """检查TARGET配置中AI列的定义"""
    print("=" * 100)
    print("检查TARGET配置中AI列的定义")
    print("=" * 100)
    
    try:
        connection = pymysql.connect(
            host='172.18.207.224',
            port=3306,
            user='app',
            password='app123456',
            database='demo',
            charset='utf8mb4'
        )
        cursor = connection.cursor()
        
        # 查询TARGET配置
        sql = """
        SELECT columns_json, header_row, data_start_row
        FROM file_definitions
        WHERE file_type = 'CUSTOMS' AND file_role = 'TARGET'
        """
        
        cursor.execute(sql)
        result = cursor.fetchone()
        
        if result:
            columns_json_str = result[0]
            header_row = result[1]
            data_start_row = result[2]
            
            print(f"\nTARGET配置:")
            print(f"  header_row: {header_row}")
            print(f"  data_start_row: {data_start_row}")
            
            # 解析JSON
            columns_json = json.loads(columns_json_str) if isinstance(columns_json_str, str) else columns_json_str
            
            # 查找AI列
            ai_columns = ['X', 'Y', 'J', 'K']
            
            print(f"\nAI列的定义:")
            for col_def in columns_json:
                col_letter = col_def.get('col')
                col_header = col_def.get('header')
                
                if col_letter in ai_columns:
                    print(f"\n{col_letter} ({col_header}):")
                    print(f"  col: {col_letter}")
                    print(f"  header: {col_header}")
        
        connection.close()
        
        print("\n" + "=" * 100)
        print("检查完成！")
        print("=" * 100)
        
    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_ai_columns_in_target_config()
