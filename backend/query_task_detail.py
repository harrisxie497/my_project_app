"""
查询任务t_aa9d170a的详细信息
"""

import pymysql
import json
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def query_task_detail():
    """查询任务t_aa9d170a的详细信息"""
    print("=" * 100)
    print("查询任务t_aa9d170a的详细信息")
    print("=" * 100)
    
    try:
        connection = pymysql.connect(
            host='172.18.207.224',
            port=3306,
            user='app',
            password='app123456',
            database='demo',
            charset='utf8mb4'
        )
        cursor = connection.cursor()
        
        # 查询任务t_aa9d170a的详细信息
        sql = """
        SELECT id, file_type, status, unique_code, flight_no, declare_date, header_params, files
        FROM tasks
        WHERE id = 't_aa9d170a'
        """
        
        cursor.execute(sql)
        result = cursor.fetchone()
        
        if result:
            task_id, file_type, status, unique_code, flight_no, declare_date, header_params, files = result
            print(f"\n任务ID: {task_id}")
            print(f"文件类型: {file_type}")
            print(f"状态: {status}")
            print(f"唯一码: {unique_code}")
            print(f"航班号: {flight_no}")
            print(f"申报日期: {declare_date}")
            print(f"\n头部参数 (header_params):")
            print(f"{header_params}")
            
            if header_params:
                try:
                    header_params_dict = json.loads(header_params)
                    print(f"\n解析后的头部参数:")
                    for key, value in header_params_dict.items():
                        print(f"  {key}: {value}")
                except Exception as e:
                    print(f"  解析失败: {str(e)}")
            
            print(f"\n文件信息 (files):")
            if files:
                try:
                    files_dict = json.loads(files)
                    print(f"\n解析后的文件信息:")
                    for key, value in files_dict.items():
                        print(f"  {key}: {value}")
                except Exception as e:
                    print(f"  解析失败: {str(e)}")
        else:
            print("\n未找到任务")
        
        cursor.close()
        connection.close()
        
        print("\n" + "=" * 100)
        print("查询完成！")
        print("=" * 100)
        
    except Exception as e:
        print(f"\n❌ 查询失败: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    query_task_detail()
