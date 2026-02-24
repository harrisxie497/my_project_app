"""
查看当前DELIVERY的file_definitions配置
"""
from app.core.database import SessionLocal
from app.models.file_definition import FileDefinition
import json

print("=" * 80)
print("查看DELIVERY的file_definitions配置")
print("=" * 80)

db = SessionLocal()

try:
    # 查询所有DELIVERY的file_definitions
    file_defs = db.query(FileDefinition).filter(
        FileDefinition.file_type == 'DELIVERY'
    ).all()
    
    print(f"\n找到 {len(file_defs)} 个配置:")
    print("=" * 80)
    
    for fd in file_defs:
        print(f"\n【{fd.file_role}配置】")
        print(f"ID: {fd.id}")
        print(f"Sheet: {fd.sheet_name}")
        print(f"Header Row: {fd.header_row}")
        print(f"Data Start Row: {fd.data_start_row}")
        print(f"Enabled: {fd.enabled}")
        print(f"\nColumns ({len(fd.columns_json)} 列):")
        print("-" * 80)
        
        for idx, col in enumerate(fd.columns_json, 1):
            col_letter = col.get('col', '')
            col_header = col.get('header', '')
            print(f"{idx:2d}. {col_letter}: {col_header}")
    
    print("\n" + "=" * 80)
    
except Exception as e:
    print(f"错误: {str(e)}")
    import traceback
    traceback.print_exc()
finally:
    db.close()
