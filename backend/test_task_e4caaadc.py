"""
测试任务ID为t_e4caaadc的任务
"""

from app.services.task_executor import TaskExecutor
from app.core.database import SessionLocal
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def test_task_e4caaadc():
    """测试任务ID为t_e4caaadc的任务"""
    print("=" * 100)
    print("测试任务ID为t_e4caaadc的任务")
    print("=" * 100)
    
    task_id = "t_e4caaadc"
    task_dir = "C:\\Users\\harris.xie\\Documents\\trae_projects\\japan\\backend\\storage\\tasks\\t_e4caaadc"
    
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
    test_task_e4caaadc()
