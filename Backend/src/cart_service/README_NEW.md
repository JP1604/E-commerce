# Cart Service - Documentación

## 🛒 Descripción

El Cart Service ahora funciona como un carrito de compras estándar de e-commerce. Los productos se consultan directamente del **Product Service** sin necesidad de duplicarlos en la base de datos del carrito.

## 🔄 Cambios Principales

### ✅ Lo que cambió:
- **Eliminada** la tabla de productos del Cart Service
- **Eliminados** los endpoints de gestión de productos (`POST /products`, etc.)
- El carrito ahora consulta productos directamente del Product Service
- Se guarda un snapshot del precio al momento de agregar al carrito
- Validación de stock contra el Product Service

### ❌ Lo que se eliminó:
- `POST /api/v1/products/` - Crear producto (ahora en Product Service)
- `GET /api/v1/products/` - Listar productos (ahora en Product Service)
- `PUT /api/v1/products/{id}` - Actualizar producto (ahora en Product Service)
- `DELETE /api/v1/products/{id}` - Eliminar producto (ahora en Product Service)

## 📋 Endpoints Disponibles

### Gestión de Carritos

#### Crear carrito
```http
POST /api/v1/carts/
Content-Type: application/json

{
  "user_id": "uuid-del-usuario",
  "status": "activo"
}
```

**Status válidos:** `"activo"`, `"vacio"`

#### Obtener carrito por ID
```http
GET /api/v1/carts/{cart_id}
```

#### Obtener carrito por usuario
```http
GET /api/v1/carts/user/{user_id}
```

#### Actualizar carrito
```http
PUT /api/v1/carts/{cart_id}
Content-Type: application/json

{
  "status": "vacio"
}
```

#### Eliminar carrito
```http
DELETE /api/v1/carts/{cart_id}
```

### Gestión de Items del Carrito

#### Agregar producto al carrito
```http
POST /api/v1/carts/{cart_id}/items
Content-Type: application/json

{
  "product_id": "uuid-del-producto-en-product-service",
  "quantity": 2
}
```

**Importante:**
- El `product_id` debe existir en el Product Service
- Se valida el stock disponible automáticamente
- El precio se captura al momento de agregar (snapshot)
- Si el producto ya existe en el carrito, se suma la cantidad

#### Listar items del carrito
```http
GET /api/v1/carts/{cart_id}/items
```

#### Actualizar cantidad de un item
```http
PUT /api/v1/carts/{cart_id}/items/{item_id}
Content-Type: application/json

{
  "quantity": 5
}
```

#### Eliminar item del carrito
```http
DELETE /api/v1/carts/{cart_id}/items/{item_id}
```

## 🔄 Flujo de Uso Típico

### 1. Crear productos (Product Service)
```http
POST http://localhost:30000/api/v1/products/
{
  "name": "Laptop",
  "description": "Gaming laptop",
  "price": 1299.99,
  "category": "Electronics",
  "stock_quantity": 10
}
```

### 2. Crear usuario (User Service)
```http
POST http://localhost:30001/api/v1/users/
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "secure123",
  "address": "123 Main St"
}
```

### 3. Crear carrito (Cart Service)
```http
POST http://localhost:30003/api/v1/carts/
{
  "user_id": "user-uuid-from-step-2",
  "status": "activo"
}
```

### 4. Agregar productos al carrito
```http
POST http://localhost:30003/api/v1/carts/{cart-id}/items
{
  "product_id": "product-uuid-from-step-1",
  "quantity": 2
}
```

### 5. Ver carrito completo
```http
GET http://localhost:30003/api/v1/carts/{cart-id}/items
```

### 6. Modificar cantidad
```http
PUT http://localhost:30003/api/v1/carts/{cart-id}/items/{item-id}
{
  "quantity": 3
}
```

### 7. Proceder al checkout
El `cart_id` y los items se pueden usar para crear una orden en el Order Service.

## 🔧 Configuración

### Variables de Entorno

```env
# URL del Product Service (para consultar productos)
PRODUCT_SERVICE_URL=http://product-service:8000

# Configuración de base de datos
DATABASE_HOST=cart-db
DATABASE_PORT=5432
DATABASE_NAME=cart_db
DATABASE_USER=postgres
DATABASE_PASSWORD=password
```

En Kubernetes, estas variables están configuradas en el ConfigMap `ecommerce-config`.

## 🗄️ Modelo de Datos

### Cart
```python
{
  "id_cart": UUID,
  "user_id": UUID,  # Referencia al User Service
  "status": "activo" | "vacio",
  "created_at": datetime,
  "updated_at": datetime
}
```

### CartItem
```python
{
  "id_cart_item": UUID,
  "cart_id": UUID,
  "product_id": UUID,  # Referencia al Product Service
  "quantity": int,
  "unit_price": float,  # Precio snapshot al agregar
  "subtotal": float,  # Calculado: quantity * unit_price
  "created_at": datetime,
  "updated_at": datetime
}
```

## ⚠️ Validaciones

1. **Producto existe:** Se verifica contra el Product Service
2. **Stock disponible:** Se valida antes de agregar al carrito
3. **Cantidad positiva:** No se permiten cantidades <= 0
4. **Carrito existe:** Se verifica antes de agregar items

## 🚀 Despliegue

### Reconstruir imagen Docker
```bash
cd Backend/src/cart_service
docker build -t cart-service:latest .
```

### Aplicar cambios en Kubernetes
```bash
# Eliminar el pod actual para que se recree con la nueva imagen
kubectl delete pod -l app=cart-service

# Verificar que se recrea correctamente
kubectl get pods -w
```

### Migración de Base de Datos
Si ya tienes datos, ejecuta el script de migración:

```bash
# Dentro del pod
kubectl exec -it <cart-service-pod> -- python -m cart_service.migrate_remove_products
```

O elimina y recrea la base de datos:

```bash
kubectl delete pvc cart-db-pvc
kubectl delete pod -l app=cart-db
# Esperar a que se recreen
```

## 📝 Notas de Migración

- Los items existentes en carritos mantendrán sus `product_id`
- Asegúrate de que esos productos existan en el Product Service
- Los precios guardados son snapshots y no se actualizan automáticamente
- Si un producto se elimina del Product Service, el item del carrito seguirá mostrando la información guardada

## 🧪 Testing

```bash
# Test simple: agregar producto al carrito
curl -X POST http://localhost:30003/api/v1/carts/{cart-id}/items \
  -H "Content-Type: application/json" \
  -d '{
    "product_id": "product-uuid",
    "quantity": 1
  }'

# Ver items del carrito
curl http://localhost:30003/api/v1/carts/{cart-id}/items
```

## 🔗 Integración con Order Service

Para crear una orden desde un carrito:

```http
POST http://localhost:30005/api/v1/orders/
{
  "id_user": "user-uuid",
  "items": [
    {
      "id_product": "product-uuid",
      "quantity": 2,
      "unit_price": 1299.99
    }
  ]
}
```

Los datos se obtienen del endpoint `GET /carts/{cart_id}/items`.
