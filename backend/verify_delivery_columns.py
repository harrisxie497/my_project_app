"""
验证DELIVERY任务生成的结果文件中每一列的数据是否符合验收标准
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.models.field_pipeline import FieldPipeline
import openpyxl
from datetime import datetime

print("=" * 80)
print("验证DELIVERY结果文件 - 每列数据验收检查")
print("=" * 80)

# 测试任务目录
task_dir = "storage/tasks/test_delivery_jkm_001"
result_file = os.path.join(task_dir, "result.xlsx")

if not os.path.exists(result_file):
    print(f"\n❌ 结果文件不存在: {result_file}")
    sys.exit(1)

print(f"\n✅ 结果文件: {result_file}")

# 加载结果文件
wb_result = openpyxl.load_workbook(result_file)
ws_result = wb_result.active

# 获取数据库会话
db = SessionLocal()

try:
    # 查询DELIVERY的field_pipelines配置
    pipelines = db.query(FieldPipeline).filter(
        FieldPipeline.file_type == 'DELIVERY',
        FieldPipeline.enabled == True
    ).order_by(FieldPipeline.order).all()

    print(f"\n数据库中共有 {len(pipelines)} 个DELIVERY字段处理配置:\n")

    # 按order排序
    pipelines_sorted = sorted(pipelines, key=lambda x: x.order if x.order else 999)

    # 读取结果文件的表头
    headers = []
    for cell in ws_result[1]:
        headers.append(cell.value)

    print(f"结果文件表头: {headers}\n")

    # 验证每一列
    verification_results = []

    for idx, pipeline in enumerate(pipelines_sorted, 1):
        target_col = pipeline.target_col
        target_header = pipeline.target_header
        map_op = pipeline.map_op
        source_cols = pipeline.source_cols
        field_type = pipeline.field_type
        rule_ref = pipeline.rule_ref
        rule_params_json = pipeline.rule_params_json

        print(f"{idx}. 列 {target_col} ({target_header})")
        print(f"   操作类型: {map_op}")
        print(f"   字段类型: {field_type}")

        # 解析source_cols (JSON字符串 -> list)
        if isinstance(source_cols, str):
            try:
                import json
                source_cols = json.loads(source_cols)
            except:
                source_cols = []

        # 在结果文件中找到该列
        col_index = None
        for i, header in enumerate(headers):
            if header == target_header:
                col_index = i + 1
                break

        if col_index is None:
            print(f"   ❌ 在结果文件中未找到该列")
            verification_results.append({
                'col': target_col,
                'header': target_header,
                'status': 'NOT_FOUND',
                'details': '列不存在'
            })
            continue

        # 读取该列的数据
        column_data = []
        for row in ws_result.iter_rows(min_col=col_index, max_col=col_index, min_row=2):
            cell_value = row[0].value
            column_data.append(cell_value)

        print(f"   数据行数: {len(column_data)}")
        print(f"   前3行数据: {column_data[:3]}")

        # 根据map_op验证数据
        validation_passed = True
        validation_errors = []

        # A列 - COPY
        if target_col == 'A' and map_op == 'COPY':
            # 验证：所有值应该是字符串，不为空
            for i, val in enumerate(column_data):
                if val is None or str(val).strip() == '':
                    validation_passed = False
                    validation_errors.append(f"第{i+2}行为空")
            if validation_passed:
                print(f"   ✅ 验证通过: COPY列，所有值都有效")

        # B列 - COPY
        elif target_col == 'B' and map_op == 'COPY':
            for i, val in enumerate(column_data):
                if val is None or str(val).strip() == '':
                    validation_passed = False
                    validation_errors.append(f"第{i+2}行为空")
            if validation_passed:
                print(f"   ✅ 验证通过: COPY列，所有值都有效")

        # C列 - COPY (日期格式)
        elif target_col == 'C' and map_op == 'COPY':
            for i, val in enumerate(column_data):
                if val is not None:
                    # 检查是否是日期格式
                    if isinstance(val, datetime):
                        pass  # 日期格式OK
                    elif isinstance(val, str):
                        try:
                            datetime.strptime(val, '%Y-%m-%d')
                        except:
                            validation_passed = False
                            validation_errors.append(f"第{i+2}行日期格式错误: {val}")
            if validation_passed:
                print(f"   ✅ 验证通过: 日期列，格式正确")

        # D列 - CALC (时间帯指定)
        elif target_col == 'D' and map_op == 'CALC':
            # 验证：时间帯指定应该是有效的时间代码或空字符串
            valid_time_slots = ['午前中', '12時-14時', '14時-16時', '16時-18時', '18時-20時', '19時-21時', '']
            for i, val in enumerate(column_data):
                if val is not None and val not in valid_time_slots:
                    validation_passed = False
                    validation_errors.append(f"第{i+2}行无效的时间帯: {val}")
            if validation_passed:
                print(f"   ✅ 验证通过: 时间帯指定列，所有值都有效")

        # E列 - COPY (数量)
        elif target_col == 'E' and map_op == 'COPY':
            # 验证：数量应该是数字
            for i, val in enumerate(column_data):
                if val is not None:
                    try:
                        num = float(val) if isinstance(val, (int, float)) else float(str(val))
                        if num < 0:
                            validation_passed = False
                            validation_errors.append(f"第{i+2}行数量不能为负: {val}")
                    except:
                        validation_passed = False
                        validation_errors.append(f"第{i+2}行数量格式错误: {val}")
            if validation_passed:
                print(f"   ✅ 验证通过: 货物個数列，格式正确")

        # N列 - CONST (固定值)
        elif target_col == 'N' and map_op == 'CONST':
            # 验证：所有值应该是相同的常量
            const_value = rule_params_json.get('value', '') if rule_params_json else ''
            for i, val in enumerate(column_data):
                if val != const_value:
                    validation_passed = False
                    validation_errors.append(f"第{i+2}行值不匹配常量: 期望={const_value}, 实际={val}")
            if validation_passed:
                print(f"   ✅ 验证通过: CONST列，所有值都是常量 '{const_value}'")

        # 通用验证：检查None值
        has_none = any(val is None for val in column_data)
        if has_none:
            validation_passed = False
            validation_errors.append("存在None值（应该替换为空字符串）")

        # 输出验证结果
        if not validation_passed:
            print(f"   ❌ 验证失败:")
            for error in validation_errors:
                print(f"      - {error}")
            verification_results.append({
                'col': target_col,
                'header': target_header,
                'status': 'FAILED',
                'details': '; '.join(validation_errors)
            })
        else:
            verification_results.append({
                'col': target_col,
                'header': target_header,
                'status': 'PASSED',
                'details': '所有验证通过'
            })

        print()

    # 总结
    print("=" * 80)
    print("验证总结")
    print("=" * 80)

    passed_count = sum(1 for r in verification_results if r['status'] == 'PASSED')
    failed_count = sum(1 for r in verification_results if r['status'] == 'FAILED')
    not_found_count = sum(1 for r in verification_results if r['status'] == 'NOT_FOUND')

    print(f"\n总列数: {len(verification_results)}")
    print(f"✅ 通过: {passed_count}")
    print(f"❌ 失败: {failed_count}")
    print(f"❓ 未找到: {not_found_count}")

    if failed_count > 0 or not_found_count > 0:
        print("\n❌ 验证未通过的列:")
        for r in verification_results:
            if r['status'] != 'PASSED':
                print(f"  - 列{r['col']} ({r['header']}): {r['details']}")
    else:
        print("\n✅ 所有列验证通过！")

finally:
    db.close()
    wb_result.close()
