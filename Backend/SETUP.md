# Instrucciones de Instalación y Uso

## 🚀 Configuración Inicial

### 1. Clonar y navegar al directorio
```bash
cd Backend
```

### 2. Crear entorno virtual
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Instalar dependencias
```bash
# Instalación base
pip install -e .

# Para desarrollo (incluye herramientas de testing y linting)
pip install -e ".[dev]"

# Para PostgreSQL (opcional)
pip install -e ".[postgresql]"
```

### 4. Configurar variables de entorno
```bash
# Copiar archivo de ejemplo
copy .env.example .env

# Editar .env con tu configuración
# DATABASE_URL=sqlite+aiosqlite:///./ecommerce.db  # Para SQLite
# DATABASE_URL=postgresql+asyncpg://user:pass@localhost/ecommerce_db  # Para PostgreSQL
```

## 🏃‍♂️ Ejecutar la aplicación

### Desarrollo
```bash
# Con recarga automática
uvicorn main:app --reload

# O usando Python directamente
python main.py
```

### Producción
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

## 📋 Endpoints Disponibles

### Health Check
- `GET /` - Información básica de la API
- `GET /api/v1/health` - Estado de la aplicación

### Productos
- `POST /api/v1/products/` - Crear producto
- `GET /api/v1/products/{id}` - Obtener producto por ID
- `PUT /api/v1/products/{id}` - Actualizar producto
- `GET /api/v1/products/` - Listar productos (con paginación)
- `PATCH /api/v1/products/{id}/stock` - Actualizar stock
- `GET /api/v1/products/recommendations/` - Productos recomendados
- `GET /api/v1/products/alerts/low-stock` - Productos con stock bajo

### Usuarios
- `POST /api/v1/users/` - Crear usuario
- `GET /api/v1/users/{id}` - Obtener usuario por ID
- `PUT /api/v1/users/{id}` - Actualizar usuario
- `GET /api/v1/users/` - Listar usuarios (con paginación)
- `POST /api/v1/users/login` - Autenticar usuario

## 📖 Documentación API

Una vez ejecutada la aplicación:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## 🧪 Testing

```bash
# Ejecutar todos los tests
pytest

# Con coverage
pytest --cov=src --cov-report=html

# Solo tests unitarios
pytest tests/unit/

# Solo tests de integración
pytest tests/integration/
```

## 🛠️ Herramientas de Desarrollo

### Formateo de código
```bash
# Formatear con black
black src/ tests/

# Ordenar imports
isort src/ tests/

# Verificar estilo con flake8
flake8 src/ tests/

# Type checking con mypy
mypy src/
```

### Pre-commit hooks
```bash
# Instalar pre-commit
pre-commit install

# Ejecutar manualmente
pre-commit run --all-files
```

## 📊 Estructura de la Base de Datos

### Modelos principales:
- **Products**: Catálogo de productos
- **Users**: Usuarios del sistema

### Configuración SQLite (desarrollo):
```env
DATABASE_URL=sqlite+aiosqlite:///./ecommerce.db
```

### Configuración PostgreSQL (producción):
```env
DATABASE_URL=postgresql+asyncpg://user:password@localhost/ecommerce_db
```

## 🔧 Configuración Avanzada

### Variables de entorno principales:
- `DATABASE_URL`: URL de conexión a la base de datos
- `SECRET_KEY`: Clave secreta para JWT
- `DEBUG`: Modo debug (True/False)
- `BACKEND_CORS_ORIGINS`: Origins permitidos para CORS

### Configuración de logging:
El sistema usa logging estándar de Python. Los logs se muestran en consola por defecto.

## 🐳 Docker (Opcional)

```dockerfile
# Dockerfile de ejemplo
FROM python:3.11-slim

WORKDIR /app
COPY . .
RUN pip install -e .

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 📈 Próximos Pasos

1. **Implementar autenticación JWT completa**
2. **Agregar validaciones avanzadas**
3. **Implementar cache con Redis**
4. **Agregar logging estructurado**
5. **Implementar rate limiting**
6. **Agregar métricas y monitoring**
7. **Configurar CI/CD**

## 🤝 Contribuir

1. Fork del repositorio
2. Crear rama feature (`git checkout -b feature/nueva-caracteristica`)
3. Commit de cambios (`git commit -am 'Agregar nueva característica'`)
4. Push a la rama (`git push origin feature/nueva-caracteristica`)
5. Crear Pull Request

## 📝 Notas de Implementación

- La arquitectura hexagonal permite fácil testeo y mantenimiento
- Las dependencias fluyen hacia adentro (dominio no depende de infraestructura)
- Los adaptadores (repositorios, servicios externos) están en la capa de infraestructura
- Los casos de uso orquestan la lógica de negocio
- La API REST es solo una interfaz más (se puede agregar GraphQL, gRPC, etc.)

## ⚠️ Limitaciones Actuales

- Autenticación simulada (no implementa JWT real)
- Hashing de passwords no implementado
- Sin migraciones de base de datos (usa create_all)
- Tests de integración requieren configuración adicional
- No incluye containerización completa