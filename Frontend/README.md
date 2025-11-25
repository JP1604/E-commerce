# E-Commerce Frontend

Frontend desarrollado en React + TypeScript con arquitectura limpia (hexagonal), integrado con el chatbot n8n.

## 🏗️ Arquitectura

```
Frontend/
├── src/
│   ├── domain/              # Entidades y contratos de repositorios
│   │   ├── entities/        # Product, Cart, Chat
│   │   └── repositories/    # Interfaces
│   ├── application/         # Casos de uso (lógica de negocio)
│   │   └── useCases/
│   ├── infrastructure/      # Implementaciones técnicas
│   │   ├── http/            # Cliente HTTP (Axios)
│   │   ├── repositories/    # Implementación de repositorios
│   │   └── di/              # Contenedor de inyección de dependencias
│   └── presentation/        # Capa de UI (React)
│       ├── components/      # Componentes reutilizables
│       ├── pages/           # Páginas
│       └── hooks/           # React hooks personalizados
```

## 🚀 Instalación

```bash
cd Frontend
npm install
```

## 🏃‍♂️ Ejecución

```bash
npm run dev
```

La aplicación correrá en: http://localhost:3000

## 🤖 Chatbot n8n

El chatbot está integrado y conectado al webhook de n8n:
- **Webhook URL**: http://localhost:5678/webhook/chatbot
- **Formato petición**: `{"user_id": "string", "message": "string"}`
- **Ubicación**: Widget flotante en la esquina inferior derecha

### Comandos del chatbot
- "ver productos" / "productos"
- "ver carrito"
- "mis órdenes"
- "ayuda"

## 🔌 Conexión con Backend

El frontend se conecta a los siguientes servicios:
- **Product Service**: http://localhost:8000
- **Cart Service**: http://localhost:8003
- **Order Service**: http://localhost:8005
- **n8n Webhook**: http://localhost:5678

Configuración de proxy en `vite.config.ts`:
```typescript
proxy: {
  '/api': {
    target: 'http://localhost:8000',
    changeOrigin: true,
  },
}
```

## 📦 Dependencias Principales

- **React 18**: Framework UI
- **TypeScript**: Tipado estático
- **React Router 6**: Navegación
- **React Query (TanStack Query)**: Gestión de estado del servidor
- **Zustand**: Estado global (si es necesario)
- **Axios**: Cliente HTTP
- **Framer Motion**: Animaciones
- **React Icons**: Iconos

## 🧪 Testing

```bash
npm run test
```

## 🏗️ Build

```bash
npm run build
```

## 📝 Notas

- El `userId` está hardcodeado como `"user-123"` (pendiente implementar autenticación)
- El chatbot widget es visible en todas las páginas
- Los productos se cargan desde el microservicio de productos
- El carrito se sincroniza automáticamente con el backend
