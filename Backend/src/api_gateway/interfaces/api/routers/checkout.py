"""Gateway checkout orchestration route.

Flow:
1) Create order in Order Service
2) Validate order in Validation Service
3) If valid, process payment in Payment Service
4) Update order status to 'pagada' in Order Service
"""

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
import httpx

from api_gateway.infrastructure.config.settings import get_settings
from api_gateway.infrastructure.http.client import get_http_client
from api_gateway.interfaces.api.schemas import CheckoutRequest, OrderCreate, PaymentInfo, DeliveryBooking, RefundRequest, DeliveryStateChange


router = APIRouter()


@router.post("/", status_code=201)
async def checkout(payload: CheckoutRequest, client: httpx.AsyncClient = Depends(get_http_client)):
    settings = get_settings()

    # 1) Create order
    try:
        create_order_resp = await client.post(
            f"{settings.order_service_url}/api/v1/orders/",
            json={"id_user": payload.id_user, "items": [i.dict(by_alias=True, exclude_none=True) for i in payload.items]},
        )
        create_order_resp.raise_for_status()
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=502, detail=f"Order creation failed: {exc}")

    order = create_order_resp.json()
    order_id = order["id_order"]
    total = order["total"]

    # 2) Validate order
    try:
        validate_resp = await client.post(
            f"{settings.order_validation_service_url}/api/v1/validations/validate",
            json={
                "id_order": order_id,
                "id_user": payload.id_user,
                "items": [{
                    "id_product": (item.id_product or item.product_id),
                    "quantity": item.quantity,
                    "unit_price": item.unit_price,
                } for item in payload.items],
                "total": total,
            },
        )
        validate_resp.raise_for_status()
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=502, detail=f"Order validation failed: {exc}")

    validation_result = validate_resp.json()
    if not validation_result.get("is_valid", False):
        raise HTTPException(status_code=400, detail={
            "message": "Order validation failed",
            "errors": validation_result.get("errors", []),
        })

    # 3) Process payment
    try:
        payment = payload.payment
        payment_payload = {}
        if payment:
            payment_payload = payment.dict(exclude_none=True)

        payment_payload.update({"id_order": order_id, "id_user": payload.id_user, "amount": total})

        payment_resp = await client.post(f"{settings.payment_service_url}/api/v1/payments/process", json=payment_payload)
        payment_resp.raise_for_status()
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=502, detail=f"Payment processing failed: {exc}")

    payment_result = payment_resp.json()
    if not payment_result.get("success", False):
        raise HTTPException(status_code=400, detail={
            "message": "Payment rejected",
            "payment": payment_result,
        })

    # 4) Update order status to 'pagada'
    try:
        update_resp = await client.patch(
            f"{settings.order_service_url}/api/v1/orders/{order_id}",
            json={"status": "pagada"},
        )
        update_resp.raise_for_status()
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=502, detail=f"Order update failed: {exc}")

    updated_order = update_resp.json()

    return {
        "order": updated_order,
        "payment": payment_result,
        "validation": validation_result,
    }


@router.post("/from-cart", status_code=201)
async def checkout_from_cart(user_id: str, client: httpx.AsyncClient = Depends(get_http_client)):
    """Checkout by reading the user's active cart."""
    settings = get_settings()

    # 0) Get user's active cart
    cart_resp = await client.get(f"{settings.cart_service_url}/api/v1/carts/user/{user_id}")
    if cart_resp.status_code != 200:
        raise HTTPException(status_code=400, detail="Active cart not found for user")
    cart = cart_resp.json()
    cart_id = cart["id_cart"]

    # Items from cart
    items_resp = await client.get(f"{settings.cart_service_url}/api/v1/carts/{cart_id}/items")
    items_resp.raise_for_status()
    cart_items = items_resp.json()

    # Transform items to order format (unit_price required)
    # If cart items lack unit_price, fetch current prices
    order_items = []
    for ci in cart_items:
        unit_price = ci.get("unit_price")
        if unit_price is None:
            p = await client.get(f"{settings.product_service_url}/api/v1/products/{ci['product_id']}")
            p.raise_for_status()
            unit_price = p.json().get("price", 0.0)
        order_items.append({
            "id_product": ci["product_id"],
            "quantity": ci["quantity"],
            "unit_price": unit_price,
        })

    # 1) Create order
    create_order_resp = await client.post(
        f"{settings.order_service_url}/api/v1/orders/",
        json={"id_user": user_id, "items": order_items},
    )
    if create_order_resp.status_code >= 400:
        return JSONResponse(status_code=create_order_resp.status_code, content=create_order_resp.json())
    order = create_order_resp.json()

    # 2) Validate order
    validate_resp = await client.post(
        f"{settings.order_validation_service_url}/api/v1/validations/validate",
        json={
            "id_order": order["id_order"],
            "id_user": user_id,
            "items": [{
                "id_product": oi["id_product"],
                "quantity": oi["quantity"],
                "unit_price": oi["unit_price"],
            } for oi in order_items],
            "total": order["total"],
        },
    )
    if validate_resp.status_code >= 400:
        return JSONResponse(status_code=validate_resp.status_code, content=validate_resp.json())
    validation = validate_resp.json()
    if not validation.get("is_valid", False):
        return JSONResponse(status_code=400, content={"detail": validation})

    # 3) For demo, process a minimal payment (cash)
    pay_resp = await client.post(
        f"{settings.payment_service_url}/api/v1/payments/process",
        json={
            "id_order": order["id_order"],
            "id_user": user_id,
            "amount": order["total"],
            "method": "cash",
            "currency": "USD",
        },
    )
    if pay_resp.status_code >= 400:
        return JSONResponse(status_code=pay_resp.status_code, content=pay_resp.json())
    payment = pay_resp.json()
    if not payment.get("success", False):
        return JSONResponse(status_code=400, content={"detail": payment})

    # 4) Update order to pagada
    upd_resp = await client.patch(
        f"{settings.order_service_url}/api/v1/orders/{order['id_order']}",
        json={"status": "pagada"},
    )
    upd_resp.raise_for_status()

    # 5) (Optional) clear cart: not implemented in service; skip for now

    return {
        "order": upd_resp.json(),
        "payment": payment,
        "validation": validation,
        "cart": {"id_cart": cart_id, "items_count": len(cart_items)},
    }


