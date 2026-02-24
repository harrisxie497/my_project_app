"""
更新DELIVERY的SOURCE配置以匹配实际用户文件
"""
from app.core.database import SessionLocal
from app.models.file_definition import FileDefinition
import json

print("=" * 80)
print("更新DELIVERY的SOURCE配置")
print("=" * 80)

db = SessionLocal()

try:
    # 查找SOURCE配置
    source_def = db.query(FileDefinition).filter(
        FileDefinition.file_type == 'DELIVERY',
        FileDefinition.file_role == 'SOURCE'
    ).first()
    
    if not source_def:
        print("[FAIL] 找不到DELIVERY的SOURCE配置")
    else:
        print(f"\n当前配置:")
        print(f"  Sheet: {source_def.sheet_name}")
        print(f"  列数: {len(source_def.columns_json)}")
        
        # 更新为实际的列配置（25列A-Y）
        new_columns = [
            {'col': 'A', 'header': 'お客様管理番号'},
            {'col': 'B', 'header': '佐川問合せ番号HAWB'},
            {'col': 'C', 'header': '配達指定日'},
            {'col': 'D', 'header': '時間帯指定'},
            {'col': 'E', 'header': '貨物個数'},
            {'col': 'F', 'header': 'お届け先人名'},
            {'col': 'G', 'header': 'お届け先住所'},
            {'col': 'H', 'header': 'お届け先電話'},
            {'col': 'I', 'header': 'お届け先郵便'},
            {'col': 'J', 'header': '依頼主'},
            {'col': 'K', 'header': '依頼主住所'},
            {'col': 'L', 'header': '依頼主郵便番号'},
            {'col': 'M', 'header': '依頼主電話'},
            {'col': 'N', 'header': '佐川顧客コード（固定）'},
            {'col': 'O', 'header': '記事欄2（品名）'},
            {'col': 'P', 'header': '記事欄2'},
            {'col': 'Q', 'header': '記事欄3'},
            {'col': 'R', 'header': '收件人省州（删）'},
            {'col': 'S', 'header': '收件人城市（删）'},
            {'col': 'T', 'header': '收件人地址1（删）'},
            {'col': 'U', 'header': '收件人地址2（删）'},
            {'col': 'V', 'header': '收件人地址3（删）'},
            {'col': 'W', 'header': '发货省（删）'},
            {'col': 'X', 'header': '发货市（删）'},
            {'col': 'Y', 'header': '发货地址（删）'}
        ]
        
        print(f"\n新配置:")
        print(f"  列数: {len(new_columns)}")
        print(f"  工作表名称: Speedy")  # 用户文件的工作表名是"Speedy"
        
        # 更新配置
        source_def.columns_json = new_columns
        source_def.sheet_name = 'Speedy'  # 更新工作表名称
        
        db.commit()
        db.refresh(source_def)
        
        print(f"\n[OK] 配置已更新")
        print(f"  Sheet: {source_def.sheet_name}")
        print(f"  列数: {len(source_def.columns_json)}")
        print(f"  前几列: {source_def.columns_json[:5]}")
    
    print("\n" + "=" * 80)
    print("[OK] DELIVERY SOURCE配置已更新完成")
    print("=" * 80)
    
except Exception as e:
    print(f"错误: {str(e)}")
    import traceback
    traceback.print_exc()
    db.rollback()
finally:
    db.close()
