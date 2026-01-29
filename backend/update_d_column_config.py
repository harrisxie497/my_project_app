#!/usr/bin/env python3
"""
更新D列（时间帯指定）的配置
"""

import sys
import os
import json

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.database import Base
from app.models.rule_item import RuleItem, FieldType, ExecutorType

def update_d_column_config():
    """更新D列的配置"""
    print("更新D列（时间帯指定）的配置...")
    
    # 创建数据库连接
    DATABASE_URL = "sqlite:///./app.db"
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    # 创建所有表（如果不存在）
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # 查找D列的规则项
        d_column_rule = db.query(RuleItem).filter(
            RuleItem.target_column == "D"
        ).first()
        
        if d_column_rule:
            print(f"找到D列的现有规则项：ID={d_column_rule.id}")
            
            # 更新配置
            d_column_rule.field_type = FieldType.FORMAT
            d_column_rule.executor = ExecutorType.PROGRAM
            d_column_rule.process_depends_on = "C,D"
            
            # 配置条件表达式规则
            proc_rules = {
                "transformation_type": "conditional_expr",
                "target_col": "D",
                "rules": [
                    {
                        "when": "C != '' && (D == 0 || D == '0')",
                        "set": "00"
                    },
                    {
                        "when": "C == '' && (D == 0 || D == '0')",
                        "set": ""
                    }
                ],
                "else": "KEEP"
            }
            
            d_column_rule.process_rules_json = proc_rules
            
            db.commit()
            print("✅ D列配置已更新")
        else:
            print("⚠️  未找到D列的规则项，需要先创建")
            print("请先创建规则表和规则项，或者使用默认配置")
            
    except Exception as e:
        print(f"❌ 更新失败：{str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    update_d_column_config()
