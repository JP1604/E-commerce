# =============================================================================
# Script de Limpieza de E-commerce en Kubernetes
# =============================================================================
# Este script elimina TODOS los recursos de E-commerce del cluster
# Uso: .\cleanup.ps1

Write-Host "🧹 Iniciando limpieza de E-commerce en Kubernetes..." -ForegroundColor Yellow
Write-Host ""

# Advertencia
Write-Host "⚠️  ADVERTENCIA: Esto eliminará TODOS los recursos del E-commerce" -ForegroundColor Red
Write-Host "   Incluyendo bases de datos y sus datos almacenados." -ForegroundColor Red
Write-Host ""

$confirmation = Read-Host "¿Estás seguro? (escribe 'SI' para continuar)"
if ($confirmation -ne "SI") {
    Write-Host "❌ Limpieza cancelada" -ForegroundColor Yellow
    exit 0
}

Write-Host ""
Write-Host "🗑️  Eliminando recursos..." -ForegroundColor Cyan
Write-Host ""

# Eliminar microservicios
Write-Host "📦 Eliminando microservicios..." -ForegroundColor White
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
    Write-Host "  → Eliminando $service..." -ForegroundColor Gray
    kubectl delete -f services/$service.yaml --ignore-not-found=true 2>$null
}

Write-Host ""

# Eliminar bases de datos
Write-Host "💾 Eliminando bases de datos..." -ForegroundColor White
$databases = @(
    "product-db",
    "user-db",
    "delivery-db",
    "cart-db",
    "order-db",
    "payment-db"
)

foreach ($db in $databases) {
    Write-Host "  → Eliminando $db..." -ForegroundColor Gray
    kubectl delete -f databases/$db.yaml --ignore-not-found=true 2>$null
}

Write-Host ""

# Eliminar configuración base
Write-Host "⚙️  Eliminando configuración base..." -ForegroundColor White
Write-Host "  → Eliminando ConfigMap..." -ForegroundColor Gray
kubectl delete -f base/configmap.yaml --ignore-not-found=true 2>$null
Write-Host "  → Eliminando Secrets..." -ForegroundColor Gray
kubectl delete -f base/secrets.yaml --ignore-not-found=true 2>$null

Write-Host ""

# Eliminar PersistentVolumeClaims (datos)
Write-Host "💽 Eliminando volúmenes de datos..." -ForegroundColor White
$pvcs = @(
    "product-db-pvc",
    "user-db-pvc",
    "delivery-db-pvc",
    "cart-db-pvc",
    "order-db-pvc",
    "payment-db-pvc"
)

foreach ($pvc in $pvcs) {
    Write-Host "  → Eliminando $pvc..." -ForegroundColor Gray
    kubectl delete pvc $pvc --ignore-not-found=true 2>$null
}

Write-Host ""
Write-Host "⏳ Esperando a que los recursos se eliminen completamente..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

Write-Host ""
Write-Host "✅ Limpieza completada" -ForegroundColor Green
Write-Host ""

# Verificar que todo se eliminó
Write-Host "📊 Verificando estado final..." -ForegroundColor Cyan
$remainingPods = kubectl get pods -o name 2>$null | Where-Object { $_ -match "product|user|delivery|cart|order|payment" }
if ($remainingPods) {
    Write-Host "⚠️  Algunos pods todavía se están eliminando:" -ForegroundColor Yellow
    kubectl get pods
} else {
    Write-Host "✅ Todos los recursos fueron eliminados exitosamente" -ForegroundColor Green
}

Write-Host ""
