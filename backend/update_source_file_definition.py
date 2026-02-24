"""
更新file_definitions中的SOURCE配置，使其与原始文件的列名一致
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.models.file_definition import FileDefinition

def update_source_file_definition():
    """更新SOURCE文件定义"""
    print("=" * 100)
    print("更新SOURCE文件定义")
    print("=" * 100)
    
    db_session = SessionLocal()
    
    try:
        # 查询SOURCE文件定义
        source_file_def = db_session.query(FileDefinition).filter(
            FileDefinition.file_type == 'CUSTOMS',
            FileDefinition.file_role == 'SOURCE'
        ).first()
        
        if source_file_def:
            print(f"\n更新前的SOURCE文件定义:")
            print(f"  ID: {source_file_def.id}")
            print(f"  文件类型: {source_file_def.file_type}")
            print(f"  文件角色: {source_file_def.file_role}")
            print(f"  工作表名称: {source_file_def.sheet_name}")
            
            # 更新列定义
            new_columns_json = [
                {'col': 'A', 'header': '会员编号'},
                {'col': 'B', 'header': '序号'},
                {'col': 'C', 'header': 'HAWB番号'},
                {'col': 'D', 'header': '現地問合せ番号'},
                {'col': 'E', 'header': '貨物個数'},
                {'col': 'F', 'header': '貨物重量'},
                {'col': 'G', 'header': '重量単位コード'},
                {'col': 'H', 'header': '品名'},
                {'col': 'I', 'header': '材质'},
                {'col': 'J', 'header': '收件人名（删）'},
                {'col': 'K', 'header': '輸入者名'},
                {'col': 'L', 'header': '英文邮编录入(删)'},
                {'col': 'M', 'header': '收件人地址(删)2'},
                {'col': 'N', 'header': '輸入者住所（删）'},
                {'col': 'O', 'header': '提取门牌(删)'},
                {'col': 'P', 'header': '輸入者住所'},
                {'col': 'Q', 'header': '輸入者 郵便番号'},
                {'col': 'R', 'header': '輸入者電話番号'},
                {'col': 'S', 'header': '輸出者名'},
                {'col': 'T', 'header': '輸出者住所'},
                {'col': 'U', 'header': 'インボイス価格条件コード'},
                {'col': 'V', 'header': 'インボイス通貨コード'},
                {'col': 'W', 'header': 'インボイス価格'},
                {'col': 'X', 'header': '单价（删）'},
                {'col': 'Y', 'header': '運賃区分コード'},
                {'col': 'Z', 'header': '運賃通貨コード'},
                {'col': 'AA', 'header': '運賃'},
                {'col': 'AB', 'header': '原産地コード'},
                {'col': 'AC', 'header': '備考'},
                {'col': 'AD', 'header': '收件人名（日文）'},
                {'col': 'AE', 'header': '收件人地址'},
                {'col': 'AF', 'header': '收件人电话'},
                {'col': 'AG', 'header': '收件人邮编'},
                {'col': 'AH', 'header': '依赖人名'},
                {'col': 'AI', 'header': '依赖人地址'},
                {'col': 'AJ', 'header': '依赖人电话'},
                {'col': 'AK', 'header': '收件地址识别码'},
                {'col': 'AL', 'header': '电商货识别码'},
                {'col': 'AM', 'header': '电商平台码'},
                {'col': 'AN', 'header': '电商平台名称'},
                {'col': 'AO', 'header': '系统预留列，不可使用'},
                {'col': 'AU', 'header': '收件人省州（删）'},
                {'col': 'AV', 'header': '收件人城市（删）'},
                {'col': 'AW', 'header': '收件人地址（删）'},
                {'col': 'AX', 'header': '申报品名（删）'},
                {'col': 'AY', 'header': '材质(删)'},
                {'col': 'AZ', 'header': '单价（删）'},
                {'col': 'BA', 'header': '发货地址（删）'},
                {'col': 'BB', 'header': '发货省（删）'},
                {'col': 'BC', 'header': '发货市（删）'},
                {'col': 'BD', 'header': '收件人地址2（删）'}
            ]
            
            source_file_def.columns_json = new_columns_json
            db_session.commit()
            
            print(f"\n更新后的SOURCE文件定义:")
            print(f"  ID: {source_file_def.id}")
            print(f"  文件类型: {source_file_def.file_type}")
            print(f"  文件角色: {source_file_def.file_role}")
            print(f"  工作表名称: {source_file_def.sheet_name}")
            print(f"  列数: {len(source_file_def.columns_json)}")
            
            print(f"\n列定义（共{len(source_file_def.columns_json)}列）:")
            for col in source_file_def.columns_json:
                print(f"  {col['col']}: {col['header']}")
            
            print(f"\n✓ 更新成功！")
        else:
            print(f"\n未找到SOURCE文件定义")
    
    except Exception as e:
        print(f"更新失败: {e}")
        import traceback
        traceback.print_exc()
        db_session.rollback()
    
    finally:
        db_session.close()
    
    print("\n" + "=" * 100)
    print("更新完成")
    print("=" * 100)

if __name__ == "__main__":
    update_source_file_definition()
