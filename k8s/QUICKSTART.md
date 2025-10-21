# 🚀 INICIO RÁPIDO - Despliegue en Kubernetes

## ⚡ 3 Comandos para Desplegar Todo

```powershell
# 1. Construir imágenes Docker (5-10 min)
cd k8s
.\build-images.ps1

# 2. Desplegar en Kubernetes (3-5 min)
.\deploy.ps1

# 3. Verificar que todo funciona
kubectl get pods
```

## 🌐 URLs de Acceso

Después del despliegue, abre estos enlaces en tu navegador:

- 🛍️  **Productos**: http://localhost:30000/docs
- 👤 **Usuarios**: http://localhost:30001/docs
- 🚚 **Entregas**: http://localhost:30002/docs
- 🛒 **Carrito**: http://localhost:30003/docs
- 📦 **Órdenes**: http://localhost:30005/docs
- ✅ **Validación**: http://localhost:30006/docs
- 💳 **Pagos**: http://localhost:30007/docs

## 📊 Comandos Esenciales

```powershell
# Ver estado de los pods
kubectl get pods

# Ver logs de un servicio
kubectl logs -l app=product-service -f

# Reiniciar un servicio
kubectl rollout restart deployment product-service

# Eliminar todo
.\cleanup.ps1
```

## 🏗️ Arquitectura Desplegada

```
┌─────────────────────────────────────────────────────────────┐
│                     KUBERNETES CLUSTER                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Product    │  │     User     │  │   Delivery   │     │
│  │   Service    │  │   Service    │  │   Service    │     │
│  │   :8000      │  │   :8001      │  │   :8002      │     │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘     │
│         │                 │                  │              │
│         ▼                 ▼                  ▼              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  Product DB  │  │   User DB    │  │ Delivery DB  │     │
│  │  PostgreSQL  │  │  PostgreSQL  │  │  PostgreSQL  │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │     Cart     │  │    Order     │  │   Payment    │     │
│  │   Service    │  │   Service    │  │   Service    │     │
│  │   :8003      │  │   :8005      │  │   :8007      │     │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘     │
│         │                 │                  │              │
│         ▼                 ▼                  ▼              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Cart DB    │  │   Order DB   │  │  Payment DB  │     │
│  │  PostgreSQL  │  │  PostgreSQL  │  │  PostgreSQL  │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│                                                              │
│  ┌─────────────────────────────┐                           │
│  │   Order Validation Service  │                           │
│  │          :8006              │                           │
│  └─────────────────────────────┘                           │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## 🎯 Características del Despliegue

### Alta Disponibilidad
- ✅ **2 réplicas** por servicio (si una falla, la otra sigue funcionando)
- ✅ **Health checks** automáticos (K8s reinicia servicios enfermos)
- ✅ **Auto-recuperación** (si un pod muere, K8s crea uno nuevo)

### Persistencia de Datos
- ✅ **PersistentVolumes** para las bases de datos
- ✅ Los datos NO se pierden si reinicias los pods

### Configuración Centralizada
- ✅ **ConfigMaps** para variables de entorno
- ✅ **Secrets** para contraseñas (base64 encoded)

### Red Interna
- ✅ Los servicios se comunican por nombre (ej: `http://product-service:8000`)
- ✅ DNS interno de Kubernetes

## ⚠️ IMPORTANTE: Antes de Empezar

### 1. Verifica Docker Desktop
```powershell
# Debe estar ejecutándose
docker ps
```

### 2. Verifica Kubernetes
```powershell
# Settings → Kubernetes → Enable Kubernetes
kubectl cluster-info
```

### 3. Verifica que tienes los Dockerfiles
Los archivos deben existir en:
- `Backend/src/product_service/Dockerfile`
- `Backend/src/user_service/Dockerfile`
- (etc.)

## 🐛 ¿Algo salió mal?

### Problema: "kubectl no es reconocido"
**Solución**: Instala kubectl o habilita Kubernetes en Docker Desktop

### Problema: "No se puede conectar al cluster"
**Solución**: Verifica que Docker Desktop está ejecutándose y K8s está habilitado

### Problema: "ImagePullBackOff"
**Solución**: Ejecuta primero `.\build-images.ps1` para construir las imágenes

### Problema: "CrashLoopBackOff"
**Solución**: 
```powershell
# Ver el error exacto
kubectl logs <nombre-del-pod>
kubectl describe pod <nombre-del-pod>
```

### Problema: Las bases de datos no inician
**Solución**: Espera 2-3 minutos, las BDs tardan en inicializarse

## 📚 Más Información

Lee el `README.md` completo para:
- Explicación detallada de cada archivo
- Configuración avanzada
- Troubleshooting completo
- Comandos útiles
- Recursos de aprendizaje

## 🎓 ¿Nuevo en Kubernetes?

No te preocupes! Los scripts hacen todo el trabajo pesado. Solo necesitas:

1. Ejecutar `build-images.ps1` (una vez)
2. Ejecutar `deploy.ps1` (despliega todo)
3. Abrir los enlaces en tu navegador

¡Eso es todo! 🚀

## 📞 Ayuda

Si tienes problemas:
1. Lee la sección de Troubleshooting arriba
2. Ejecuta: `kubectl get pods` y `kubectl get events`
3. Revisa los logs: `kubectl logs <pod-name>`

---

**¡Disfruta tu aplicación en Kubernetes!** 🎉
