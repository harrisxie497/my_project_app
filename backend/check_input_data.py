"""
确认输入的数据是多少
"""

import re
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def check_input_data():
    """确认输入的数据是多少"""
    print("=" * 100)
    print("确认输入的数据是多少")
    print("=" * 100)
    
    log_file_path = r"C:\Users\harris.xie\Documents\trae_projects\japan\backend\test_task_t_f37e2c5b.log"
    
    try:
        # 读取日志文件
        with open(log_file_path, 'r', encoding='utf-8') as f:
            log_content = f.read()
        
        # 查找AI批量处理的输入数据量
        pattern = r"AI 规则批量处理 - 列名: (.*?), 数据量: (\d+)"
        matches = re.findall(pattern, log_content)
        
        print(f"\nAI批量处理的输入数据量:")
        for match in matches:
            col_name, data_count = match
            print(f"  列名: {col_name}, 数据量: {data_count}")
        
        # 查找AI批量处理返回值
        pattern = r"AI 批量处理返回值 - 列: (.*?), 返回值: \[(.*?)\]"
        matches = re.findall(pattern, log_content, re.DOTALL)
        
        print(f"\nAI批量处理返回值:")
        for match in matches:
            col_name, return_value = match
            return_list = return_value.split("', '")
            print(f"  列名: {col_name}, 返回值数量: {len(return_list)}, 有效值数量: {sum(1 for v in return_list if v and v.strip() != '')}")
        
        print("\n" + "=" * 100)
        print("检查完成！")
        print("=" * 100)
        
    except Exception as e:
        print(f"\n❌ 检查失败: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    check_input_data()
