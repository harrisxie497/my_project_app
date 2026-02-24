"""
运行任务t_aa9d170a，使用新的结果文件名来测试修复
"""

from app.services.task_executor import TaskExecutor
from app.core.database import SessionLocal
import logging
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def run_task_t_aa9d170a_fixed():
    """运行任务t_aa9d170a，使用新的结果文件名"""
    print("=" * 100)
    print("运行任务t_aa9d170a（修复版本）")
    print("=" * 100)
    
    # 任务目录
    task_dir = r'C:\Users\harris.xie\Documents\trae_projects\japan\backend\storage\tasks\t_aa9d170a'
    
    # 原始文件路径
    original_file_path = os.path.join(task_dir, 'original.xlsx')
    
    # 结果文件路径（使用新的文件名）
    result_file_path = os.path.join(task_dir, 'result_fixed.xlsx')
    
    # 任务ID
    task_id = 't_aa9d170a'
    
    # 文件类型
    file_type = 'CUSTOMS'
    
    print(f"\n任务ID: {task_id}")
    print(f"文件类型: {file_type}")
    print(f"原始文件: {original_file_path}")
    print(f"结果文件: {result_file_path}")
    
    # 检查文件是否存在
    if not os.path.exists(original_file_path):
        print(f"\n❌ 原始文件不存在: {original_file_path}")
        return
    
    print(f"\n✅ 原始文件存在")
    
    # 创建数据库会话
    db = SessionLocal()
    
    try:
        # 创建任务执行器
        print(f"\n创建任务执行器...")
        executor = TaskExecutor(
            db_session=db,
            task_id=task_id,
            file_type=file_type
        )
        
        # 执行任务
        print(f"\n开始执行任务...")
        stats = executor.execute(
            original_file_path=original_file_path,
            result_file_path=result_file_path
        )
        
        print(f"\n✅ 任务执行完成！")
        print(f"\n统计信息:")
        for key, value in stats.items():
            print(f"  {key}: {value}")
        
        # 检查结果文件
        if os.path.exists(result_file_path):
            print(f"\n✅ 结果文件已生成: {result_file_path}")
        else:
            print(f"\n❌ 结果文件未生成: {result_file_path}")
        
    except Exception as e:
        print(f"\n❌ 任务执行失败: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()
    
    print("\n" + "=" * 100)
    print("运行完成！")
    print("=" * 100)

if __name__ == "__main__":
    run_task_t_aa9d170a_fixed()
