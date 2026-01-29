#!/usr/bin/env python3
"""
测试D列（时间帯指定）条件表达式处理
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.delivery_processor import DeliveryProcessor

def test_d_column_processing():
    """测试D列（时间帯指定）条件表达式处理"""
    print("测试D列（时间帯指定）条件表达式处理...")
    
    # 创建测试数据
    test_data = [
        # 测试用例1：C（配達指定日）不为空，D（时间帯指定）为0，应该返回"00"
        {
            "お客様管理番号": "TEST001",
            "佐川問合せ番号HAWB": "123456",
            "配達指定日": "20251123",  # C列
            "時間帯指定": 0,           # D列
            "貨物個数": 1,
            "お届け先人名": "テスト ユーザー",
            "お届け先住所": "東京都渋谷区渋谷1-1-1",
            "お届け先電話": "03-1234-5678",
            "お届け先郵便": "1500002",
            "依頼主": "テスト会社",
            "依頼主住所": "東京都千代田区千代田1-1-1",
            "依頼主郵便番号": "1000001",
            "依頼主電話": "03-8765-4321",
            "佐川顧客コード（固定）": "123456",
            "記事欄2": "",
            "記事欄3": ""
        },
        # 测试用例2：C（配達指定日）为空，D（时间帯指定）为0，应该返回""
        {
            "お客様管理番号": "TEST002",
            "佐川問合せ番号HAWB": "654321",
            "配達指定日": "",         # C列为空
            "時間帯指定": 0,           # D列
            "貨物個数": 1,
            "お届け先人名": "テスト ユーザー2",
            "お届け先住所": "東京都新宿区新宿1-1-1",
            "お届け先電話": "03-1111-2222",
            "お届け先郵便": "1600002",
            "依頼主": "テスト会社2",
            "依頼主住所": "東京都中央区中央1-1-1",
            "依頼主郵便番号": "1000002",
            "依頼主電話": "03-3333-4444",
            "佐川顧客コード（固定）": "123456",
            "記事欄2": "",
            "記事欄3": ""
        },
        # 测试用例3：C（配達指定日）不为空，D（时间帯指定）为'0'，应该返回"00"
        {
            "お客様管理番号": "TEST003",
            "佐川問合せ番号HAWB": "987654",
            "配達指定日": "20251124",  # C列
            "時間帯指定": "0",         # D列为字符串'0'
            "貨物個数": 1,
            "お届け先人名": "テスト ユーザー3",
            "お届け先住所": "東京都港区港1-1-1",
            "お届け先電話": "03-5555-6666",
            "お届け先郵便": "1050001",
            "依頼主": "テスト会社3",
            "依頼主住所": "東京都品川区品川1-1-1",
            "依頼主郵便番号": "1400002",
            "依頼主電話": "03-7777-8888",
            "佐川顧客コード（固定）": "123456",
            "記事欄2": "",
            "記事欄3": ""
        }
    ]
    
    # 创建处理器实例
    processor = DeliveryProcessor(task_dir=".")
    
    # 查看默认处理规则
    print("\n默认处理规则：")
    rules = processor._get_default_processing_rules()
    for rule in rules:
        print(f"  - {rule['field_name']}: {rule['transformation_type']}")
    
    # 调用处理方法
    print("\n调用字段处理方法...")
    processed_data = processor._process_fields(test_data)
    
    # 验证结果
    print("\n验证处理结果...")
    print(f"处理前数据：{test_data[0]['時間帯指定']}")
    print(f"处理后数据：{processed_data[0]['時間帯指定']}")
    
    # 测试用例1验证
    result1 = processed_data[0]["時間帯指定"]
    expected1 = "00"
    print(f"测试用例1: C='20251123', D=0 -> 结果: {result1} (预期: {expected1})")
    assert result1 == expected1, f"测试用例1失败: {result1} != {expected1}"
    
    # 测试用例2验证
    result2 = processed_data[1]["時間帯指定"]
    expected2 = ""
    print(f"测试用例2: C='', D=0 -> 结果: {repr(result2)} (预期: {repr(expected2)})")
    assert result2 == expected2, f"测试用例2失败: {repr(result2)} != {repr(expected2)}"
    
    # 测试用例3验证
    result3 = processed_data[2]["時間帯指定"]
    expected3 = "00"
    print(f"测试用例3: C='20251124', D='0' -> 结果: {result3} (预期: {expected3})")
    assert result3 == expected3, f"测试用例3失败: {result3} != {expected3}"
    
    print("\n✅ 所有测试用例通过！D列条件表达式处理正常工作。")

if __name__ == "__main__":
    test_d_column_processing()
