"""
检查AI批量处理的输入输出对比
"""

def check_ai_batch_input_output():
    """检查AI批量处理的输入输出对比"""
    print("=" * 100)
    print("检查AI批量处理的输入输出对比")
    print("=" * 100)
    
    log_file = r'C:\Users\harris.xie\Documents\trae_projects\japan\backend\logs\app.log'
    
    # 读取日志文件
    with open(log_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # 查找最后一次批量执行AI规则的日志
    batch_indices = [idx for idx, line in enumerate(lines) if '批量执行AI规则：policy_ai_text_dress_clean，数据量：20' in line]
    
    if batch_indices:
        batch_idx = batch_indices[-1]
        
        # 查找"调用AI的输入数据"的日志
        input_start_idx = None
        for idx in range(batch_idx, min(batch_idx + 50, len(lines))):
            if '调用AI的输入数据:' in lines[idx]:
                input_start_idx = idx + 1
                break
        
        # 查找"AI返回的输出数据"的日志
        output_start_idx = None
        for idx in range(batch_idx, min(batch_idx + 100, len(lines))):
            if 'AI返回的输出数据:' in lines[idx]:
                output_start_idx = idx + 1
                break
        
        if input_start_idx and output_start_idx:
            # 提取输入数据
            input_data = []
            for idx in range(input_start_idx, min(input_start_idx + 30, len(lines))):
                line = lines[idx].strip()
                if line.startswith('===') or line.startswith('调用AI的提示词'):
                    break
                input_data.append(line)
            
            # 提取输出数据
            output_data = []
            for idx in range(output_start_idx, min(output_start_idx + 30, len(lines))):
                line = lines[idx].strip()
                if line.startswith('===') or line.startswith('解析后的结果数量'):
                    break
                output_data.append(line)
            
            print(f"\n输入数据（{len(input_data)}行）:")
            for idx, line in enumerate(input_data):
                print(f"  {idx+1}. {line}")
            
            print(f"\n输出数据（{len(output_data)}行）:")
            for idx, line in enumerate(output_data):
                print(f"  {idx+1}. {line}")
            
            print(f"\n对比分析:")
            print(f"  输入数量: {len(input_data)}")
            print(f"  输出数量: {len(output_data)}")
            print(f"  匹配: {len(input_data) == len(output_data)}")
            
            # 检查空值
            empty_input_indices = [idx for idx, line in enumerate(input_data) if not line or line.strip() == '']
            empty_output_indices = [idx for idx, line in enumerate(output_data) if not line or line.strip() == '']
            
            print(f"  输入空值位置: {[idx+1 for idx in empty_input_indices]}")
            print(f"  输出空值位置: {[idx+1 for idx in empty_output_indices]}")
        else:
            print("\n未找到输入或输出数据")
    else:
        print("\n未找到批量执行AI规则的日志")
    
    print("\n" + "=" * 100)
    print("检查完成")
    print("=" * 100)

if __name__ == "__main__":
    check_ai_batch_input_output()
