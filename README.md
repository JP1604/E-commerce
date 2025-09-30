# 🛒 E-commerce Microservices Platform# Simple E-commerce Backend



Una plataforma completa de e-commerce implementada con **arquitectura de microservicios** usando **arquitectura hexagonal** y **FastAPI**.Una implementación simple de backend para e-commerce usando arquitectura hexagonal.



## 🏗️ Arquitectura del Sistema## Arquitectura



### Microservicios ImplementadosEste proyecto sigue los principios de **Arquitectura Hexagonal** (Ports and Adapters):



| Servicio | Puerto | Base de Datos | Responsabilidad |```

|----------|---------|---------------|-----------------|src/

| **Product Service** | 8000 | PostgreSQL:5432 | Gestión del catálogo de productos |├── domain/              # Capa de Dominio

| **User Service** | 8001 | PostgreSQL:5433 | Gestión de usuarios y autenticación |│   ├── entities/        # Entidades de negocio

| **Delivery Service** | 8002 | PostgreSQL:5434 | Gestión de entregas y envíos |│   └── repositories/    # Interfaces de repositorios

| **Cart Service** | 8003 | PostgreSQL:5436 | Gestión del carrito de compras |├── application/         # Capa de Aplicación

| **Order Service** | 8005 | PostgreSQL:5437 | Gestión de órdenes de compra |│   └── dtos/           # Data Transfer Objects

| **Order Validation Service** | 8006 | En memoria | Validación de órdenes |├── infrastructure/      # Capa de Infraestructura

| **Payment Service** | 8007 | PostgreSQL:5435 | Procesamiento de pagos |│   ├── config/         # Configuración

│   ├── database/       # Configuración de base de datos

### Arquitectura Hexagonal por Servicio│   └── repositories/   # Implementaciones de repositorios

└── interfaces/         # Capa de Interfaces

```    └── api/            # API REST con FastAPI

📦 microservice/```

├── 🔷 domain/                    # Capa de Dominio (núcleo del negocio)

│   ├── entities/                 # Entidades de dominio## Características

│   └── repositories/             # Interfaces de repositorios

├── 🔶 application/               # Capa de Aplicación (casos de uso)- ✅ API REST con FastAPI

│   ├── dtos/                     # Data Transfer Objects- ✅ Base de datos PostgreSQL con asyncpg

│   └── use_cases/                # Casos de uso del negocio- ✅ Operaciones CRUD para productos

├── 🔸 infrastructure/            # Capa de Infraestructura (detalles técnicos)- ✅ Arquitectura hexagonal básica

│   ├── config/                   # Configuración- ✅ Inyección de dependencias simple

│   ├── database/                 # Modelos y conexión de BD

│   ├── repositories/             # Implementaciones de repositorios## Requisitos

│   └── gateways/                 # Integraciones externas

├── 🔹 interfaces/                # Capa de Interfaces (API)- Python 3.9+

│   └── api/                      # Controladores REST- PostgreSQL 12+

└── 📋 container.py               # Inyección de dependencias- FastAPI

```- SQLAlchemy

- asyncpg

## ✨ Características Principales- Uvicorn



- 🚀 **Microservicios con FastAPI** - APIs REST de alto rendimiento## Instalación

- 🐘 **PostgreSQL** - Base de datos robusta para cada servicio

- 🐳 **Docker Compose** - Orquestación de contenedores1. **Instalar PostgreSQL** (si no lo tienes):

