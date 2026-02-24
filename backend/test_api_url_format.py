"""
测试脚本：测试不同格式的汇率API URL
"""
import requests

api_key = "c06e7281b839d210bd636db0"

# 测试不同的URL格式
url_formats = [
    "https://v6.exchangerate-api.com/v6/latest?apikey={}&base={}&symbols={}",
    "https://v6.exchangerate-api.com/v6/latest?api_key={}&base={}&symbols={}",
    "https://v6.exchangerate-api.com/v6/{}/latest?apikey={}",
    "https://v6.exchangerate-api.com/v6/{}/pair/{}/JPY?apikey={}",
]

test_currency = "USD"

print("=" * 100)
print("测试不同格式的汇率API URL")
print("=" * 100)

for idx, url_format in enumerate(url_formats, 1):
    print(f"\n测试格式 {idx}:")
    print(f"URL模板: {url_format}")
    
    try:
        if "pair" in url_format:
            url = url_format.format(test_currency, api_key)
        elif len(url_format.split("{}")) == 3:
            url = url_format.format(api_key, test_currency, "JPY")
        elif "{}/pair" in url_format:
            url = url_format.format(test_currency, api_key)
        else:
            url = url_format.format(api_key, test_currency, "JPY")
        
        print(f"实际URL: {url[:100]}..." if len(url) > 100 else f"实际URL: {url}")
        
        response = requests.get(url, timeout=10)
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            print(f"[OK] 成功!")
            try:
                data = response.json()
                print(f"响应数据: {data}")
            except:
                print(f"响应文本: {response.text[:200]}")
        else:
            print(f"[FAIL] 失败: {response.text[:200]}")

    except Exception as e:
        print(f"[ERROR] 错误: {str(e)}")
