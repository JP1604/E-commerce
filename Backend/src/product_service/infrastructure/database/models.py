"""Simple SQLAlchemy models."""

from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String, Text, Float, LargeBinary
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

from .connection import Base


class ProductModel(Base):
    """Simple SQLAlchemy model for Product entity."""
    
    __tablename__ = "products"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    price = Column(Float, nullable=False)
    category = Column(String(100), nullable=False)
    stock_quantity = Column(Integer, nullable=False, default=0)
    image_bin = Column(LargeBinary, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())