"""
重新执行DELIVERY任务并查看P列格式化
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import logging

# 设置DEBUG级别日志
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

from app.core.database import SessionLocal
from app.services.task_executor import TaskExecutor

print("=" * 80)
print("重新执行DELIVERY任务测试P列格式化")
print("=" * 80)

# 任务ID
task_id = 't_fd68ef09'

try:
    db = SessionLocal()
    
    print(f"\n开始执行任务: {task_id}")
    print("=" * 80)
    
    # 创建任务执行器
    executor = TaskExecutor(db, task_id, 'DELIVERY')
    
    # 执行任务
    result = executor.execute()
    
    print("\n" + "=" * 80)
    print("任务执行完成")
    print(f"输出文件: {result.get('output_file')}")
    print(f"统计信息: {result.get('stats')}")
    print("=" * 80)
    
    db.close()
    
    print("\n请检查以下内容:")
    print("1. 查看日志中是否有 '使用unique_code作为常量值（格式化后）' 的日志")
    print("2. 打开结果文件，查看P列（記事欄2）的值")
    print("3. 确认P列的值是否为 '160-0327 0890'")
    
except Exception as e:
    print(f"\n[FAIL] 任务执行失败: {str(e)}")
    import traceback
    traceback.print_exc()
