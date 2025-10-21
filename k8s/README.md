# 🚀 Guía de Despliegue en Kubernetes - E-commerce

Esta guía te ayudará a desplegar tu plataforma de E-commerce en Kubernetes paso a paso.

## 📚 ¿Qué es Kubernetes?

**Kubernetes (K8s)** es como un "director de orquesta" para tus aplicaciones en contenedores. Imagina que:

- **Docker** es el contenedor donde vive tu aplicación
- **Kubernetes** es quien decide dónde y cómo ejecutar esos contenedores
- Si una aplicación falla, K8s la reinicia automáticamente
- Si hay mucho tráfico, K8s puede crear más copias de tu aplicación

### Conceptos Básicos (para principiantes)

| Concepto | ¿Qué es? | Analogía |
|----------|----------|----------|
| **Pod** | El contenedor más pequeño que K8s maneja | Una caja que contiene tu aplicación |
| **Deployment** | Define cómo se debe ejecutar tu aplicación | Un plano de construcción |
| **Service** | Expone tu aplicación en la red | Una dirección postal |
| **ConfigMap** | Configuración no sensible | Un archivo de ajustes |
| **Secret** | Información confidencial (contraseñas) | Una caja fuerte |
| **PVC** | Almacenamiento persistente | Un disco duro |

## 📁 Estructura de Archivos

```
k8s/
├── base/                          # Configuración base
│   ├── configmap.yaml            # Variables de entorno comunes
│   └── secrets.yaml              # Contraseñas y datos sensibles
│
├── databases/                     # Bases de datos PostgreSQL
│   ├── product-db.yaml           # BD del servicio de productos
│   ├── user-db.yaml              # BD del servicio de usuarios
│   ├── delivery-db.yaml          # BD del servicio de entregas
│   ├── cart-db.yaml              # BD del servicio de carrito
│   ├── order-db.yaml             # BD del servicio de órdenes
│   └── payment-db.yaml           # BD del servicio de pagos
│
├── services/                      # Microservicios de la aplicación
│   ├── product-service.yaml      # Servicio de productos (8000)
│   ├── user-service.yaml         # Servicio de usuarios (8001)
│   ├── delivery-service.yaml    # Servicio de entregas (8002)
│   ├── cart-service.yaml         # Servicio de carrito (8003)
│   ├── order-service.yaml        # Servicio de órdenes (8005)
│   ├── order-validation-service.yaml  # Validación (8006)
│   └── payment-service.yaml      # Servicio de pagos (8007)
│
├── build-images.ps1              # Script para construir imágenes Docker
├── deploy.ps1                    # Script para desplegar todo
├── cleanup.ps1                   # Script para eliminar todo
└── README.md                     # Este archivo
```

## 🎯 Prerrequisitos

### 1. Instalar un Cluster de Kubernetes Local

Elige **UNA** de estas opciones:

