"""
测试excel_reader.py的功能

测试场景：
1. 正常场景 - 有数据库配置，正常读取Excel
2. 无配置场景 - 不提供file_type和file_role参数
3. 配置不存在场景 - 提供的file_type和file_role在数据库中不存在
4. 表头匹配失败场景 - Excel表头与数据库配置不匹配
5. 空数据场景 - Excel文件只有表头，没有数据行
6. 边界场景 - 只有一条数据、遇到空行停止等
"""

from app.services.excel_reader import read_excel_file
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def test_normal_case():
    """
    测试正常场景 - 有数据库配置，正常读取Excel
    
    预期结果：
    - 成功读取Excel文件
    - data_row_count应该等于实际数据行数
    - 每列的数据长度应该等于data_row_count
    """
    print("=" * 100)
    print("测试1: 正常场景 - 有数据库配置，正常读取Excel")
    print("=" * 100)
    
    file_path = "C:\\Users\\harris.xie\\Documents\\trae_projects\\japan\\backend\\storage\\tasks\\t_2174140b\\original.xlsx"
    
    try:
        print(f"\n开始读取文件: {file_path}")
        print(f"文件类型: CUSTOMS, 文件角色: SOURCE")
        
        result = read_excel_file(
            file_path=file_path,
            file_type='CUSTOMS',
            file_role='SOURCE'
        )
        
        print("\n" + "=" * 100)
        print("读取结果")
        print("=" * 100)
        print(f"worksheet: {result['worksheet'].title}")
        print(f"first_row长度: {len(result['first_row'])}")
        print(f"column_data列数: {len(result['column_data'])}")
        print(f"data_row_count: {result.get('data_row_count', 'N/A')}")
        
        # 验证数据一致性
        print("\n" + "-" * 100)
        print("数据一致性验证")
        print("-" * 100)
        
        data_row_count = result.get('data_row_count', 0)
        all_match = True
        
        for i, col in enumerate(result['column_data'], start=1):
            col_len = col.get('len', 0)
            match = col_len == data_row_count
            all_match = all_match and match
            
            status = "✓" if match else "✗"
            print(f"  {status} 列{i} ({col.get('source_cols')} - {col.get('head')}): {col_len} 行")
        
        print("\n" + "-" * 100)
        if all_match:
            print("✓ 所有列的数据行数一致，测试通过！")
        else:
            print("✗ 存在列数据行数不一致，测试失败！")
        print("-" * 100)
        
        return all_match
        
    except Exception as e:
        print(f"\n✗ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_no_config():
    """
    测试无配置场景 - 不提供file_type和file_role参数
    
    预期结果：
    - 能够读取Excel文件
    - columns_config为空，无法读取数据
    - data_row_count应该为0
    - column_data应该为空列表
    """
    print("\n" + "=" * 100)
    print("测试2: 无配置场景 - 不提供file_type和file_role参数")
    print("=" * 100)
    
    file_path = "C:\\Users\\harris.xie\\Documents\\trae_projects\\japan\\backend\\storage\\tasks\\t_2174140b\\original.xlsx"
    
    try:
        print(f"\n开始读取文件: {file_path}")
        print(f"不提供file_type和file_role参数")
        
        result = read_excel_file(
            file_path=file_path
        )
        
        print("\n" + "=" * 100)
        print("读取结果")
        print("=" * 100)
        print(f"worksheet: {result['worksheet'].title}")
        print(f"first_row长度: {len(result['first_row'])}")
        print(f"column_data列数: {len(result['column_data'])}")
        print(f"data_row_count: {result.get('data_row_count', 'N/A')}")
        
        # 验证结果
        data_row_count = result.get('data_row_count', 0)
        column_data_count = len(result['column_data'])
        
        print("\n" + "-" * 100)
        print("验证结果")
        print("-" * 100)
        
        if data_row_count == 0 and column_data_count == 0:
            print("✓ 无配置时，data_row_count和column_data都为0，测试通过！")
            return True
        else:
            print(f"✗ 无配置时，data_row_count={data_row_count}, column_data_count={column_data_count}，测试失败！")
            return False
        
    except Exception as e:
        print(f"\n✗ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_config_not_exist():
    """
    测试配置不存在场景 - 提供的file_type和file_role在数据库中不存在
    
    预期结果：
    - 能够读取Excel文件
    - columns_config为空，无法读取数据
    - data_row_count应该为0
    - column_data应该为空列表
    """
    print("\n" + "=" * 100)
    print("测试3: 配置不存在场景 - 提供的file_type和file_role在数据库中不存在")
    print("=" * 100)
    
    file_path = "C:\\Users\\harris.xie\\Documents\\trae_projects\\japan\\backend\\storage\\tasks\\t_2174140b\\original.xlsx"
    
    try:
        print(f"\n开始读取文件: {file_path}")
        print(f"文件类型: INVALID, 文件角色: INVALID")
        
        result = read_excel_file(
            file_path=file_path,
            file_type='INVALID',
            file_role='INVALID'
        )
        
        print("\n" + "=" * 100)
        print("读取结果")
        print("=" * 100)
        print(f"worksheet: {result['worksheet'].title}")
        print(f"first_row长度: {len(result['first_row'])}")
        print(f"column_data列数: {len(result['column_data'])}")
        print(f"data_row_count: {result.get('data_row_count', 'N/A')}")
        
        # 验证结果
        data_row_count = result.get('data_row_count', 0)
        column_data_count = len(result['column_data'])
        
        print("\n" + "-" * 100)
        print("验证结果")
        print("-" * 100)
        
        if data_row_count == 0 and column_data_count == 0:
            print("✓ 配置不存在时，data_row_count和column_data都为0，测试通过！")
            return True
        else:
            print(f"✗ 配置不存在时，data_row_count={data_row_count}, column_data_count={column_data_count}，测试失败！")
            return False
        
    except Exception as e:
        print(f"\n✗ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_data_row_count_logic():
    """
    测试data_row_count逻辑 - 验证第一列空值停止逻辑
    
    预期结果：
    - data_row_count应该等于第一列有值的行数
    - 遇到第一列空值时应该立即停止
    """
    print("\n" + "=" * 100)
    print("测试4: data_row_count逻辑 - 验证第一列空值停止逻辑")
    print("=" * 100)
    
    file_path = "C:\\Users\\harris.xie\\Documents\\trae_projects\\japan\\backend\\storage\\tasks\\t_2174140b\\original.xlsx"
    
    try:
        print(f"\n开始读取文件: {file_path}")
        print(f"文件类型: CUSTOMS, 文件角色: SOURCE")
        
        result = read_excel_file(
            file_path=file_path,
            file_type='CUSTOMS',
            file_role='SOURCE'
        )
        
        print("\n" + "=" * 100)
        print("读取结果")
        print("=" * 100)
        print(f"worksheet: {result['worksheet'].title}")
        print(f"data_row_count: {result.get('data_row_count', 'N/A')}")
        
        # 获取第一列的数据
        first_col = None
        for col in result['column_data']:
            if col.get('source_cols') == 'A':
                first_col = col
                break
        
        if first_col:
            print(f"\n第一列 ({first_col.get('head')}) 数据:")
            print(f"  数据长度: {len(first_col.get('data', []))}")
            
            # 显示前5条和后5条数据
            data = first_col.get('data', [])
            print(f"  前5条: {data[:5]}")
            print(f"  后5条: {data[-5:]}")
            
            # 检查是否有空值
            empty_count = sum(1 for val in data if val is None or str(val).strip() == "")
            print(f"  空值数量: {empty_count}")
            
            print("\n" + "-" * 100)
            print("验证结果")
            print("-" * 100)
            
            data_row_count = result.get('data_row_count', 0)
            first_col_len = len(data)
            
            if data_row_count == first_col_len and empty_count == 0:
                print(f"✓ data_row_count={data_row_count}, 第一列数据长度={first_col_len}, 无空值，测试通过！")
                return True
            else:
                print(f"✗ data_row_count={data_row_count}, 第一列数据长度={first_col_len}, 空值数量={empty_count}，测试失败！")
                return False
        else:
            print("✗ 未找到第一列数据，测试失败！")
            return False
        
    except Exception as e:
        print(f"\n✗ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def run_all_tests():
    """
    运行所有测试用例
    
    返回：
        - 测试结果统计
    """
    print("\n" + "=" * 100)
    print("开始运行所有测试用例")
    print("=" * 100)
    
    tests = [
        ("正常场景", test_normal_case),
        ("无配置场景", test_no_config),
        ("配置不存在场景", test_config_not_exist),
        ("data_row_count逻辑", test_data_row_count_logic),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n✗ 测试 '{test_name}' 执行失败: {str(e)}")
            import traceback
            traceback.print_exc()
            results.append((test_name, False))
    
    # 打印测试总结
    print("\n" + "=" * 100)
    print("测试总结")
    print("=" * 100)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ 通过" if result else "✗ 失败"
        print(f"  {status} - {test_name}")
    
    print("\n" + "-" * 100)
    print(f"总计: {passed}/{total} 测试通过")
    print("-" * 100)
    
    return passed == total


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
