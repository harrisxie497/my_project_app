import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.core.config import settings

print("=" * 50)
print("配置验证")
print("=" * 50)

print(f"\nDeepSeek AI配置：")
print(f"  API Key: {settings.DEEPSEEK_API_KEY[:10]}...{settings.DEEPSEEK_API_KEY[-4:] if len(settings.DEEPSEEK_API_KEY) > 10 else settings.DEEPSEEK_API_KEY}")
print(f"  API URL: {settings.DEEPSEEK_API_URL}")

print(f"\n汇率API配置：")
print(f"  API Key: {settings.EXCHANGE_RATE_API_KEY[:10]}...{settings.EXCHANGE_RATE_API_KEY[-4:] if len(settings.EXCHANGE_RATE_API_KEY) > 10 else settings.EXCHANGE_RATE_API_KEY}")
print(f"  API URL: {settings.EXCHANGE_RATE_API_URL}")

print(f"\n其他配置：")
print(f"  数据库URL: {settings.DATABASE_URL}")
print(f"  存储路径: {settings.TASKS_STORAGE_PATH}")

print("\n" + "=" * 50)

if settings.DEEPSEEK_API_KEY and settings.DEEPSEEK_API_KEY != "":
    print("✅ DeepSeek API Key已配置")
else:
    print("⚠️  DeepSeek API Key未配置，请设置DEEPSEEK_API_KEY环境变量")

if settings.EXCHANGE_RATE_API_KEY and settings.EXCHANGE_RATE_API_KEY != "":
    print("✅ 汇率API Key已配置")
else:
    print("⚠️  汇率API Key未配置，请设置EXCHANGE_RATE_API_KEY环境变量")

print("=" * 50)
