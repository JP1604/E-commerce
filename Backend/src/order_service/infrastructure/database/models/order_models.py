"""Order database models."""

from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import Column, DateTime, Enum, Float, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from sqlalchemy.orm import relationship

from order_service.infrastructure.database.connection import Base
from order_service.domain.entities.order import OrderStatus


class OrderModel(Base):
    """Order database model."""
    
    __tablename__ = "orders"
    
    id_order = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid4)
    id_user = Column(PostgresUUID(as_uuid=True), nullable=False)
    id_cart = Column(PostgresUUID(as_uuid=True), nullable=False)
    total = Column(Float, nullable=False, default=0.0)
    status = Column(Enum(OrderStatus), nullable=False, default=OrderStatus.CREATED)
    payment_id = Column(PostgresUUID(as_uuid=True), nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True)
    
    # Relationship with order items
    items = relationship("OrderItemModel", back_populates="order", cascade="all, delete-orphan")


class OrderItemModel(Base):
    """Order item database model."""
    
    __tablename__ = "order_items"
    
    id_order_item = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid4)
    id_order = Column(PostgresUUID(as_uuid=True), ForeignKey("orders.id_order"), nullable=False)
    id_product = Column(PostgresUUID(as_uuid=True), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    subtotal = Column(Float, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    # Relationship with order
    order = relationship("OrderModel", back_populates="items")
