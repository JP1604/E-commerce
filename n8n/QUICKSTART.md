# 🚀 Guía de Configuración Rápida - n8n Chatbot

## ⚡ Inicio Rápido (5 minutos)

### 1. Iniciar n8n
```bash
cd C:\Users\afperez\E-commerce
docker-compose up -d n8n
```

Espera unos segundos y verifica:
```bash
docker-compose ps n8n
```

### 2. Acceder a n8n
1. Abre tu navegador en: **http://localhost:5678**
2. Credenciales:
   - **Usuario**: `admin`
   - **Contraseña**: `admin123`

### 3. Importar el Workflow del Chatbot
1. En n8n, haz clic en **"Workflows"** (menú lateral izquierdo)
2. Clic en **"Add Workflow"** → **"Import from File"**
3. Selecciona el archivo: `n8n/workflows/chatbot-ecommerce.json`
4. Una vez importado, verás el workflow completo
5. **¡IMPORTANTE!** Haz clic en el botón **"Active"** (esquina superior derecha) para activar el workflow

### 4. Probar el Chatbot

#### Opción A: Script Automático (Recomendado)
```powershell
cd n8n
.\test-chatbot.ps1
```

#### Opción B: Manual con curl
```bash
curl -X POST http://localhost:5678/webhook-test/chatbot -H "Content-Type: application/json" -d "{\"user_id\": \"user123\", \"message\": \"ayuda\"}"
```

#### Opción C: Desde n8n (Modo Test)
1. En el workflow, haz clic en el nodo **"Webhook"**
2. Clic en **"Listen for test event"**
3. Envía una petición de prueba
4. Verás la respuesta en n8n

---

## 🎯 URLs Importantes

| Servicio | URL | Descripción |
|----------|-----|-------------|
| n8n Dashboard | http://localhost:5678 | Interfaz de n8n |
| Webhook Test | http://localhost:5678/webhook-test/chatbot | Webhook para pruebas |
| Webhook Prod | http://localhost:5678/webhook/chatbot | Webhook producción |
| Product Service | http://localhost:8000/docs | API de productos |
| User Service | http://localhost:8001/docs | API de usuarios |
| Cart Service | http://localhost:8003/docs | API de carrito |
| Order Service | http://localhost:8005/docs | API de órdenes |
| Payment Service | http://localhost:8007/docs | API de pagos |

---

## 📱 Comandos del Chatbot

| Comando | Descripción | Ejemplo |
|---------|-------------|---------|
| `ayuda` | Muestra todos los comandos | `"ayuda"` |
| `ver productos` | Lista productos disponibles | `"ver productos"` |
| `buscar [nombre]` | Busca productos | `"buscar laptop"` |
| `ver carrito` | Muestra tu carrito | `"ver mi carrito"` |
| `agregar [id]` | Agrega producto al carrito | `"agregar abc123"` |
| `mis órdenes` | Lista tus órdenes | `"mis órdenes"` |
| `estado orden [id]` | Estado de una orden | `"estado orden abc123"` |
| `pagar` | Info para pagar | `"pagar"` |

---

## 🔧 Configuración Avanzada

### Cambiar el Puerto de n8n
Edita `docker-compose.yaml`:
```yaml
n8n:
  ports:
    - "5678:5678"  # Cambia 5678 por el puerto deseado
```

### Cambiar Credenciales
Edita `docker-compose.yaml`:
```yaml
environment:
  - N8N_BASIC_AUTH_USER=tu_usuario
  - N8N_BASIC_AUTH_PASSWORD=tu_contraseña
```

### Personalizar Respuestas del Chatbot
1. Abre n8n
2. Edita el workflow
3. Busca los nodos de tipo "Set" (ej: "Formatear Productos", "Menú de Ayuda")
4. Modifica el campo "response" con tu texto personalizado
5. Guarda el workflow

---

## 🐛 Solución de Problemas

