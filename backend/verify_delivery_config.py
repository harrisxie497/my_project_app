"""
验证MySQL数据库中的DELIVERY配置
"""
from app.core.database import SessionLocal
from app.models.file_definition import FileDefinition
import json

print("=" * 80)
print("验证MySQL数据库中的DELIVERY配置")
print("=" * 80)

db = SessionLocal()

try:
    # 查询SOURCE配置
    source_def = db.query(FileDefinition).filter(
        FileDefinition.file_type == 'DELIVERY',
        FileDefinition.file_role == 'SOURCE'
    ).first()
    
    if source_def:
        print("\n【SOURCE配置】")
        print(f"  ID: {source_def.id}")
        print(f"  Sheet: {source_def.sheet_name}")
        print(f"  Header Row: {source_def.header_row}")
        print(f"  Data Start Row: {source_def.data_start_row}")
        print(f"  Enabled: {source_def.enabled}")
        print(f"  列数: {len(source_def.columns_json)}")
        print("\n  列定义:")
        for i, col in enumerate(source_def.columns_json, 1):
            print(f"    {i}. {col['col']}: {col['header']}")
    
    # 查询OUTPUT配置
    output_def = db.query(FileDefinition).filter(
        FileDefinition.file_type == 'DELIVERY',
        FileDefinition.file_role == 'OUTPUT'
    ).first()
    
    if output_def:
        print("\n【OUTPUT配置】")
        print(f"  ID: {output_def.id}")
        print(f"  Sheet: {output_def.sheet_name}")
        print(f"  Header Row: {output_def.header_row}")
        print(f"  Data Start Row: {output_def.data_start_row}")
        print(f"  Enabled: {output_def.enabled}")
        print(f"  列数: {len(output_def.columns_json)}")
        print("\n  列定义:")
        for i, col in enumerate(output_def.columns_json, 1):
            print(f"    {i}. {col['col']}: {col['header']}")
    
    print("\n" + "=" * 80)
    print("[OK] 配置验证完成")
    print("=" * 80)
    
except Exception as e:
    print(f"\n[FAIL] 错误: {str(e)}")
    import traceback
    traceback.print_exc()
finally:
    db.close()
