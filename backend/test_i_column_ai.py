"""
测试I列（材质）的AI处理
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.services.ai_rule_executor import AIRuleExecutor
from app.services.deepseek_ai_service import DeepSeekAIService
from app.core.config import settings
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def test_i_column():
    """测试I列（材质）的AI处理"""
    print("=" * 100)
    print("测试I列（材质）的AI处理")
    print("=" * 100)
    
    # 创建AI服务
    api_key = getattr(settings, 'DEEPSEEK_API_KEY', '')
    base_url = getattr(settings, 'DEEPSEEK_API_URL', 'https://api.deepseek.com/v1')
    ai_service = DeepSeekAIService(api_key, base_url)
    
    # 创建AI规则执行器
    ai_executor = AIRuleExecutor(ai_service=ai_service)
    
    # 测试数据
    test_data = [
        {'I': 'ABS'},
        {'I': 'ABS'},
        {'I': 'PLASTIC'},
        {'I': 'PLASTIC'}
    ]
    
    # 规则引用
    rule_ref = 'policy_ai_material_en'
    
    # 规则参数
    rule_params = {}
    
    print(f"\n测试数据: {test_data}")
    print(f"规则引用: {rule_ref}")
    
    # 执行AI规则
    print("\n开始执行AI规则...")
    try:
        results = ai_executor.execute_batch(
            rule_ref=rule_ref,
            input_data_list=test_data,
            rule_params=rule_params
        )
        
        print(f"\nAI规则执行完成！")
        print(f"结果数量: {len(results)}")
        
        for i, result in enumerate(results):
            print(f"\n结果{i+1}:")
            print(f"  输入: {test_data[i].get('I')}")
            print(f"  输出: {result}")
    except Exception as e:
        print(f"\nAI规则执行失败: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 100)
    print("测试完成！")
    print("=" * 100)

if __name__ == "__main__":
    test_i_column()
