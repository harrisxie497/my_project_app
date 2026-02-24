"""
检查最新日志中是否有X、Y、J、K列的处理记录
"""

import re

def check_latest_log_for_ai_columns():
    """检查最新日志中是否有X、Y、J、K列的处理记录"""
    print("=" * 100)
    print("检查最新日志中是否有X、Y、J、K列的处理记录")
    print("=" * 100)
    
    # 读取日志文件
    log_file_path = r'C:\Users\harris.xie\Documents\trae_projects\japan\backend\logs\app.log'
    
    with open(log_file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # 查找X、Y、J、K列的处理记录（只查找最新的记录）
    ai_columns = ['X', 'Y', 'J', 'K']
    
    # 找到最新的"解析原始文件"日志
    start_idx = -1
    for i in range(len(lines) - 1, -1, -1):
        if "解析原始文件" in lines[i]:
            start_idx = i
            break
    
    if start_idx == -1:
        print("❌ 没有找到'解析原始文件'日志")
        return
    
    print(f"\n从第{start_idx}行开始查找AI列的处理记录:")
    
    for col in ai_columns:
        print(f"\n{col}列:")
        found = False
        for i in range(start_idx, len(lines)):
            line = lines[i]
            if f"处理列配置 - 列名: {col}," in line:
                print(f"  ✅ 找到处理列配置记录: {line.strip()}")
                found = True
            if f"AI规则批量处理 - 列名: {col}," in line:
                print(f"  ✅ 找到AI规则批量处理记录: {line.strip()}")
                found = True
            if f"字段 {col} 的依赖未满足" in line:
                print(f"  ❌ 找到依赖未满足记录: {line.strip()}")
                found = True
        
        if not found:
            print(f"  ❌ 没有找到任何处理记录")
    
    print("\n" + "=" * 100)
    print("检查完成！")
    print("=" * 100)

if __name__ == "__main__":
    check_latest_log_for_ai_columns()
