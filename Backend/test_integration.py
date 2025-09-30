"""
Script de prueba de integración entre microservicios.
Ejecutar después de levantar todos los servicios con docker-compose.
"""

import asyncio
import httpx
import json
from uuid import uuid4

# URLs de los servicios
ORDER_SERVICE_URL = "http://localhost:8005"
VALIDATION_SERVICE_URL = "http://localhost:8006"
PAYMENT_SERVICE_URL = "http://localhost:8007"
USER_SERVICE_URL = "http://localhost:8001"
PRODUCT_SERVICE_URL = "http://localhost:8000"


async def test_complete_order_flow():
    """Prueba el flujo completo de una orden."""
    
    print("🚀 Iniciando prueba de integración de microservicios...")
    
    async with httpx.AsyncClient() as client:
        
        # 1. Crear una orden
        print("\n📦 1. Creando orden...")
        order_data = {
            "id_user": str(uuid4()),
            "items": [
                {
                    "id_product": str(uuid4()),
                    "quantity": 2,
                    "unit_price": 29.99
                },
                {
                    "id_product": str(uuid4()),
                    "quantity": 1,
                    "unit_price": 15.50
                }
            ]
        }
        
        try:
            response = await client.post(f"{ORDER_SERVICE_URL}/api/v1/orders/", json=order_data)
            if response.status_code == 201:
                order = response.json()
                print(f"✅ Orden creada: {order['id_order']}")
                print(f"   Total: ${order['total']}")
                print(f"   Estado: {order['status']}")
            else:
                print(f"❌ Error creando orden: {response.status_code}")
                print(response.text)
                return
        except Exception as e:
            print(f"❌ Error conectando con Order Service: {e}")
            return
        
        # 2. Validar la orden
        print("\n🔍 2. Validando orden...")
        validation_data = {
            "id_order": order["id_order"],
            "id_user": order["id_user"],
            "items": [
                {
                    "id_product": str(item["id_product"]),
                    "quantity": item["quantity"],
                    "unit_price": item["unit_price"]
                }
                for item in order["items"]
            ],
            "total": order["total"]
        }
        
        try:
            response = await client.post(f"{VALIDATION_SERVICE_URL}/api/v1/validations/validate", json=validation_data)
            if response.status_code == 200:
                validation = response.json()
                print(f"✅ Validación completada: {validation['id_validation']}")
                print(f"   Válida: {validation['is_valid']}")
                print(f"   Mensaje: {validation['message']}")
                if validation['errors']:
                    print("   Errores encontrados:")
                    for error in validation['errors']:
                        print(f"     - {error['rule']}: {error['message']}")
            else:
                print(f"❌ Error validando orden: {response.status_code}")
                print(response.text)
        except Exception as e:
            print(f"❌ Error conectando con Validation Service: {e}")
        
        # 3. Procesar pago
        print("\n💳 3. Procesando pago...")
        payment_data = {
            "id_order": order["id_order"],
            "id_user": order["id_user"],
            "amount": order["total"],
            "method": "credit_card",
            "currency": "USD",
            "description": f"Pago para orden {order['id_order']}",
            "card_number": "4111111111111111",  # Número de prueba
            "card_holder_name": "Juan Perez",
            "card_expiry_month": 12,
            "card_expiry_year": 2025,
            "card_cvv": "123"
        }
        
        try:
            response = await client.post(f"{PAYMENT_SERVICE_URL}/api/v1/payments/process", json=payment_data)
            if response.status_code == 201:
                payment = response.json()
                print(f"✅ Pago procesado: {payment['id_payment']}")
                print(f"   Estado: {payment['status']}")
                print(f"   Exitoso: {payment['success']}")
                print(f"   Referencia: {payment['reference_number']}")
                if payment['gateway_transaction_id']:
                    print(f"   ID Transacción: {payment['gateway_transaction_id']}")
            else:
                print(f"❌ Error procesando pago: {response.status_code}")
                print(response.text)
        except Exception as e:
            print(f"❌ Error conectando con Payment Service: {e}")
        
        # 4. Actualizar estado de la orden (si el pago fue exitoso)
        if 'payment' in locals() and payment.get('success'):
            print("\n📋 4. Actualizando estado de orden...")
            update_data = {
                "status": "pagada"
            }
            
            try:
                response = await client.patch(f"{ORDER_SERVICE_URL}/api/v1/orders/{order['id_order']}", json=update_data)
                if response.status_code == 200:
                    updated_order = response.json()
                    print(f"✅ Orden actualizada: {updated_order['status']}")
                else:
                    print(f"❌ Error actualizando orden: {response.status_code}")
            except Exception as e:
                print(f"❌ Error actualizando orden: {e}")
        
        # 5. Consultar estado final
        print("\n📊 5. Consultando estado final...")
        try:
            response = await client.get(f"{ORDER_SERVICE_URL}/api/v1/orders/{order['id_order']}")
            if response.status_code == 200:
                final_order = response.json()
                print(f"✅ Estado final de la orden:")
                print(f"   ID: {final_order['id_order']}")
                print(f"   Estado: {final_order['status']}")
                print(f"   Total: ${final_order['total']}")
                print(f"   Creada: {final_order['created_at']}")
                if final_order['updated_at']:
                    print(f"   Actualizada: {final_order['updated_at']}")
        except Exception as e:
            print(f"❌ Error consultando orden: {e}")
    
    print("\n🎉 Prueba de integración completada!")


async def test_service_health():
    """Verifica que todos los servicios estén funcionando."""
    
    print("🏥 Verificando salud de los servicios...")
    
    services = [
        ("Order Service", ORDER_SERVICE_URL),
        ("Validation Service", VALIDATION_SERVICE_URL),
        ("Payment Service", PAYMENT_SERVICE_URL)
    ]
    
    async with httpx.AsyncClient() as client:
        for name, url in services:
            try:
                response = await client.get(f"{url}/", timeout=5.0)
                if response.status_code == 200:
                    print(f"✅ {name}: OK")
                else:
                    print(f"⚠️ {name}: {response.status_code}")
            except Exception as e:
                print(f"❌ {name}: No disponible ({e})")


if __name__ == "__main__":
    print("🔧 Test de Microservicios E-commerce")
    print("=" * 50)
    
    # Verificar servicios
    asyncio.run(test_service_health())
    
    print("\n" + "=" * 50)
    
    # Ejecutar prueba completa
    asyncio.run(test_complete_order_flow())
