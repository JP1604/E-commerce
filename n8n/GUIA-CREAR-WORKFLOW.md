# 🎨 Guía: Crear Workflow del Chatbot desde Cero en n8n

## 📋 Prerequisitos

✅ n8n debe estar corriendo (docker-compose up -d n8n)  
✅ Navegador abierto en: http://localhost:5678  
✅ Credenciales: `admin` / `admin123`

---

## 🚀 Paso 1: Crear Nuevo Workflow

1. **Inicia sesión en n8n** con las credenciales
2. En el menú lateral izquierdo, haz clic en **"Workflows"**
3. Haz clic en el botón **"+ Add Workflow"** (arriba a la derecha)
4. Dale un nombre al workflow: **"Chatbot E-commerce"**

---

## 🎯 Paso 2: Agregar el Webhook (Trigger)

El webhook es el punto de entrada donde los usuarios enviarán mensajes.

### Acción:
1. Haz clic en el botón **"+ Add first step"** en el canvas
2. Busca **"Webhook"** en el buscador
3. Selecciona **"Webhook"** (el trigger, no el nodo de acción)

### Configuración del Webhook:
```
HTTP Method: POST
Path: chatbot
Response Mode: Respond to Webhook
```

### Resultado:
- Verás la URL del webhook generada automáticamente
- Ejemplo: `http://localhost:5678/webhook-test/chatbot`

---

## 🎯 Paso 3: Agregar el Switch (Identificar Comandos)

Este nodo analizará el mensaje del usuario y lo dirigirá al flujo correcto.

### Acción:
1. Haz clic en el **"+"** después del nodo Webhook
2. Busca **"Switch"** y selecciónalo

### Configuración del Switch:

#### Mode: `Rules`

#### Regla 1 - Ver Productos:
```
Output: 0
Conditions: String
  - Value 1: {{ $json.body.message.toLowerCase() }}
  - Operation: contains
  - Value 2: productos
```

#### Regla 2 - Ver Carrito:
```
Output: 1
Conditions: String
  - Value 1: {{ $json.body.message.toLowerCase() }}
  - Operation: contains
  - Value 2: carrito
```

#### Regla 3 - Ver Órdenes:
```
Output: 2
Conditions: String
  - Value 1: {{ $json.body.message.toLowerCase() }}
  - Operation: contains
  - Value 2: orden
```

#### Regla 4 - Información de Pago:
```
Output: 3
Conditions: String
  - Value 1: {{ $json.body.message.toLowerCase() }}
  - Operation: contains
  - Value 2: pagar
```

#### Regla 5 - Ayuda:
```
Output: 4
Conditions: String
  - Value 1: {{ $json.body.message.toLowerCase() }}
  - Operation: contains
  - Value 2: ayuda
```

#### Fallback (Default):
- Deja activado "Fallback Output"

---

## 🎯 Paso 4: Flujo de "Ver Productos"

### 4.1 Agregar HTTP Request:
1. Desde la salida **0** del Switch, agrega **"HTTP Request"**

**Configuración:**
```
Method: GET
URL: http://product_service:8000/api/v1/products/
```

**Nota**: Usamos `product_service` (nombre del contenedor) en lugar de `localhost`

### 4.2 Formatear Respuesta:
1. Después del HTTP Request, agrega un nodo **"Set"**
2. Renómbralo a: **"Formatear Productos"**

**Configuración:**
```
Keep Only Set: false

Values to Set:
  - Name: response
  - Type: String
  - Value:
```

```javascript
🛍️ **Productos Disponibles:**

{{ $json.map((p, i) => `${i+1}. **${p.name}** - $${p.price}
   📦 Stock: ${p.stock_quantity} unidades
   ID: ${p.id}`).join('\n\n') }}

💬 Para agregar al carrito escribe: "agregar [product_id]"
```

---

## 🎯 Paso 5: Flujo de "Ver Carrito"

### 5.1 Agregar HTTP Request:
1. Desde la salida **1** del Switch, agrega **"HTTP Request"**

**Configuración:**
```
Method: GET
URL: http://cart_service:8003/api/v1/carts/user/{{ $('Webhook').item.json.body.user_id }}
```

### 5.2 Formatear Respuesta:
1. Después del HTTP Request, agrega un nodo **"Set"**
2. Renómbralo a: **"Formatear Carrito"**

