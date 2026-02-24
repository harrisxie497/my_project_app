"""
检查用户提到的表头顺序是否与field_pipelines的order_num顺序一致
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.models.field_pipeline import FieldPipeline

def check_field_pipelines_order():
    """检查field_pipelines的order_num顺序"""
    print("=" * 100)
    print("检查field_pipelines的order_num顺序")
    print("=" * 100)
    
    db_session = SessionLocal()
    
    try:
        # 查询field_pipelines
        field_pipelines = db_session.query(FieldPipeline).filter(
            FieldPipeline.file_type.like('%CUSTOMS%')
        ).order_by(FieldPipeline.order_num).all()
        
        print(f"\nfield_pipelines的order_num顺序（共{len(field_pipelines)}个）:")
        for idx, fp in enumerate(field_pipelines, start=1):
            print(f"  {idx}. order_num: {fp.order_num}, target_col: {fp.target_col}, target_header: {fp.target_header}")
        
        # 提取表头顺序
        pipeline_headers = [fp.target_header for fp in field_pipelines]
        
        # 用户提到的表头顺序
        user_headers = ['会员编号', '序号', 'HAWB番号', '貨物個数', '重量単位コード', '品名', '材质', '貨物重量', '現地問合せ番号', '輸入者 郵便番号', '輸入者電話番号', '輸出者名', '輸出者住所', 'インボイス価格条件コード', 'インボイス通貨コード', 'インボイス価格', '運賃区分コード', '運賃通貨コード', '運賃', '原産地コード', '備考', '收件人名（日文）', '收件人地址', '收件人电话', '收件人邮编', '依赖人名', '依赖人地址', '依赖人电话', '收件地址识别码', '电商货识别码', '电商平台码', '电商平台名称', '系统预留列，不可使用', '輸入者名', '輸入者住所']
        
        print(f"\n\n用户提到的表头顺序:")
        for idx, header in enumerate(user_headers, start=1):
            print(f"  {idx}. {header}")
        
        # 比较两个顺序
        print(f"\n\n比较field_pipelines的order_num顺序与用户提到的表头顺序:")
        if pipeline_headers == user_headers:
            print("  ✓ 两个顺序完全一致")
        else:
            print("  ✗ 两个顺序不一致")
            
            # 找出不一致的地方
            print(f"\n  不一致的列:")
            max_len = max(len(pipeline_headers), len(user_headers))
            for idx in range(max_len):
                pipeline_header = pipeline_headers[idx] if idx < len(pipeline_headers) else "（无）"
                user_header = user_headers[idx] if idx < len(user_headers) else "（无）"
                if pipeline_header != user_header:
                    print(f"    第{idx+1}列: field_pipelines='{pipeline_header}', 用户提到的='{user_header}'")
    
    except Exception as e:
        print(f"查询失败: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        db_session.close()
    
    print("\n" + "=" * 100)
    print("检查完成")
    print("=" * 100)

if __name__ == "__main__":
    check_field_pipelines_order()
