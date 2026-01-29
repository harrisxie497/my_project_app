from sqlalchemy.orm import Session
from uuid import uuid4
from app.core.database import SessionLocal, engine, Base
from app.models.file_definition import FileDefinition
from app.models.field_pipeline import FieldPipeline
from app.models.rule_definition import RuleDefinition

# 删除现有表并重新创建（适合开发环境）
# 注意：生产环境应该使用数据库迁移工具
print("正在删除现有表...")
FieldPipeline.__table__.drop(engine, checkfirst=True)
FileDefinition.__table__.drop(engine, checkfirst=True)
RuleDefinition.__table__.drop(engine, checkfirst=True)
print("正在创建新表...")
Base.metadata.create_all(bind=engine)

# 创建数据库会话
db = SessionLocal()

try:
    # ---------------------- 派送文件 (DELIVERY) 配置 ----------------------
    print("\n开始初始化派送文件配置...")
    
    # 1. file_definitions - 派送文件定义
    delivery_file_definitions = [
        {
            "id": f"fd_{uuid4().hex[:8]}",
            "file_type": "DELIVERY",
            "file_role": "source",
            "sheet_name": "Delivery",
            "header_row": 1,
            "data_start_row": 2,
            "columns_json": [
                {"col": "A", "header": "COL_A"}, {"col": "B", "header": "COL_B"}, {"col": "C", "header": "COL_C"}, {"col": "D", "header": "COL_D"},
                {"col": "E", "header": "COL_E"}, {"col": "F", "header": "COL_F"}, {"col": "G", "header": "COL_G"}, {"col": "H", "header": "COL_H"},
                {"col": "I", "header": "COL_I"}, {"col": "J", "header": "COL_J"}, {"col": "K", "header": "COL_K"}, {"col": "L", "header": "COL_L"},
                {"col": "M", "header": "COL_M"}, {"col": "N", "header": "COL_N"}, {"col": "O", "header": "COL_O"}, {"col": "P", "header": "COL_P"},
                {"col": "Q", "header": "COL_Q"}, {"col": "R", "header": "COL_R"}, {"col": "S", "header": "COL_S"}, {"col": "T", "header": "COL_T"},
                {"col": "U", "header": "COL_U"}, {"col": "V", "header": "COL_V"}, {"col": "W", "header": "COL_W"}, {"col": "X", "header": "COL_X"},
                {"col": "Y", "header": "COL_Y"}
            ],
            "enabled": True
        },
        {
            "id": f"fd_{uuid4().hex[:8]}",
            "file_type": "DELIVERY",
            "file_role": "output",
            "sheet_name": "Delivery",
            "header_row": 1,
            "data_start_row": 2,
            "columns_json": [
                {"col": "A", "header": "COL_A"}, {"col": "B", "header": "COL_B"}, {"col": "C", "header": "COL_C"}, {"col": "D", "header": "COL_D"},
                {"col": "E", "header": "COL_E"}, {"col": "F", "header": "COL_F"}, {"col": "G", "header": "COL_G"}, {"col": "H", "header": "COL_H"},
                {"col": "I", "header": "COL_I"}, {"col": "J", "header": "COL_J"}, {"col": "K", "header": "COL_K"}, {"col": "L", "header": "COL_L"},
                {"col": "M", "header": "COL_M"}, {"col": "N", "header": "COL_N"}, {"col": "O", "header": "COL_O"}, {"col": "P", "header": "COL_P"},
                {"col": "Q", "header": "COL_Q"}, {"col": "R", "header": "COL_R"}, {"col": "S", "header": "COL_S"}, {"col": "T", "header": "COL_T"},
                {"col": "U", "header": "COL_U"}, {"col": "V", "header": "COL_V"}, {"col": "W", "header": "COL_W"}, {"col": "X", "header": "COL_X"},
                {"col": "Y", "header": "COL_Y"}
            ],
            "enabled": True
        }
    ]
    
    # 先删除现有派送文件定义
    db.query(FileDefinition).filter(FileDefinition.file_type == "DELIVERY").delete()
    db.commit()
    
    # 插入新的派送文件定义
    for fd in delivery_file_definitions:
        file_def = FileDefinition(**fd)
        db.add(file_def)
    db.commit()
    print("✅ 派送文件定义已创建")
    
    # 2. field_pipelines - 派送字段映射
    delivery_field_pipelines = [
        {"id": f"fp_{uuid4().hex[:8]}", "file_type": "DELIVERY", "target_col": "A", "target_header": "COL_A", "map_op": "COPY", "source_cols": ["A"], "field_type": "COPY", "rule_ref": [], "depends_on": [], "order": 1, "enabled": True},
        {"id": f"fp_{uuid4().hex[:8]}", "file_type": "DELIVERY", "target_col": "B", "target_header": "COL_B", "map_op": "COPY", "source_cols": ["B"], "field_type": "COPY", "rule_ref": [], "depends_on": [], "order": 2, "enabled": True},
        {"id": f"fp_{uuid4().hex[:8]}", "file_type": "DELIVERY", "target_col": "C", "target_header": "COL_C", "map_op": "COPY", "source_cols": ["C"], "field_type": "FORMAT", "rule_ref": ["fmt_date_yyyy_mm_dd"], "depends_on": [], "order": 3, "enabled": True},
        {"id": f"fp_{uuid4().hex[:8]}", "file_type": "DELIVERY", "target_col": "D", "target_header": "COL_D", "map_op": "COPY", "source_cols": ["C", "D"], "field_type": "FORMAT", "rule_ref": ["fmt_delivery_d_conditional"], "depends_on": ["C"], "order": 4, "enabled": True},
        {"id": f"fp_{uuid4().hex[:8]}", "file_type": "DELIVERY", "target_col": "E", "target_header": "COL_E", "map_op": "COPY", "source_cols": ["E"], "field_type": "COPY", "rule_ref": [], "depends_on": [], "order": 5, "enabled": True},
        {"id": f"fp_{uuid4().hex[:8]}", "file_type": "DELIVERY", "target_col": "F", "target_header": "COL_F", "map_op": "COPY", "source_cols": ["F"], "field_type": "COPY", "rule_ref": [], "depends_on": [], "order": 6, "enabled": True},
        {"id": f"fp_{uuid4().hex[:8]}", "file_type": "DELIVERY", "target_col": "G", "target_header": "COL_G", "map_op": "COPY", "source_cols": ["G"], "field_type": "COPY", "rule_ref": [], "depends_on": [], "order": 7, "enabled": True},
        {"id": f"fp_{uuid4().hex[:8]}", "file_type": "DELIVERY", "target_col": "H", "target_header": "COL_H", "map_op": "COPY", "source_cols": ["H"], "field_type": "COPY", "rule_ref": [], "depends_on": [], "order": 8, "enabled": True},
        {"id": f"fp_{uuid4().hex[:8]}", "file_type": "DELIVERY", "target_col": "I", "target_header": "COL_I", "map_op": "COPY", "source_cols": ["I"], "field_type": "COPY", "rule_ref": [], "depends_on": [], "order": 9, "enabled": True},
        {"id": f"fp_{uuid4().hex[:8]}", "file_type": "DELIVERY", "target_col": "J", "target_header": "COL_J", "map_op": "COPY", "source_cols": ["J"], "field_type": "FORMAT", "rule_ref": ["default_fixed_j"], "depends_on": [], "order": 10, "enabled": True},
        {"id": f"fp_{uuid4().hex[:8]}", "file_type": "DELIVERY", "target_col": "K", "target_header": "COL_K", "map_op": "COPY", "source_cols": ["K"], "field_type": "FORMAT", "rule_ref": ["default_fixed_k"], "depends_on": [], "order": 11, "enabled": True},
        {"id": f"fp_{uuid4().hex[:8]}", "file_type": "DELIVERY", "target_col": "L", "target_header": "COL_L", "map_op": "COPY", "source_cols": ["L"], "field_type": "COPY", "rule_ref": [], "depends_on": [], "order": 12, "enabled": True},
        {"id": f"fp_{uuid4().hex[:8]}", "file_type": "DELIVERY", "target_col": "M", "target_header": "COL_M", "map_op": "COPY", "source_cols": ["M"], "field_type": "FORMAT", "rule_ref": ["default_fixed_m"], "depends_on": [], "order": 13, "enabled": True},
        {"id": f"fp_{uuid4().hex[:8]}", "file_type": "DELIVERY", "target_col": "N", "target_header": "COL_N", "map_op": "COPY", "source_cols": ["N"], "field_type": "COPY", "rule_ref": [], "depends_on": [], "order": 14, "enabled": True},
        {"id": f"fp_{uuid4().hex[:8]}", "file_type": "DELIVERY", "target_col": "O", "target_header": "COL_O", "map_op": "COPY", "source_cols": ["O"], "field_type": "COPY", "rule_ref": [], "depends_on": [], "order": 15, "enabled": True},
        {"id": f"fp_{uuid4().hex[:8]}", "file_type": "DELIVERY", "target_col": "P", "target_header": "COL_P", "map_op": "INPUT", "source_cols": [], "field_type": "RULE_FIX", "rule_ref": ["require_non_empty"], "depends_on": [], "order": 16, "enabled": True},
        {"id": f"fp_{uuid4().hex[:8]}", "file_type": "DELIVERY", "target_col": "Q", "target_header": "COL_Q", "map_op": "COPY", "source_cols": ["Q", "A"], "field_type": "CALC", "rule_ref": ["default_to_col_a_if_empty"], "depends_on": ["A"], "order": 17, "enabled": True},
        {"id": f"fp_{uuid4().hex[:8]}", "file_type": "DELIVERY", "target_col": "R", "target_header": "COL_R", "map_op": "CONST", "source_cols": [], "field_type": "CONST", "rule_ref": ["const_empty"], "depends_on": [], "order": 18, "enabled": True},
        {"id": f"fp_{uuid4().hex[:8]}", "file_type": "DELIVERY", "target_col": "S", "target_header": "COL_S", "map_op": "CONST", "source_cols": [], "field_type": "CONST", "rule_ref": ["const_empty"], "depends_on": [], "order": 19, "enabled": True},
        {"id": f"fp_{uuid4().hex[:8]}", "file_type": "DELIVERY", "target_col": "T", "target_header": "COL_T", "map_op": "CONST", "source_cols": [], "field_type": "CONST", "rule_ref": ["const_empty"], "depends_on": [], "order": 20, "enabled": True},
        {"id": f"fp_{uuid4().hex[:8]}", "file_type": "DELIVERY", "target_col": "U", "target_header": "COL_U", "map_op": "CONST", "source_cols": [], "field_type": "CONST", "rule_ref": ["const_empty"], "depends_on": [], "order": 21, "enabled": True},
        {"id": f"fp_{uuid4().hex[:8]}", "file_type": "DELIVERY", "target_col": "V", "target_header": "COL_V", "map_op": "CONST", "source_cols": [], "field_type": "CONST", "rule_ref": ["const_empty"], "depends_on": [], "order": 22, "enabled": True},
        {"id": f"fp_{uuid4().hex[:8]}", "file_type": "DELIVERY", "target_col": "W", "target_header": "COL_W", "map_op": "CONST", "source_cols": [], "field_type": "CONST", "rule_ref": ["const_empty"], "depends_on": [], "order": 23, "enabled": True},
        {"id": f"fp_{uuid4().hex[:8]}", "file_type": "DELIVERY", "target_col": "X", "target_header": "COL_X", "map_op": "CONST", "source_cols": [], "field_type": "CONST", "rule_ref": ["const_empty"], "depends_on": [], "order": 24, "enabled": True},
        {"id": f"fp_{uuid4().hex[:8]}", "file_type": "DELIVERY", "target_col": "Y", "target_header": "COL_Y", "map_op": "CONST", "source_cols": [], "field_type": "CONST", "rule_ref": ["const_empty"], "depends_on": [], "order": 25, "enabled": True}
    ]
    
    # 先删除现有派送字段映射
    db.query(FieldPipeline).filter(FieldPipeline.file_type == "DELIVERY").delete()
    db.commit()
    
    # 插入新的派送字段映射
    for fp in delivery_field_pipelines:
        field_pipeline = FieldPipeline(**fp)
        db.add(field_pipeline)
    db.commit()
    print("✅ 派送字段映射已创建")
    
    # 3. rule_definitions - 派送规则定义
    delivery_rule_definitions = [
        {
            "rule_ref": "fmt_date_yyyy_mm_dd",
            "rule_type": "FORMAT",
            "executor_type": "program",
            "schema_json": {
                "type": "object",
                "properties": {
                    "input_format": {"type": "string"},
                    "output_format": {"type": "string", "enum": ["YYYY-MM-DD"]},
                    "timezone": {"type": "string"}
                },
                "required": ["output_format"]
            },
            "enabled": True
        },
        {
            "rule_ref": "fmt_delivery_d_conditional",
            "rule_type": "FORMAT",
            "executor_type": "program",
            "schema_json": {
                "type": "object",
                "properties": {
                    "when_d_equals": {"type": "string", "default": "0"},
                    "if_c_not_empty_output": {"type": "string", "default": "00"},
                    "if_c_empty_output": {"type": "string", "default": ""},
                    "else_mode": {"type": "string", "enum": ["KEEP_ORIGINAL_D", "EMPTY"], "default": "KEEP_ORIGINAL_D"}
                },
                "required": ["when_d_equals"]
            },
            "enabled": True
        },
        {
            "rule_ref": "default_fixed_j",
            "rule_type": "FORMAT",
            "executor_type": "program",
            "schema_json": {
                "type": "object",
                "properties": {
                    "default_value": {"type": "string"}
                },
                "required": ["default_value"]
            },
            "enabled": True
        },
        {
            "rule_ref": "default_fixed_k",
            "rule_type": "FORMAT",
            "executor_type": "program",
            "schema_json": {
                "type": "object",
                "properties": {
                    "default_value": {"type": "string"}
                },
                "required": ["default_value"]
            },
            "enabled": True
        },
        {
            "rule_ref": "default_fixed_m",
            "rule_type": "FORMAT",
            "executor_type": "program",
            "schema_json": {
                "type": "object",
                "properties": {
                    "default_value": {"type": "string"}
                },
                "required": ["default_value"]
            },
            "enabled": True
        },
        {
            "rule_ref": "default_to_col_a_if_empty",
            "rule_type": "CALC",
            "executor_type": "program",
            "schema_json": {
                "type": "object",
                "properties": {
                    "primary_col": {"type": "string", "enum": ["Q"]},
                    "fallback_target_col": {"type": "string", "enum": ["A"]},
                    "empty_values": {"type": "array", "items": {"type": "string"}, "default": ["", "null"]}
                },
                "required": ["primary_col", "fallback_target_col"]
            },
            "enabled": True
        },
        {
            "rule_ref": "require_non_empty",
            "rule_type": "RULE_FIX",
            "executor_type": "program",
            "schema_json": {
                "type": "object",
                "properties": {
                    "error_code": {"type": "string", "default": "REQUIRED"},
                    "error_message": {"type": "string", "default": "Field is required"},
                    "block_on_fail": {"type": "boolean", "default": True}
                },
                "required": ["block_on_fail"]
            },
            "enabled": True
        },
        {
            "rule_ref": "const_empty",
            "rule_type": "CONST",
            "executor_type": "program",
            "schema_json": {
                "type": "object",
                "properties": {
                    "value": {"type": "string", "default": ""}
                },
                "required": ["value"]
            },
            "enabled": True
        }
    ]
    
    # 插入或更新派送规则定义
    for rd in delivery_rule_definitions:
        # 检查规则是否已存在
        existing_rule = db.query(RuleDefinition).filter(RuleDefinition.rule_ref == rd["rule_ref"]).first()
        if existing_rule:
            # 更新现有规则
            for key, value in rd.items():
                setattr(existing_rule, key, value)
        else:
            # 创建新规则
            rule_def = RuleDefinition(**rd)
            db.add(rule_def)
    db.commit()
    print("✅ 派送规则定义已创建/更新")
    
    print("派送文件配置初始化完成！")
    
    # ---------------------- 清关文件 (CUSTOMS) 配置 ----------------------
    print("\n开始初始化清关文件配置...")
    
    # 1. file_definitions - 清关文件定义
    customs_file_definitions = [
        {
            "id": f"fd_{uuid4().hex[:8]}",
            "file_type": "CUSTOMS",
            "file_role": "source",
            "sheet_name": "Customs",
            "header_row": 1,
            "data_start_row": 2,
            "columns_json": [
                {"col": "A", "header": "COL_A"}, {"col": "B", "header": "COL_B"}, {"col": "C", "header": "COL_C"}, {"col": "D", "header": "COL_D"},
                {"col": "E", "header": "COL_E"}, {"col": "F", "header": "COL_F"}, {"col": "G", "header": "COL_G"}, {"col": "H", "header": "COL_H"},
                {"col": "I", "header": "COL_I"}, {"col": "J", "header": "COL_J"}, {"col": "K", "header": "COL_K"}, {"col": "L", "header": "COL_L"},
                {"col": "M", "header": "COL_M"}, {"col": "N", "header": "COL_N"}, {"col": "O", "header": "COL_O"}, {"col": "P", "header": "COL_P"},
                {"col": "Q", "header": "COL_Q"}, {"col": "R", "header": "COL_R"}, {"col": "S", "header": "COL_S"}, {"col": "T", "header": "COL_T"},
                {"col": "U", "header": "COL_U"}, {"col": "V", "header": "COL_V"}, {"col": "W", "header": "COL_W"}, {"col": "X", "header": "COL_X"},
                {"col": "Y", "header": "COL_Y"}, {"col": "Z", "header": "COL_Z"}, {"col": "AA", "header": "COL_AA"}, {"col": "AB", "header": "COL_AB"},
                {"col": "AC", "header": "COL_AC"}, {"col": "AD", "header": "COL_AD"}, {"col": "AE", "header": "COL_AE"}, {"col": "AF", "header": "COL_AF"},
                {"col": "AG", "header": "COL_AG"}, {"col": "AH", "header": "COL_AH"}
            ],
            "enabled": True
        },
        {
            "id": f"fd_{uuid4().hex[:8]}",
            "file_type": "CUSTOMS",
            "file_role": "output",
            "sheet_name": "Customs",
            "header_row": 1,
            "data_start_row": 2,
            "columns_json": [
                {"col": "A", "header": "COL_A"}, {"col": "B", "header": "COL_B"}, {"col": "C", "header": "COL_C"}, {"col": "D", "header": "COL_D"},
                {"col": "E", "header": "COL_E"}, {"col": "F", "header": "COL_F"}, {"col": "G", "header": "COL_G"}, {"col": "H", "header": "COL_H"},
                {"col": "I", "header": "COL_I"}, {"col": "J", "header": "COL_J"}, {"col": "K", "header": "COL_K"}, {"col": "L", "header": "COL_L"},
                {"col": "M", "header": "COL_M"}, {"col": "N", "header": "COL_N"}, {"col": "O", "header": "COL_O"}, {"col": "P", "header": "COL_P"},
                {"col": "Q", "header": "COL_Q"}, {"col": "R", "header": "COL_R"}, {"col": "S", "header": "COL_S"}, {"col": "T", "header": "COL_T"},
                {"col": "U", "header": "COL_U"}, {"col": "V", "header": "COL_V"}, {"col": "W", "header": "COL_W"}, {"col": "X", "header": "COL_X"},
                {"col": "Y", "header": "COL_Y"}, {"col": "Z", "header": "COL_Z"}, {"col": "AA", "header": "COL_AA"}, {"col": "AB", "header": "COL_AB"},
                {"col": "AC", "header": "COL_AC"}, {"col": "AD", "header": "COL_AD"}, {"col": "AE", "header": "COL_AE"}, {"col": "AF", "header": "COL_AF"},
                {"col": "AG", "header": "COL_AG"}, {"col": "AH", "header": "COL_AH"}
            ],
            "enabled": True
        }
    ]
    
    # 先删除现有清关文件定义
    db.query(FileDefinition).filter(FileDefinition.file_type == "CUSTOMS").delete()
    db.commit()
    
    # 插入新的清关文件定义
    for fd in customs_file_definitions:
        file_def = FileDefinition(**fd)
        db.add(file_def)
    db.commit()
    print("✅ 清关文件定义已创建")
    
    # 2. field_pipelines - 清关字段映射（核心字段，根据文档简化）
    customs_field_pipelines = [
        # 固定值字段 (CONST)
        {"id": f"fp_{uuid4().hex[:8]}", "file_type": "CUSTOMS", "target_col": "A", "target_header": "COL_A", "map_op": "CONST", "source_cols": [], "field_type": "CONST", "rule_ref": ["const_value"], "depends_on": [], "order": 1, "enabled": True},
        {"id": f"fp_{uuid4().hex[:8]}", "file_type": "CUSTOMS", "target_col": "E", "target_header": "COL_E", "map_op": "CONST", "source_cols": [], "field_type": "CONST", "rule_ref": ["const_value"], "depends_on": [], "order": 5, "enabled": True},
        {"id": f"fp_{uuid4().hex[:8]}", "file_type": "CUSTOMS", "target_col": "G", "target_header": "COL_G", "map_op": "CONST", "source_cols": [], "field_type": "CONST", "rule_ref": ["const_value"], "depends_on": [], "order": 7, "enabled": True},
        {"id": f"fp_{uuid4().hex[:8]}", "file_type": "CUSTOMS", "target_col": "N", "target_header": "COL_N", "map_op": "CONST", "source_cols": [], "field_type": "CONST", "rule_ref": ["const_value"], "depends_on": [], "order": 14, "enabled": True},
        {"id": f"fp_{uuid4().hex[:8]}", "file_type": "CUSTOMS", "target_col": "O", "target_header": "COL_O", "map_op": "CONST", "source_cols": [], "field_type": "CONST", "rule_ref": ["const_value"], "depends_on": [], "order": 15, "enabled": True},
        {"id": f"fp_{uuid4().hex[:8]}", "file_type": "CUSTOMS", "target_col": "P", "target_header": "COL_P", "map_op": "CONST", "source_cols": [], "field_type": "CONST", "rule_ref": ["const_value"], "depends_on": [], "order": 16, "enabled": True},
        {"id": f"fp_{uuid4().hex[:8]}", "file_type": "CUSTOMS", "target_col": "Q", "target_header": "COL_Q", "map_op": "CONST", "source_cols": [], "field_type": "CONST", "rule_ref": ["const_value"], "depends_on": [], "order": 17, "enabled": True},
        {"id": f"fp_{uuid4().hex[:8]}", "file_type": "CUSTOMS", "target_col": "S", "target_header": "COL_S", "map_op": "CONST", "source_cols": [], "field_type": "CONST", "rule_ref": ["const_value"], "depends_on": [], "order": 19, "enabled": True},
        {"id": f"fp_{uuid4().hex[:8]}", "file_type": "CUSTOMS", "target_col": "T", "target_header": "COL_T", "map_op": "CONST", "source_cols": [], "field_type": "CONST", "rule_ref": ["const_value"], "depends_on": [], "order": 20, "enabled": True},
        {"id": f"fp_{uuid4().hex[:8]}", "file_type": "CUSTOMS", "target_col": "V", "target_header": "COL_V", "map_op": "CONST", "source_cols": [], "field_type": "CONST", "rule_ref": ["const_value"], "depends_on": [], "order": 22, "enabled": True},
        {"id": f"fp_{uuid4().hex[:8]}", "file_type": "CUSTOMS", "target_col": "AE", "target_header": "COL_AE", "map_op": "CONST", "source_cols": [], "field_type": "CONST", "rule_ref": ["const_value"], "depends_on": [], "order": 31, "enabled": True},
        {"id": f"fp_{uuid4().hex[:8]}", "file_type": "CUSTOMS", "target_col": "AF", "target_header": "COL_AF", "map_op": "CONST", "source_cols": [], "field_type": "CONST", "rule_ref": ["const_value"], "depends_on": [], "order": 32, "enabled": True},
        
        # 序号字段 (CALC)
        {"id": f"fp_{uuid4().hex[:8]}", "file_type": "CUSTOMS", "target_col": "B", "target_header": "COL_B", "map_op": "COPY", "source_cols": [], "field_type": "CALC", "rule_ref": ["seq_from_1"], "depends_on": [], "order": 2, "enabled": True},
        
        # 复制字段 (COPY)
        {"id": f"fp_{uuid4().hex[:8]}", "file_type": "CUSTOMS", "target_col": "C", "target_header": "COL_C", "map_op": "COPY", "source_cols": ["C"], "field_type": "COPY", "rule_ref": [], "depends_on": [], "order": 3, "enabled": True},
        {"id": f"fp_{uuid4().hex[:8]}", "file_type": "CUSTOMS", "target_col": "D", "target_header": "COL_D", "map_op": "COPY", "source_cols": ["C"], "field_type": "COPY", "rule_ref": [], "depends_on": [], "order": 4, "enabled": True},
        
        # AI字段 (AI)
        {"id": f"fp_{uuid4().hex[:8]}", "file_type": "CUSTOMS", "target_col": "F", "target_header": "COL_F", "map_op": "COPY", "source_cols": ["H", "I"], "field_type": "AI", "rule_ref": ["ai_weight_infer"], "depends_on": [], "order": 6, "enabled": True},
        {"id": f"fp_{uuid4().hex[:8]}", "file_type": "CUSTOMS", "target_col": "H", "target_header": "COL_H", "map_op": "COPY", "source_cols": ["H"], "field_type": "AI", "rule_ref": ["ai_goods_name_en"], "depends_on": [], "order": 8, "enabled": True},
        {"id": f"fp_{uuid4().hex[:8]}", "file_type": "CUSTOMS", "target_col": "I", "target_header": "COL_I", "map_op": "COPY", "source_cols": ["I"], "field_type": "AI", "rule_ref": ["ai_material_translate_and_map"], "depends_on": [], "order": 9, "enabled": True},
        {"id": f"fp_{uuid4().hex[:8]}", "file_type": "CUSTOMS", "target_col": "J", "target_header": "COL_J", "map_op": "COPY", "source_cols": ["J"], "field_type": "AI", "rule_ref": ["ai_translate_ja_to_en"], "depends_on": [], "order": 10, "enabled": True},
        {"id": f"fp_{uuid4().hex[:8]}", "file_type": "CUSTOMS", "target_col": "K", "target_header": "COL_K", "map_op": "COPY", "source_cols": ["K"], "field_type": "AI", "rule_ref": ["ai_translate_ja_to_en"], "depends_on": [], "order": 11, "enabled": True},
        {"id": f"fp_{uuid4().hex[:8]}", "file_type": "CUSTOMS", "target_col": "X", "target_header": "COL_X", "map_op": "COPY", "source_cols": ["X"], "field_type": "AI", "rule_ref": ["ai_receiver_name_clean_ja"], "depends_on": [], "order": 24, "enabled": True},
        {"id": f"fp_{uuid4().hex[:8]}", "file_type": "CUSTOMS", "target_col": "Y", "target_header": "COL_Y", "map_op": "COPY", "source_cols": ["Y"], "field_type": "AI", "rule_ref": ["ai_receiver_address_compose_ja"], "depends_on": [], "order": 25, "enabled": True},
        
        # 格式化字段 (FORMAT)
        {"id": f"fp_{uuid4().hex[:8]}", "file_type": "CUSTOMS", "target_col": "L", "target_header": "COL_L", "map_op": "COPY", "source_cols": ["L"], "field_type": "FORMAT", "rule_ref": ["remove_chars"], "depends_on": [], "order": 12, "enabled": True},
        {"id": f"fp_{uuid4().hex[:8]}", "file_type": "CUSTOMS", "target_col": "M", "target_header": "COL_M", "map_op": "COPY", "source_cols": ["M"], "field_type": "FORMAT", "rule_ref": ["remove_chars"], "depends_on": [], "order": 13, "enabled": True},
        {"id": f"fp_{uuid4().hex[:8]}", "file_type": "CUSTOMS", "target_col": "Z", "target_header": "COL_Z", "map_op": "COPY", "source_cols": ["Z"], "field_type": "FORMAT", "rule_ref": ["remove_chars"], "depends_on": [], "order": 26, "enabled": True},
        {"id": f"fp_{uuid4().hex[:8]}", "file_type": "CUSTOMS", "target_col": "AA", "target_header": "COL_AA", "map_op": "COPY", "source_cols": ["AA"], "field_type": "FORMAT", "rule_ref": ["remove_chars"], "depends_on": [], "order": 27, "enabled": True},
        {"id": f"fp_{uuid4().hex[:8]}", "file_type": "CUSTOMS", "target_col": "AB", "target_header": "COL_AB", "map_op": "COPY", "source_cols": ["AB"], "field_type": "FORMAT", "rule_ref": ["remove_chars"], "depends_on": [], "order": 28, "enabled": True},
        {"id": f"fp_{uuid4().hex[:8]}", "file_type": "CUSTOMS", "target_col": "AC", "target_header": "COL_AC", "map_op": "COPY", "source_cols": ["AC"], "field_type": "FORMAT", "rule_ref": ["remove_chars"], "depends_on": [], "order": 29, "enabled": True},
        {"id": f"fp_{uuid4().hex[:8]}", "file_type": "CUSTOMS", "target_col": "AD", "target_header": "COL_AD", "map_op": "COPY", "source_cols": ["AD"], "field_type": "FORMAT", "rule_ref": ["remove_chars"], "depends_on": [], "order": 30, "enabled": True},
        
        # 计算字段 (CALC)
        {"id": f"fp_{uuid4().hex[:8]}", "file_type": "CUSTOMS", "target_col": "R", "target_header": "COL_R", "map_op": "COPY", "source_cols": ["X"], "field_type": "CALC", "rule_ref": ["fx_convert_price"], "depends_on": [], "order": 18, "enabled": True},
        {"id": f"fp_{uuid4().hex[:8]}", "file_type": "CUSTOMS", "target_col": "AG", "target_header": "COL_AG", "map_op": "COPY", "source_cols": [], "field_type": "CALC", "rule_ref": ["lookup_platform_code_with_default"], "depends_on": [], "order": 33, "enabled": True},
        {"id": f"fp_{uuid4().hex[:8]}", "file_type": "CUSTOMS", "target_col": "AH", "target_header": "COL_AH", "map_op": "COPY", "source_cols": [], "field_type": "CALC", "rule_ref": ["map_platform_name_from_code_with_default"], "depends_on": ["AG"], "order": 34, "enabled": True}
    ]
    
    # 先删除现有清关字段映射
    db.query(FieldPipeline).filter(FieldPipeline.file_type == "CUSTOMS").delete()
    db.commit()
    
    # 插入新的清关字段映射
    for fp in customs_field_pipelines:
        field_pipeline = FieldPipeline(**fp)
        db.add(field_pipeline)
    db.commit()
    print("✅ 清关字段映射已创建")
    
    # 3. rule_definitions - 清关规则定义
    customs_rule_definitions = [
        {
            "rule_ref": "const_value",
            "rule_type": "CONST",
            "executor_type": "program",
            "schema_json": {
                "type": "object",
                "properties": {
                    "value": {"type": "string"}
                },
                "required": ["value"]
            },
            "enabled": True
        },
        {
            "rule_ref": "seq_from_1",
            "rule_type": "CALC",
            "executor_type": "program",
            "schema_json": {
                "type": "object",
                "properties": {
                    "start_from": {"type": "integer", "default": 1}
                }
            },
            "enabled": True
        },
        {
            "rule_ref": "remove_chars",
            "rule_type": "FORMAT",
            "executor_type": "program",
            "schema_json": {
                "type": "object",
                "properties": {
                    "chars": {"type": "array", "items": {"type": "string"}}
                },
                "required": ["chars"]
            },
            "enabled": True
        },
        {
            "rule_ref": "fx_convert_price",
            "rule_type": "CALC",
            "executor_type": "web",
            "schema_json": {
                "type": "object",
                "properties": {
                    "currency": {"type": "string", "default": "JPY"},
                    "target_currency": {"type": "string", "default": "USD"},
                    "exchange_rate_api": {"type": "string"}
                },
                "required": ["currency", "target_currency"]
            },
            "enabled": True
        },
        {
            "rule_ref": "ai_translate_ja_to_en",
            "rule_type": "AI",
            "executor_type": "ai",
            "schema_json": {
                "type": "object",
                "properties": {
                    "prompt_template": {"type": "string"},
                    "max_length": {"type": "integer"},
                    "confidence_threshold": {"type": "number", "default": 0.8}
                },
                "required": ["prompt_template"]
            },
            "enabled": True
        },
        {
            "rule_ref": "ai_material_translate_and_map",
            "rule_type": "AI",
            "executor_type": "ai",
            "schema_json": {
                "type": "object",
                "properties": {
                    "prompt_template": {"type": "string"},
                    "material_mapping": {"type": "object"},
                    "confidence_threshold": {"type": "number", "default": 0.8}
                },
                "required": ["prompt_template"]
            },
            "enabled": True
        },
        {
            "rule_ref": "ai_goods_name_en",
            "rule_type": "AI",
            "executor_type": "ai",
            "schema_json": {
                "type": "object",
                "properties": {
                    "prompt_template": {"type": "string"},
                    "max_length": {"type": "integer"},
                    "confidence_threshold": {"type": "number", "default": 0.8}
                },
                "required": ["prompt_template"]
            },
            "enabled": True
        },
        {
            "rule_ref": "ai_weight_infer",
            "rule_type": "AI",
            "executor_type": "ai",
            "schema_json": {
                "type": "object",
                "properties": {
                    "prompt_template": {"type": "string"},
                    "confidence_threshold": {"type": "number", "default": 0.8}
                },
                "required": ["prompt_template"]
            },
            "enabled": True
        },
        {
            "rule_ref": "ai_receiver_name_clean_ja",
            "rule_type": "AI",
            "executor_type": "ai",
            "schema_json": {
                "type": "object",
                "properties": {
                    "prompt_template": {"type": "string"},
                    "confidence_threshold": {"type": "number", "default": 0.8}
                },
                "required": ["prompt_template"]
            },
            "enabled": True
        },
        {
            "rule_ref": "ai_receiver_address_compose_ja",
            "rule_type": "AI",
            "executor_type": "ai",
            "schema_json": {
                "type": "object",
                "properties": {
                    "prompt_template": {"type": "string"},
                    "confidence_threshold": {"type": "number", "default": 0.8}
                },
                "required": ["prompt_template"]
            },
            "enabled": True
        },
        {
            "rule_ref": "lookup_platform_code_with_default",
            "rule_type": "CALC",
            "executor_type": "program",
            "schema_json": {
                "type": "object",
                "properties": {
                    "platform_mapping": {"type": "object"},
                    "default_code": {"type": "string", "default": "DEFAULT"}
                },
                "required": ["platform_mapping", "default_code"]
            },
            "enabled": True
        },
        {
            "rule_ref": "map_platform_name_from_code_with_default",
            "rule_type": "CALC",
            "executor_type": "program",
            "schema_json": {
                "type": "object",
                "properties": {
                    "platform_name_mapping": {"type": "object"},
                    "default_name": {"type": "string", "default": "未知平台"}
                },
                "required": ["platform_name_mapping", "default_name"]
            },
            "enabled": True
        }
    ]
    
    # 插入或更新清关规则定义
    for rd in customs_rule_definitions:
        # 检查规则是否已存在
        existing_rule = db.query(RuleDefinition).filter(RuleDefinition.rule_ref == rd["rule_ref"]).first()
        if existing_rule:
            # 更新现有规则
            for key, value in rd.items():
                setattr(existing_rule, key, value)
        else:
            # 创建新规则
            rule_def = RuleDefinition(**rd)
            db.add(rule_def)
    db.commit()
    print("✅ 清关规则定义已创建/更新")
    
    print("清关文件配置初始化完成！")
    
    print("\n所有配置初始化完成！")
    
except Exception as e:
    print(f"\n配置初始化失败: {e}")
    db.rollback()
finally:
    db.close()