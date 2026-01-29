from sqlalchemy import Column, String, Boolean, Integer, DateTime, JSON
from sqlalchemy.sql import func
from app.core.database import Base

class FieldPipeline(Base):
    __tablename__ = "field_pipelines"
    
    id = Column(String(36), primary_key=True, index=True)
    file_type = Column(String(20), index=True, nullable=False)  # DELIVERY/CUSTOMS
    target_col = Column(String(10), nullable=False)  # A, B, C...
    target_header = Column(String(100), nullable=False)
    map_op = Column(String(20), nullable=False)  # COPY/CONST/INPUT
    source_cols = Column(JSON, nullable=False)  # ["A", "B"]
    field_type = Column(String(20), nullable=False)  # COPY/FORMAT/DEFAULT/CALC/RULE_FIX/CONST
    rule_ref = Column(JSON, nullable=False)  # ["rule1", "rule2"]
    depends_on = Column(JSON, nullable=False)  # ["A", "B"]
    order = Column(Integer, nullable=False, default=10)
    enabled = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
