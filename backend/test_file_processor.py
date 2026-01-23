#!/usr/bin/env python3
"""
测试文件处理器功能
"""

import os
import sys
import tempfile
from datetime import datetime

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.file_processor import FileProcessor

def test_file_processor():
    """测试文件处理器"""
    print("开始测试文件处理器...")
    
    try:
        # 创建临时目录
        with tempfile.TemporaryDirectory() as temp_dir:
            # 创建测试文件
            test_file_path = os.path.join(temp_dir, "original.xlsx")
            
            # 使用openpyxl创建一个简单的测试Excel文件
            from openpyxl import Workbook
            wb = Workbook()
            ws = wb.active
            
            # 写入测试数据
            ws.append(["記事欄2", "MAWB NO", "FLIGHT NO", "ARRIVAL DATE"])
            ws.append(["160-03270890", "16003270890", "CX596", "20251123"])
            ws.append([None, "16003270891", "cx597", "20251124"])
            ws.append(["160-03270892", None, "CX598", "20251125"])
            
            # 保存测试文件
            wb.save(test_file_path)
            print(f"创建测试文件: {test_file_path}")
            
            # 测试派送文件处理
            print("\n=== 测试派送文件处理 ===")
            processor = FileProcessor(temp_dir, "delivery")
            stats = processor.process()
            print(f"处理结果统计: {stats}")
            
            # 检查结果文件是否生成
            result_file = os.path.join(temp_dir, "result.xlsx")
            diff_file = os.path.join(temp_dir, "diff.xlsx")
            
            if os.path.exists(result_file):
                print(f"结果文件生成成功: {result_file}")
            else:
                print(f"结果文件生成失败: {result_file}")
                return False
            
            if os.path.exists(diff_file):
                print(f"差异文件生成成功: {diff_file}")
            else:
                print(f"差异文件生成失败: {diff_file}")
                return False
            
            # 测试清关文件处理
            print("\n=== 测试清关文件处理 ===")
            processor = FileProcessor(temp_dir, "customs")
            stats = processor.process()
            print(f"处理结果统计: {stats}")
            
        print("\n✅ 文件处理器测试通过！")
        return True
        
    except Exception as e:
        print(f"\n❌ 文件处理器测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_file_processor()
    sys.exit(0 if success else 1)