#### Opción A: Docker Desktop (Recomendado para Windows)
1. Instala [Docker Desktop](https://www.docker.com/products/docker-desktop)
2. Abre Docker Desktop
3. Ve a Settings → Kubernetes
4. Marca "Enable Kubernetes"
5. Haz clic en "Apply & Restart"
6. Espera a que el ícono de K8s se ponga verde ✅

#### Opción B: Minikube
```powershell
# Instalar Minikube
choco install minikube

# Iniciar cluster
minikube start
```

### 2. Verificar kubectl

```powershell
# Verificar que kubectl está instalado
kubectl version --client

# Verificar conexión al cluster
kubectl cluster-info
```

Si ves información del cluster, ¡estás listo! 🎉

## 🚀 Despliegue Rápido (3 pasos)

### Paso 1: Construir las Imágenes Docker

```powershell
# Desde la carpeta k8s/
cd k8s
.\build-images.ps1
```

Este script:
- ✅ Verifica que Docker esté instalado
- ✅ Construye las 7 imágenes de tus microservicios
- ✅ Muestra un resumen al final

**Tiempo estimado**: 5-10 minutos

### Paso 2: Desplegar en Kubernetes

```powershell
# Desde la carpeta k8s/
.\deploy.ps1
```

Este script:
1. ✅ Verifica la conexión a K8s
2. ✅ Crea ConfigMaps y Secrets
3. ✅ Despliega las 6 bases de datos PostgreSQL
4. ✅ Espera a que las bases de datos estén listas
5. ✅ Despliega los 7 microservicios
6. ✅ Muestra las URLs de acceso

**Tiempo estimado**: 3-5 minutos

### Paso 3: Verificar el Despliegue

```powershell
# Ver todos los pods (deben estar Running)
kubectl get pods

# Ver todos los servicios
kubectl get services
```

## 🌐 Acceder a los Servicios

Una vez desplegado, accede a la documentación interactiva (Swagger):

### 🚀 API Gateway (Punto de Entrada Principal)
| Servicio | URL | Descripción |
|----------|-----|-------------|
| **API Gateway** | http://localhost:30080/docs | **Punto de entrada único** - Accede a todos los servicios |

### 🔧 Servicios Individuales
| Servicio | URL | Descripción |
|----------|-----|-------------|
| **Product Service** | http://localhost:30000/docs | Gestión de productos |
| **User Service** | http://localhost:30001/docs | Gestión de usuarios |
| **Delivery Service** | http://localhost:30002/docs | Gestión de entregas |
| **Cart Service** | http://localhost:30003/docs | Carrito de compras |
| **Order Service** | http://localhost:30005/docs | Gestión de órdenes |
| **Order Validation** | http://localhost:30006/docs | Validación de órdenes |
| **Payment Service** | http://localhost:30007/docs | Procesamiento de pagos |

### 📡 Endpoints del API Gateway
- **Productos**: `http://localhost:30080/api/products/`
- **Usuarios**: `http://localhost:30080/api/users/`
- **Carritos**: `http://localhost:30080/api/carts/`
- **Órdenes**: `http://localhost:30080/api/orders/`
- **Checkout**: `http://localhost:30080/api/checkout/`

## 📊 Comandos Útiles

### Ver el Estado de las Aplicaciones

```powershell
# Ver todos los pods
kubectl get pods

# Ver pods con más detalles
kubectl get pods -o wide

# Ver servicios
kubectl get services

# Ver todo a la vez
kubectl get all
```

### Ver Logs de un Servicio

```powershell
# Ver logs de un pod específico
kubectl logs <nombre-del-pod>

# Ver logs en tiempo real (como tail -f)
kubectl logs -f <nombre-del-pod>

# Ver logs de un servicio específico
kubectl logs -l app=product-service
```

**Ejemplo**:
```powershell
# Ver logs del product-service
kubectl logs -l app=product-service -f
```

### Inspeccionar un Pod

```powershell
# Ver detalles de un pod
kubectl describe pod <nombre-del-pod>

# Entrar a un pod (como SSH)
kubectl exec -it <nombre-del-pod> -- /bin/bash

# Ejecutar un comando en un pod
kubectl exec <nombre-del-pod> -- env
```

### Reiniciar un Servicio

```powershell
# Reiniciar todos los pods de un deployment
kubectl rollout restart deployment product-service

# Escalar un servicio (cambiar número de réplicas)
kubectl scale deployment product-service --replicas=3
```

### Ver Recursos del Cluster

```powershell
# Ver uso de CPU y memoria
kubectl top pods

# Ver nodos del cluster
kubectl get nodes

# Ver almacenamiento
kubectl get pvc
```

## 🧹 Limpieza y Mantenimiento

### Eliminar Todo

```powershell
# Desde la carpeta k8s/
.\cleanup.ps1
```

**⚠️ ADVERTENCIA**: Esto elimina TODO, incluyendo las bases de datos y sus datos.

### Eliminar Solo un Servicio

```powershell
# Eliminar un servicio específico
kubectl delete -f services/product-service.yaml

# Eliminar una base de datos específica
kubectl delete -f databases/product-db.yaml
```

### Re-desplegar un Servicio Actualizado

```powershell
# 1. Reconstruir la imagen
cd ..\Backend
docker build -f src/product_service/Dockerfile -t product-service:latest .

# 2. Reiniciar el deployment
kubectl rollout restart deployment product-service

# 3. Verificar que se actualizó
kubectl get pods
```

## 🔧 Configuración Avanzada

### Cambiar Recursos (CPU/Memoria)

Edita el archivo YAML del servicio:

```yaml
resources:
  requests:
    memory: "256Mi"  # Mínimo garantizado
    cpu: "250m"      # 0.25 cores
  limits:
    memory: "512Mi"  # Máximo permitido
    cpu: "500m"      # 0.5 cores
```

### Cambiar Número de Réplicas

```yaml
spec:
  replicas: 3  # Cambia este número
```

O directamente:
```powershell
kubectl scale deployment product-service --replicas=3
```

### Cambiar Contraseñas

1. Edita `base/secrets.yaml`
2. Aplica los cambios:
```powershell
kubectl apply -f base/secrets.yaml
kubectl rollout restart deployment product-service
```

### Exponer Servicios con LoadBalancer

Cambia en el archivo YAML del servicio:

```yaml
spec:
  type: LoadBalancer  # Cambia de NodePort a LoadBalancer
```

## 🐛 Troubleshooting (Solución de Problemas)

### Los Pods no se Inician

```powershell
# Ver por qué un pod no inicia
kubectl describe pod <nombre-pod>

# Ver logs del pod
kubectl logs <nombre-pod>

# Eventos recientes del cluster
kubectl get events --sort-by='.lastTimestamp'
```

**Problemas comunes**:
- ❌ **ImagePullBackOff**: La imagen Docker no existe o no se puede descargar
  - Solución: Verifica que ejecutaste `build-images.ps1`
  
- ❌ **CrashLoopBackOff**: La aplicación se inicia pero falla inmediatamente
  - Solución: Revisa los logs con `kubectl logs`
  
- ❌ **Pending**: El pod no puede ser programado
  - Solución: Verifica que tienes suficientes recursos en el cluster

### No Puedo Conectarme a los Servicios

```powershell
# Verificar que el servicio existe
kubectl get services

# Verificar que los pods están Running
kubectl get pods

# Probar conexión interna (desde un pod)
kubectl exec -it <nombre-pod> -- curl http://product-service:8000/health
```

### Base de Datos no se Conecta

```powershell
# Ver logs de la base de datos
kubectl logs -l app=product-db

# Ver si el pod está listo
kubectl get pods -l app=product-db

# Conectarse manualmente a la BD
kubectl exec -it <pod-db> -- psql -U ecommerce_user -d ecommerce
```

### Health Checks Fallan

Los health checks verifican si tu aplicación está saludable. Si fallan:

1. Verifica que tu aplicación tiene un endpoint `/health`
2. Ajusta los tiempos en el YAML:

```yaml
livenessProbe:
  initialDelaySeconds: 60  # Aumenta si tu app tarda en iniciar
  periodSeconds: 10
  timeoutSeconds: 5
  failureThreshold: 3      # Número de fallos antes de reiniciar
```

## 📈 Monitoreo y Métricas

### Ver Uso de Recursos

```powershell
# Instalar metrics-server (si no está instalado)
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml

# Ver uso de CPU/memoria
kubectl top nodes
kubectl top pods
```

### Dashboard de Kubernetes

```powershell
# Instalar dashboard
kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.7.0/aio/deploy/recommended.yaml

# Acceder al dashboard
kubectl proxy
# Abre: http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/
```

## 🔒 Seguridad (Producción)

**⚠️ IMPORTANTE**: Los archivos actuales son para **desarrollo**. En producción:

### 1. Secrets Seguros

```powershell
# NO uses secrets.yaml en producción
# En su lugar, crea secrets desde la línea de comando
kubectl create secret generic ecommerce-secrets \
  --from-literal=PRODUCT_DB_PASSWORD='contraseña-super-segura'
```

### 2. Variables de Entorno desde Secrets

```yaml
env:
- name: DATABASE_PASSWORD
  valueFrom:
    secretKeyRef:
      name: ecommerce-secrets
      key: PRODUCT_DB_PASSWORD
```

### 3. RBAC (Control de Acceso)

Define quién puede hacer qué en tu cluster.

### 4. Network Policies

Controla qué pods pueden comunicarse entre sí.

## 📝 Checklist de Despliegue

- [ ] Docker Desktop instalado y ejecutándose
- [ ] Kubernetes habilitado en Docker Desktop
- [ ] kubectl instalado y funcionando
- [ ] Imágenes Docker construidas (`build-images.ps1`)
- [ ] Cluster accesible (`kubectl cluster-info`)
- [ ] ConfigMaps y Secrets aplicados
- [ ] Bases de datos desplegadas y running
- [ ] Servicios desplegados y running
- [ ] Health checks pasando
- [ ] Servicios accesibles desde el navegador

## 🎓 Recursos de Aprendizaje

- [Documentación oficial de Kubernetes](https://kubernetes.io/docs/home/)
- [Kubernetes Tutorial for Beginners](https://kubernetes.io/docs/tutorials/kubernetes-basics/)
- [Docker & Kubernetes: The Complete Guide (Udemy)](https://www.udemy.com/course/docker-and-kubernetes-the-complete-guide/)
- [Play with Kubernetes](https://labs.play-with-k8s.com/) - Prueba K8s en el navegador

## 💡 Próximos Pasos

Una vez que domines lo básico, considera:

1. **Ingress Controller**: Routing avanzado (nginx, traefik)
2. **Helm**: Gestor de paquetes de K8s
3. **CI/CD**: Automatizar despliegues con GitHub Actions
4. **Service Mesh**: Istio o Linkerd para microservicios
5. **Monitoring**: Prometheus + Grafana
6. **Logging**: ELK Stack o Loki

## 🆘 Soporte

Si tienes problemas:

1. Revisa la sección de Troubleshooting arriba
2. Verifica los logs: `kubectl logs <pod-name>`
3. Describe el pod: `kubectl describe pod <pod-name>`
4. Busca en Stack Overflow con la etiqueta `kubernetes`

---

¡Feliz despliegue! 🚀 Si tienes dudas, pregunta sin miedo. Kubernetes tiene una curva de aprendizaje, pero vale la pena.
