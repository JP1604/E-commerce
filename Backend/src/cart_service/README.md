# Cart Service

Microservicio de carrito de compras para el sistema de e-commerce, implementado con arquitectura hexagonal y FastAPI.

## Características

- **Arquitectura Hexagonal**: Separación clara entre dominio, aplicación e infraestructura
- **Microservicio Independiente**: Base de datos propia y contenedor Docker independiente
- **API REST**: Endpoints para gestión de carritos, items y productos
- **Base de Datos**: PostgreSQL con SQLAlchemy async
- **Validación**: Pydantic para validación de datos de entrada

## Entidades del Dominio

### Cart (Carrito)
- `id_cart`: Identificador único del carrito
- `user_id`: ID del usuario propietario
- `status`: Estado del carrito (activo/vacio)
- `created_at`, `updated_at`: Timestamps

### CartItem (Item del Carrito)
- `id_cart_item`: Identificador único del item
- `cart_id`: ID del carrito al que pertenece
- `product_id`: ID del producto
- `quantity`: Cantidad del producto
- `unit_price`: Precio unitario
- `subtotal`: Subtotal calculado (quantity * unit_price)

### Product (Producto)
- `id_product`: Identificador único del producto
- `name`: Nombre del producto
- `description`: Descripción del producto
- `price`: Precio del producto
- `status`: Estado del producto (activo/inactivo)

## Endpoints de la API

### Carritos
- `POST /api/v1/carts/` - Crear carrito
- `GET /api/v1/carts/{cart_id}` - Obtener carrito por ID
- `GET /api/v1/carts/user/{user_id}` - Obtener carrito activo por usuario
- `PUT /api/v1/carts/{cart_id}` - Actualizar carrito
- `DELETE /api/v1/carts/{cart_id}` - Eliminar carrito

### Items del Carrito
- `POST /api/v1/carts/{cart_id}/items` - Agregar item al carrito
- `GET /api/v1/carts/{cart_id}/items` - Obtener items del carrito

### Productos
- `POST /api/v1/products/` - Crear producto
- `GET /api/v1/products/{product_id}` - Obtener producto por ID
- `GET /api/v1/products/` - Listar productos (con filtro opcional por estado)
- `PUT /api/v1/products/{product_id}` - Actualizar producto
- `DELETE /api/v1/products/{product_id}` - Eliminar producto

## Configuración

### Variables de Entorno
- `DATABASE_URL`: URL de conexión a la base de datos
- `DATABASE_HOST`: Host de la base de datos (default: localhost)
- `DATABASE_PORT`: Puerto de la base de datos (default: 5432)
- `DATABASE_NAME`: Nombre de la base de datos (default: cart_db)
- `DATABASE_USER`: Usuario de la base de datos (default: postgres)
- `DATABASE_PASSWORD`: Contraseña de la base de datos (default: password)
- `DEBUG`: Modo debug (default: False)
- `PORT`: Puerto del servicio (default: 8010)

## Ejecución

### Con Docker Compose
```bash
docker-compose up cart_service
```

### Localmente
```bash
cd Backend/src/cart_service
pip install -e .
uvicorn cart_service.main:app --host 0.0.0.0 --port 8010
```

## Estructura del Proyecto

```
cart_service/
├── domain/                    # Capa de dominio
│   ├── entities/             # Entidades del dominio
│   └── repositories/         # Interfaces de repositorios
├── application/              # Capa de aplicación
│   ├── dtos/                 # Data Transfer Objects
│   └── use_cases/            # Casos de uso
├── infrastructure/           # Capa de infraestructura
│   ├── config/               # Configuración
│   ├── database/             # Modelos y conexión de BD
│   └── repositories/         # Implementaciones de repositorios
├── interfaces/               # Capa de interfaces
│   └── api/                  # API REST
│       ├── controllers/      # Controladores
│       ├── middlewares/      # Middlewares
│       └── routers/          # Routers
├── container.py              # Contenedor de dependencias
├── main.py                   # Aplicación principal
└── Dockerfile                # Imagen Docker
```

## Casos de Uso

- **CreateCartUseCase**: Crear un nuevo carrito para un usuario
- **GetCartUseCase**: Obtener carrito por ID o por usuario
- **UpdateCartUseCase**: Actualizar estado del carrito
- **DeleteCartUseCase**: Eliminar carrito
- **AddItemToCartUseCase**: Agregar producto al carrito
- **GetCartItemsUseCase**: Obtener items del carrito
- **CreateProductUseCase**: Crear nuevo producto
- **GetProductUseCase**: Obtener producto por ID
- **ListProductsUseCase**: Listar productos con filtros
