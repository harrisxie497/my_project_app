from sqlalchemy import Column, String, Boolean, Integer, DateTime, JSON
from sqlalchemy.sql import func
from app.core.database import Base

class FileDefinition(Base):
    __tablename__ = "file_definitions"
    
    id = Column(String(36), primary_key=True, index=True)
    file_type = Column(String(20), index=True, nullable=False)  # DELIVERY/CUSTOMS
    file_role = Column(String(10), nullable=False)  # source/output
    sheet_name = Column(String(100), nullable=False)
    header_row = Column(Integer, nullable=False, default=1)
    data_start_row = Column(Integer, nullable=False, default=2)
    columns_json = Column(JSON, nullable=False)  # [{"col": "A", "header": "COL_A"}]
    enabled = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