### ❌ Error: "No se puede conectar a n8n"
**Solución:**
```bash
# Verificar que n8n esté corriendo
docker-compose ps n8n

# Si no está corriendo, iniciarlo
docker-compose up -d n8n

# Ver logs para más detalles
docker-compose logs -f n8n
```

### ❌ Error: "Webhook no responde"
**Solución:**
1. Verifica que el workflow esté **activo** (botón "Active" en verde)
2. Verifica la URL del webhook en el nodo "Webhook"
3. Prueba con el botón "Listen for test event"

### ❌ Error: "No se conecta con los servicios"
**Solución:**
```bash
# Verificar que todos los servicios estén corriendo
docker-compose ps

# Iniciar todos los servicios
docker-compose up -d

# Verificar conectividad desde n8n
docker exec -it n8n_ecommerce curl http://product_service:8000/api/v1/products/
```

### ❌ Error: "Respuesta vacía del servicio"
**Solución:**
1. Verifica que haya datos de prueba en los servicios
2. Crea productos/usuarios/carritos de prueba
3. Revisa los logs del servicio específico:
```bash
docker-compose logs product_service
docker-compose logs cart_service
```

---

## 📊 Monitoreo

### Ver Ejecuciones del Workflow
1. En n8n, ve a **"Executions"** (menú lateral)
2. Verás todas las ejecuciones con su estado (success/error)
3. Haz clic en cualquier ejecución para ver detalles

### Ver Logs en Tiempo Real
```bash
# Logs de n8n
docker-compose logs -f n8n

# Logs de todos los servicios
docker-compose logs -f
```

### Verificar Estado de Servicios
```bash
# Ver todos los contenedores
docker-compose ps

# Verificar salud de un servicio
curl http://localhost:8000/docs  # Product Service
curl http://localhost:8003/docs  # Cart Service
```

---

## 🚀 Próximos Pasos

### 1. Agregar Más Funcionalidades al Chatbot
- Búsqueda de productos por categoría
- Eliminar items del carrito
- Cancelar órdenes
- Consultar historial de pagos
- Soporte para cupones de descuento

### 2. Integrar con Plataformas de Mensajería
En n8n puedes agregar nodos para:
- **WhatsApp Business API**: Chatbot en WhatsApp
- **Telegram**: Bot de Telegram
- **Slack**: Integración con Slack
- **Discord**: Bot de Discord

### 3. Agregar Inteligencia Artificial
- Integrar OpenAI GPT para respuestas más naturales
- Usar NLU (Natural Language Understanding) para entender mejor los mensajes
- Implementar recomendaciones de productos

### 4. Mejorar la Experiencia de Usuario
- Agregar botones interactivos
- Incluir imágenes de productos
- Enviar notificaciones proactivas
- Implementar sesiones de usuario

---

## 📚 Recursos Adicionales

- **Documentación de n8n**: https://docs.n8n.io
- **Comunidad n8n**: https://community.n8n.io
- **Ejemplos de workflows**: https://n8n.io/workflows

---

## 💡 Tips y Trucos

### Debugging en n8n
1. Usa el botón **"Execute Node"** para probar nodos individuales
2. Activa **"Save successful executions"** en settings
3. Usa nodos "Set" para imprimir valores intermedios

### Optimización
1. Cachea respuestas frecuentes
2. Usa "If" nodes para validar inputs antes de hacer llamadas HTTP
3. Implementa retry logic para APIs inestables

### Seguridad
1. Nunca expongas credenciales en el workflow
2. Usa variables de entorno para datos sensibles
3. Implementa rate limiting en producción
4. Valida y sanitiza todos los inputs del usuario

---

## 🎉 ¡Listo!

Tu chatbot está configurado y funcionando. Puedes empezar a probarlo enviando mensajes al webhook.

**Webhook Test URL**: http://localhost:5678/webhook-test/chatbot

**Ejemplo de petición:**
```json
{
  "user_id": "user123",
  "message": "ver productos"
}
```

¡Disfruta de tu chatbot! 🤖
