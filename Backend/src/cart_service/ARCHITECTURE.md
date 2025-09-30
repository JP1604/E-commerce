# Arquitectura del Microservicio de Carrito

## Diagrama de Arquitectura Hexagonal

```
┌─────────────────────────────────────────────────────────────────┐
│                        INTERFACES LAYER                        │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  │
│  │   Cart API      │  │  Product API    │  │   Middlewares   │  │
│  │   Controller    │  │   Controller    │  │   (CORS, etc)   │  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                      APPLICATION LAYER                         │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  │
│  │   Cart DTOs     │  │  Product DTOs   │  │   Cart Item     │  │
│  │                 │  │                 │  │     DTOs        │  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘  │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  │
│  │  Create Cart    │  │  Add Item to    │  │  Create Product │  │
│  │   Use Case      │  │    Cart Use     │  │    Use Case     │  │
│  │                 │  │     Case        │  │                 │  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                        DOMAIN LAYER                            │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  │
│  │     Cart        │  │   Cart Item     │  │    Product      │  │
│  │    Entity       │  │    Entity       │  │    Entity       │  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘  │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  │
│  │  Cart Repository│  │ Cart Item Repo  │  │ Product Repo    │  │
│  │   Interface     │  │   Interface     │  │   Interface     │  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    INFRASTRUCTURE LAYER                        │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  │
│  │   PostgreSQL    │  │  SQLAlchemy     │  │   Settings      │  │
│  │   Database      │  │    Models       │  │  Configuration  │  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘  │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  │
│  │  Cart Repo      │  │ Cart Item Repo  │  │ Product Repo    │  │
│  │ Implementation  │  │ Implementation  │  │ Implementation  │  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

## Flujo de Datos

### 1. Crear Carrito
```
Cliente → CartController → CreateCartUseCase → CartRepository → Database
```

### 2. Agregar Item al Carrito
```
Cliente → CartController → AddItemToCartUseCase → CartItemRepository + ProductRepository → Database
```

### 3. Obtener Items del Carrito
```
Cliente → CartController → GetCartItemsUseCase → CartItemRepository → Database
```

## Principios de Diseño

### 1. Separación de Responsabilidades
- **Domain Layer**: Contiene la lógica de negocio pura
- **Application Layer**: Orquesta los casos de uso
- **Infrastructure Layer**: Maneja detalles técnicos (BD, APIs externas)
- **Interfaces Layer**: Expone la funcionalidad al exterior

### 2. Inversión de Dependencias
- Las capas internas no dependen de las externas
- Se usan interfaces para desacoplar implementaciones
- El contenedor de DI resuelve las dependencias

### 3. Independencia del Microservicio
- Base de datos propia (PostgreSQL en puerto 5434)
- Contenedor Docker independiente
- Configuración específica
- API REST propia

## Entidades del Dominio

### Cart (Carrito)
```python
class Cart(BaseEntity):
    user_id: UUID
    status: CartStatus  # activo, vacio
```

### CartItem (Item del Carrito)
```python
class CartItem(BaseEntity):
    cart_id: UUID
    product_id: UUID
    quantity: int
    unit_price: float
    subtotal: float  # Calculado: quantity * unit_price
```

### Product (Producto)
```python
class Product(BaseEntity):
    name: str
    description: str
    price: float
    status: ProductStatus  # activo, inactivo
```

## Casos de Uso Principales

1. **Gestión de Carritos**
   - Crear carrito para usuario
   - Obtener carrito activo
   - Actualizar estado del carrito
   - Eliminar carrito

2. **Gestión de Items**
   - Agregar producto al carrito
   - Actualizar cantidad
   - Eliminar item del carrito
   - Listar items del carrito

3. **Gestión de Productos**
   - Crear producto
   - Obtener producto por ID
   - Listar productos
   - Actualizar producto
   - Eliminar producto

## Configuración de Base de Datos

### Tablas
- `carts`: Almacena información de carritos
- `cart_items`: Almacena items dentro de carritos
- `products`: Almacena información de productos

### Relaciones
- Un carrito puede tener muchos items (1:N)
- Un producto puede estar en muchos items (1:N)
- Un item pertenece a un carrito y un producto (N:1)

## Endpoints de la API

### Carritos
- `POST /api/v1/carts/` - Crear carrito
- `GET /api/v1/carts/{cart_id}` - Obtener carrito
- `GET /api/v1/carts/user/{user_id}` - Obtener carrito por usuario
- `PUT /api/v1/carts/{cart_id}` - Actualizar carrito
- `DELETE /api/v1/carts/{cart_id}` - Eliminar carrito

### Items del Carrito
- `POST /api/v1/carts/{cart_id}/items` - Agregar item
- `GET /api/v1/carts/{cart_id}/items` - Listar items

### Productos
- `POST /api/v1/products/` - Crear producto
- `GET /api/v1/products/{product_id}` - Obtener producto
- `GET /api/v1/products/` - Listar productos
- `PUT /api/v1/products/{product_id}` - Actualizar producto
- `DELETE /api/v1/products/{product_id}` - Eliminar producto
