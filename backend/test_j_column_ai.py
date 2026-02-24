"""
测试J列（輸入者名）的AI处理
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

def test_j_column():
    """测试J列（輸入者名）的AI处理"""
    print("=" * 100)
    print("测试J列（輸入者名）的AI处理")
    print("=" * 100)
    
    # 创建AI服务
    api_key = getattr(settings, 'DEEPSEEK_API_KEY', '')
    base_url = getattr(settings, 'DEEPSEEK_API_URL', 'https://api.deepseek.com/v1')
    ai_service = DeepSeekAIService(api_key, base_url)
    
    # 创建AI规则执行器
    ai_executor = AIRuleExecutor(ai_service=ai_service)
    
    # 测试数据
    test_data = [
        {'K': '# 使用PYTHON实现简单的数据可视化', 'X': '堀裕子'},
        {'K': None, 'X': '高橋亜衣美'},
        {'K': '下面是一个使用PYTHON的MATPLOTLIB和SEABORN库创建数据可视化的示例。这个示例将展示如何创建多种类型的图表，并添加必要的样式和注释。', 'X': '溝川康之'},
        {'K': None, 'X': '池上千夏'}
    ]
    
    # 规则引用
    rule_ref = 'policy_translate_from_targetcol_en_upper'
    
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
            print(f"  输入K: {test_data[i].get('K')}")
            print(f"  输入X: {test_data[i].get('X')}")
            print(f"  输出: {result}")
    except Exception as e:
        print(f"\nAI规则执行失败: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 100)
    print("测试完成！")
    print("=" * 100)

if __name__ == "__main__":
    test_j_column()
