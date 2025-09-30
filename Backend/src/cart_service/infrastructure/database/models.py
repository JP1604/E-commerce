"""SQLAlchemy models for cart service."""

from datetime import datetime
from sqlalchemy import Column, DateTime, String, Integer, Float, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

from .connection import Base


class ProductModel(Base):
    __tablename__ = "products"

    id_product = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    description = Column(String(1000), nullable=False)
    price = Column(Float, nullable=False)
    status = Column(Enum('activo', 'inactivo', name='product_status'), nullable=False, default='activo')
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    cart_items = relationship("CartItemModel", back_populates="product")


class CartModel(Base):
    __tablename__ = "carts"

    id_cart = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    status = Column(Enum('activo', 'vacio', name='cart_status'), nullable=False, default='activo')
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    cart_items = relationship("CartItemModel", back_populates="cart", cascade="all, delete-orphan")


class CartItemModel(Base):
    __tablename__ = "cart_items"

    id_cart_item = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cart_id = Column(UUID(as_uuid=True), ForeignKey("carts.id_cart"), nullable=False)
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id_product"), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    cart = relationship("CartModel", back_populates="cart_items")
    product = relationship("ProductModel", back_populates="cart_items")
