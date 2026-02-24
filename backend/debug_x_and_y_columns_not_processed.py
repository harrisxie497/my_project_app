"""
调试为什么X列和Y列没有被处理
"""

from app.services.excel_reader import read_excel_file
import pymysql
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def debug_x_and_y_columns_not_processed():
    """调试为什么X列和Y列没有被处理"""
    print("=" * 100)
    print("调试为什么X列和Y列没有被处理")
    print("=" * 100)
    
    # 原始文件路径
    original_file_path = r'C:\Users\harris.xie\Documents\trae_projects\japan\backend\storage\tasks\t_aa9d170a\original.xlsx'
    
    # 文件类型
    file_type = 'CUSTOMS'
    
    # 读取Excel文件
    print(f"\n读取Excel文件...")
    result = read_excel_file(
        original_file_path,
        sheet_name=None,
        file_type=file_type,
        file_role='SOURCE'
    )
    
    column_data = result["column_data"]
    data_row_count = result["data_row_count"]
    
    print(f"\n数据行数: {data_row_count}")
    print(f"列数: {len(column_data)}")
    
    # 查询X列和Y列的field_pipelines配置
    print(f"\n查询X列和Y列的field_pipelines配置...")
    connection = pymysql.connect(
        host='172.18.207.224',
        port=3306,
        user='app',
        password='app123456',
        database='demo',
        charset='utf8mb4'
    )
    try:
        with connection.cursor() as cursor:
            sql = """
            SELECT target_col, target_header, map_op, field_type, rule_ref, source_cols, depends_on, enabled
            FROM field_pipelines
            WHERE file_type = 'CUSTOMS' AND target_col IN ('X', 'Y')
            ORDER BY target_col
            """
            cursor.execute(sql)
            results = cursor.fetchall()
            
            print(f"\n找到 {len(results)} 个AI列:\n")
            
            for result in results:
                target_col, target_header, map_op, field_type, rule_ref, source_cols, depends_on, enabled = result
                
                print(f"{target_col} ({target_header}):")
                print(f"  map_op: {map_op}")
                print(f"  field_type: {field_type}")
                print(f"  rule_ref: {rule_ref}")
                print(f"  source_cols: {source_cols}")
                print(f"  depends_on: {depends_on}")
                print(f"  enabled: {enabled}")
                
                # 检查source_cols是否在column_data中
                if source_cols:
                    for source_col in source_cols:
                        found = False
                        for col in column_data:
                            col_source_cols = col.get('source_cols')
                            if col_source_cols == source_col:
                                found = True
                                print(f"\n  源列 {source_col}:")
                                print(f"    col: {col.get('source_cols')}")
                                print(f"    head: {col.get('head')}")
                                print(f"    data长度: {len(col.get('data', []))}")
                                break
                        
                        if not found:
                            print(f"\n  ❌ 源列 {source_col} 未在column_data中找到")
                
                print()
    finally:
        connection.close()
    
    print("\n" + "=" * 100)
    print("调试完成！")
    print("=" * 100)

if __name__ == "__main__":
    debug_x_and_y_columns_not_processed()
