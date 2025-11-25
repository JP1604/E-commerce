# ✅ Configuración Completa del Chatbot n8n

## 🎉 ¡Todo está listo!

He configurado exitosamente un chatbot con n8n para tu plataforma de e-commerce.

---

## 📁 Archivos Creados

```
E-commerce/
├── docker-compose.yaml           ✅ Actualizado con servicio n8n
├── CHATBOT-SETUP.md              ✅ Guía de configuración
└── n8n/
    ├── README.md                 ✅ Documentación completa
    ├── QUICKSTART.md             ✅ Guía de inicio rápido
    ├── EJEMPLOS.md               ✅ Ejemplos de uso
    ├── test-chatbot.ps1          ✅ Script de pruebas automáticas
    └── workflows/
        └── chatbot-ecommerce.json ✅ Workflow del chatbot
```

---

## 🚀 Pasos Siguientes

### 1. Acceder a n8n
n8n ya está corriendo. Abre tu navegador en:

🌐 **http://localhost:5678**

**Credenciales:**
- 👤 Usuario: `admin`
- 🔑 Contraseña: `admin123`

### 2. Importar el Workflow del Chatbot

1. En n8n, haz clic en **"Workflows"** (menú izquierdo)
2. Clic en **"Add Workflow"** → **"Import from File"**
3. Selecciona el archivo:
   ```
   C:\Users\afperez\E-commerce\n8n\workflows\chatbot-ecommerce.json
   ```
4. Una vez importado, **activa el workflow**:
   - Botón **"Active"** (esquina superior derecha debe estar en verde)

### 3. Probar el Chatbot

#### Opción A: Script Automático (Recomendado) 🎯
```powershell
cd C:\Users\afperez\E-commerce\n8n
.\test-chatbot.ps1
```

Este script:
- ✅ Verifica que n8n esté corriendo
- ✅ Ejecuta 6 pruebas diferentes
- ✅ Muestra las respuestas del chatbot
- ✅ Incluye modo interactivo

#### Opción B: Prueba Manual 🔧
```powershell
curl -X POST http://localhost:5678/webhook-test/chatbot `
  -H "Content-Type: application/json" `
  -d '{\"user_id\": \"user123\", \"message\": \"ayuda\"}'
```

---

## 💬 Comandos del Chatbot

| Comando | Qué hace | Ejemplo |
|---------|----------|---------|
| `ayuda` | Muestra menú de ayuda | `"ayuda"` |
| `ver productos` | Lista productos | `"ver productos"` |
| `ver carrito` | Muestra tu carrito | `"ver mi carrito"` |
| `mis órdenes` | Lista tus órdenes | `"mis órdenes"` |
| `pagar` | Info sobre pagos | `"pagar"` |

---

## 🔗 URLs del Chatbot

| Tipo | URL | Uso |
|------|-----|-----|
| **Test** | http://localhost:5678/webhook-test/chatbot | Pruebas y desarrollo |
| **Producción** | http://localhost:5678/webhook/chatbot | Uso en producción |

---

## 🎯 Ejemplo de Petición

### Con PowerShell:
```powershell
$body = @{
    user_id = "user123"
    message = "ver productos"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:5678/webhook-test/chatbot" `
  -Method Post `
  -Body $body `
  -ContentType "application/json"
```

### Con curl:
```bash
curl -X POST http://localhost:5678/webhook-test/chatbot \
  -H "Content-Type: application/json" \
  -d '{"user_id": "user123", "message": "ver productos"}'
```

### Respuesta Esperada:
```
🛍️ Productos Disponibles:

1. Laptop Dell XPS 13 - $1299.99
   📦 Stock: 15 unidades
   ID: abc123...

💬 Para agregar al carrito escribe: "agregar [product_id]"
```

---

## 🔧 Integración con tu Backend

El chatbot se comunica con tus microservicios:

| Servicio | Puerto | Función en el Chatbot |
|----------|--------|----------------------|
| **Product Service** | 8000 | Consulta de productos |
| **User Service** | 8001 | Gestión de usuarios |
| **Cart Service** | 8003 | Gestión del carrito |
| **Order Service** | 8005 | Gestión de órdenes |
| **Payment Service** | 8007 | Procesamiento de pagos |

---

## 📊 Arquitectura del Flujo

```
Usuario envía mensaje
    ↓
Webhook n8n recibe petición
    ↓
Switch identifica comando
    ↓
