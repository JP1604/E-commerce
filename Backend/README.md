# Simple E-commerce Backend

Una implementación simple de backend para e-commerce usando arquitectura hexagonal.

## Arquitectura

Este proyecto sigue los principios de **Arquitectura Hexagonal** (Ports and Adapters):

```
src/
├── domain/              # Capa de Dominio
│   ├── entities/        # Entidades de negocio
│   └── repositories/    # Interfaces de repositorios
├── application/         # Capa de Aplicación
│   └── dtos/           # Data Transfer Objects
├── infrastructure/      # Capa de Infraestructura
│   ├── config/         # Configuración
│   ├── database/       # Configuración de base de datos
│   └── repositories/   # Implementaciones de repositorios
└── interfaces/         # Capa de Interfaces
    └── api/            # API REST con FastAPI
```

## Características

- ✅ API REST con FastAPI
- ✅ Base de datos PostgreSQL con asyncpg
- ✅ Operaciones CRUD para productos
- ✅ Arquitectura hexagonal básica
- ✅ Inyección de dependencias simple

## Requisitos

- Python 3.9+
- PostgreSQL 12+
- FastAPI
- SQLAlchemy
- asyncpg
- Uvicorn

## Instalación

1. **Instalar PostgreSQL** (si no lo tienes):
   - Windows: Descargar desde [postgresql.org](https://www.postgresql.org/download/)
   - Crear base de datos: `createdb ecommerce_db`

2. **Crear un entorno virtual**:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

3. **Instalar dependencias**:
```bash
pip install -e .
```

4. **Configurar variables de entorno**:
```bash
copy .env.example .env
# Editar .env con tus credenciales de PostgreSQL
```

5. **Inicializar la base de datos**:
```bash
python init_db.py
```

## Uso

1. Ejecutar el servidor:
```bash
python main.py
```

2. Abrir el navegador en: http://localhost:8000
3. Ver la documentación de la API en: http://localhost:8000/docs

## API Endpoints

### Productos

- `GET /products/` - Listar todos los productos
- `POST /products/` - Crear un nuevo producto
- `GET /products/{id}` - Obtener un producto por ID
- `PUT /products/{id}` - Actualizar un producto
- `DELETE /products/{id}` - Eliminar un producto

## Estructura del Producto

```json
{
  "id": "uuid",
  "name": "string",
  "description": "string",
  "price": 0.0,
  "stock_quantity": 0,
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

## Notas sobre la Arquitectura

Esta es una versión **base y educativa** que demuestra:

1. **Separación de capas**: Dominio, Aplicación, Infraestructura, Interfaces
2. **Inversión de dependencias**: El dominio no depende de la infraestructura
3. **Repository Pattern**: Abstracción de la capa de datos
4. **DTOs**: Separación entre modelos de dominio y API
5. **PostgreSQL**: Base de datos robusta para producción

Es ideal para:
- Aprender arquitectura hexagonal
- Entender principios SOLID
- Base para proyectos más complejos
- Desarrollo con PostgreSQL

## Comandos Útiles PostgreSQL

```bash
# Conectar a PostgreSQL
psql -U your_user -d ecommerce_db

# Ver tablas
\dt

# Ver datos de productos
SELECT * FROM products;

# Reiniciar base de datos
python init_db.py
```