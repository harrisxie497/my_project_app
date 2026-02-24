"""
检查D列的处理逻辑
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.services.field_handlers import calc_time_slot_with_delivery_date

def check_d_column_logic():
    """检查D列的处理逻辑"""
    print("=" * 100)
    print("检查D列的处理逻辑")
    print("=" * 100)
    
    # 测试数据
    c_values = [None, __import__('datetime').datetime(2025, 12, 14, 0, 0), None, None, None]
    d_values = [0, 0, 0, 0, 0]
    
    print(f"\n测试数据:")
    print(f"  C列（配達指定日）: {c_values}")
    print(f"  D列（時間帯指定）: {d_values}")
    
    print(f"\n处理结果:")
    for idx, (c_value, d_value) in enumerate(zip(c_values, d_values), start=1):
        result = calc_time_slot_with_delivery_date(d_value, c_value)
        print(f"  第{idx}行: C列={c_value}, D列={d_value}, 结果={result}")
    
    print("\n" + "=" * 100)
    print("检查完成")
    print("=" * 100)

if __name__ == "__main__":
    check_d_column_logic()
