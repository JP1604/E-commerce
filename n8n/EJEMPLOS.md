# Ejemplos de Uso del Chatbot E-commerce

## 📋 Requisitos Previos

1. Tener todos los servicios corriendo:
```bash
docker-compose up -d
```

2. Importar el workflow en n8n:
   - Abre http://localhost:5678
   - Usuario: `admin` / Contraseña: `admin123`
   - Importa el archivo `chatbot-ecommerce.json`
   - Activa el workflow

3. Crear datos de prueba (usuarios, productos):
```bash
# Ver el script de inicialización en Backend/
```

## 🧪 Ejemplos de Peticiones

### 1. Ver Ayuda
```bash
curl -X POST http://localhost:5678/webhook-test/chatbot \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "123e4567-e89b-12d3-a456-426614174000",
    "message": "ayuda"
  }'
```

**Respuesta esperada:**
```
🤖 Bienvenido al Asistente Virtual de E-commerce
...
[Lista de comandos disponibles]
```

### 2. Ver Productos Disponibles
```bash
curl -X POST http://localhost:5678/webhook-test/chatbot \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "123e4567-e89b-12d3-a456-426614174000",
    "message": "ver productos"
  }'
```

**Respuesta esperada:**
```
🛍️ Productos Disponibles:

1. Laptop Dell XPS 13 - $1299.99
   📦 Stock: 15 unidades
   ID: abc123...

2. Mouse Logitech MX - $79.99
   📦 Stock: 50 unidades
   ID: def456...
```

### 3. Ver Mi Carrito
```bash
curl -X POST http://localhost:5678/webhook-test/chatbot \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "123e4567-e89b-12d3-a456-426614174000",
    "message": "ver mi carrito"
  }'
```

**Respuesta esperada:**
```
🛒 Tu Carrito:

1. Laptop Dell XPS 13 x1
   💰 Precio: $1299.99
   📊 Subtotal: $1299.99

💵 Total: $1299.99

💬 Escribe "crear orden" para continuar
```

### 4. Ver Mis Órdenes
```bash
curl -X POST http://localhost:5678/webhook-test/chatbot \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "123e4567-e89b-12d3-a456-426614174000",
    "message": "mis órdenes"
  }'
```

**Respuesta esperada:**
```
📦 Tus Órdenes:

1. Orden #abc12345
   📅 Fecha: 24/11/2025
   💰 Total: $1299.99
   📊 Estado: pagada
   🆔 ID: abc12345-e89b-12d3-a456-426614174000
```

### 5. Información de Pago
```bash
curl -X POST http://localhost:5678/webhook-test/chatbot \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "123e4567-e89b-12d3-a456-426614174000",
    "message": "pagar"
  }'
```

**Respuesta esperada:**
```
💳 Procesar Pago

Para procesar el pago de tu orden, por favor proporciona:

1️⃣ ID de la orden
2️⃣ Método de pago (credit_card, debit_card, paypal, bank_transfer, cash)

Ejemplo: "pagar [order_id] con credit_card"
```

## 🎯 Flujo Completo de Compra

### Paso 1: Ver productos disponibles
```bash
curl -X POST http://localhost:5678/webhook-test/chatbot \
  -H "Content-Type: application/json" \
  -d '{"user_id": "user123", "message": "ver productos"}'
```

### Paso 2: Agregar producto al carrito
Primero necesitas crear el carrito y agregar items usando el API directamente:

```bash
# Crear carrito
curl -X POST http://localhost:8003/api/v1/carts/ \
  -H "Content-Type: application/json" \
  -d '{"user_id": "user123"}'

# Agregar item (necesitas el cart_id de la respuesta anterior)
curl -X POST http://localhost:8003/api/v1/carts/{cart_id}/items \
  -H "Content-Type: application/json" \
  -d '{
    "product_id": "product123",
    "quantity": 1,
    "price": 1299.99
  }'
```

### Paso 3: Ver el carrito
```bash
curl -X POST http://localhost:5678/webhook-test/chatbot \
  -H "Content-Type: application/json" \
  -d '{"user_id": "user123", "message": "ver carrito"}'
```

### Paso 4: Crear orden
```bash
# Esto se hace directamente con el API
curl -X POST http://localhost:8005/api/v1/orders/ \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user123",
    "items": [
      {
        "product_id": "product123",
        "quantity": 1,
        "price": 1299.99
      }
    ],
    "total_amount": 1299.99,
    "status": "creada"
  }'
```

### Paso 5: Ver órdenes
```bash
curl -X POST http://localhost:5678/webhook-test/chatbot \
  -H "Content-Type: application/json" \
  -d '{"user_id": "user123", "message": "mis órdenes"}'
```

### Paso 6: Procesar pago
```bash
# Esto se hace directamente con el API
curl -X POST http://localhost:8007/api/v1/payments/process \
  -H "Content-Type: application/json" \
  -d '{
    "order_id": "order123",
    "user_id": "user123",
    "amount": 1299.99,
    "payment_method": "credit_card"
  }'
```

## 🔧 Pruebas con Postman

### Configuración de Colección

1. **Crear nueva colección**: "E-commerce Chatbot"
2. **Variables de entorno**:
   - `base_url`: http://localhost:5678
   - `webhook_path`: /webhook-test/chatbot
   - `user_id`: 123e4567-e89b-12d3-a456-426614174000

### Request Template

**POST** `{{base_url}}{{webhook_path}}`

**Headers:**
```
Content-Type: application/json
```

**Body (JSON):**
```json
{
  "user_id": "{{user_id}}",
  "message": "tu mensaje aquí"
}
```

### Tests a realizar

1. ✅ Comando de ayuda
2. ✅ Ver productos
3. ✅ Ver carrito vacío
4. ✅ Ver órdenes
5. ✅ Información de pago
6. ✅ Comando no reconocido

## 🐛 Debugging

### Ver logs de n8n:
```bash
docker-compose logs -f n8n
```

### Ver ejecuciones en n8n:
1. Abre http://localhost:5678
2. Ve a "Executions" en el menú lateral
3. Revisa el historial de ejecuciones

### Verificar servicios:
```bash
# Ver todos los contenedores
docker-compose ps

# Verificar product service
curl http://localhost:8000/docs

# Verificar cart service
curl http://localhost:8003/docs

# Verificar order service
curl http://localhost:8005/docs
```

## 📱 Integración con Frontend

Para integrar con tu aplicación web/móvil:

```javascript
// Ejemplo en JavaScript
async function sendMessageToChatbot(userId, message) {
  const response = await fetch('http://localhost:5678/webhook/chatbot', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      user_id: userId,
      message: message
    })
  });
  
  const data = await response.json();
  return data.response;
}

// Uso
const reply = await sendMessageToChatbot('user123', 'ver productos');
console.log(reply);
```

## 🌐 Integración con Plataformas de Mensajería

n8n puede integrarse con:
- WhatsApp Business API
- Telegram
- Slack
- Discord
- Facebook Messenger

Solo necesitas agregar los nodos correspondientes al workflow.

## 🔐 Consideraciones de Seguridad

Para producción:
1. Implementa autenticación de usuarios
2. Valida y sanitiza inputs
3. Usa HTTPS
4. Implementa rate limiting
5. Encripta datos sensibles
6. Usa tokens JWT para sesiones
