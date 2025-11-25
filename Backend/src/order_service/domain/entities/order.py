"""Order domain entity."""

from datetime import datetime
from enum import Enum
from typing import List, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class OrderStatus(str, Enum):
    """Order status enumeration."""
    CREATED = "creada"
    PAID = "pagada"
    SHIPPED = "enviada"
    DELIVERED = "entregada"
    CANCELLED = "cancelada"


class OrderItem(BaseModel):
    """Order item entity."""
    id_order_item: UUID = Field(default_factory=uuid4)
    id_order: UUID
    id_product: UUID
    quantity: int = Field(gt=0)
    unit_price: float = Field(gt=0)
    subtotal: float = Field(gt=0)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    def calculate_subtotal(self) -> float:
        """Calculate subtotal for this item."""
        return self.quantity * self.unit_price

    class Config:
        """Pydantic config."""
        from_attributes = True


class Order(BaseModel):
    """Order domain entity."""
    id_order: UUID = Field(default_factory=uuid4)
    id_user: UUID
    id_cart: UUID
    total: float = Field(ge=0)
    status: OrderStatus = OrderStatus.CREATED
    payment_id: Optional[UUID] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None
    
    # Order items
    items: List[OrderItem] = Field(default_factory=list)

    def add_item(self, id_product: UUID, quantity: int, unit_price: float) -> OrderItem:
        """Add an item to the order."""
        item = OrderItem(
            id_order=self.id_order,
            id_product=id_product,
            quantity=quantity,
            unit_price=unit_price,
            subtotal=quantity * unit_price
        )
        self.items.append(item)
        self.calculate_total()
        return item

    def remove_item(self, id_order_item: UUID) -> bool:
        """Remove an item from the order."""
        for i, item in enumerate(self.items):
            if item.id_order_item == id_order_item:
                self.items.pop(i)
                self.calculate_total()
                return True
        return False

    def calculate_total(self) -> float:
        """Calculate total order amount."""
        self.total = sum(item.subtotal for item in self.items)
        return self.total

    def update_status(self, new_status: OrderStatus) -> None:
        """Update order status."""
        self.status = new_status
        self.updated_at = datetime.utcnow()

    def can_be_cancelled(self) -> bool:
        """Check if order can be cancelled."""
        return self.status in [OrderStatus.CREATED, OrderStatus.PAID]

    def can_be_shipped(self) -> bool:
        """Check if order can be shipped."""
        return self.status == OrderStatus.PAID

    class Config:
        """Pydantic config."""
        from_attributes = True
