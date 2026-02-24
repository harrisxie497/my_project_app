#!/usr/bin/env python3
"""
测试normalize_copy_one_decimal函数
"""

import sys
sys.path.insert(0, 'c:/Users/harris.xie/Documents/trae_projects/japan/backend')

from app.services.field_handlers import normalize_copy_one_decimal

# 测试用例
test_cases = [
    # (输入, 期望输出, 测试描述)
    ("1.234", "1.2", "标准情况：三位小数四舍五入到一位小数"),
    ("2.567", "2.6", "四舍五入：2.567 -> 2.6"),
    ("0.890", "0.9", "四舍五入：0.890 -> 0.9"),
    ("1.200", "1.2", "末尾0处理：1.200 -> 1.2"),
    ("1.000", "1.0", "全0小数位：1.000 -> 1.0"),
    ("5.500", "5.5", "半进位：5.500 -> 5.5"),
    ("1.23kg", "1.2", "包含单位：1.23kg -> 1.2"),
    ("2.56 kg", "2.6", "包含空格和单位：2.56 kg -> 2.6"),
    ("0.89 KG", "0.9", "大写单位：0.89 KG -> 0.9"),
    ("3", "3.0", "整数：3 -> 3.0"),
    ("3.", "3.0", "只有小数点：3. -> 3.0"),
    (None, None, "None值（允许为空）"),
    ("", None, "空字符串（允许为空）"),
    ("   ", None, "纯空格（允许为空）"),
    ("1.234.567", "1234.6", "多个小数点（只保留第一个）"),
    ("abc", None, "纯字母（无法提取数字）"),
]

print("=" * 80)
print("测试 normalize_copy_one_decimal 函数")
print("=" * 80)

passed = 0
failed = 0

for i, (input_val, expected, description) in enumerate(test_cases, 1):
    print(f"\n测试用例 {i}: {description}")
    print(f"  输入: {repr(input_val)}")

    try:
        result = normalize_copy_one_decimal(input_val, allow_null=True)
        print(f"  输出: {repr(result)}")
        print(f"  期望: {repr(expected)}")

        if result == expected:
            print(f"  [通过]")
            passed += 1
        else:
            print(f"  [失败]")
            failed += 1
    except Exception as e:
        print(f"  异常: {e}")
        if expected is None:
            print(f"  [通过] (期望异常)")
            passed += 1
        else:
            print(f"  [失败]")
            failed += 1

print("\n" + "=" * 80)
print(f"测试完成：通过 {passed}/{len(test_cases)}，失败 {failed}/{len(test_cases)}")
print("=" * 80)
