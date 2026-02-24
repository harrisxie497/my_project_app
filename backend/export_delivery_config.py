"""
导出DELIVERY的file_definitions配置到JSON文件
"""
from app.core.database import SessionLocal
from app.models.file_definition import FileDefinition
import json

print("=" * 80)
print("导出DELIVERY的file_definitions配置")
print("=" * 80)

db = SessionLocal()

try:
    file_defs = db.query(FileDefinition).filter(
        FileDefinition.file_type == 'DELIVERY'
    ).all()
    
    config = {}
    for fd in file_defs:
        config[fd.file_role] = {
            'id': str(fd.id),
            'sheet_name': fd.sheet_name,
            'header_row': fd.header_row,
            'data_start_row': fd.data_start_row,
            'enabled': fd.enabled,
            'columns': fd.columns_json
        }
    
    # 保存到文件
    output_file = 'delivery_file_definitions_config.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    
    print(f"\n[OK] 配置已导出到: {output_file}")
    print(f"  SOURCE: {len(config.get('SOURCE', {}).get('columns', []))} 列")
    print(f"  OUTPUT: {len(config.get('OUTPUT', {}).get('columns', []))} 列")
    print("\n" + "=" * 80)
    print("您可以编辑该JSON文件，然后使用下面的命令导入:")
    print("python import_delivery_config.py")
    print("=" * 80)
    
except Exception as e:
    print(f"错误: {str(e)}")
    import traceback
    traceback.print_exc()
finally:
    db.close()