- 🏗️ **Arquitectura Hexagonal** - Separación clara de capas   - Windows: Descargar desde [postgresql.org](https://www.postgresql.org/download/)

- 🔗 **Comunicación entre servicios** - HTTP REST APIs   - Crear base de datos: `createdb ecommerce_db`

- 📝 **Documentación automática** - Swagger/OpenAPI para cada servicio

- 🧪 **Health checks** - Monitoreo de salud de servicios2. **Crear un entorno virtual**:

- 🔒 **Configuración por ambiente** - Variables de entorno```bash

- 📊 **Logs centralizados** - Para debugging y monitoreopython -m venv venv

venv\Scripts\activate  # Windows

## 🚀 Instalación y Ejecución```



### Prerrequisitos3. **Instalar dependencias**:

```bash

- 🐳 **Docker** y **Docker Compose**pip install -e .

- 🐍 **Python 3.11+** (para desarrollo local)```

- 💾 **PostgreSQL** (ejecutado via Docker)

4. **Configurar variables de entorno**:

### Ejecución con Docker (Recomendado)```bash

copy .env.example .env

```bash# Editar .env con tus credenciales de PostgreSQL

# 1. Clonar el repositorio```

git clone <repository-url>

cd E-commerce5. **Inicializar la base de datos**:

```bash

# 2. Construir y ejecutar todos los serviciospython init_db.py

docker compose up -d --build```



# 3. Verificar que todos los servicios estén ejecutándose## Uso

docker compose ps

1. Ejecutar el servidor:

# 4. Ver logs de un servicio específico```bash

docker compose logs -f product_servicepython main.py

``````



### Limpieza Completa del Sistema2. Abrir el navegador en: http://localhost:8000

3. Ver la documentación de la API en: http://localhost:8000/docs

```bash

# Detener todos los servicios## API Endpoints

docker compose down

### Productos

# Limpiar imágenes, volúmenes y caché

docker system prune -a --volumes -f- `GET /products/` - Listar todos los productos

- `POST /products/` - Crear un nuevo producto

# Reconstruir desde cero- `GET /products/{id}` - Obtener un producto por ID

docker compose build --no-cache- `PUT /products/{id}` - Actualizar un producto

docker compose up -d- `DELETE /products/{id}` - Eliminar un producto

```

## Estructura del Producto

## 📚 Documentación de APIs

```json

Una vez ejecutados los servicios, accede a la documentación interactiva:{

  "id": "uuid",

| Servicio | Documentación Swagger |  "name": "string",

|----------|----------------------|  "description": "string",

| 🛍️ **Products** | http://localhost:8000/docs |  "price": 0.0,

| 👥 **Users** | http://localhost:8001/docs |  "stock_quantity": 0,

| 🚚 **Delivery** | http://localhost:8002/docs |  "created_at": "datetime",

| 🛒 **Cart** | http://localhost:8003/docs |  "updated_at": "datetime"

| 📋 **Orders** | http://localhost:8005/docs |}

| ✅ **Order Validation** | http://localhost:8006/docs |```

| 💳 **Payments** | http://localhost:8007/docs |

## Notas sobre la Arquitectura

## 🔄 Flujo de Trabajo Típico

Esta es una versión **base y educativa** que demuestra:

### Arquitectura de Comunicación

```1. **Separación de capas**: Dominio, Aplicación, Infraestructura, Interfaces

Cliente → Product Service (Catálogo)2. **Inversión de dependencias**: El dominio no depende de la infraestructura

       → User Service (Autenticación)3. **Repository Pattern**: Abstracción de la capa de datos

       → Cart Service (Carrito)4. **DTOs**: Separación entre modelos de dominio y API

       → Order Service (Órdenes)5. **PostgreSQL**: Base de datos robusta para producción

       → Order Validation Service (Validación)

       → Payment Service (Pagos)Es ideal para:

       → Delivery Service (Envíos)- Aprender arquitectura hexagonal

```- Entender principios SOLID

- Base para proyectos más complejos

### Ejemplo de Flujo Completo- Desarrollo con PostgreSQL



```bash## Comandos Útiles PostgreSQL

# 1. Crear un usuario

curl -X POST http://localhost:8001/api/v1/users/ \```bash

  -H "Content-Type: application/json" \# Conectar a PostgreSQL

  -d '{"name":"Juan Pérez","email":"juan@example.com"}'psql -U your_user -d ecommerce_db



# 2. Obtener productos disponibles# Ver tablas

curl http://localhost:8000/api/v1/products/\dt



# 3. Agregar productos al carrito# Ver datos de productos

curl -X POST http://localhost:8003/api/v1/carts/{cart_id}/items \SELECT * FROM products;

  -H "Content-Type: application/json" \

  -d '{"product_id":"uuid","quantity":2}'# Reiniciar base de datos

python init_db.py

# 4. Crear una orden```
curl -X POST http://localhost:8005/api/v1/orders/ \
  -H "Content-Type: application/json" \
  -d '{"user_id":"uuid","items":[...]}'

# 5. Validar la orden
curl -X POST http://localhost:8006/api/v1/validations/validate \
  -H "Content-Type: application/json" \
  -d '{"order_id":"uuid"}'

# 6. Procesar el pago
curl -X POST http://localhost:8007/api/v1/payments/process \
  -H "Content-Type: application/json" \
  -d '{"order_id":"uuid","amount":100.0,"payment_method":"credit_card"}'
```

## 🗄️ Estructura de Base de Datos

### Entidades Principales

- **Product**: Catálogo de productos con categorías
- **User**: Usuarios del sistema
- **Cart & CartItem**: Carrito de compras
- **Order & OrderItem**: Órdenes de compra
- **Payment**: Procesamiento de pagos
- **Delivery**: Información de entregas

### Esquemas de Datos

```json
// Product
{
  "id": "uuid",
  "name": "string",
  "description": "string", 
  "price": "decimal",
  "stock_quantity": "integer",
  "category": "string",
  "created_at": "datetime",
  "updated_at": "datetime"
}

// Order
{
  "id": "uuid",
  "user_id": "uuid",
  "total": "decimal",
  "status": "creada|pagada|enviada|entregada|cancelada",
  "items": [
    {
      "product_id": "uuid",
      "quantity": "integer", 
      "price": "decimal"
    }
  ]
}

// Payment  
{
  "id": "uuid",
  "order_id": "uuid",
  "amount": "decimal",
  "payment_method": "credit_card|debit_card|paypal",
  "status": "pendiente|aprobado|rechazado|reembolsado"
}
```

## 🔧 Desarrollo Local

### Configuración del Entorno

```bash
# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Instalar dependencias
pip install -e .

# Ejecutar un servicio específico
cd src/product_service
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Variables de Entorno

Cada servicio utiliza variables de entorno para configuración:

```env
# Database
DATABASE_URL=postgresql+asyncpg://user:pass@host:port/db
DATABASE_ECHO=false

# Service
DEBUG=true
PROJECT_NAME=Simple E-commerce Backend
BACKEND_CORS_ORIGINS=["http://localhost:3000"]

# Service-specific
STRIPE_SECRET_KEY=sk_test_...  # Payment Service
PAYPAL_CLIENT_ID=...          # Payment Service
```

## 🐛 Debugging y Logs

```bash
# Ver logs de todos los servicios
docker compose logs -f

# Ver logs de un servicio específico
docker compose logs -f payment_service

# Acceder a un contenedor para debugging
docker compose exec product_service bash

# Ver el estado de las bases de datos
docker compose exec product_db psql -U ecommerce_user -d ecommerce
```

## 🏗️ Principios de Arquitectura

### Arquitectura Hexagonal
- **Dominio**: Lógica de negocio pura, independiente de tecnología  
- **Aplicación**: Casos de uso y coordinación
- **Infraestructura**: Detalles técnicos (BD, APIs externas)
- **Interfaces**: Puntos de entrada (REST APIs)

### Principios SOLID
- **Single Responsibility**: Cada servicio tiene una responsabilidad
- **Open/Closed**: Extensible sin modificar código existente
- **Liskov Substitution**: Interfaces intercambiables
- **Interface Segregation**: Interfaces específicas
- **Dependency Inversion**: Dependencia hacia abstracciones

### Patrones Implementados
- 🏗️ **Repository Pattern**: Abstracción de acceso a datos
- 🎯 **Dependency Injection**: Inyección de dependencias
- 📦 **DTO Pattern**: Transferencia de datos entre capas
- 🚪 **Gateway Pattern**: Integración con servicios externos
- 🏭 **Factory Pattern**: Creación de objetos complejos

## 🧪 Testing y Calidad

```bash
# Ejecutar tests unitarios
python -m pytest tests/unit/

# Ejecutar tests de integración
python -m pytest tests/integration/

# Coverage report
python -m pytest --cov=src tests/

# Linting con flake8
flake8 src/

# Type checking con mypy
mypy src/
```

## 📊 Monitoreo y Observabilidad

### Health Checks
Cada servicio expone un endpoint de salud:
```bash
curl http://localhost:8000/health  # Product Service
curl http://localhost:8001/health  # User Service
# ... otros servicios
```

### Métricas
- **Response Time**: Tiempo de respuesta de APIs
- **Error Rate**: Tasa de errores por servicio
- **Throughput**: Requests por segundo
- **Database Connections**: Conexiones activas a BD

## 🔒 Seguridad

### Implementado
- ✅ **CORS Configuration**: Control de origen cruzado
- ✅ **Environment Variables**: Configuración segura
- ✅ **Database Isolation**: Base de datos por servicio
- ✅ **Input Validation**: Validación con Pydantic

### Por Implementar
- 🔄 **JWT Authentication**: Autenticación con tokens
- 🔄 **Rate Limiting**: Límites de requests
- 🔄 **API Keys**: Autenticación de servicios
- 🔄 **HTTPS**: Comunicación segura

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

### Guías de Contribución
- Seguir principios de arquitectura hexagonal
- Incluir tests para nuevo código
- Actualizar documentación
- Usar convenciones de naming consistentes
- Agregar docstrings a funciones públicas

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 🚀 Próximas Funcionalidades

### En Desarrollo
- [ ] **Authentication & Authorization** con JWT
- [ ] **Message Queue** con Redis/RabbitMQ
- [ ] **Event Sourcing** para órdenes
- [ ] **API Gateway** con Kong/Traefik

### Planificado
- [ ] **Monitoring** con Prometheus/Grafana
- [ ] **Circuit Breaker** para resilencia
- [ ] **Cache** con Redis
- [ ] **Tests** automatizados (unit, integration, e2e)
- [ ] **CI/CD Pipeline** con GitHub Actions
- [ ] **Kubernetes Deployment**
- [ ] **Service Mesh** con Istio

## 📞 Soporte

Para soporte técnico o preguntas:
- 📧 **Email**: soporte@ecommerce.com
- 💬 **Discord**: [Servidor de Discord](#)
- 📖 **Wiki**: [Documentación Completa](./docs/)
- 🐛 **Issues**: [GitHub Issues](../../issues)

---

⭐ Si este proyecto te fue útil, ¡no olvides darle una estrella!