┌─────────────┬─────────────┬─────────────┬─────────────┐
│  Productos  │   Carrito   │   Órdenes   │    Ayuda    │
│      ↓      │      ↓      │      ↓      │      ↓      │
│   API 8000  │   API 8003  │   API 8005  │   Menú     │
│      ↓      │      ↓      │      ↓      │      ↓      │
│  Formatear  │  Formatear  │  Formatear  │  Formatear  │
└─────────────┴─────────────┴─────────────┴─────────────┘
    ↓
Respuesta al usuario
```

---

## 🎨 Personalización

### Cambiar Respuestas:
1. Abre n8n → Edita el workflow
2. Busca nodos tipo "Set" (ej: "Formatear Productos")
3. Modifica el campo `response`
4. Guarda (el cambio se aplica inmediatamente)

### Agregar Nuevos Comandos:
1. Edita el nodo "Identificar Comando"
2. Agrega nueva condición en el Switch
3. Crea nodos para procesar el comando
4. Conecta con los servicios necesarios

---

## 📱 Integración con Aplicaciones

### JavaScript/TypeScript:
```javascript
async function sendToChatbot(userId, message) {
  const response = await fetch('http://localhost:5678/webhook/chatbot', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ user_id: userId, message: message })
  });
  return await response.json();
}

// Uso:
const reply = await sendToChatbot('user123', 'ver productos');
console.log(reply.response);
```

### Python:
```python
import requests

def send_to_chatbot(user_id, message):
    response = requests.post(
        'http://localhost:5678/webhook/chatbot',
        json={'user_id': user_id, 'message': message}
    )
    return response.json()

# Uso:
reply = send_to_chatbot('user123', 'ver productos')
print(reply['response'])
```

---

## 🌐 Integración con WhatsApp/Telegram

n8n puede integrarse fácilmente con:
- ✅ WhatsApp Business API
- ✅ Telegram Bot
- ✅ Slack
- ✅ Discord
- ✅ Facebook Messenger
- ✅ Microsoft Teams

Solo necesitas:
1. Agregar el nodo correspondiente en n8n
2. Configurar las credenciales
3. Conectar con tu workflow actual

---

## 🐛 Troubleshooting

### ❌ n8n no responde
```powershell
# Ver logs
docker-compose logs n8n

# Reiniciar
docker-compose restart n8n
```

### ❌ Webhook no funciona
- ✅ Verifica que el workflow esté **activo** (botón verde)
- ✅ Prueba con "Listen for test event" en n8n
- ✅ Revisa la URL del webhook

### ❌ No se conecta con servicios
```powershell
# Ver servicios corriendo
docker ps

# Verificar conectividad
docker exec -it n8n_ecommerce curl http://product_service:8000/docs
```

---

## 📚 Documentación

- 📖 **Guía Rápida**: `n8n/QUICKSTART.md`
- 📝 **Ejemplos**: `n8n/EJEMPLOS.md`
- 📘 **Completa**: `n8n/README.md`
- 🎯 **Este resumen**: `CHATBOT-SETUP.md`

---

## 🎉 ¡Listo para Usar!

Tu chatbot está **100% configurado** y listo para:
- ✅ Responder preguntas de usuarios
- ✅ Consultar productos
- ✅ Gestionar carritos
- ✅ Revisar órdenes
- ✅ Procesar información de pagos

### Próximos Pasos Recomendados:

1. **Ahora**: Importa el workflow y pruébalo
2. **Hoy**: Personaliza las respuestas
3. **Esta semana**: Agrega más comandos
4. **Próximo**: Integra con WhatsApp/Telegram

---

## 💡 Tips Finales

- 🔍 **Debugging**: Panel "Executions" en n8n muestra historial
- 🧪 **Testing**: Botón "Execute Node" prueba nodos individuales
- 📊 **Logs**: `docker-compose logs -f n8n`
- 💾 **Backup**: Exporta workflows regularmente
- 🔐 **Seguridad**: Cambia credenciales para producción

---

## 🙋 ¿Necesitas Ayuda?

Revisa la documentación en la carpeta `n8n/` o:
- Ejecuta: `.\test-chatbot.ps1` para pruebas automáticas
- Abre n8n en http://localhost:5678 y explora el workflow
- Revisa los logs: `docker-compose logs n8n`

---

**¡Disfruta de tu nuevo chatbot! 🤖✨**
