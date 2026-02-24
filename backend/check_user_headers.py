"""
检查用户提到的表头顺序是否在日志中
"""

import re

def check_user_headers():
    """检查用户提到的表头顺序"""
    print("=" * 100)
    print("检查用户提到的表头顺序")
    print("=" * 100)
    
    log_file = r"C:\Users\harris.xie\Documents\trae_projects\japan\backend\logs\app.log"
    
    # 用户提到的表头顺序
    user_headers = ['会员编号', '序号', 'HAWB番号', '貨物個数', '重量単位コード', '品名', '材质', '貨物重量', '現地問合せ番号', '輸入者 郵便番号', '輸入者電話番号', '輸出者名', '輸出者住所', 'インボイス価格条件コード', 'インボイス通貨コード', 'インボイス価格', '運賃区分コード', '運賃通貨コード', '運賃', '原産地コード', '備考', '收件人名（日文）', '收件人地址', '收件人电话', '收件人邮编', '依赖人名', '依赖人地址', '依赖人电话', '收件地址识别码', '电商货识别码', '电商平台码', '电商平台名称', '系统预留列，不可使用', '輸入者名', '輸入者住所']
    
    print(f"\n用户提到的表头顺序（共{len(user_headers)}列）:")
    for idx, header in enumerate(user_headers, start=1):
        print(f"  {idx}. {header}")
    
    # 在日志中查找这个表头顺序
    with open(log_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # 查找包含"貨物個数"在"現地問合せ番号"之前的写入表头日志
    print(f"\n\n在日志中查找包含'貨物個数'在'現地問合せ番号'之前的写入表头日志:")
    for line in lines:
        if "写入表头" in line and "貨物個数" in line and "現地問合せ番号" in line:
            # 检查"貨物個数"是否在"現地問合せ番号"之前
            if line.index("貨物個数") < line.index("現地問合せ番号"):
                print(f"  {line.strip()}")
    
    # 查找包含"輸入者名"在最后的写入表头日志
    print(f"\n\n在日志中查找包含'輸入者名'在最后的写入表头日志:")
    for line in lines:
        if "写入表头" in line and "輸入者名" in line:
            # 检查"輸入者名"是否在最后
            if "輸入者名" in line and "輸入者住所" in line:
                # 提取表头列表
                match = re.search(r'\[.*\]', line)
                if match:
                    headers_str = match.group(0)
                    # 检查"輸入者名"和"輸入者住所"是否在最后
                    if headers_str.endswith("輸入者名', '輸入者住所']"):
                        print(f"  {line.strip()}")
    
    print("\n" + "=" * 100)
    print("检查完成")
    print("=" * 100)

if __name__ == "__main__":
    check_user_headers()
