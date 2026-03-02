"""
测试M列的add_prefix_zero功能
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.services import field_handlers

def test_normalize_copy_then_regex():
    """测试normalize_copy_then_regex函数"""
    print("=" * 100)
    print("测试M列的add_prefix_zero功能")
    print("=" * 100)
    
    test_cases = [
        {
            'name': '以0开头的电话号码',
            'input': '09012345678',
            'expected': '09012345678',
            'params': {
                'regex': r'^\d{9,11}$',
                'required': True,
                'remove_dash': True,
                'remove_leading_trailing_spaces': True,
                'remove_middle_spaces': True,
                'add_prefix_zero': True
            }
        },
        {
            'name': '不以0开头的电话号码',
            'input': '9012345678',
            'expected': '09012345678',
            'params': {
                'regex': r'^\d{9,11}$',
                'required': True,
                'remove_dash': True,
                'remove_leading_trailing_spaces': True,
                'remove_middle_spaces': True,
                'add_prefix_zero': True
            }
        },
        {
            'name': '带横杠的电话号码',
            'input': '090-1234-5678',
            'expected': '09012345678',
            'params': {
                'regex': r'^\d{9,11}$',
                'required': True,
                'remove_dash': True,
                'remove_leading_trailing_spaces': True,
                'remove_middle_spaces': True,
                'add_prefix_zero': True
            }
        },
        {
            'name': '带空格的电话号码',
            'input': ' 9012345678  ',
            'expected': '09012345678',
            'params': {
                'regex': r'^\d{9,11}$',
                'required': True,
                'remove_dash': True,
                'remove_leading_trailing_spaces': True,
                'remove_middle_spaces': True,
                'add_prefix_zero': True
            }
        },
        {
            'name': '空值',
            'input': '',
            'expected': None,
            'params': {
                'regex': r'^\d{9,11}$',
                'required': True,
                'remove_dash': True,
                'remove_leading_trailing_spaces': True,
                'remove_middle_spaces': True,
                'add_prefix_zero': True
            },
            'should_raise': True
        },
        {
            'name': 'None值',
            'input': None,
            'expected': None,
            'params': {
                'regex': r'^\d{9,11}$',
                'required': False,
                'remove_dash': True,
                'remove_leading_trailing_spaces': True,
                'remove_middle_spaces': True,
                'add_prefix_zero': True
            }
        },
        {
            'name': '不添加前缀0（add_prefix_zero=False）',
            'input': '9012345678',
            'expected': '9012345678',
            'params': {
                'regex': r'^\d{9,11}$',
                'required': True,
                'remove_dash': True,
                'remove_leading_trailing_spaces': True,
                'remove_middle_spaces': True,
                'add_prefix_zero': False
            }
        }
    ]
    
    passed = 0
    failed = 0
    
    for idx, test_case in enumerate(test_cases, 1):
        print(f"\n测试用例 {idx}: {test_case['name']}")
        print(f"  输入: {repr(test_case['input'])}")
        print(f"  期望: {repr(test_case['expected'])}")
        
        try:
            result = field_handlers.normalize_copy_then_regex(
                test_case['input'],
                **test_case['params']
            )
            
            if test_case.get('should_raise'):
                print(f"  ❌ 失败: 应该抛出异常，但没有")
                failed += 1
            elif result == test_case['expected']:
                print(f"  ✅ 通过: 结果 = {repr(result)}")
                passed += 1
            else:
                print(f"  ❌ 失败: 结果 = {repr(result)}, 期望 = {repr(test_case['expected'])}")
                failed += 1
        except Exception as e:
            if test_case.get('should_raise'):
                print(f"  ✅ 通过: 正确抛出异常 - {str(e)}")
                passed += 1
            else:
                print(f"  ❌ 失败: 意外异常 - {str(e)}")
                failed += 1
    
    print("\n" + "=" * 100)
    print(f"测试结果: 通过 {passed}/{len(test_cases)}, 失败 {failed}/{len(test_cases)}")
    print("=" * 100)
    
    return passed == len(test_cases)

if __name__ == "__main__":
    success = test_normalize_copy_then_regex()
    sys.exit(0 if success else 1)
