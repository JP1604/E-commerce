"""Create order use case."""

from uuid import UUID
from typing import List

from order_service.domain.entities.order import Order, OrderItem
from order_service.domain.repositories.order_repository import OrderRepository
from order_service.application.dtos.order_dto import OrderCreateDTO, OrderResponseDTO, OrderItemResponseDTO
from order_service.infrastructure.clients.cart_client import CartServiceClient
from order_service.infrastructure.clients.payment_client import PaymentServiceClient


class CreateOrderUseCase:
    """Use case for creating orders."""

    def __init__(
        self,
        order_repository: OrderRepository,
        cart_client: CartServiceClient = None,
        payment_client: PaymentServiceClient = None
    ):
        self.order_repository = order_repository
        self.cart_client = cart_client or CartServiceClient()
        self.payment_client = payment_client or PaymentServiceClient()

    async def execute(self, order_data: OrderCreateDTO) -> OrderResponseDTO:
        """Execute create order use case."""
        # 1. Fetch cart items from Cart Service (BEFORE db transaction)
        cart_items = await self.cart_client.get_cart_items(order_data.id_cart)
        
        if not cart_items:
            raise ValueError("Cart is empty or not found")
        
        # 2. Create new order
        order = Order(
            id_user=order_data.id_user,
            id_cart=order_data.id_cart,
            total=0.0
        )
        
        # 3. Add items to order from cart
        for cart_item in cart_items:
            order.add_item(
                id_product=UUID(cart_item["product_id"]),
                quantity=cart_item["quantity"],
                unit_price=cart_item["unit_price"]
            )
        
        # 4. Save order
        created_order = await self.order_repository.create(order)
        
        # Convert to response DTO first
        response_dto = self._to_response_dto(created_order)
        
        # 5. Create payment automatically (AFTER db transaction completes)
        # This happens asynchronously after returning the order
        try:
            payment_response = await self.payment_client.create_payment(
                order_id=created_order.id_order,
                user_id=created_order.id_user,
                amount=created_order.total,
                payment_method=order_data.payment_method
            )
            
            # Update response with payment_id
            response_dto.payment_id = UUID(payment_response["id_payment"])
            
        except Exception as e:
            print(f"Warning: Payment creation failed: {e}")
            # Order is still created even if payment fails
        
        # 6. Clear cart after successful order
        try:
            await self.cart_client.clear_cart(order_data.id_cart)
        except Exception as e:
            print(f"Warning: Could not clear cart: {e}")
        
        return response_dto

    def _to_response_dto(self, order: Order) -> OrderResponseDTO:
        """Convert order entity to response DTO."""
        items_dto = [
            OrderItemResponseDTO(
                id_order_item=item.id_order_item,
                id_order=item.id_order,
                id_product=item.id_product,
                quantity=item.quantity,
                unit_price=item.unit_price,
                subtotal=item.subtotal,
                created_at=item.created_at
            )
            for item in order.items
        ]
        
        return OrderResponseDTO(
            id_order=order.id_order,
            id_user=order.id_user,
            id_cart=order.id_cart,
            total=order.total,
            status=order.status,
            payment_id=order.payment_id,
            created_at=order.created_at,
            updated_at=order.updated_at,
            items=items_dto
        )
        return OrderResponseDTO(
            id_order=order.id_order,
            id_user=order.id_user,
            total=order.total,
            status=order.status,
            created_at=order.created_at,
            updated_at=order.updated_at,
            items=items_dto
        )
