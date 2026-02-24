"""
测试AI规则执行器是否正确初始化
"""

from app.services.deepseek_ai_service import DeepSeekAIService
from app.services.ai_rule_executor import AIRuleExecutor
from app.core.config import settings
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def test_ai_executor():
    """测试AI规则执行器"""
    print("=" * 100)
    print("测试AI规则执行器")
    print("=" * 100)
    
    # 检查配置
    print(f"\nDEEPSEEK_API_KEY: {settings.DEEPSEEK_API_KEY[:10]}...")
    print(f"DEEPSEEK_API_URL: {settings.DEEPSEEK_API_URL}")
    
    # 创建AI服务
    print(f"\n创建AI服务...")
    ai_service = DeepSeekAIService(settings.DEEPSEEK_API_KEY, settings.DEEPSEEK_API_URL)
    print(f"✅ AI服务创建成功")
    
    # 创建AI规则执行器
    print(f"\n创建AI规则执行器...")
    ai_rule_executor = AIRuleExecutor(ai_service)
    print(f"✅ AI规则执行器创建成功")
    
    # 测试批量处理
    print(f"\n测试批量处理...")
    input_data_list = [
        {"AD": "堀 裕子 [ホリ ユウコ]"},
        {"AD": "高橋 亜衣美"},
        {"AD": "溝川　康之"}
    ]
    rule_params = {}
    
    result = ai_rule_executor.execute_batch("policy_ai_text_ja_clean", input_data_list, rule_params)
    
    print(f"\n输入数据:")
    for idx, input_data in enumerate(input_data_list):
        print(f"  {idx+1}. {input_data.get('AD', '')}")
    
    print(f"\n输出结果:")
    for idx, output in enumerate(result):
        print(f"  {idx+1}. {output}")
    
    print("\n" + "=" * 100)
    print("测试完成！")
    print("=" * 100)

if __name__ == "__main__":
    test_ai_executor()
