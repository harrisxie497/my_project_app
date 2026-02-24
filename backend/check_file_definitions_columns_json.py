"""
检查file_definitions表中的columns_json配置
"""

import pymysql
import json

def check_file_definitions_columns_json():
    """检查file_definitions表中的columns_json配置"""
    print("=" * 100)
    print("检查file_definitions表中的columns_json配置")
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
        
        # 查询file_definitions配置
        sql = """
        SELECT file_type, file_role, columns_json
        FROM file_definitions
        WHERE file_type = 'CUSTOMS' AND file_role = 'OUTPUT'
        """
        
        cursor.execute(sql)
        results = cursor.fetchall()
        
        print(f"\n找到 {len(results)} 个file_definitions配置:\n")
        
        for result in results:
            file_type, file_role, columns_json = result
            
            print(f"文件类型: {file_type}")
            print(f"文件角色: {file_role}")
            
            # 解析columns_json
            if columns_json:
                columns = json.loads(columns_json)
                print(f"\nColumns JSON:")
                print(json.dumps(columns, indent=2, ensure_ascii=False))
            print()
        
        connection.close()
        
        print("=" * 100)
        print("检查完成！")
        print("=" * 100)
        
    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_file_definitions_columns_json()
