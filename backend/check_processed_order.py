"""
检查处理顺序是否与用户提到的表头顺序一致
"""

import re

def check_processed_order():
    """检查处理顺序"""
    print("=" * 100)
    print("检查处理顺序是否与用户提到的表头顺序一致")
    print("=" * 100)
    
    log_file = r"C:\Users\harris.xie\Documents\trae_projects\japan\backend\logs\app.log"
    
    # 用户提到的表头顺序
    user_headers = ['会员编号', '序号', 'HAWB番号', '貨物個数', '重量単位コード', '品名', '材质', '貨物重量', '現地問合せ番号', '輸入者 郵便番号', '輸入者電話番号', '輸出者名', '輸出者住所', 'インボイス価格条件コード', 'インボイス通貨コード', 'インボイス価格', '運賃区分コード', '運賃通貨コード', '運賃', '原産地コード', '備考', '收件人名（日文）', '收件人地址', '收件人电话', '收件人邮编', '依赖人名', '依赖人地址', '依赖人电话', '收件地址识别码', '电商货识别码', '电商平台码', '电商平台名称', '系统预留列，不可使用', '輸入者名', '輸入者住所']
    
    print(f"\n用户提到的表头顺序（共{len(user_headers)}列）:")
    for idx, header in enumerate(user_headers, start=1):
        print(f"  {idx}. {header}")
    
    # 在日志中查找"处理列配置"日志，看看处理顺序
    with open(log_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # 提取处理顺序
    processed_cols = []
    for line in lines:
        if "处理列配置 - 列名:" in line and "customs_processor" in line:
            # 提取列名
            match = re.search(r"列名: ([A-Z]+),", line)
            if match:
                col_letter = match.group(1)
                processed_cols.append(col_letter)
    
    print(f"\n\n处理顺序（列字母，共{len(processed_cols)}列）:")
    for idx, col_letter in enumerate(processed_cols, start=1):
        print(f"  {idx}. {col_letter}")
    
    # 将列字母映射到表头
    col_to_header = {
        'A': '会员编号', 'B': '序号', 'C': 'HAWB番号', 'D': '現地問合せ番号',
        'E': '貨物個数', 'F': '貨物重量', 'G': '重量単位コード', 'H': '品名',
        'I': '材质', 'J': '輸入者名', 'K': '輸入者住所', 'L': '輸入者 郵便番号',
        'M': '輸入者電話番号', 'N': '輸出者名', 'O': '輸出者住所',
        'P': 'インボイス価格条件コード', 'Q': 'インボイス通貨コード', 'R': 'インボイス価格',
        'S': '運賃区分コード', 'T': '運賃通貨コード', 'U': '運賃', 'V': '原産地コード',
        'W': '備考', 'X': '收件人名（日文）', 'Y': '收件人地址', 'Z': '收件人电话',
        'AA': '收件人邮编', 'AB': '依赖人名', 'AC': '依赖人地址', 'AD': '依赖人电话',
        'AE': '收件地址识别码', 'AF': '电商货识别码', 'AG': '电商平台码',
        'AH': '电商平台名称', 'AI': '系统预留列，不可使用'
    }
    
    processed_headers = [col_to_header.get(col, col) for col in processed_cols]
    
    print(f"\n\n处理顺序（表头，共{len(processed_headers)}列）:")
    for idx, header in enumerate(processed_headers, start=1):
        print(f"  {idx}. {header}")
    
    # 比较两个顺序
    print(f"\n\n比较两个顺序:")
    if processed_headers == user_headers:
        print("  ✓ 处理顺序与用户提到的表头顺序一致")
    else:
        print("  ✗ 处理顺序与用户提到的表头顺序不一致")
        
        # 找出不一致的地方
        print(f"\n  不一致的列:")
        max_len = max(len(processed_headers), len(user_headers))
        for idx in range(max_len):
            processed_header = processed_headers[idx] if idx < len(processed_headers) else "（无）"
            user_header = user_headers[idx] if idx < len(user_headers) else "（无）"
            if processed_header != user_header:
                print(f"    第{idx+1}列: 处理顺序='{processed_header}', 用户提到的='{user_header}'")
    
    print("\n" + "=" * 100)
    print("检查完成")
    print("=" * 100)

if __name__ == "__main__":
    check_processed_order()
