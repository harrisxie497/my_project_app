"""
测试unique_code格式化功能
"""

def format_unique_code(unique_code: str) -> str:
    """
    格式化unique_code: "160-03270890" -> "160-0327 0890"
    """
    if unique_code and len(unique_code) >= 8:
        return unique_code[:8] + ' ' + unique_code[8:]
    return unique_code

print("=" * 80)
print("测试unique_code格式化: '160-03270890' -> '160-0327 0890'")
print("=" * 80)

test_cases = [
    ("160-03270890", "160-0327 0890"),
    ("160-03270889", "160-0327 0889"),
    ("160-12345678", "160-1234 5678"),
    ("", ""),
    ("short", "short"),
]

print("\n测试用例:")
all_passed = True
for input_val, expected in test_cases:
    result = format_unique_code(input_val)
    passed = result == expected
    all_passed = all_passed and passed
    status = "[OK]" if passed else "[FAIL]"
    print(f"\n{status} 输入: '{input_val}'")
    print(f"    期望: '{expected}'")
    print(f"    实际: '{result}'")

print("\n" + "=" * 80)
if all_passed:
    print("所有测试通过!")
else:
    print("部分测试失败!")
print("=" * 80)
