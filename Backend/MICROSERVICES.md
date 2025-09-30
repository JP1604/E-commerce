# E-commerce Microservices

Este proyecto implementa una arquitectura de microservicios para un sistema de E-commerce usando arquitectura hexagonal.

## Servicios Implementados

### 1. Product Service (Puerto 8000)
**Responsabilidad**: Gestión del catálogo de productos

**Endpoints principales**:
- `POST /api/v1/products/` - Crear nuevo producto
- `GET /api/v1/products/` - Obtener todos los productos
- `GET /api/v1/products/{product_id}` - Obtener producto por ID
- `PUT /api/v1/products/{product_id}` - Actualizar producto
- `DELETE /api/v1/products/{product_id}` - Eliminar producto

**Base de datos**: PostgreSQL (puerto 5432)
**Entidades**: Product

### 2. User Service (Puerto 8001)
**Responsabilidad**: Gestión de usuarios

**Endpoints principales**:
- `POST /api/v1/users/` - Crear nuevo usuario
- `GET /api/v1/users/` - Obtener todos los usuarios
- `GET /api/v1/users/{user_id}` - Obtener usuario por ID
- `PUT /api/v1/users/{user_id}` - Actualizar usuario
- `DELETE /api/v1/users/{user_id}` - Eliminar usuario

**Base de datos**: PostgreSQL (puerto 5433)
**Entidades**: User

### 3. Delivery Service (Puerto 8002)
**Responsabilidad**: Gestión de entregas

**Base de datos**: PostgreSQL (puerto 5434)
**Entidades**: Delivery

### 4. Cart Service (Puerto 8003)
**Responsabilidad**: Gestión del carrito de compras

**Endpoints principales**:
- `POST /api/v1/carts/` - Crear nuevo carrito
- `GET /api/v1/carts/{cart_id}` - Obtener carrito por ID
- `GET /api/v1/carts/user/{user_id}` - Obtener carrito de un usuario
- `POST /api/v1/carts/{cart_id}/items` - Agregar item al carrito
- `GET /api/v1/carts/{cart_id}/items` - Obtener items del carrito
- `GET /api/v1/products/` - Obtener productos disponibles
- `POST /api/v1/products/` - Crear nuevo producto

**Base de datos**: PostgreSQL (puerto 5436)
**Entidades**: Cart, CartItem, Product

### 5. Order Service (Puerto 8005)
**Responsabilidad**: Gestión de órdenes de compra

**Endpoints principales**:
- `POST /api/v1/orders/` - Crear nueva orden
- `GET /api/v1/orders/{order_id}` - Obtener orden por ID
- `GET /api/v1/orders/user/{user_id}` - Obtener órdenes de un usuario
- `PATCH /api/v1/orders/{order_id}` - Actualizar estado de orden
- `GET /api/v1/orders/` - Listar todas las órdenes

**Base de datos**: PostgreSQL (puerto 5434)
**Entidades**: Order, OrderItem

### 6. Order Validation Service (Puerto 8006)
**Responsabilidad**: Validación de órdenes antes del procesamiento

**Endpoints principales**:
- `POST /api/v1/validations/validate` - Validar una orden
- `GET /api/v1/validations/{validation_id}` - Obtener validación por ID
- `GET /api/v1/validations/order/{order_id}` - Obtener validación por orden
- `GET /api/v1/validations/` - Listar todas las validaciones

**Validaciones realizadas**:
- Verificación de usuario activo
- Disponibilidad de productos
- Disponibilidad de stock
- Validación de precios

**Base de datos**: En memoria (para simplicidad)

### 7. Payment Processing Service (Puerto 8007)
**Responsabilidad**: Procesamiento de pagos y reembolsos

**Endpoints principales**:
- `POST /api/v1/payments/process` - Procesar pago
- `GET /api/v1/payments/{payment_id}` - Obtener pago por ID
- `GET /api/v1/payments/order/{order_id}` - Obtener pagos de una orden
- `GET /api/v1/payments/user/{user_id}` - Obtener pagos de un usuario
- `POST /api/v1/payments/{payment_id}/refund` - Procesar reembolso

**Base de datos**: PostgreSQL (puerto 5435)
**Entidades**: Payment
**Gateway**: Mock implementation (para desarrollo)

## Arquitectura Hexagonal

Cada servicio sigue la arquitectura hexagonal con las siguientes capas:

```
src/
├── domain/
│   ├── entities/          # Entidades de dominio
│   └── repositories/      # Interfaces de repositorios
├── application/
│   ├── dtos/             # Data Transfer Objects
│   └── use_cases/        # Casos de uso
├── infrastructure/
│   ├── config/           # Configuración
│   ├── database/         # Modelos de BD y conexión
│   ├── repositories/     # Implementaciones de repositorios
│   └── gateways/         # Gateways externos (solo payment)
├── interfaces/
│   └── api/              # Controladores REST
└── container.py          # Inyección de dependencias
```

## Comunicación entre Servicios

- **Order Validation Service** → **User Service**: Verificar usuario activo
- **Order Validation Service** → **Product Service**: Verificar productos y stock
- **Payment Service** → **Order Service**: Actualizar estado de orden (futuro)
- **Payment Service** → **User Service**: Verificar usuario (futuro)

## Ejecutar los Servicios

```bash
# Ejecutar todos los servicios
docker-compose up -d

# Ejecutar servicios específicos
docker-compose up order_service payment_service order_validation_service

# Ver logs
docker-compose logs -f order_service
```

## URLs de Documentación

Una vez ejecutados los servicios:

- **Product Service**: http://localhost:8000/docs
- **User Service**: http://localhost:8001/docs
- **Delivery Service**: http://localhost:8002/docs
- **Cart Service**: http://localhost:8003/docs
- **Order Service**: http://localhost:8005/docs
- **Order Validation Service**: http://localhost:8006/docs  
- **Payment Service**: http://localhost:8007/docs

## Flujo de Trabajo Típico

1. **Crear Orden**: `POST /api/v1/orders/`
2. **Validar Orden**: `POST /api/v1/validations/validate`
3. **Procesar Pago**: `POST /api/v1/payments/process`
4. **Actualizar Estado**: `PATCH /api/v1/orders/{order_id}`

## Estados de Orden

- `creada` - Orden creada
- `pagada` - Pago procesado exitosamente
- `enviada` - Orden enviada
- `entregada` - Orden entregada
- `cancelada` - Orden cancelada

## Estados de Pago

- `pendiente` - Pago pendiente
- `aprobado` - Pago aprobado
- `rechazado` - Pago rechazado
- `reembolsado` - Pago reembolsado

## Métodos de Pago Soportados

- Tarjeta de crédito (`credit_card`)
- Tarjeta de débito (`debit_card`)
- PayPal (`paypal`)
- Transferencia bancaria (`bank_transfer`)
- Efectivo (`cash`)

## Configuración de Desarrollo

Para desarrollo local, cada servicio puede ejecutarse independientemente:

```bash
# Order Service
cd src/order_service
uvicorn main:app --host 0.0.0.0 --port 8005 --reload

# Order Validation Service  
cd src/order_validation_service
uvicorn main:app --host 0.0.0.0 --port 8006 --reload

# Payment Service
cd src/payment_service
uvicorn main:app --host 0.0.0.0 --port 8007 --reload
```
