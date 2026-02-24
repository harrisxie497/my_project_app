"""
检查为什么file_definitions的OUTPUT的columns_json顺序没有被正确使用
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.models.file_definition import FileDefinition

def check_output_columns_json_detail():
    """检查OUTPUT的columns_json详细信息"""
    print("=" * 100)
    print("检查OUTPUT的columns_json详细信息")
    print("=" * 100)
    
    db_session = SessionLocal()
    
    try:
        # 查询OUTPUT文件定义
        output_file_def = db_session.query(FileDefinition).filter(
            FileDefinition.file_type == 'CUSTOMS',
            FileDefinition.file_role == 'OUTPUT'
        ).first()
        
        if output_file_def:
            columns_json = output_file_def.columns_json
            print(f"\nOUTPUT的columns_json:")
            print(f"  类型: {type(columns_json)}")
            print(f"  长度: {len(columns_json)}")
            print(f"\n列顺序:")
            for idx, col in enumerate(columns_json, start=1):
                print(f"  {idx}. 列字母: {col.get('col')}, 表头: {col.get('header')}")
            
            # 检查是否有重复的表头
            headers = [col.get('header') for col in columns_json]
            unique_headers = list(dict.fromkeys(headers))
            if len(headers) != len(unique_headers):
                print(f"\n\n警告：发现重复的表头！")
                print(f"  原始表头数量: {len(headers)}")
                print(f"  唯一表头数量: {len(unique_headers)}")
                
                # 找出重复的表头
                from collections import Counter
                header_counts = Counter(headers)
                for header, count in header_counts.items():
                    if count > 1:
                        print(f"  表头 '{header}' 重复了 {count} 次")
            else:
                print(f"\n\n没有发现重复的表头")
        else:
            print("未找到OUTPUT文件定义")
    
    except Exception as e:
        print(f"查询失败: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        db_session.close()
    
    print("\n" + "=" * 100)
    print("检查完成")
    print("=" * 100)

if __name__ == "__main__":
    check_output_columns_json_detail()
