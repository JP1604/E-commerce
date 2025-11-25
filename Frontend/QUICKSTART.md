# Guía de Inicio Rápido - Frontend E-Commerce

## 🎯 Inicio Rápido

### 1. Iniciar servicios del Backend (Docker)

```powershell
cd c:\Users\afperez\E-commerce
docker-compose up -d
```

Esto iniciará:
- ✅ Product Service (puerto 8000)
- ✅ Cart Service (puerto 8003)
- ✅ Order Service (puerto 8005)
- ✅ n8n (puerto 5678)
- ✅ PostgreSQL databases

### 2. Activar el workflow de n8n

1. Abre http://localhost:5678 en tu navegador
2. Login: `admin` / `admin123`
3. Abre el workflow "E-Commerce Chatbot"
4. Haz clic en el botón "Active" (esquina superior derecha)
5. Verifica que el estado sea **"Active"**

### 3. Iniciar el Frontend

```powershell
cd c:\Users\afperez\E-commerce\Frontend
.\start-frontend.ps1
```

O manualmente:

```powershell
cd c:\Users\afperez\E-commerce\Frontend
npm install
npm run dev
```

### 4. Abrir la aplicación

Abre tu navegador en: **http://localhost:3000**

## 🧪 Probar el Chatbot

1. En la landing page, verás un botón flotante con el icono 🤖 en la esquina inferior derecha
2. Haz clic para abrir el chatbot
3. Prueba estos comandos:
   - "ver productos"
   - "productos"
   - "ayuda"
   - "ver carrito"

## 📂 Estructura del Proyecto

```
Frontend/
├── src/
│   ├── domain/              # Entidades y contratos
│   │   ├── entities/        # Product, Cart, Chat
│   │   └── repositories/    # Interfaces de repositorios
│   ├── application/         # Casos de uso
│   │   └── useCases/        # Lógica de negocio
│   ├── infrastructure/      # Implementaciones
│   │   ├── http/            # Cliente Axios
│   │   ├── repositories/    # Repos implementados
│   │   └── di/              # Inyección de dependencias
│   └── presentation/        # UI React
│       ├── components/      # Chatbot, Header, ProductCard
│       ├── pages/           # LandingPage
│       └── hooks/           # useProducts, useCart, useChatbot
```

## 🔗 Endpoints Configurados

| Servicio | URL | Descripción |
|----------|-----|-------------|
| Frontend | http://localhost:3000 | Aplicación React |
| Backend API | http://localhost:8000 | API Gateway |
| Product Service | http://localhost:8000/api/v1/products | Productos |
| Cart Service | http://localhost:8003 | Carrito |
| n8n Webhook | http://localhost:5678/webhook/chatbot | Chatbot |

## 🎨 Características Implementadas

### ✅ Landing Page
- Hero section con buscador
- Filtros por categoría
- Grid de productos con imágenes
- Botón "Agregar al carrito"
- Responsive design

### ✅ Chatbot Widget
- Widget flotante (bottom-right)
- Ventana de chat con historial
- Integración con n8n webhook
- Acciones rápidas
- Animaciones suaves
- Indicador de escritura

### ✅ Header
- Logo y navegación
- Icono de carrito con badge de cantidad
- Icono de perfil
- Sticky header

### ✅ Arquitectura Limpia
- Separación de capas (Domain, Application, Infrastructure, Presentation)
- Inyección de dependencias
- React Query para data fetching
- Custom hooks para cada funcionalidad

## 🐛 Troubleshooting

### El frontend no carga productos
- Verifica que el backend esté corriendo: `docker ps`
- Verifica que el product_service responda: `Invoke-RestMethod http://localhost:8000/api/v1/products`

### El chatbot no responde
- Verifica que n8n esté corriendo: `docker ps | Select-String n8n`
- Verifica que el workflow esté **Active** en n8n (http://localhost:5678)
- Verifica que el webhook esté registrado: Debe aparecer en la pestaña "Executions"

### Error de CORS
- El Vite proxy está configurado para `/api` → `http://localhost:8000`
- El n8n webhook se llama directamente (mismo origin después del proxy)

## 📝 Próximos Pasos

- [ ] Implementar autenticación (reemplazar `userId` hardcodeado)
- [ ] Crear página de detalle de producto
- [ ] Crear página de carrito completo
- [ ] Crear página de checkout
- [ ] Agregar más comandos al chatbot (órdenes, perfil, etc.)
- [ ] Tests unitarios
- [ ] Tests E2E

## 🎓 Tecnologías Utilizadas

- React 18
- TypeScript
- Vite
- React Router 6
- React Query (TanStack Query)
- Axios
- Framer Motion
- React Icons
