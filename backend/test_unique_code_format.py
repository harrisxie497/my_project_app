"""
测试unique_code格式化逻辑
"""

def format_unique_code(unique_code: str) -> str:
    """
    格式化unique_code: "160-03270890" -> "160-0327 0890"
    """
    if unique_code and len(unique_code) >= 12:
        return unique_code[:7] + ' ' + unique_code[7:]
    return unique_code

print("=" * 80)
print("测试unique_code格式化")
print("=" * 80)

# 测试用例
test_cases = [
    "160-03270890",
    "160-03270889",
    "160-12345678",
    "",
    "short",
    "123-45678901"
]

for i, test in enumerate(test_cases, 1):
    formatted = format_unique_code(test)
    print(f"\n{i}. 输入: '{test}'")
    print(f"   输出: '{formatted}'")

print("\n" + "=" * 80)
print("测试完成")
print("=" * 80)