**Configuración:**
```
Values to Set:
  - Name: response
  - Type: String
  - Value:
```

```javascript
🛒 **Tu Carrito:**

{{ $json.items && $json.items.length > 0 ? 
   $json.items.map((item, i) => `${i+1}. ${item.product_name || 'Producto'} x${item.quantity}
   💰 Precio: $${item.price}
   📊 Subtotal: $${item.price * item.quantity}`).join('\n\n') + 
   '\n\n💵 **Total: $' + $json.items.reduce((sum, item) => sum + (item.price * item.quantity), 0) + '**' 
   : '¡Tu carrito está vacío! 😊\n\nEscribe "ver productos" para empezar a comprar.' 
}}

💬 Escribe "crear orden" para continuar
```

---

## 🎯 Paso 6: Flujo de "Ver Órdenes"

### 6.1 Agregar HTTP Request:
1. Desde la salida **2** del Switch, agrega **"HTTP Request"**

**Configuración:**
```
Method: GET
URL: http://order_service:8005/api/v1/orders/user/{{ $('Webhook').item.json.body.user_id }}
```

### 6.2 Formatear Respuesta:
1. Después del HTTP Request, agrega un nodo **"Set"**
2. Renómbralo a: **"Formatear Órdenes"**

**Configuración:**
```
Values to Set:
  - Name: response
  - Type: String
  - Value:
```

```javascript
📦 **Tus Órdenes:**

{{ $json.length > 0 ? 
   $json.map((order, i) => `${i+1}. **Orden #${order.id.slice(0,8)}**
   📅 Fecha: ${new Date(order.created_at).toLocaleDateString()}
   💰 Total: $${order.total_amount}
   📊 Estado: ${order.status}
   🆔 ID: ${order.id}`).join('\n\n') 
   : '¡No tienes órdenes aún! 😊\n\nEscribe "ver productos" para empezar a comprar.' 
}}

💬 Para ver detalles escribe: "estado orden [order_id]"
```

---

## 🎯 Paso 7: Flujo de "Información de Pago"

### 7.1 Agregar Set (sin HTTP Request):
1. Desde la salida **3** del Switch, agrega **"Set"**
2. Renómbralo a: **"Instrucciones de Pago"**

**Configuración:**
```
Values to Set:
  - Name: response
  - Type: String
  - Value:
```

```
💳 **Procesar Pago**

Para procesar el pago de tu orden, por favor proporciona:

1️⃣ ID de la orden
2️⃣ Método de pago (credit_card, debit_card, paypal, bank_transfer, cash)

Ejemplo: "pagar [order_id] con credit_card"

💬 ¿Necesitas ayuda? Escribe "ayuda"
```

---

## 🎯 Paso 8: Flujo de "Ayuda"

### 8.1 Agregar Set:
1. Desde la salida **4** del Switch, agrega **"Set"**
2. Renómbralo a: **"Menú de Ayuda"**

**Configuración:**
```
Values to Set:
  - Name: response
  - Type: String
  - Value:
```

```
🤖 **Bienvenido al Asistente Virtual de E-commerce**

¿En qué puedo ayudarte hoy? Estos son los comandos disponibles:

🛍️ **Productos**
• "ver productos" - Lista todos los productos
• "buscar [nombre]" - Busca productos específicos

🛒 **Carrito**
• "agregar [product_id]" - Agrega producto al carrito
• "ver carrito" - Muestra tu carrito actual
• "vaciar carrito" - Limpia tu carrito

📦 **Órdenes**
• "crear orden" - Crea orden con tu carrito
• "mis órdenes" - Lista todas tus órdenes
• "estado orden [order_id]" - Consulta estado de una orden

💳 **Pagos**
• "pagar orden [order_id]" - Procesa el pago
• "métodos de pago" - Muestra opciones de pago

❓ **Ayuda**
• "ayuda" - Muestra este menú
• "soporte" - Contacta con soporte

💬 ¿Qué te gustaría hacer?
```

---

## 🎯 Paso 9: Flujo Fallback (Default)

### 9.1 Agregar Set:
1. Desde la salida **Fallback** del Switch, agrega **"Set"**
2. Renómbralo a: **"Respuesta Predeterminada"**

**Configuración:**
```
Values to Set:
  - Name: response
  - Type: String
  - Value:
```

