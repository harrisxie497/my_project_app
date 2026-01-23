#!/usr/bin/env python3
"""
使用真实的源文件测试文件处理器
"""

import os
import sys
import tempfile
import shutil

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.file_processor import FileProcessor

def test_real_delivery_file():
    """使用真实的派送文件源文件测试"""
    print("开始使用真实源文件测试...")
    
    try:
        # 真实源文件路径
        source_file_path = "c:\\Users\\harris.xie\\Documents\\trae_projects\\japan\\docs\\佐川指定时间带表格源文件（对应 派送文件成品）.xlsx"
        
        # 创建测试目录（保留结果文件）
        test_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_results")
        os.makedirs(test_dir, exist_ok=True)
        print(f"创建测试目录: {test_dir}")
        
        # 复制源文件到测试目录
        original_file_path = os.path.join(test_dir, "original.xlsx")
        shutil.copy2(source_file_path, original_file_path)
        print(f"复制源文件到测试目录: {original_file_path}")
        
        # 测试派送文件处理
        print("\n=== 测试派送文件处理 ===")
        processor = FileProcessor(test_dir, "delivery")
        stats = processor.process()
        print(f"处理结果统计: {stats}")
        
        # 检查结果文件是否生成
        result_file = os.path.join(test_dir, "result.xlsx")
        diff_file = os.path.join(test_dir, "diff.xlsx")
        
        if os.path.exists(result_file):
            print(f"✅ 结果文件生成成功: {result_file}")
        else:
            print(f"❌ 结果文件生成失败: {result_file}")
            return False
        
        if os.path.exists(diff_file):
            print(f"✅ 差异文件生成成功: {diff_file}")
        else:
            print(f"❌ 差异文件生成失败: {diff_file}")
            return False
        
        print(f"\n✅ 测试完成！所有文件已生成到: {test_dir}")
        return True
        
    except Exception as e:
        print(f"\n❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_real_delivery_file()
    sys.exit(0 if success else 1)
