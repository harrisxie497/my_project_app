"""
检查日志中是否有X列和Y列的处理记录（包括所有记录）
"""

import re

def check_log_for_x_and_y_columns():
    """检查日志中是否有X列和Y列的处理记录"""
    print("=" * 100)
    print("检查日志中是否有X列和Y列的处理记录")
    print("=" * 100)
    
    # 读取日志文件
    log_file_path = r'C:\Users\harris.xie\Documents\trae_projects\japan\backend\logs\app.log'
    
    with open(log_file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # 查找X列和Y列的处理记录
    columns_to_check = ['X', 'Y']
    
    print(f"\n查找X列和Y列的处理记录:")
    for col in columns_to_check:
        print(f"\n{col}列:")
        found = False
        for i, line in enumerate(lines):
            if f"处理列配置 - 列名: {col}," in line:
                print(f"  ✅ 找到处理列配置记录 (行{i+1}): {line.strip()}")
                found = True
            if f"AI规则批量处理 - 列名: {col}," in line:
                print(f"  ✅ 找到AI规则批量处理记录 (行{i+1}): {line.strip()}")
                found = True
            if f"字段 {col} 的依赖未满足" in line:
                print(f"  ❌ 找到依赖未满足记录 (行{i+1}): {line.strip()}")
                found = True
        
        if not found:
            print(f"  ❌ 没有找到任何处理记录")
    
    print("\n" + "=" * 100)
    print("检查完成！")
    print("=" * 100)

if __name__ == "__main__":
    check_log_for_x_and_y_columns()
