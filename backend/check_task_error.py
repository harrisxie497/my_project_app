"""
检查任务 t_553349be 的详细信息和错误原因
"""
from app.core.database import SessionLocal
from app.models.task import Task
import json

print("=" * 80)
print("检查任务 t_553349be")
print("=" * 80)

db = SessionLocal()

try:
    # 查询任务
    task = db.query(Task).filter(Task.id == 't_553349be').first()
    
    if not task:
        print("[FAIL] 任务不存在: t_553349be")
    else:
        print("\n【任务基本信息】")
        print("-" * 80)
        print(f"任务ID: {task.id}")
        print(f"文件类型: {task.file_type}")
        print(f"唯一标识码: {task.unique_code}")
        print(f"状态: {task.status}")
        print(f"创建人ID: {task.created_by_user_id}")
        print(f"航班号: {task.flight_no}")
        print(f"报关日期: {task.declare_date}")
        print(f"进度阶段: {task.progress_stage}")
        print(f"进度消息: {task.progress_message}")
        print(f"创建时间: {task.created_at}")
        print(f"开始时间: {task.started_at}")
        print(f"完成时间: {task.finished_at}")
        
        print("\n【Header Params】")
        print("-" * 80)
        if task.header_params:
            try:
                if isinstance(task.header_params, str):
                    header_dict = json.loads(task.header_params)
                    print(json.dumps(header_dict, indent=2, ensure_ascii=False))
                else:
                    print(json.dumps(task.header_params, indent=2, ensure_ascii=False))
            except Exception as e:
                print(f"解析header_params失败: {e}")
                print(f"原始值: {task.header_params}")
        else:
            print("无")
        
        print("\n【错误信息】")
        print("-" * 80)
        if task.error:
            print(json.dumps(task.error, indent=2, ensure_ascii=False))
        else:
            print("无")
        
        print("\n【统计信息】")
        print("-" * 80)
        if task.stats:
            print(json.dumps(task.stats, indent=2, ensure_ascii=False))
        else:
            print("无")
        
        print("\n【文件信息】")
        print("-" * 80)
        if task.files:
            print(json.dumps(task.files, indent=2, ensure_ascii=False))
        else:
            print("无")
        
        # 根据状态给出建议
        print("\n" + "=" * 80)
        print("【问题诊断】")
        print("-" * 80)
        
        if task.status == 'FAILED':
            if task.error:
                error_msg = str(task.error)
                if 'FileDefinition' in error_msg or 'field_pipeline' in error_msg.lower():
                    print("[可能原因] 数据库配置缺失")
                    print("[建议] 检查file_definitions和field_pipelines表")
                elif 'file not found' in error_msg.lower():
                    print("[可能原因] 源文件丢失或路径错误")
                    print("[建议] 检查files字段中的源文件路径")
                elif 'permission' in error_msg.lower():
                    print("[可能原因] 文件权限问题")
                    print("[建议] 检查存储目录的读写权限")
                elif 'ai' in error_msg.lower():
                    print("[可能原因] AI服务错误")
                    print("[建议] 检查DeepSeek API配置")
                else:
                    print(f"[错误信息] {error_msg}")
            else:
                print("[警告] 任务状态为FAILED但没有错误信息")
        
        elif task.status == 'QUEUED':
            print("[状态] 任务在队列中等待处理")
            print("[建议] 检查后台任务处理器是否正在运行")
        
        elif task.status == 'PROCESSING':
            print("[状态] 任务正在处理中")
            print("[当前阶段]", task.progress_stage or "未知")
            print("[建议] 等待任务完成或检查是否卡住")
        
        elif task.status == 'SUCCESS':
            print("[状态] 任务已成功完成")
            print("[建议] 检查生成的输出文件")
        
        print("=" * 80)
        
except Exception as e:
    print(f"错误: {str(e)}")
    import traceback
    traceback.print_exc()
finally:
    db.close()
