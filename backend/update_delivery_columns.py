"""
修改DELIVERY的file_definitions的columns_json
"""
from app.core.database import SessionLocal
from app.models.file_definition import FileDefinition
import json

# ============================================
# 在这里配置您想要的列定义
# ============================================

# SOURCE配置 - 输入文件的列定义
SOURCE_COLUMNS = [
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
    {'col': 'Y', 'header': '发货地址（删）'},
]

# OUTPUT配置 - 输出文件的列定义
OUTPUT_COLUMNS = [
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
]

# ============================================
# 执行更新（无需修改以下代码）
# ============================================

print("=" * 80)
print("修改DELIVERY的file_definitions的columns_json")
print("=" * 80)

db = SessionLocal()

try:
    # 查找SOURCE配置
    source_def = db.query(FileDefinition).filter(
        FileDefinition.file_type == 'DELIVERY',
        FileDefinition.file_role == 'SOURCE'
    ).first()
    
    # 查找OUTPUT配置
    output_def = db.query(FileDefinition).filter(
        FileDefinition.file_type == 'DELIVERY',
        FileDefinition.file_role == 'OUTPUT'
    ).first()
    
    # 显示当前配置
    print("\n【当前SOURCE配置】")
    print("-" * 80)
    if source_def:
        print(f"Sheet: {source_def.sheet_name}")
        print(f"列数: {len(source_def.columns_json)}")
        print(f"前3列: {source_def.columns_json[:3]}")
    
    print("\n【当前OUTPUT配置】")
    print("-" * 80)
    if output_def:
        print(f"Sheet: {output_def.sheet_name}")
        print(f"列数: {len(output_def.columns_json)}")
        print(f"前3列: {output_def.columns_json[:3]}")
    
    # 显示新配置
    print("\n【新SOURCE配置】")
    print("-" * 80)
    print(f"列数: {len(SOURCE_COLUMNS)}")
    for idx, col in enumerate(SOURCE_COLUMNS, 1):
        print(f"{idx:2d}. {col['col']}: {col['header']}")
    
    print("\n【新OUTPUT配置】")
    print("-" * 80)
    print(f"列数: {len(OUTPUT_COLUMNS)}")
    for idx, col in enumerate(OUTPUT_COLUMNS, 1):
        print(f"{idx:2d}. {col['col']}: {col['header']}")
    
    # 确认更新
    print("\n" + "=" * 80)
    choice = input("是否确认更新配置？(y/n): ").strip().lower()
    
    if choice == 'y':
        # 更新SOURCE配置
        if source_def:
            source_def.columns_json = SOURCE_COLUMNS
            print(f"\n[OK] SOURCE配置已更新")
        
        # 更新OUTPUT配置
        if output_def:
            output_def.columns_json = OUTPUT_COLUMNS
            print(f"[OK] OUTPUT配置已更新")
        
        # 提交更改
        db.commit()
        
        print("\n" + "=" * 80)
        print("[OK] 所有配置已成功保存到数据库")
        print("=" * 80)
    else:
        print("\n[取消] 配置未更新")
    
except Exception as e:
    print(f"\n[FAIL] 错误: {str(e)}")
    import traceback
    traceback.print_exc()
    db.rollback()
finally:
    db.close()
