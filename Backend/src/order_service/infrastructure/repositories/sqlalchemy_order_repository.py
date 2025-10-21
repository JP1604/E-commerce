"""SQLAlchemy implementation of order repository."""

from typing import List, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from order_service.domain.entities.order import Order, OrderItem
from order_service.domain.repositories.order_repository import OrderRepository
from order_service.infrastructure.database.models.order_models import OrderModel, OrderItemModel


class SQLAlchemyOrderRepository(OrderRepository):
    """SQLAlchemy implementation of order repository."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, order: Order) -> Order:
        """Create a new order."""
        # Convert domain entity to database model
        order_model = OrderModel(
            id_order=order.id_order,
            id_user=order.id_user,
            total=order.total,
            status=order.status,
            created_at=order.created_at,
            updated_at=order.updated_at
        )
        
        # Add order items
        for item in order.items:
            item_model = OrderItemModel(
                id_order_item=item.id_order_item,
                id_order=item.id_order,
                id_product=item.id_product,
                quantity=item.quantity,
                unit_price=item.unit_price,
                subtotal=item.subtotal,
                created_at=item.created_at
            )
            order_model.items.append(item_model)
        
        self.session.add(order_model)
        await self.session.commit()

        # Re-load with items eagerly to avoid async lazy-load during mapping
        from sqlalchemy import select
        stmt = select(OrderModel).options(selectinload(OrderModel.items)).where(OrderModel.id_order == order_model.id_order)
        result = await self.session.execute(stmt)
        loaded_order_model = result.scalar_one()
        
        return self._to_domain_entity(loaded_order_model)

    async def get_by_id(self, order_id: UUID) -> Optional[Order]:
        """Get order by ID."""
        stmt = select(OrderModel).options(selectinload(OrderModel.items)).where(OrderModel.id_order == order_id)
        result = await self.session.execute(stmt)
        order_model = result.scalar_one_or_none()
        
        if not order_model:
            return None
        
        return self._to_domain_entity(order_model)

    async def get_by_user_id(self, user_id: UUID) -> List[Order]:
        """Get orders by user ID."""
        stmt = select(OrderModel).options(selectinload(OrderModel.items)).where(OrderModel.id_user == user_id)
        result = await self.session.execute(stmt)
        order_models = result.scalars().all()
        
        return [self._to_domain_entity(order_model) for order_model in order_models]

    async def update(self, order: Order) -> Order:
        """Update an existing order."""
        stmt = select(OrderModel).where(OrderModel.id_order == order.id_order)
        result = await self.session.execute(stmt)
        order_model = result.scalar_one_or_none()
        
        if not order_model:
            raise ValueError(f"Order with ID {order.id_order} not found")
        
        # Update order fields
        order_model.total = order.total
        order_model.status = order.status
        order_model.updated_at = order.updated_at
        
        await self.session.commit()
        await self.session.refresh(order_model)
        
        return self._to_domain_entity(order_model)

    async def delete(self, order_id: UUID) -> bool:
        """Delete an order."""
        stmt = select(OrderModel).where(OrderModel.id_order == order_id)
        result = await self.session.execute(stmt)
        order_model = result.scalar_one_or_none()
        
        if not order_model:
            return False
        
        await self.session.delete(order_model)
        await self.session.commit()
        return True

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Order]:
        """Get all orders with pagination."""
        stmt = select(OrderModel).options(selectinload(OrderModel.items)).offset(skip).limit(limit)
        result = await self.session.execute(stmt)
        order_models = result.scalars().all()
        
        return [self._to_domain_entity(order_model) for order_model in order_models]

    def _to_domain_entity(self, order_model: OrderModel) -> Order:
        """Convert database model to domain entity."""
        # Convert order items
        items = []
        for item_model in order_model.items:
            item = OrderItem(
                id_order_item=item_model.id_order_item,
                id_order=item_model.id_order,
                id_product=item_model.id_product,
                quantity=item_model.quantity,
                unit_price=item_model.unit_price,
                subtotal=item_model.subtotal,
                created_at=item_model.created_at
            )
            items.append(item)
        
        # Convert order
        order = Order(
            id_order=order_model.id_order,
            id_user=order_model.id_user,
            total=order_model.total,
            status=order_model.status,
            created_at=order_model.created_at,
            updated_at=order_model.updated_at,
            items=items
        )
        
        return order
