"""
创建并执行一个新的DELIVERY任务来测试P列格式化
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import logging
import uuid
import shutil

from app.core.database import SessionLocal
from app.models.task import Task

print("=" * 80)
print("创建并执行新的DELIVERY任务")
print("=" * 80)

# 创建测试目录
test_dir = "storage/tasks/test_p_column_" + str(uuid.uuid4())[:8]
os.makedirs(test_dir, exist_ok=True)
os.makedirs(os.path.join(test_dir, "original"), exist_ok=True)

# 复制测试文件
source_file = "storage/tasks/t_fd68ef09/original.xlsx"
dest_file = os.path.join(test_dir, "original.xlsx")

if os.path.exists(source_file):
    shutil.copy2(source_file, dest_file)
    print(f"\n复制测试文件: {dest_file}")
else:
    print(f"\n[FAIL] 源文件不存在: {source_file}")
    exit(1)

# 创建任务记录
db = SessionLocal()

try:
    task = Task(
        id='test_p_col_' + str(uuid.uuid4())[:8],
        file_type='DELIVERY',
        unique_code='160-03270890',
        flight_no='JL123',
        declare_date='2026-02-08',
        status='QUEUED',
        files={
            'original': 'original.xlsx'
        }
    )
    
    db.add(task)
    db.commit()
    
    print(f"\n创建任务:")
    print(f"  任务ID: {task.id}")
    print(f"  文件类型: {task.file_type}")
    print(f"  unique_code: {task.unique_code}")
    print(f"  状态: {task.status}")
    
    # 执行任务
    print("\n开始执行任务...")
    from app.services.task_executor import TaskExecutor
    
    executor = TaskExecutor(db, task.id, 'DELIVERY')
    result = executor.execute()
    
    print("\n任务执行完成:")
    print(f"  输出文件: {result.get('output_file')}")
    print(f"  统计信息: {result.get('stats')}")
    
    # 检查结果文件
    result_file = result.get('output_file')
    if result_file and os.path.exists(result_file):
        print(f"\n检查结果文件: {result_file}")
        
        import openpyxl
        workbook = openpyxl.load_workbook(result_file)
        worksheet = workbook.active
        
        print(f"\n表头:")
        headers = []
        for cell in worksheet[1]:
            headers.append(cell.value)
            if cell.value:
                print(f"  列{len(headers)}: {cell.value}")
        
        # 找到P列
        p_col_idx = None
        for idx, header in enumerate(headers):
            if header == '記事欄2':
                p_col_idx = idx
                print(f"\n找到P列（記事欄2），是第{p_col_idx + 1}列")
                break
        
        if p_col_idx is not None:
            first_value = worksheet.cell(row=2, column=p_col_idx + 1).value
            print(f"\n第一个数据值: '{first_value}'")
            
            if first_value == "160-0327 0890":
                print("\n[OK] P列格式正确: '160-0327 0890' ✓")
            elif first_value == "160-03270890":
                print("\n[FAIL] P列未格式化: '160-03270890'")
                print("       期望: '160-0327 0890'")
            else:
                print(f"\n[INFO] P列值: '{first_value}'")
        
        workbook.close()
    
    db.close()
    
    print("\n" + "=" * 80)
    print("测试完成")
    print("=" * 80)
    
except Exception as e:
    print(f"\n[FAIL] 错误: {str(e)}")
    import traceback
    traceback.print_exc()
    db.rollback()
    db.close()
