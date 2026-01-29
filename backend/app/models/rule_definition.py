from sqlalchemy import Column, String, Boolean, DateTime, JSON
from sqlalchemy.sql import func
from app.core.database import Base

class RuleDefinition(Base):
    __tablename__ = "rule_definitions"
    
    rule_ref = Column(String(100), primary_key=True, index=True)
    rule_type = Column(String(20), nullable=False)  # FORMAT/CALC/RULE_FIX/CONST
    executor_type = Column(String(20), nullable=False)  # program/ai/web
    schema_json = Column(JSON, nullable=False)
    enabled = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
