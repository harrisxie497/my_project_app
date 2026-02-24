"""
对比file_definitions的OUTPUT的columns_json顺序与用户提到的表头顺序
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.models.file_definition import FileDefinition

def compare_orders():
    """对比两个顺序"""
    print("=" * 100)
    print("对比file_definitions的OUTPUT的columns_json顺序与用户提到的表头顺序")
    print("=" * 100)
    
    # 用户提到的表头顺序
    user_headers = ['会员编号', '序号', 'HAWB番号', '貨物個数', '重量単位コード', '品名', '材质', '貨物重量', '現地問合せ番号', '輸入者 郵便番号', '輸入者電話番号', '輸出者名', '輸出者住所', 'インボイス価格条件コード', 'インボイス通貨コード', 'インボイス価格', '運賃区分コード', '運賃通貨コード', '運賃', '原産地コード', '備考', '收件人名（日文）', '收件人地址', '收件人电话', '收件人邮编', '依赖人名', '依赖人地址', '依赖人电话', '收件地址识别码', '电商货识别码', '电商平台码', '电商平台名称', '系统预留列，不可使用', '輸入者名', '輸入者住所']
    
    print(f"\n用户提到的表头顺序（共{len(user_headers)}列）:")
    for idx, header in enumerate(user_headers, start=1):
        print(f"  {idx}. {header}")
    
    # 查询file_definitions中OUTPUT的columns_json
    db_session = SessionLocal()
    
    try:
        output_file_def = db_session.query(FileDefinition).filter(
            FileDefinition.file_type == 'CUSTOMS',
            FileDefinition.file_role == 'OUTPUT'
        ).first()
        
        if output_file_def:
            columns_json = output_file_def.columns_json
            output_headers = [col.get('header', '') for col in columns_json]
            
            print(f"\n\nfile_definitions的OUTPUT的columns_json顺序（共{len(output_headers)}列）:")
            for idx, header in enumerate(output_headers, start=1):
                print(f"  {idx}. {header}")
            
            # 比较两个顺序
            print(f"\n\n比较两个顺序:")
            if output_headers == user_headers:
                print("  ✓ 两个顺序完全一致")
            else:
                print("  ✗ 两个顺序不一致")
                
                # 找出不一致的地方
                print(f"\n  不一致的列:")
                max_len = max(len(output_headers), len(user_headers))
                for idx in range(max_len):
                    output_header = output_headers[idx] if idx < len(output_headers) else "（无）"
                    user_header = user_headers[idx] if idx < len(user_headers) else "（无）"
                    if output_header != user_header:
                        print(f"    第{idx+1}列: file_definitions='{output_header}', 用户提到的='{user_header}'")
        else:
            print("未找到OUTPUT文件定义")
    
    except Exception as e:
        print(f"查询失败: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        db_session.close()
    
    print("\n" + "=" * 100)
    print("对比完成")
    print("=" * 100)

if __name__ == "__main__":
    compare_orders()
