"""
直接测试calc_time_slot_with_delivery_date函数
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.services.field_handlers import calc_time_slot_with_delivery_date

print("=" * 80)
print("测试calc_time_slot_with_delivery_date函数")
print("=" * 80)

test_cases = [
    {
        "d_value": 0,
        "c_value": "2026-02-10",
        "expected": "00",
        "desc": "C不为空，D=0 -> 应为00"
    },
    {
        "d_value": 5,
        "c_value": "2026-02-11",
        "expected": "05",
        "desc": "C不为空，D=5 -> 应为05"
    },
    {
        "d_value": 12,
        "c_value": "2026-02-12",
        "expected": "12",
        "desc": "C不为空，D=12 -> 应为12"
    },
    {
        "d_value": 0,
        "c_value": None,
        "expected": "",
        "desc": "C为空，D=0 -> 应为空"
    },
    {
        "d_value": 8,
        "c_value": None,
        "expected": "08",
        "desc": "C为空，D=8 -> 应为08"
    },
    {
        "d_value": 15,
        "c_value": None,
        "expected": "15",
        "desc": "C为空，D=15 -> 应为15"
    },
    {
        "d_value": 0,
        "c_value": "",
        "expected": "",
        "desc": "C为空字符串，D=0 -> 应为空"
    }
]

all_passed = True

for test_case in test_cases:
    d_value = test_case["d_value"]
    c_value = test_case["c_value"]
    expected = test_case["expected"]
    desc = test_case["desc"]

    result = calc_time_slot_with_delivery_date(d_value, c_value)

    print(f"\n{desc}")
    print(f"  输入: d_value={repr(d_value)}, c_value={repr(c_value)}")
    print(f"  结果: {repr(result)}")
    print(f"  期望: {repr(expected)}")

    if result == expected:
        print(f"  [通过]")
    else:
        print(f"  [失败]")
        all_passed = False

print("\n" + "=" * 80)
if all_passed:
    print("[成功] 函数测试全部通过！")
else:
    print("[失败] 函数测试有失败！")
print("=" * 80)
