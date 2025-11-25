# n8n Chatbot para E-commerce

## 🚀 Configuración

### Credenciales de acceso
- **URL**: http://localhost:5678
- **Usuario**: admin
- **Contraseña**: admin123

### Iniciar n8n
```bash
docker-compose up -d n8n
```

## 🤖 Workflows Disponibles

### 1. Chatbot E-commerce
**Archivo**: `chatbot-ecommerce.json`

Este workflow permite a los usuarios interactuar con el chatbot para:
- Consultar productos disponibles
- Ver detalles de productos específicos
- Agregar productos al carrito
- Consultar estado de órdenes
- Realizar pagos

### Webhook URL
- **Test**: http://localhost:5678/webhook-test/chatbot
- **Production**: http://localhost:5678/webhook/chatbot

## 📋 Funcionalidades del Chatbot

### Comandos Disponibles

1. **Ver productos** - Lista todos los productos disponibles
2. **Buscar producto [nombre]** - Busca productos por nombre
3. **Agregar al carrito [product_id]** - Agrega un producto al carrito
4. **Ver mi carrito** - Muestra los items del carrito actual
5. **Crear orden** - Crea una orden con los items del carrito
6. **Pagar orden [order_id]** - Procesa el pago de una orden
7. **Mis órdenes** - Lista todas las órdenes del usuario
8. **Estado orden [order_id]** - Consulta el estado de una orden
9. **Ayuda** - Muestra todos los comandos disponibles

## 🔧 Integración con Backend

El chatbot se comunica con los siguientes servicios:

- **Product Service** (8000): Consulta de productos
- **User Service** (8001): Gestión de usuarios
- **Cart Service** (8003): Gestión del carrito
- **Order Service** (8005): Gestión de órdenes
- **Payment Service** (8007): Procesamiento de pagos

## 📝 Importar Workflows

1. Abre n8n en http://localhost:5678
2. Inicia sesión con las credenciales
3. Ve a **Workflows** → **Import from File**
4. Selecciona el archivo `chatbot-ecommerce.json`
5. Activa el workflow

## 🧪 Probar el Chatbot

### Usando curl:
```bash
curl -X POST http://localhost:5678/webhook-test/chatbot \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "123e4567-e89b-12d3-a456-426614174000",
    "message": "ver productos"
  }'
```

### Usando Postman:
1. Método: POST
2. URL: http://localhost:5678/webhook-test/chatbot
3. Body (JSON):
```json
{
  "user_id": "123e4567-e89b-12d3-a456-426614174000",
  "message": "ayuda"
}
```

## 🎨 Personalización

### Agregar nuevos comandos:
1. Edita el workflow en n8n
2. Agrega un nuevo "Switch" branch para el comando
3. Conecta con el servicio correspondiente
4. Define la respuesta del chatbot

### Cambiar respuestas:
Las respuestas del chatbot están en los nodos "Set" de cada comando. Puedes personalizarlas según tu marca.

## 🔐 Seguridad

Para producción, considera:
- Cambiar las credenciales de n8n
- Implementar autenticación en webhooks
- Usar HTTPS
- Validar tokens de usuario
- Implementar rate limiting

## 📊 Monitoreo

Puedes ver la ejecución de workflows en:
- n8n Dashboard → Executions
- Logs del contenedor: `docker-compose logs -f n8n`

## 🆘 Troubleshooting

### El webhook no responde:
1. Verifica que n8n esté corriendo: `docker ps | grep n8n`
2. Verifica que el workflow esté activo
3. Revisa los logs: `docker-compose logs n8n`

### Error al conectar con servicios:
1. Verifica que todos los servicios estén corriendo
2. Usa nombres de contenedor en las URLs (no localhost)
3. Verifica las variables de entorno en docker-compose.yaml
