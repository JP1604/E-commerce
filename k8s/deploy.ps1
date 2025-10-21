# Script de Despliegue de E-commerce en Kubernetes
# Uso: .\deploy.ps1

Write-Host ""
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "  Iniciando despliegue de E-commerce en Kubernetes" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""

# Verificar kubectl
Write-Host "Paso 1: Verificando kubectl..." -ForegroundColor Yellow
$null = kubectl version --client 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] kubectl no esta instalado" -ForegroundColor Red
    exit 1
}
Write-Host "[OK] kubectl esta disponible" -ForegroundColor Green
Write-Host ""

# Verificar conexion al cluster
Write-Host "Paso 2: Verificando conexion al cluster..." -ForegroundColor Yellow
$null = kubectl cluster-info 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] No se puede conectar al cluster" -ForegroundColor Red
    exit 1
}
Write-Host "[OK] Conectado al cluster" -ForegroundColor Green
Write-Host ""

# Desplegar configuracion base
Write-Host "Paso 3: Desplegando configuracion base..." -ForegroundColor Yellow
Write-Host "  Aplicando ConfigMap..." -ForegroundColor White
kubectl apply -f base/configmap.yaml
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Error al aplicar ConfigMap" -ForegroundColor Red
    exit 1
}

Write-Host "  Aplicando Secrets..." -ForegroundColor White
kubectl apply -f base/secrets.yaml
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Error al aplicar Secrets" -ForegroundColor Red
    exit 1
}
Write-Host "[OK] Configuracion base desplegada" -ForegroundColor Green
Write-Host ""

# Desplegar bases de datos
Write-Host "Paso 4: Desplegando bases de datos PostgreSQL..." -ForegroundColor Yellow
$databases = @(
    "product-db",
    "user-db",
    "delivery-db",
    "cart-db",
    "order-db",
    "payment-db"
)

foreach ($db in $databases) {
    Write-Host "  Desplegando $db..." -ForegroundColor White
    kubectl apply -f databases/$db.yaml
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[ERROR] Error al desplegar $db" -ForegroundColor Red
    }
}
Write-Host "[OK] Bases de datos desplegadas" -ForegroundColor Green
Write-Host ""

# Esperar a que las bases de datos esten listas
Write-Host "Paso 5: Esperando a que las bases de datos esten listas..." -ForegroundColor Yellow
Write-Host "  Esto puede tomar 1-2 minutos..." -ForegroundColor White

$maxWaitTime = 300
$elapsed = 0
$checkInterval = 10

while ($elapsed -lt $maxWaitTime) {
    $readyDbs = 0
    foreach ($db in $databases) {
        $ready = kubectl get pods -l app=$db -o jsonpath='{.items[0].status.containerStatuses[0].ready}' 2>&1
        if ($ready -eq "true") {
            $readyDbs++
        }
    }
    
    Write-Host "  Bases de datos listas: $readyDbs/$($databases.Count)" -ForegroundColor White
    
    if ($readyDbs -eq $databases.Count) {
        Write-Host "[OK] Todas las bases de datos estan listas" -ForegroundColor Green
        break
    }
    
    Start-Sleep -Seconds $checkInterval
    $elapsed += $checkInterval
}

if ($elapsed -ge $maxWaitTime) {
    Write-Host "[ADVERTENCIA] Timeout esperando bases de datos" -ForegroundColor Yellow
    Write-Host "Continuando con el despliegue..." -ForegroundColor Yellow
}
Write-Host ""

# Desplegar microservicios
Write-Host "Paso 6: Desplegando microservicios..." -ForegroundColor Yellow
$services = @(
    "product-service",
    "user-service",
    "delivery-service",
    "cart-service",
    "order-service",
    "order-validation-service",
    "payment-service"
)

foreach ($service in $services) {
    Write-Host "  Desplegando $service..." -ForegroundColor White
    kubectl apply -f services/$service.yaml
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[ADVERTENCIA] Error al desplegar $service" -ForegroundColor Yellow
    }
}
Write-Host "[OK] Microservicios desplegados" -ForegroundColor Green
Write-Host ""

# Verificar estado
Write-Host "Paso 7: Verificando estado del despliegue..." -ForegroundColor Yellow
Write-Host ""
Write-Host "Pods desplegados:" -ForegroundColor White
kubectl get pods
Write-Host ""
Write-Host "Servicios expuestos:" -ForegroundColor White
kubectl get services
Write-Host ""

# Mostrar informacion de acceso
Write-Host "======================================================================" -ForegroundColor Green
Write-Host "  DESPLIEGUE COMPLETADO" -ForegroundColor Green
Write-Host "======================================================================" -ForegroundColor Green
Write-Host ""

$nodeIP = "localhost"

Write-Host "URLs de acceso a los servicios:" -ForegroundColor Cyan
Write-Host ""
Write-Host "  Product Service:           http://${nodeIP}:30000/docs" -ForegroundColor White
Write-Host "  User Service:              http://${nodeIP}:30001/docs" -ForegroundColor White
Write-Host "  Delivery Service:          http://${nodeIP}:30002/docs" -ForegroundColor White
Write-Host "  Cart Service:              http://${nodeIP}:30003/docs" -ForegroundColor White
Write-Host "  Order Service:             http://${nodeIP}:30005/docs" -ForegroundColor White
Write-Host "  Order Validation Service:  http://${nodeIP}:30006/docs" -ForegroundColor White
Write-Host "  Payment Service:           http://${nodeIP}:30007/docs" -ForegroundColor White
Write-Host ""

Write-Host "Comandos utiles:" -ForegroundColor Cyan
Write-Host ""
Write-Host "  Ver pods:           kubectl get pods" -ForegroundColor White
Write-Host "  Ver logs:           kubectl logs NOMBRE-POD" -ForegroundColor White
Write-Host "  Describir pod:      kubectl describe pod NOMBRE-POD" -ForegroundColor White
Write-Host "  Ver servicios:      kubectl get services" -ForegroundColor White
Write-Host "  Eliminar todo:      .\cleanup.ps1" -ForegroundColor White
Write-Host ""
Write-Host "======================================================================" -ForegroundColor Green
Write-Host ""
