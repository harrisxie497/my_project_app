"""
测试DEFAULT操作：当源值为空时使用默认值
"""
from app.services.field_handlers import copy_equal_to, validate_copy_then_equal_to_target_col

print("=" * 80)
print("测试DEFAULT操作")
print("=" * 80)

# 测试用例
test_cases = [
    {
        "source_value": "TEST",
        "target_value": "DIDA",
        "expected": "TEST",
        "description": "源值不为空，应返回源值"
    },
    {
        "source_value": "",
        "target_value": "DIDA",
        "expected": "DIDA",
        "description": "源值为空字符串，应返回默认值"
    },
    {
        "source_value": None,
        "target_value": "DIDA",
        "expected": "DIDA",
        "description": "源值为None，应返回默认值"
    },
    {
        "source_value": "   ",
        "target_value": "DIDA",
        "expected": "DIDA",
        "description": "源值为空白字符，应返回默认值"
    },
    {
        "source_value": "千葉県",
        "target_value": "千葉県流山市平方8061GLPALFALINK81F13番シャッター",
        "expected": "千葉県",
        "description": "源值不为空，应返回源值"
    },
    {
        "source_value": "",
        "target_value": "千葉県流山市平方8061GLPALFALINK81F13番シャッター",
        "expected": "千葉県流山市平方8061GLPALFALINK81F13番シャッター",
        "description": "源值为空，应返回默认值"
    },
    {
        "source_value": "12345678",
        "target_value": "0471377848",
        "expected": "12345678",
        "description": "源值不为空，应返回源值"
    },
    {
        "source_value": "",
        "target_value": "0471377848",
        "expected": "0471377848",
        "description": "源值为空，应返回默认值"
    }
]

print("\n【测试 validate_copy_then_equal_to_target_col 函数】")
print("-" * 80)

passed = 0
failed = 0

for i, test_case in enumerate(test_cases, 1):
    source_value = test_case["source_value"]
    target_value = test_case["target_value"]
    expected = test_case["expected"]
    description = test_case["description"]
    
    result = validate_copy_then_equal_to_target_col(source_value, target_value, "")
    
    if result == expected:
        print(f"[通过] 测试用例 {i}: {description}")
        print(f"       源值: {repr(source_value)}, 默认值: {repr(target_value)}")
        print(f"       期望: {repr(expected)}, 实际: {repr(result)}")
        passed += 1
    else:
        print(f"[失败] 测试用例 {i}: {description}")
        print(f"       源值: {repr(source_value)}, 默认值: {repr(target_value)}")
        print(f"       期望: {repr(expected)}, 实际: {repr(result)}")
        failed += 1

print("\n【测试 copy_equal_to 函数】")
print("-" * 80)

for i, test_case in enumerate(test_cases, 1):
    source_value = test_case["source_value"]
    target_value = test_case["target_value"]
    expected = test_case["expected"]
    description = test_case["description"]
    
    result = copy_equal_to(source_value, target_value)
    
    if result == expected:
        print(f"[通过] 测试用例 {i}: {description}")
        passed += 1
    else:
        print(f"[失败] 测试用例 {i}: {description}")
        print(f"       源值: {repr(source_value)}, 默认值: {repr(target_value)}")
        print(f"       期望: {repr(expected)}, 实际: {repr(result)}")
        failed += 1

print("\n" + "=" * 80)
print(f"测试结果: 通过 {passed} 个, 失败 {failed} 个")
print("=" * 80)
