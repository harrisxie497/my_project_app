#!/usr/bin/env python3
"""
测试条件表达式处理
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.base_processor import BaseProcessor

class TestProcessor(BaseProcessor):
    """测试用处理器"""
    
    def __init__(self):
        # 不需要实际的文件路径，只测试条件表达式处理
        super().__init__(task_dir=".")
    
    def _get_template_mapping(self):
        pass
    
    def _get_processing_rules(self):
        pass

def test_conditional_expr():
    """测试条件表达式处理"""
    print("测试条件表达式处理...")
    
    processor = TestProcessor()
    
    # 测试用例1：C不为空，D为0，应该返回"00"
    test_row1 = {
        "C": "20251123",
        "D": 0
    }
    
    params = {
        "transformation_type": "conditional_expr",
        "target_col": "D",
        "rules": [
            {
                "when": "C != '' && (D == 0 || D == '0')",
                "set": "00"
            },
            {
                "when": "C == '' && (D == 0 || D == '0')",
                "set": ""
            }
        ],
        "else": "KEEP"
    }
    
    result1 = processor._process_conditional_expr(test_row1, params)
    print(f"测试用例1结果: {result1} (预期: '00')")
    assert result1 == "00", f"测试用例1失败: {result1}"
    
    # 测试用例2：C为空，D为0，应该返回""
    test_row2 = {
        "C": "",
        "D": 0
    }
    
    result2 = processor._process_conditional_expr(test_row2, params)
    print(f"测试用例2结果: {result2} (预期: '')")
    assert result2 == "", f"测试用例2失败: {result2}"
    
    # 测试用例3：C为空，D为'0'，应该返回""
    test_row3 = {
        "C": "",
        "D": "0"
    }
    
    result3 = processor._process_conditional_expr(test_row3, params)
    print(f"测试用例3结果: {result3} (预期: '')")
    assert result3 == "", f"测试用例3失败: {result3}"
    
    # 测试用例4：C不为空，D为'0'，应该返回"00"
    test_row4 = {
        "C": "20251123",
        "D": "0"
    }
    
    result4 = processor._process_conditional_expr(test_row4, params)
    print(f"测试用例4结果: {result4} (预期: '00')")
    assert result4 == "00", f"测试用例4失败: {result4}"
    
    # 测试用例5：D为其他值，应该保持不变
    test_row5 = {
        "C": "20251123",
        "D": "12"
    }
    
    result5 = processor._process_conditional_expr(test_row5, params)
    print(f"测试用例5结果: {result5} (预期: '12')")
    assert result5 == "12", f"测试用例5失败: {result5}"
    
    print("所有测试用例通过！")

if __name__ == "__main__":
    test_conditional_expr()
