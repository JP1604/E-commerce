# 🧪 Pruebas de Integración - E-commerce Microservices

Este directorio contiene las pruebas de integración para validar la funcionalidad de las entidades del sistema de e-commerce.

## 🚀 Ejecución de Pruebas

### Comando Principal
```bash
cd Backend
python -m pytest tests/integration/test_simple_integration.py -v
```

### Resultado Esperado
```
======================== 8 passed, 2 warnings in 0.37s =======================
```

## 📊 Pruebas Implementadas

Las pruebas validan:
- ✅ **Creación de entidades** (Product, Cart)
- ✅ **Validación de enums** (ProductStatus, CartStatus)
- ✅ **Validación de datos** (campos requeridos, precios)
- ✅ **Serialización** (métodos to_dict)
- ✅ **Manejo de UUIDs** y timestamps
- ✅ **Lógica de negocio** funcionando correctamente

