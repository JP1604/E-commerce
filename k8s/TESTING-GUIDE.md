# 🧪 Guía de Pruebas - E-commerce en Kubernetes

Esta guía te muestra cómo probar que todo funciona correctamente.

## 📋 Índice de Pruebas

1. [Pruebas Previas al Despliegue](#1-pruebas-previas-al-despliegue)
2. [Desplegar en Kubernetes](#2-desplegar-en-kubernetes)
3. [Verificar el Despliegue](#3-verificar-el-despliegue)
4. [Probar los Servicios](#4-probar-los-servicios)
5. [Pruebas de Integración](#5-pruebas-de-integración)
6. [Verificar Alta Disponibilidad](#6-verificar-alta-disponibilidad)

---

## 1. Pruebas Previas al Despliegue

### 🐳 Verificar Docker

```powershell
# Abrir PowerShell y ejecutar:

# 1. Verificar que Docker está ejecutándose
docker ps

# Deberías ver una tabla vacía o con contenedores
# Si ves un error, abre Docker Desktop
```

### ☸️ Verificar Kubernetes

```powershell
# 2. Verificar que K8s está funcionando
kubectl version --short

# Deberías ver algo como:
# Client Version: v1.28.x
# Server Version: v1.28.x
```

```powershell
# 3. Verificar conexión al cluster
kubectl cluster-info

# Deberías ver:
# Kubernetes control plane is running at...
```

```powershell
# 4. Verificar que no hay nada desplegado aún
kubectl get pods

# Deberías ver:
# No resources found in default namespace.
```

✅ Si todos estos comandos funcionan, ¡estás listo para desplegar!

---

## 2. Desplegar en Kubernetes

### Paso 2.1: Construir las Imágenes Docker

```powershell
# Ir a la carpeta k8s
cd c:\Users\afperez\E-commerce\k8s

# Construir todas las imágenes
.\build-images.ps1
```

**¿Qué esperar?**
- ✅ Verás mensajes de construcción para cada servicio
- ⏱️ Tomará 5-10 minutos
- ✅ Al final: "Todas las imágenes fueron construidas exitosamente"

**Si hay errores:**
```powershell
# Verifica que los Dockerfiles existen
ls ..\Backend\src\*\Dockerfile
```

### Paso 2.2: Desplegar Todo

```powershell
# Ejecutar el script de despliegue
.\deploy.ps1
```

**¿Qué esperar?**
- ✅ Verás pasos del 1 al 7
- ⏱️ Tomará 3-5 minutos
- ✅ Al final: "DESPLIEGUE COMPLETADO" con URLs

---

## 3. Verificar el Despliegue

### 🔍 Verificación Básica

```powershell
# Ver TODOS los pods
kubectl get pods

# Deberías ver 20 pods:
# - 6 bases de datos (product-db, user-db, etc.)
# - 14 servicios (2 réplicas de cada uno de los 7 servicios)
#
# Todos deben estar en estado "Running" con "2/2" en READY
```

**Ejemplo de salida esperada:**
```
NAME                                      READY   STATUS    RESTARTS   AGE
cart-db-xxxxx                            1/1     Running   0          3m
cart-service-xxxxx                       1/1     Running   0          2m
cart-service-yyyyy                       1/1     Running   0          2m
delivery-db-xxxxx                        1/1     Running   0          3m
...
```

### 🔍 Verificación Detallada

```powershell
# Ver servicios expuestos
kubectl get services

# Deberías ver 13 servicios:
# - 6 bases de datos (ClusterIP)
# - 7 servicios de aplicación (NodePort)
```

```powershell
# Ver volúmenes de datos
kubectl get pvc

# Deberías ver 6 PVCs (uno por cada base de datos)
# Todos deben estar en estado "Bound"
```

### ⏳ Si los pods no están "Running"

```powershell
# Esperar un poco más (las BDs tardan en iniciar)
Start-Sleep -Seconds 30
kubectl get pods

# Ver eventos recientes
kubectl get events --sort-by='.lastTimestamp' | Select-Object -Last 20

# Ver por qué un pod no inicia
kubectl describe pod <nombre-del-pod>
```

---

## 4. Probar los Servicios

### 🌐 Prueba 1: Acceder a Swagger UI

Abre tu navegador y visita cada URL:

#### Product Service (Puerto 30000)
```
http://localhost:30000/docs
```
**✅ Deberías ver**: La documentación interactiva de Swagger con endpoints como:
- `POST /api/v1/products/`
- `GET /api/v1/products/`
- `GET /api/v1/products/{product_id}`

#### User Service (Puerto 30001)
```
http://localhost:30001/docs
```

#### Delivery Service (Puerto 30002)
```
http://localhost:30002/docs
```

#### Cart Service (Puerto 30003)
```
http://localhost:30003/docs
```

#### Order Service (Puerto 30005)
```
http://localhost:30005/docs
```

#### Order Validation Service (Puerto 30006)
```
http://localhost:30006/docs
```

#### Payment Service (Puerto 30007)
```
http://localhost:30007/docs
```

### 🔧 Prueba 2: Health Check

```powershell
# Verificar que cada servicio responde
curl http://localhost:30000/health
curl http://localhost:30001/health
curl http://localhost:30002/health
curl http://localhost:30003/health
curl http://localhost:30005/health
curl http://localhost:30006/health
curl http://localhost:30007/health
```

**✅ Cada uno debería responder**: `{"status":"ok"}` o similar

---

## 5. Pruebas de Integración

Vamos a probar el flujo completo del E-commerce:

### 🧪 Prueba Completa: Crear una Orden

#### Paso 1: Crear un Producto

```powershell
# Usar PowerShell o Swagger UI
$body = @{
    name = "Laptop Dell XPS"
    description = "Laptop de alta gama"
    price = 1500.00
    stock_quantity = 10
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "http://localhost:30000/api/v1/products/" `
    -Method POST `
    -Body $body `
    -ContentType "application/json"

# Guardar el ID del producto
$productId = $response.id
Write-Host "Producto creado con ID: $productId"
```

**✅ Deberías obtener**: Un JSON con el producto creado

#### Paso 2: Crear un Usuario

```powershell
$body = @{
    name = "Juan Pérez"
    email = "juan@example.com"
    phone = "+34612345678"
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "http://localhost:30001/api/v1/users/" `
    -Method POST `
    -Body $body `
    -ContentType "application/json"

$userId = $response.id
Write-Host "Usuario creado con ID: $userId"
```

#### Paso 3: Crear un Carrito

```powershell
$body = @{
    user_id = $userId
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "http://localhost:30003/api/v1/carts/" `
    -Method POST `
    -Body $body `
    -ContentType "application/json"

$cartId = $response.id
Write-Host "Carrito creado con ID: $cartId"
```

#### Paso 4: Agregar Producto al Carrito

```powershell
$body = @{
    product_id = $productId
    quantity = 2
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:30003/api/v1/carts/$cartId/items" `
    -Method POST `
    -Body $body `
    -ContentType "application/json"

Write-Host "Producto agregado al carrito"
```

#### Paso 5: Crear una Orden

```powershell
$body = @{
    user_id = $userId
    items = @(
        @{
            product_id = $productId
            quantity = 2
            price = 1500.00
        }
    )
} | ConvertTo-Json -Depth 3

$response = Invoke-RestMethod -Uri "http://localhost:30005/api/v1/orders/" `
    -Method POST `
    -Body $body `
    -ContentType "application/json"

$orderId = $response.id
Write-Host "Orden creada con ID: $orderId"
```

#### Paso 6: Validar la Orden

```powershell
$body = @{
    order_id = $orderId
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "http://localhost:30006/api/v1/validations/validate" `
    -Method POST `
    -Body $body `
    -ContentType "application/json"

Write-Host "Validación: $($response.is_valid)"
```

#### Paso 7: Procesar el Pago

```powershell
$body = @{
    order_id = $orderId
    amount = 3000.00
    payment_method = "credit_card"
    user_id = $userId
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "http://localhost:30007/api/v1/payments/process" `
    -Method POST `
    -Body $body `
    -ContentType "application/json"

Write-Host "Pago procesado: $($response.status)"
```

### ✅ Si todo funciona correctamente:
- ✅ Producto creado
- ✅ Usuario creado
- ✅ Carrito creado
- ✅ Producto agregado al carrito
- ✅ Orden creada
- ✅ Orden validada
- ✅ Pago procesado

---

## 6. Verificar Alta Disponibilidad

### 🧪 Prueba: ¿Qué pasa si un pod muere?

```powershell
# 1. Ver los pods de product-service
kubectl get pods -l app=product-service

# Deberías ver 2 pods Running
```

```powershell
# 2. Eliminar uno de los pods
kubectl delete pod <nombre-del-primer-pod>
```

```powershell
# 3. Ver qué pasa inmediatamente
kubectl get pods -l app=product-service -w

# Verás que:
# - El pod eliminado desaparece
# - K8s crea uno nuevo automáticamente
# - Siempre hay 2 pods (alta disponibilidad)
```

```powershell
# 4. Verificar que el servicio sigue funcionando
curl http://localhost:30000/health

# ✅ Debería seguir respondiendo sin problemas
```

**🎯 Esto demuestra que Kubernetes mantiene tu aplicación funcionando incluso si hay fallos**

---

## 7. Pruebas de Logs

### Ver Logs en Tiempo Real

```powershell
# Ver logs de product-service
kubectl logs -l app=product-service -f

# Presiona Ctrl+C para salir
```

### Ver Logs de un Pod Específico

```powershell
# Listar pods
kubectl get pods

# Ver logs de un pod específico
kubectl logs product-service-xxxxx

# Ver las últimas 50 líneas
kubectl logs product-service-xxxxx --tail=50
```

### Ver Logs de Todos los Servicios

```powershell
# Ver logs de todos los pods
kubectl logs -l app=product-service --all-containers=true
```

---

## 8. Pruebas de Conexión a Base de Datos

### Conectarse a PostgreSQL

```powershell
# Conectarse a la base de datos de productos
kubectl exec -it <nombre-pod-product-db> -- psql -U ecommerce_user -d ecommerce

# Una vez dentro:
# \dt              - Ver tablas
# SELECT * FROM products;  - Ver productos
# \q               - Salir
```

### Verificar Datos Persistentes

```powershell
# 1. Crear un producto
curl -X POST http://localhost:30000/api/v1/products/ `
  -H "Content-Type: application/json" `
  -d '{"name":"Test Product","price":100,"stock_quantity":5}'

# 2. Eliminar el pod de product-service
kubectl delete pod -l app=product-service

# 3. Esperar a que se recree
Start-Sleep -Seconds 10

# 4. Verificar que el producto sigue ahí
curl http://localhost:30000/api/v1/products/

# ✅ El producto debe seguir existiendo (datos persistentes)
```

---

## 9. Pruebas de Performance

### Verificar Recursos

```powershell
# Ver uso de CPU y memoria
kubectl top pods

# Deberías ver algo como:
# NAME                        CPU(cores)   MEMORY(bytes)
# product-service-xxxxx       50m          256Mi
```

### Escalar un Servicio

```powershell
# Aumentar a 5 réplicas
kubectl scale deployment product-service --replicas=5

# Verificar que se crearon 5 pods
kubectl get pods -l app=product-service

# Reducir de nuevo a 2
kubectl scale deployment product-service --replicas=2
```

---

## 10. Limpieza y Re-despliegue

### Limpiar Todo

```powershell
# Eliminar todo el despliegue
.\cleanup.ps1

# Confirmar con: SI
```

### Verificar Limpieza

```powershell
# No debería haber pods
kubectl get pods

# No debería haber servicios (excepto kubernetes)
kubectl get services

# No debería haber PVCs
kubectl get pvc
```

### Re-desplegar

```powershell
# Desplegar de nuevo
.\deploy.ps1

# Todo debería funcionar igual que antes
```

---

## 📊 Checklist de Pruebas

Usa este checklist para verificar todo:

### Pre-despliegue
- [ ] Docker Desktop ejecutándose
- [ ] Kubernetes habilitado
- [ ] `kubectl` funciona
- [ ] `docker ps` funciona

### Construcción
- [ ] `build-images.ps1` ejecutado sin errores
- [ ] 7 imágenes Docker creadas
- [ ] `docker images` muestra las imágenes

### Despliegue
- [ ] `deploy.ps1` ejecutado sin errores
- [ ] 20 pods en estado "Running"
- [ ] 13 servicios creados
- [ ] 6 PVCs en estado "Bound"

### Acceso Web
- [ ] http://localhost:30000/docs funciona (Product)
- [ ] http://localhost:30001/docs funciona (User)
- [ ] http://localhost:30002/docs funciona (Delivery)
- [ ] http://localhost:30003/docs funciona (Cart)
- [ ] http://localhost:30005/docs funciona (Order)
- [ ] http://localhost:30006/docs funciona (Validation)
- [ ] http://localhost:30007/docs funciona (Payment)

### Health Checks
- [ ] Todos los servicios responden a `/health`

### Funcionalidad
- [ ] Puedes crear un producto
- [ ] Puedes crear un usuario
- [ ] Puedes crear un carrito
- [ ] Puedes agregar items al carrito
- [ ] Puedes crear una orden
- [ ] Puedes validar una orden
- [ ] Puedes procesar un pago

### Alta Disponibilidad
- [ ] Al eliminar un pod, K8s lo recrea
- [ ] El servicio sigue funcionando con un pod menos

### Persistencia
- [ ] Los datos sobreviven al reinicio de pods
- [ ] Las bases de datos mantienen la información

---

## 🐛 Troubleshooting de Pruebas

### Problema: No puedo acceder a localhost:30000

**Solución 1**: Verificar que el servicio está expuesto
```powershell
kubectl get services product-service
```

**Solución 2**: Si usas Minikube
```powershell
minikube service product-service --url
# Usa la URL que te devuelve
```

### Problema: Los pods están en "CrashLoopBackOff"

```powershell
# Ver el error exacto
kubectl logs <nombre-del-pod>

# Ver detalles del pod
kubectl describe pod <nombre-del-pod>

# Causas comunes:
# - La BD no está lista aún (espera 1-2 minutos)
# - Error en las variables de entorno
# - Error en el código de la aplicación
```

### Problema: "Connection refused" al hacer curl

```powershell
# 1. Verificar que el pod está Running
kubectl get pods -l app=product-service

# 2. Verificar que el servicio existe
kubectl get service product-service

# 3. Probar desde dentro del cluster
kubectl run test --rm -it --image=curlimages/curl -- curl http://product-service:8000/health
```

### Problema: Las pruebas de integración fallan

```powershell
# Verificar logs de todos los servicios involucrados
kubectl logs -l app=product-service --tail=50
kubectl logs -l app=user-service --tail=50
kubectl logs -l app=order-service --tail=50
```

---

## 📝 Resultados Esperados

Al finalizar todas las pruebas, deberías tener:

✅ 20 pods en estado "Running"
✅ 7 servicios accesibles vía web
✅ Flujo completo de E-commerce funcionando
✅ Alta disponibilidad verificada
✅ Persistencia de datos comprobada
✅ Logs accesibles
✅ Recursos monitoreados

---

## 🎉 ¡Felicidades!

Si todas las pruebas pasaron, tu aplicación de E-commerce está correctamente desplegada en Kubernetes con:

- ✅ Alta disponibilidad (2 réplicas por servicio)
- ✅ Persistencia de datos
- ✅ Auto-recuperación ante fallos
- ✅ Configuración centralizada
- ✅ Servicios interconectados

**¡Tu aplicación está lista para producción (con algunos ajustes de seguridad)!** 🚀