```javascript
❌ **Lo siento, no entendí tu mensaje**

"{{ $('Webhook').item.json.body.message }}"

Por favor, intenta con uno de estos comandos:
• ver productos
• ver carrito
• mis órdenes
• ayuda

💬 ¿En qué puedo ayudarte?
```

---

## 🎯 Paso 10: Agregar el Nodo de Respuesta

Este nodo final enviará la respuesta al usuario.

### Acción:
1. Conecta **TODOS** los nodos "Set" (Formatear Productos, Formatear Carrito, etc.) a un único nodo **"Respond to Webhook"**
2. Busca **"Respond to Webhook"** y agrégalo

**Configuración:**
```
Respond With: All Incoming Items
```

### Resultado:
El workflow debe verse así:

```
Webhook → Switch → [6 ramas]
                   ├→ HTTP Request (Productos) → Set → Respond
                   ├→ HTTP Request (Carrito) → Set → Respond
                   ├→ HTTP Request (Órdenes) → Set → Respond
                   ├→ Set (Pago) → Respond
                   ├→ Set (Ayuda) → Respond
                   └→ Set (Default) → Respond
```

---

## 🎯 Paso 11: Activar y Probar

### 11.1 Guardar el Workflow:
1. Haz clic en el botón **"Save"** (arriba a la derecha)

### 11.2 Activar:
1. Haz clic en el botón **"Inactive"** para cambiarlo a **"Active"** (verde)

### 11.3 Probar con "Listen for test event":
1. Haz clic en el nodo **Webhook**
2. Clic en **"Listen for test event"**
3. En otra terminal ejecuta:

```powershell
curl -X POST http://localhost:5678/webhook-test/chatbot `
  -H "Content-Type: application/json" `
  -d '{\"user_id\": \"user123\", \"message\": \"ayuda\"}'
```

4. Deberías ver la ejecución en n8n y la respuesta del chatbot

---

## 🎯 Paso 12: Ver Ejecuciones

1. En el menú lateral, haz clic en **"Executions"**
2. Verás el historial de todas las ejecuciones
3. Haz clic en cualquiera para ver los detalles

---

## 🐛 Troubleshooting

### ❌ Error: "Could not connect to product_service"
**Solución**: Verifica que los servicios estén corriendo:
```powershell
docker ps | Select-String "product_service"
```

Si no está corriendo:
```powershell
docker-compose up -d product_service
```

### ❌ El Switch no funciona
**Solución**: Verifica que:
- Las expresiones usen `.toLowerCase()`
- La operación sea "contains" no "equals"
- El path sea `$json.body.message`

### ❌ El webhook no responde
**Solución**:
1. Verifica que el workflow esté **Active** (verde)
2. Usa la URL correcta: `/webhook-test/chatbot`
3. Verifica el método sea POST

---

## ✅ Resultado Final

Tu workflow debe:
- ✅ Recibir mensajes via webhook
- ✅ Identificar comandos del usuario
- ✅ Consultar los microservicios
- ✅ Formatear respuestas bonitas
- ✅ Responder al usuario

---

## 🎉 ¡Felicidades!

Has creado tu primer chatbot con n8n. Ahora puedes:
- Personalizarlo con tu marca
- Agregar más comandos
- Integrar con WhatsApp/Telegram
- Agregar IA con GPT

---

## 📝 Notas Importantes

1. **URLs de servicios**: Usa nombres de contenedor, no `localhost`
   - ✅ `http://product_service:8000`
   - ❌ `http://localhost:8000`

2. **Expresiones de n8n**: Usa `{{ }}` para variables
   - Ejemplo: `{{ $json.body.message }}`

3. **Acceso a datos**: 
   - Del webhook: `$('Webhook').item.json.body.user_id`
   - Del nodo actual: `$json.items`
   - De un nodo específico: `$('HTTP Request').item.json.data`

4. **Testing**: Siempre prueba con "Listen for test event" antes de activar

---

## 🚀 Próximos Pasos

1. ✅ Crea datos de prueba en tus servicios
2. ✅ Prueba cada comando del chatbot
3. ✅ Personaliza las respuestas
4. ✅ Agrega más funcionalidades
5. ✅ Integra con aplicaciones frontend

¡Disfruta de tu chatbot! 🤖
