#!/usr/bin/env python3
"""
测试CUSTOMS文件处理全流程：从读取到写入
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.services.excel_reader import ExcelReader
from app.services.excel_writer import ExcelWriter
from app.services.customs_processor import CustomsProcessor
from app.core.database import SessionLocal
from app.models.field_pipeline import FieldPipeline
from app.models.rule_definition import RuleDefinition

def test_customs_full_pipeline():
    """测试CUSTOMS文件处理全流程"""
    
    # 测试文件路径
    input_file = 'c:/Users/harris.xie/Documents/trae_projects/japan/data/test_customs.xlsx'
    output_file = 'c:/Users/harris.xie/Documents/trae_projects/japan/data/test_customs_output.xlsx'
    
    print("=" * 80)
    print("CUSTOMS文件处理全流程测试")
    print("=" * 80)
    
    # 步骤1：读取Excel文件
    print("\n步骤1：读取Excel文件")
    print("-" * 80)
    
    try:
        reader = ExcelReader(input_file, sheet_name=0)
        data = reader.read_all()
        print(f"✅ 成功读取 {len(data)} 行数据")
        
        if len(data) > 0:
            print(f"  前3行数据示例：")
            for i in range(min(3, len(data))):
                print(f"  行{i+1}: {data[i].get('F', 'N/A')}")
        
    except FileNotFoundError:
        print(f"❌ 文件不存在: {input_file}")
        print("  使用测试数据替代...")
        
        # 创建测试数据
        data = [
            {'A': 'test1', 'B': 'data1', 'C': '2026-02-06', 'F': '1.234', 'H': '飞轮玩具(12-24M)', 'I': 'ABS(100%)', 'X': '田中 太郎', 'Y': '東京都渋谷区渋谷1-2-3', 'J': '山田 太郎', 'K': '東京都渋谷区渋谷1-2-3'},
            {'A': 'test2', 'B': 'data2', 'C': '2026-02-07', 'F': '2.567', 'H': 'T恤(L码)', 'I': '棉(100%)', 'X': '鈴木 花子', 'Y': '大阪府大阪市中央区1-2-3', 'J': '田中 花子', 'K': '大阪府大阪市中央区1-2-3'},
            {'A': 'test3', 'B': 'data3', 'C': '2026-02-08', 'F': '0.890', 'H': '连衣裙(XL码)', 'I': '涤纶(100%)', 'X': '佐藤 一郎', 'Y': '愛知県名古屋市中区1-2-3', 'J': '鈴木 一郎', 'K': '愛知県名古屋市中区1-2-3'},
            {'A': 'test4', 'B': 'data4', 'C': '2026-02-09', 'F': '3.500', 'H': '鞋子', 'I': '皮革', 'X': '田中', 'Y': '大阪府大阪市中央区1-2-3', 'J': '田中 花子', 'K': '大阪府大阪市中央区1-2-3'},
            {'A': 'test5', 'B': 'data5', 'C': '2026-02-10', 'F': '5.123kg', 'H': '包包', 'I': '帆布', 'X': '鈴木', 'Y': '愛知県名古屋市中区1-2-3', 'J': '鈴木 一郎', 'K': '愛知県名古屋市中区1-2-3'},
            {'A': 'test6', 'B': 'data6', 'C': '2026-02-11', 'F': '', 'H': '帽子', 'I': '棉', 'X': '佐藤', 'Y': '東京都渋谷区渋谷1-2-3', 'J': '佐藤 一郎', 'K': '東京都渋谷区渋谷1-2-3'},
            {'A': 'test7', 'B': 'data7', 'C': '2026-02-12', 'F': None, 'H': '手套', 'I': '羊毛', 'X': '田中', 'Y': '大阪府大阪市中央区1-2-3', 'J': '田中 花子', 'K': '大阪府大阪市中央区1-2-3'},
        ]
        print(f"✅ 创建 {len(data)} 行测试数据")
    
    # 步骤2：查看F列的pipeline配置
    print("\n步骤2：查看F列的pipeline配置")
    print("-" * 80)
    
    db = SessionLocal()
    try:
        pipelines = db.query(FieldPipeline).filter(
            FieldPipeline.target_col == 'F',
            FieldPipeline.file_type == 'CUSTOMS',
            FieldPipeline.enabled == True
        ).all()
        
        print(f"找到 {len(pipelines)} 个F列配置：")
        for i, p in enumerate(pipelines, 1):
            print(f"  {i}. rule_ref: {p.rule_ref}, target_header: {p.target_header}")
        
        if len(pipelines) > 0:
            pipeline = pipelines[0]
            print(f"\n使用第一个配置进行测试：")
            print(f"  rule_ref: {pipeline.rule_ref}")
            print(f"  source_cols: {pipeline.source_cols}")
            
            # 获取规则参数
            rules = db.query(RuleDefinition).filter(
                RuleDefinition.rule_ref.in_(pipeline.rule_ref)
            ).all()
            
            for rule in rules:
                print(f"\n规则 {rule.rule_ref}:")
                print(f"  rule_type: {rule.rule_type}")
                print(f"  handler: {rule.schema_json.get('handler')}")
                print(f"  desc: {rule.schema_json.get('desc')}")
    finally:
        db.close()
    
    # 步骤3：处理数据
    print("\n步骤3：处理数据")
    print("-" * 80)
    
    try:
        processor = CustomsProcessor(file_type='CUSTOMS')
        processed_data = processor.process_batch(data)
        print(f"✅ 成功处理 {len(processed_data)} 行数据")
        
        # 显示F列处理结果
        print(f"\nF列（货物重量）处理结果：")
        for i, (original, processed) in enumerate(zip([row.get('F', '') for row in data], [row.get('F', '') for row in processed_data]), 1):
            print(f"  行{i}: {repr(original)} -> {repr(processed)}")
        
    except Exception as e:
        print(f"❌ 处理失败: {e}")
        import traceback
        traceback.print_exc()
        processed_data = data  # 使用原始数据
    
    # 步骤4：写入Excel文件
    print("\n步骤4：写入Excel文件")
    print("-" * 80)
    
    try:
        # 获取列名（从处理后的数据）
        if len(processed_data) > 0:
            headers = list(processed_data[0].keys())
        else:
            headers = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'X', 'Y']
        
        writer = ExcelWriter(output_file, sheet_name="Processed", headers=headers)
        
        # 添加标题行
        writer.write_headers(headers)
        
        # 添加数据行
        for row in processed_data:
            writer.write_row([row.get(h, '') for h in headers])
        
        writer.save()
        
        print(f"✅ 成功写入 {len(processed_data)} 行数据到 {output_file}")
        print(f"  列数: {len(headers)}")
        
    except Exception as e:
        print(f"❌ 写入失败: {e}")
        import traceback
        traceback.print_exc()
    
    # 步骤5：验证结果
    print("\n步骤5：验证结果")
    print("-" * 80)
    
    # 验证F列的处理结果
    f_values = [row.get('F', '') for row in processed_data]
    
    print(f"\nF列值验证（应保留1位小数，空值返回空字符串）：")
    passed = 0
    failed = 0
    
    for i, (orig, proc) in enumerate(zip([row.get('F', '') for row in data], f_values), 1):
        # 检查格式
        if proc == '' or (isinstance(proc, str) and len(proc.split('.')) == 2 and len(proc.split('.')[1]) == 1):
            print(f"  行{i}: {repr(orig)} -> {repr(proc)} ✓")
            passed += 1
        else:
            print(f"  行{i}: {repr(orig)} -> {repr(proc)} ✗ (格式错误)")
            failed += 1
    
    print(f"\n验证结果：通过 {passed}/{len(f_values)}，失败 {failed}/{len(f_values)}")
    
    # 步骤6：测试其他AI列
    print("\n步骤6：验证其他AI列的处理")
    print("-" * 80)
    
    ai_columns = [
        ('H', '品名'),
        ('I', '材质'),
        ('J', '輸入者名'),
        ('K', '輸入者住所'),
        ('X', '收件人名'),
        ('Y', '收件人地址'),
    ]
    
    for col, name in ai_columns:
        print(f"\n{name}列（{col}）：")
        values = [row.get(col, '') for row in processed_data[:3]]  # 显示前3行
        for i, val in enumerate(values, 1):
            print(f"  行{i}: {repr(val)}")
    
    print("\n" + "=" * 80)
    print("测试完成")
    print("=" * 80)

if __name__ == "__main__":
    test_customs_full_pipeline()
