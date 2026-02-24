"""
测试脚本：读取.env文件
"""
import os
from dotenv import load_dotenv

# 加载.env文件
env_path = r"c:\Users\harris.xie\Documents\trae_projects\japan\backend\.env"
load_dotenv(env_path)

# 读取环境变量
api_key = os.getenv('EXCHANGE_RATE_API_KEY', '')
api_url = os.getenv('EXCHANGE_RATE_API_URL', '')

print("=" * 100)
print("读取.env文件")
print("=" * 100)
print(f"API URL: {api_url}")
print(f"API KEY: {api_key[:20]}..." if api_key else "未配置")
print(f"API KEY 长度: {len(api_key)}")
print("")

# 也测试DEEPSEEK的配置
deepseek_key = os.getenv('DEEPSEEK_API_KEY', '')
deepseek_url = os.getenv('DEEPSEEK_API_URL', '')

print("DEEPSEEK配置:")
print(f"  API URL: {deepseek_url}")
print(f"  API KEY: {deepseek_key[:20]}..." if deepseek_key else "未配置")
print(f"  API KEY 长度: {len(deepseek_key)}")
