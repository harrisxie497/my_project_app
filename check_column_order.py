"""
检查结果文件中的列顺序和表头
"""
import openpyxl

result_file = "storage/tasks/test_delivery_jkm_001/result.xlsx"

print(f"检查文件: {result_file}\n")

wb = openpyxl.load_workbook(result_file)
ws = wb.active

# 获取表头
headers = [cell.value for cell in ws[1]]
print("结果文件表头（按列索引）:")
for idx, header in enumerate(headers, start=1):
    print(f"  列{idx}: {header}")

wb.close()
