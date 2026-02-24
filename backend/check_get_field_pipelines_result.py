"""
检查_get_field_pipelines方法的返回结果
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.services.customs_processor import CustomsProcessor
import logging
import pymysql

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def check_get_field_pipelines_result():
    """检查_get_field_pipelines方法的返回结果"""
    print("=" * 100)
    print("检查_get_field_pipelines方法的返回结果")
    print("=" * 100)
    
    # 创建数据库连接
    db_session = pymysql.connect(
        host='172.18.207.224',
        port=3306,
        user='app',
        password='app123456',
        database='demo',
        charset='utf8mb4'
    )
    
    # 创建CustomsProcessor实例
    task_dir = r'C:\Users\harris.xie\Documents\trae_projects\japan\backend\storage\tasks\t_aa9d170a'
    processor = CustomsProcessor(db_session=db_session, task_dir=task_dir)
    
    # 调用_get_field_pipelines方法
    field_pipelines = processor._get_field_pipelines()
    
    print(f"\n获取到 {len(field_pipelines)} 个字段处理配置:\n")
    
    # 查找AI列的配置
    ai_columns = ['H', 'I', 'J', 'K', 'X', 'Y']
    
    for pipeline in field_pipelines:
        target_col = pipeline.get('target_col')
        if target_col in ai_columns:
            print(f"{target_col} ({pipeline.get('target_header')}):")
            print(f"  map_op: {pipeline.get('map_op')}")
            print(f"  source_cols: {pipeline.get('source_cols')}")
            print(f"  field_type: {pipeline.get('field_type')}")
            print(f"  rule_ref: {pipeline.get('rule_ref')}")
            print(f"  depends_on: {pipeline.get('depends_on')}")
            print(f"  order_num: {pipeline.get('order_num')}")
            print()
    
    # 检查X、Y、J、K列是否在field_pipelines中
    missing_columns = []
    for col in ai_columns:
        found = False
        for pipeline in field_pipelines:
            if pipeline.get('target_col') == col:
                found = True
                break
        if not found:
            missing_columns.append(col)
    
    if missing_columns:
        print(f"\n❌ 以下列未在field_pipelines中找到: {missing_columns}")
    else:
        print(f"\n✅ 所有AI列都在field_pipelines中找到")
    
    print("\n" + "=" * 100)
    print("检查完成！")
    print("=" * 100)
    
    # 关闭数据库会话
    db_session.close()

if __name__ == "__main__":
    check_get_field_pipelines_result()
