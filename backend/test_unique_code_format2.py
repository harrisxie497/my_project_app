"""
测试unique_code格式化逻辑
"""

def analyze_unique_code(unique_code: str) -> None:
    """分析unique_code的每个字符"""
    print(f"unique_code: '{unique_code}'")
    print(f"长度: {len(unique_code)}")
    print("\n字符分析:")
    for i, char in enumerate(unique_code):
        print(f"  索引{i}: '{char}'")

def format_unique_code(unique_code: str) -> str:
    """
    格式化unique_code: "160-03270890" -> "160-0327 0890"
    """
    print(f"\n格式化过程:")
    print(f"  输入: '{unique_code}'")
    print(f"  长度: {len(unique_code)}")

    if unique_code and len(unique_code) >= 8:
        # 在索引7后插入空格
        prefix = unique_code[:8]
        suffix = unique_code[8:]
        result = prefix + ' ' + suffix
        print(f"  前8个字符: '{prefix}'")
        print(f"  后续字符: '{suffix}'")
        print(f"  结果: '{result}'")
        return result
    return unique_code

print("=" * 80)
print("测试unique_code格式化")
print("=" * 80)

# 先分析原始格式
analyze_unique_code("160-03270890")

print("\n" + "=" * 80)
print("格式化测试")
print("=" * 80)

# 测试用例
test_cases = [
    "160-03270890",
    "160-03270889",
]

for i, test in enumerate(test_cases, 1):
    print(f"\n测试{i}:")
    formatted = format_unique_code(test)
    print(f"  最终结果: '{formatted}'")

print("\n" + "=" * 80)
print("测试完成")
print("=" * 80)
