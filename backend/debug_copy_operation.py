"""
调试COPY操作没有正确复制数据的问题
"""

from app.services.excel_reader import read_excel_file
from app.services.customs_processor import CustomsProcessor
from app.core.database import SessionLocal
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def debug_copy_operation():
    """调试COPY操作"""
    print("=" * 100)
    print("调试COPY操作没有正确复制数据的问题")
    print("=" * 100)
    
    # 任务目录
    task_dir = r'C:\Users\harris.xie\Documents\trae_projects\japan\backend\storage\tasks\t_aa9d170a'
    
    # 原始文件路径
    original_file_path = f'{task_dir}\\original.xlsx'
    
    # 文件类型
    file_type = 'CUSTOMS'
    
    print(f"\n任务目录: {task_dir}")
    print(f"原始文件: {original_file_path}")
    print(f"文件类型: {file_type}")
    
    # 创建数据库会话
    db = SessionLocal()
    
    try:
        # 步骤1: 读取Excel文件
        print(f"\n步骤1: 读取Excel文件")
        print("=" * 100)
        
        result = read_excel_file(
            original_file_path,
            file_type=file_type,
            file_role='SOURCE'
        )
        
        column_data = result["column_data"]
        data_row_count = result["data_row_count"]
        
        print(f"\n读取完成:")
        print(f"  列数: {len(column_data)}")
        print(f"  数据行数: {data_row_count}")
        
        # 显示列数据
        print(f"\n列数据:")
        for col in column_data:
            source_cols = col.get('source_cols')
            head = col.get('head')
            data_len = col.get('len')
            print(f"  {source_cols} ({head}): {data_len}行数据")
        
        # 步骤2: 检查COPY类型列的源列数据
        print(f"\n步骤2: 检查COPY类型列的源列数据")
        print("=" * 100)
        
        check_columns = ['HAWB番号', '現地問合せ番号', '貨物重量', '輸入者 郵便番号', '輸入者電話番号']
        
        for header in check_columns:
            # 查找列
            col_data = None
            for col in column_data:
                if col.get('head') == header:
                    col_data = col
                    break
            
            if col_data:
                source_cols = col_data.get('source_cols')
                data = col_data.get('data')
                
                print(f"\n{header}:")
                print(f"  source_cols: {source_cols}")
                print(f"  数据长度: {len(data)}")
                print(f"  前5行数据: {data[:5]}")
            else:
                print(f"\n{header}: 未找到列")
        
        # 步骤3: 检查field_pipelines配置
        print(f"\n步骤3: 检查field_pipelines配置")
        print("=" * 100)
        
        from app.services.customs_processor import get_field_pipelines
        
        pipelines = get_field_pipelines(db)
        
        for header in check_columns:
            # 查找pipeline
            pipeline = None
            for p in pipelines:
                if p.get('target_header') == header:
                    pipeline = p
                    break
            
            if pipeline:
                target_col = pipeline.get('target_col')
                source_cols = pipeline.get('source_cols')
                map_op = pipeline.get('map_op')
                field_type = pipeline.get('field_type')
                
                print(f"\n{header}:")
                print(f"  target_col: {target_col}")
                print(f"  source_cols: {source_cols}")
                print(f"  map_op: {map_op}")
                print(f"  field_type: {field_type}")
            else:
                print(f"\n{header}: 未找到pipeline")
        
    except Exception as e:
        print(f"\n❌ 调试失败: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()
    
    print("\n" + "=" * 100)
    print("调试完成！")
    print("=" * 100)

if __name__ == "__main__":
    debug_copy_operation()
