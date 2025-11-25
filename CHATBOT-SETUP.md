# 🤖 Chatbot E-commerce con n8n - Resumen

## ✅ ¿Qué se ha configurado?

He integrado **n8n** a tu proyecto de e-commerce para crear un **chatbot inteligente** que permite a los usuarios interactuar con tu plataforma de forma conversacional.

## 📦 Archivos Creados

```
E-commerce/
├── docker-compose.yaml          [✓ Actualizado - Incluye servicio n8n]
└── n8n/
    ├── README.md                [✓ Documentación completa de n8n]
    ├── QUICKSTART.md            [✓ Guía de inicio rápido]
    ├── EJEMPLOS.md              [✓ Ejemplos de uso detallados]
    ├── test-chatbot.ps1         [✓ Script de pruebas]
    └── workflows/
        └── chatbot-ecommerce.json   [✓ Workflow del chatbot]
```

## 🚀 Cómo Usar el Chatbot

### Paso 1: Iniciar n8n
```powershell
cd C:\Users\afperez\E-commerce
docker-compose up -d n8n
```

### Paso 2: Acceder a n8n
1. Abre: **http://localhost:5678**
2. Credenciales:
   - **Usuario**: `admin`
   - **Contraseña**: `admin123`

### Paso 3: Importar el Workflow
1. En n8n, ve a **Workflows** (menú lateral)
2. Clic en **"Add Workflow"** → **"Import from File"**
3. Selecciona: `n8n/workflows/chatbot-ecommerce.json`
4. **¡IMPORTANTE!** Activa el workflow (botón "Active" en la esquina superior derecha)

### Paso 4: Probar el Chatbot

#### Opción A: Script Automático (Recomendado)
```powershell
cd n8n
.\test-chatbot.ps1
```

#### Opción B: Prueba Manual
```powershell
curl -X POST http://localhost:5678/webhook-test/chatbot `
  -H "Content-Type: application/json" `
  -d '{\"user_id\": \"user123\", \"message\": \"ayuda\"}'
```

## 💬 Comandos Disponibles

| Comando | Descripción | Ejemplo |
|---------|-------------|---------|
| `ayuda` | Muestra todos los comandos | `"ayuda"` |
| `ver productos` | Lista productos disponibles | `"ver productos"` |
| `ver carrito` | Muestra tu carrito | `"ver mi carrito"` |
| `mis órdenes` | Lista tus órdenes | `"mis órdenes"` |
| `pagar` | Información para pagar | `"pagar"` |

## 🔗 URLs Importantes

| Servicio | URL |
|----------|-----|
| **n8n Dashboard** | http://localhost:5678 |
| **Webhook Test** | http://localhost:5678/webhook-test/chatbot |
| **Webhook Prod** | http://localhost:5678/webhook/chatbot |

## 🎯 Características del Chatbot

### Lo que hace:
✅ Responde a comandos de texto en lenguaje natural  
✅ Consulta productos disponibles en tu backend  
✅ Muestra el carrito del usuario  
✅ Lista órdenes y su estado  
✅ Proporciona información sobre pagos  
✅ Interfaz conversacional amigable  

### Servicios integrados:
- **Product Service** (8000): Consulta de productos
- **User Service** (8001): Gestión de usuarios
- **Cart Service** (8003): Gestión del carrito
- **Order Service** (8005): Gestión de órdenes
- **Payment Service** (8007): Procesamiento de pagos

## 📊 Arquitectura del Chatbot

```
Usuario → Webhook n8n → Switch de Comandos
                          ├→ Consultar Productos → Product Service
                          ├→ Ver Carrito → Cart Service
                          ├→ Ver Órdenes → Order Service
                          ├→ Info Pagos → Payment Service
                          └→ Ayuda → Menú de Comandos
```

## 🧪 Ejemplo de Interacción

**Usuario**: `"ver productos"`  
**Chatbot**:
```
🛍️ Productos Disponibles:

1. Laptop Dell XPS 13 - $1299.99
   📦 Stock: 15 unidades
   ID: abc123...

2. Mouse Logitech MX - $79.99
   📦 Stock: 50 unidades
   ID: def456...

💬 Para agregar al carrito escribe: "agregar [product_id]"
```

## 🔧 Personalización

### Cambiar respuestas del chatbot:
1. Abre n8n → Edita el workflow
2. Busca nodos tipo "Set" (ej: "Formatear Productos", "Menú de Ayuda")
3. Modifica el campo "response"
4. Guarda y el cambio se aplica inmediatamente

### Agregar nuevos comandos:
1. Edita el nodo "Identificar Comando"
2. Agrega nueva regla en el "Switch"
3. Crea nodos para procesar el nuevo comando
4. Conecta con los servicios necesarios

## 📚 Documentación

- **Guía Rápida**: `n8n/QUICKSTART.md`
- **Ejemplos Detallados**: `n8n/EJEMPLOS.md`
- **Documentación Completa**: `n8n/README.md`

## 🐛 Solución de Problemas

### ❌ n8n no inicia
```powershell
docker-compose logs n8n
docker-compose up -d n8n
```

### ❌ Webhook no responde
1. Verifica que el workflow esté **activo** (botón verde)
2. Revisa la URL del webhook
3. Prueba con "Listen for test event" en n8n

### ❌ No se conecta con servicios
```powershell
# Verificar que todos los servicios estén corriendo
docker-compose ps

# Iniciar todos los servicios
docker-compose up -d
```

## 🎨 Próximos Pasos

### Puedes agregar:
- 🔍 Búsqueda de productos por nombre/categoría
- 🗑️ Eliminar items del carrito
- ❌ Cancelar órdenes
- 📊 Estadísticas de compras
- 🎫 Sistema de cupones de descuento
- 📱 Integración con WhatsApp/Telegram
- 🤖 IA con GPT para respuestas naturales

### Integrar con plataformas:
- **WhatsApp Business API**
- **Telegram Bot**
- **Slack**
- **Discord**
- **Facebook Messenger**

Solo necesitas agregar los nodos correspondientes en n8n.

## 💡 Tips

1. **Debugging**: Usa el panel "Executions" en n8n para ver el historial
2. **Testing**: Usa "Execute Node" para probar nodos individuales
3. **Logs**: `docker-compose logs -f n8n`
4. **Backup**: Exporta tus workflows regularmente

## 🔐 Seguridad

Para producción considera:
- Cambiar credenciales de n8n
- Implementar autenticación en webhooks
- Usar HTTPS
- Validar tokens de usuario
- Implementar rate limiting

## ✅ Resumen

Tu chatbot está listo para:
1. ✅ Iniciar con `docker-compose up -d n8n`
2. ✅ Acceder en http://localhost:5678
3. ✅ Importar el workflow
4. ✅ Activar y probar

¡Disfruta de tu nuevo chatbot! 🤖
