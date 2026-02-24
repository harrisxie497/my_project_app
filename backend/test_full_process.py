"""
从excel_read.py到excel_write.py整个流程都跑一次，确认每一列的数据最终写了多少行
"""

from app.services.excel_reader import read_excel_file
from app.services.task_executor import TaskExecutor
from app.core.database import SessionLocal
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def test_full_process():
    """测试完整流程"""
    print("=" * 100)
    print("测试完整流程 - 从excel_read.py到excel_write.py")
    print("=" * 100)
    
    task_id = "t_0fc5b76e"
    task_dir = "C:\\Users\\harris.xie\\Documents\\trae_projects\\japan\\backend\\storage\\tasks\\t_0fc5b76e"
    
    db_session = SessionLocal()
    try:
        # 使用TaskExecutor来初始化CustomsProcessor
        task_executor = TaskExecutor(
            db_session=db_session,
            task_id=task_id,
            file_type='CUSTOMS'
        )
        
        # 运行完整流程
        original_file_path = f"{task_dir}\\original.xlsx"
        result_file_path = f"{task_dir}\\result.xlsx"
        stats = task_executor.execute(original_file_path, result_file_path)
        
        print("\n" + "=" * 100)
        print("流程执行完成！")
        print("=" * 100)
        
        # 输出统计信息
        print("\n" + "=" * 100)
        print("统计信息")
        print("=" * 100)
        print(f"总行数: {stats.get('total_rows', 0)}")
        print(f"修复字段数: {stats.get('fixed_count', 0)}")
        print(f"补齐字段数: {stats.get('filled_count', 0)}")
        print(f"汇率变更行数: {stats.get('fx_changed_rows', 0)}")
        print(f"LLM补齐字段数: {stats.get('llm_filled_count', 0)}")
        
        # 读取结果文件，查看每一列的数据
        print("\n" + "=" * 100)
        print("读取结果文件，查看每一列的数据")
        print("=" * 100)
        
        result = read_excel_file(
            file_path=processor.result_file_path,
            file_type='CUSTOMS',
            file_role='SOURCE'
        )
        
        print(f"\n结果文件路径: {processor.result_file_path}")
        print(f"总列数: {len(result.get('column_data', []))}")
        
        # 输出每一列的数据行数、前5个和最后5个
        for col in result.get('column_data', []):
            col_name = col.get('head', '')
            col_data = col.get('data', [])
            col_len = len(col_data)
            
            print(f"\n{'=' * 100}")
            print(f"列: {col_name}")
            print(f"{'=' * 100}")
            print(f"数据行数: {col_len}")
            
            if col_len > 0:
                print(f"前5个数据: {col_data[:5]}")
                print(f"最后5个数据: {col_data[-5:]}")
            else:
                print("前5个数据: []")
                print("最后5个数据: []")
        
        print("\n" + "=" * 100)
        print("测试完成！")
        print("=" * 100)
        
    except Exception as e:
        print(f"\n❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        db_session.close()


if __name__ == "__main__":
    test_full_process()
