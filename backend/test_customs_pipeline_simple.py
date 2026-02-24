#!/usr/bin/env python3
"""
测试CUSTOMS文件处理全流程（简化版）
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.models.field_pipeline import FieldPipeline
from app.models.rule_definition import RuleDefinition
from app.services.field_handlers_v2 import process_field_v2

def test_customs_pipeline():
    """测试CUSTOMS pipeline处理"""
    
    # 测试数据（模拟Excel读取的数据）
    test_data = [
        {'A': 'test1', 'B': 'data1', 'C': '2026-02-06', 'F': '1.234', 'H': '飞轮玩具(12-24M)', 'I': 'ABS(100%)', 'X': '田中 太郎', 'Y': '東京都渋谷区渋谷1-2-3', 'J': '山田 太郎', 'K': '東京都渋谷区渋谷1-2-3'},
        {'A': 'test2', 'B': 'data2', 'C': '2026-02-07', 'F': '2.567', 'H': 'T恤(L码)', 'I': '棉(100%)', 'X': '鈴木 花子', 'Y': '大阪府大阪市中央区1-2-3', 'J': '田中 花子', 'K': '大阪府大阪市中央区1-2-3'},
        {'A': 'test3', 'B': 'data3', 'C': '2026-02-08', 'F': '0.890', 'H': '连衣裙(XL码)', 'I': '涤纶(100%)', 'X': '佐藤 一郎', 'Y': '愛知県名古屋市中区1-2-3', 'J': '鈴木 一郎', 'K': '愛知県名古屋市中区1-2-3'},
        {'A': 'test4', 'B': 'data4', 'C': '2026-02-09', 'F': '3.500', 'H': '鞋子', 'I': '皮革', 'X': '田中', 'Y': '大阪府大阪市中央区1-2-3', 'J': '田中 花子', 'K': '大阪府大阪市中央区1-2-3'},
        {'A': 'test5', 'B': 'data5', 'C': '2026-02-10', 'F': '5.123kg', 'H': '包包', 'I': '帆布', 'X': '鈴木', 'Y': '愛知県名古屋市中区1-2-3', 'J': '鈴木 一郎', 'K': '愛知県名古屋市中区1-2-3'},
        {'A': 'test6', 'B': 'data6', 'C': '2026-02-11', 'F': '', 'H': '帽子', 'I': '棉', 'X': '佐藤', 'Y': '東京都渋谷区渋谷1-2-3', 'J': '佐藤 一郎', 'K': '東京都渋谷区渋谷1-2-3'},
        {'A': 'test7', 'B': 'data7', 'C': '2026-02-12', 'F': None, 'H': '手套', 'I': '羊毛', 'X': '田中', 'Y': '大阪府大阪市中央区1-2-3', 'J': '田中 花子', 'K': '大阪府大阪市中央区1-2-3'},
    ]
    
    print("=" * 80)
    print("CUSTOMS文件处理全流程测试（简化版）")
    print("=" * 80)
    
    # 获取pipeline配置
    db = SessionLocal()
    try:
        # 获取所有启用的pipeline配置
        pipelines = db.query(FieldPipeline).filter(
            FieldPipeline.file_type == 'CUSTOMS',
            FieldPipeline.enabled == True
        ).order_by(FieldPipeline.order_num).all()
        
        print(f"\n找到 {len(pipelines)} 个启用的pipeline配置：")
        
        # 获取规则定义
        rules = db.query(RuleDefinition).all()
        rule_params_json = {}
        for rule in rules:
            rule_params_json[rule.rule_ref] = rule.schema_json
        
        # 测试每个字段
        test_columns = ['F', 'H', 'I', 'J', 'K', 'X', 'Y']
        
        for col in test_columns:
            col_pipelines = [p for p in pipelines if p.target_col == col]
            if not col_pipelines:
                print(f"\n列 {col}: 未找到pipeline配置")
                continue
            
            pipeline = col_pipelines[0]
            print(f"\n列 {col} ({pipeline.target_header}):")
            print(f"  rule_ref: {pipeline.rule_ref}")
            print(f"  map_op: {pipeline.map_op}")
            print(f"  source_cols: {pipeline.source_cols}")
            print(f"  field_type: {pipeline.field_type}")
            
            # 构建pipeline配置
            full_pipeline = {
                'target_col': pipeline.target_col,
                'target_header': pipeline.target_header,
                'rule_ref': pipeline.rule_ref,
                'source_cols': pipeline.source_cols,
                'rule_params_json': rule_params_json,
                'depends_on': pipeline.depends_on,
                'field_type': pipeline.field_type,
                'map_op': pipeline.map_op,
            }
            
            # 处理数据
            print(f"\n处理数据：")
            for i, row_data in enumerate(test_data, 1):
                row_data['_row_index'] = i - 1
                original_value = row_data.get(col, '')
                
                try:
                    processed_value = process_field_v2(
                        map_op=full_pipeline.get('map_op'),
                        source_cols=full_pipeline.get('source_cols', []),
                        field_type=full_pipeline.get('field_type', 'TEXT'),
                        rule_ref=full_pipeline.get('rule_ref', []),
                        row=row_data,
                        pipeline=full_pipeline,
                    )
                    
                    status = 'OK' if str(processed_value) != str(original_value) else '=='
                    print(f"  行{i}: {repr(original_value):20} -> {repr(str(processed_value) if processed_value is not None else 'None'):20} {status}")
                    
                except Exception as e:
                    print(f"  行{i}: {repr(original_value):20} -> ERROR: {str(e)}")
        
        # 验证F列结果
        print(f"\n" + "=" * 80)
        print("F列（货物重量）验证：")
        print("=" * 80)
        
        f_pipeline = [p for p in pipelines if p.target_col == 'F'][0]
        f_full_pipeline = {
            'target_col': f_pipeline.target_col,
            'target_header': f_pipeline.target_header,
            'rule_ref': f_pipeline.rule_ref,
            'source_cols': f_pipeline.source_cols,
            'rule_params_json': rule_params_json,
        }
        
        print(f"\nF列配置：")
        print(f"  rule_ref: {f_pipeline.rule_ref}")
        print(f"  期望: 保留1位小数，空值返回空字符串")
        
        print(f"\nF列处理结果：")
        passed = 0
        failed = 0
        
        for i, row_data in enumerate(test_data, 1):
            row_data['_row_index'] = i - 1
            original_value = row_data.get('F', '')
            
            try:
                processed_value = process_field_v2(
                    map_op=f_full_pipeline.get('map_op'),
                    source_cols=f_full_pipeline.get('source_cols', []),
                    field_type=f_full_pipeline.get('field_type', 'TEXT'),
                    rule_ref=f_full_pipeline.get('rule_ref', []),
                    row=row_data,
                    pipeline=f_full_pipeline,
                )
                
                # 检查格式：应该是空字符串或一位小数
                if processed_value == '' or (isinstance(processed_value, str) and len(processed_value.split('.')) == 2 and len(processed_value.split('.')[1]) == 1):
                    print(f"  行{i}: {repr(original_value):20} -> {repr(processed_value):20} OK")
                    passed += 1
                else:
                    print(f"  行{i}: {repr(original_value):20} -> {repr(processed_value):20} FAIL")
                    failed += 1
                    
            except Exception as e:
                print(f"  行{i}: {repr(original_value):20} -> ERROR: {str(e)} ✗")
                failed += 1
        
        print(f"\n验证结果：通过 {passed}/{len(test_data)}，失败 {failed}/{len(test_data)}")
        
        if passed == len(test_data):
            print("\nOK: F列测试全部通过！")
        else:
            print(f"\nFAIL: F列测试有 {failed} 个失败")
        
    finally:
        db.close()
    
    print("\n" + "=" * 80)
    print("测试完成")
    print("=" * 80)

if __name__ == "__main__":
    test_customs_pipeline()
