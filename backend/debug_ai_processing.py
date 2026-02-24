"""
调试AI规则处理
"""

from app.services.customs_processor import CustomsProcessor
from app.core.database import SessionLocal
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def debug_ai_processing():
    """调试AI规则处理"""
    print("=" * 100)
    print("调试AI规则处理")
    print("=" * 100)
    
    # 任务目录
    task_dir = r'C:\Users\harris.xie\Documents\trae_projects\japan\backend\storage\tasks\t_aa9d170a'
    
    # 原始文件路径
    original_file_path = f'{task_dir}\\original.xlsx'
    
    # 结果文件路径
    result_file_path = f'{task_dir}\\result_debug.xlsx'
    
    # 文件类型
    file_type = 'CUSTOMS'
    
    # 创建数据库会话
    db = SessionLocal()
    
    try:
        # 创建处理器
        print(f"\n创建处理器...")
        processor = CustomsProcessor(task_dir, db, file_type)
        
        # 读取原始文件
        print(f"\n读取原始文件...")
        result = processor.read_excel_file(original_file_path, file_type, 'SOURCE')
        
        column_data = result["column_data"]
        data_row_count = result["data_row_count"]
        
        print(f"\n数据行数: {data_row_count}")
        print(f"列数: {len(column_data)}")
        
        # 检查AI列的数据
        ai_columns = ['X', 'Y', 'J', 'K']
        
        print(f"\n检查AI列的数据:")
        for col_data in column_data:
            col_letter = col_data.get('col')
            col_header = col_data.get('head')
            
            if col_letter in ai_columns:
                print(f"\n{col_letter} ({col_header}):")
                print(f"  col: {col_letter}")
                print(f"  head: {col_header}")
                print(f"  data长度: {len(col_data.get('data', []))}")
                print(f"  前5行数据: {col_data.get('data', [])[:5]}")
        
        db.close()
        
        print("\n" + "=" * 100)
        print("调试完成！")
        print("=" * 100)
        
    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_ai_processing()