@router.post("/{order_id}/ship")
async def ship_order(order_id: str, client: httpx.AsyncClient = Depends(get_http_client)):
    """Mark order as shipped (enviada)."""
    settings = get_settings()
    try:
        resp = await client.patch(
            f"{settings.order_service_url}/api/v1/orders/{order_id}", json={"status": "enviada"}
        )
        resp.raise_for_status()
        return resp.json()
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=502, detail=f"Order update failed: {exc}")


@router.post("/{order_id}/deliver")
async def deliver_order(order_id: str, client: httpx.AsyncClient = Depends(get_http_client)):
    """Mark order as delivered (entregada)."""
    settings = get_settings()
    try:
        resp = await client.patch(
            f"{settings.order_service_url}/api/v1/orders/{order_id}", json={"status": "entregada"}
        )
        resp.raise_for_status()
        return resp.json()
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=502, detail=f"Order update failed: {exc}")


@router.post("/{order_id}/cancel")
async def cancel_order(order_id: str, client: httpx.AsyncClient = Depends(get_http_client)):
    """Cancel order (cancelada)."""
    settings = get_settings()
    try:
        resp = await client.patch(
            f"{settings.order_service_url}/api/v1/orders/{order_id}", json={"status": "cancelada"}
        )
        resp.raise_for_status()
        return resp.json()
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=502, detail=f"Order update failed: {exc}")


@router.post("/{order_id}/delivery/book", status_code=201)
async def book_delivery(order_id: str, payload: DeliveryBooking, client: httpx.AsyncClient = Depends(get_http_client)):
    """Create a delivery booking for an order in Delivery Service."""
    settings = get_settings()
    try:
        body = {"order_id": order_id, **payload.dict(exclude_none=True)}
        resp = await client.post(f"{settings.delivery_service_url}/api/v1/deliveries/", json=body)
        resp.raise_for_status()
        return resp.json()
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=502, detail=f"Delivery booking failed: {exc}")


@router.post("/delivery/{delivery_id}/state")
async def change_delivery_state(delivery_id: str, payload: DeliveryStateChange, client: httpx.AsyncClient = Depends(get_http_client)):
    """Change delivery state (BOOKED, CONFIRMED, CANCELLED)."""
    settings = get_settings()
    try:
        resp = await client.post(
            f"{settings.delivery_service_url}/api/v1/deliveries/{delivery_id}/state",
            params={"new_state": payload.new_state},
        )
        resp.raise_for_status()
        return resp.json()
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=502, detail=f"Delivery state change failed: {exc}")


@router.post("/{payment_id}/refund")
async def refund_payment(payment_id: str, payload: RefundRequest, client: httpx.AsyncClient = Depends(get_http_client)):
    """Trigger a refund via Payment Service."""
    settings = get_settings()
    try:
        resp = await client.post(
            f"{settings.payment_service_url}/api/v1/payments/{payment_id}/refund",
            json=payload.dict(exclude_none=True),
        )
        resp.raise_for_status()
        return resp.json()
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=502, detail=f"Refund failed: {exc}")


