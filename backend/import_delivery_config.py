"""
从JSON文件导入DELIVERY的file_definitions配置
"""
from app.core.database import SessionLocal
from app.models.file_definition import FileDefinition
import json
import os

print("=" * 80)
print("导入DELIVERY的file_definitions配置")
print("=" * 80)

# 检查配置文件是否存在
config_file = 'delivery_file_definitions_config.json'
if not os.path.exists(config_file):
    print(f"[FAIL] 配置文件不存在: {config_file}")
    print("\n请先运行 export_delivery_config.py 导出配置")
    exit(1)

# 读取配置文件
with open(config_file, 'r', encoding='utf-8') as f:
    config = json.load(f)

print("\n【要导入的配置】")
print("-" * 80)
for role, fd_config in config.items():
    print(f"\n{role}:")
    print(f"  Sheet: {fd_config.get('sheet_name')}")
    print(f"  列数: {len(fd_config.get('columns', []))}")
    print(f"  前3列: {fd_config.get('columns', [])[:3]}")

# 确认导入
print("\n" + "=" * 80)
choice = input("是否确认导入配置？(y/n): ").strip().lower()

if choice != 'y':
    print("\n[取消] 配置未导入")
    exit(0)

# 执行导入
db = SessionLocal()

try:
    # 更新SOURCE配置
    if 'SOURCE' in config:
        source_config = config['SOURCE']
        source_def = db.query(FileDefinition).filter(
            FileDefinition.file_type == 'DELIVERY',
            FileDefinition.file_role == 'SOURCE'
        ).first()
        
        if source_def:
            source_def.sheet_name = source_config.get('sheet_name')
            source_def.header_row = source_config.get('header_row')
            source_def.data_start_row = source_config.get('data_start_row')
            source_def.enabled = source_config.get('enabled', True)
            source_def.columns_json = source_config.get('columns', [])
            print(f"\n[OK] SOURCE配置已更新")
    
    # 更新OUTPUT配置
    if 'OUTPUT' in config:
        output_config = config['OUTPUT']
        output_def = db.query(FileDefinition).filter(
            FileDefinition.file_type == 'DELIVERY',
            FileDefinition.file_role == 'OUTPUT'
        ).first()
        
        if output_def:
            output_def.sheet_name = output_config.get('sheet_name')
            output_def.header_row = output_config.get('header_row')
            output_def.data_start_row = output_config.get('data_start_row')
            output_def.enabled = output_config.get('enabled', True)
            output_def.columns_json = output_config.get('columns', [])
            print(f"[OK] OUTPUT配置已更新")
    
    # 提交更改
    db.commit()
    
    print("\n" + "=" * 80)
    print("[OK] 所有配置已成功保存到数据库")
    print("=" * 80)
    
except Exception as e:
    print(f"\n[FAIL] 错误: {str(e)}")
    import traceback
    traceback.print_exc()
    db.rollback()
finally:
    db.close()
