"""
检查AI批量处理返回值的数量
"""

import re
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def check_ai_batch_output():
    """检查AI批量处理返回值的数量"""
    print("=" * 100)
    print("检查AI批量处理返回值的数量")
    print("=" * 100)
    
    log_file_path = "C:\\Users\\harris.xie\\Documents\\trae_projects\\japan\\backend\\test_task_t_f37e2c5b.log"
    
    try:
        # 读取日志文件
        with open(log_file_path, 'r', encoding='utf-8') as f:
            log_content = f.read()
        
        # 查找AI批量处理返回值
        y_pattern = r"AI 批量处理返回值 - 列: Y, 返回值: \[(.*?)\]"
        y_match = re.search(y_pattern, log_content)
        
        if y_match:
            y_return_value = y_match.group(1)
            print(f"\nY列（收件人地址）的返回值:")
            print(f"返回值: {y_return_value}")
            
            # 计算返回值的数量
            y_items = y_match.group(1).split("', '")
            print(f"返回值数量: {len(y_items)}")
            print(f"返回值前10个: {y_items[:10]}")
        
        k_pattern = r"AI 批量处理返回值 - 列: K, 返回值: \[(.*?)\]"
        k_match = re.search(k_pattern, log_content)
        
        if k_match:
            k_return_value = k_match.group(1)
            print(f"\nK列（輸入者住所）的返回值:")
            print(f"返回值: {k_return_value}")
            
            # 计算返回值的数量
            k_items = k_match.group(1).split("', '")
            print(f"返回值数量: {len(k_items)}")
            print(f"返回值前10个: {k_items[:10]}")
        
        j_pattern = r"AI 批量处理返回值 - 列: J, 返回值: \[(.*?)\]"
        j_match = re.search(j_pattern, log_content)
        
        if j_match:
            j_return_value = j_match.group(1)
            print(f"\nJ列（輸入者名）的返回值:")
            print(f"返回值: {j_return_value}")
            
            # 计算返回值的数量
            j_items = j_match.group(1).split("', '")
            print(f"返回值数量: {len(j_items)}")
            print(f"返回值前10个: {j_items[:10]}")
        
        print("\n" + "=" * 100)
        print("检查完成！")
        print("=" * 100)
        
    except Exception as e:
        print(f"\n❌ 检查失败: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    check_ai_batch_output()
