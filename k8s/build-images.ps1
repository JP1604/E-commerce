# Script para Construir Imagenes Docker de los Microservicios
# Uso: .\build-images.ps1

Write-Host "Construyendo imagenes Docker para E-commerce..." -ForegroundColor Cyan
Write-Host ""

# Verificar que Docker esta instalado
try {
    $null = docker version 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR: Docker no esta instalado o no esta ejecutandose" -ForegroundColor Red
        Write-Host "Instala Docker Desktop desde: https://www.docker.com/products/docker-desktop" -ForegroundColor Yellow
        exit 1
    }
    Write-Host "[OK] Docker esta disponible" -ForegroundColor Green
}
catch {
    Write-Host "ERROR: Error al verificar Docker" -ForegroundColor Red
    exit 1
}

Write-Host ""

# Cambiar al directorio Backend
$backendPath = Join-Path $PSScriptRoot "..\Backend"
if (-not (Test-Path $backendPath)) {
    Write-Host "ERROR: No se encuentra el directorio Backend" -ForegroundColor Red
    exit 1
}

Set-Location $backendPath
Write-Host "Directorio de trabajo: $backendPath" -ForegroundColor White
Write-Host ""

# Lista de servicios para construir
$services = @(
    @{Name="api-gateway"; Path="src/api_gateway/Dockerfile"}
    @{Name="product-service"; Path="src/product_service/Dockerfile"}
    @{Name="user-service"; Path="src/user_service/Dockerfile"}
    @{Name="delivery-service"; Path="src/delivery_service/Dockerfile"}
    @{Name="cart-service"; Path="src/cart_service/Dockerfile"}
    @{Name="order-service"; Path="src/order_service/Dockerfile"}
    @{Name="order-validation-service"; Path="src/order_validation_service/Dockerfile"}
    @{Name="payment-service"; Path="src/payment_service/Dockerfile"}
)

$successCount = 0
$failCount = 0

# Construir cada servicio
foreach ($service in $services) {
    Write-Host "Construyendo $($service.Name)..." -ForegroundColor Cyan
    
    # Verificar que existe el Dockerfile
    if (-not (Test-Path $service.Path)) {
        Write-Host "  [ADVERTENCIA] Dockerfile no encontrado: $($service.Path)" -ForegroundColor Yellow
        Write-Host "  Saltando..." -ForegroundColor Yellow
        $failCount++
        Write-Host ""
        continue
    }
    
    # Construir la imagen
    docker build -f $service.Path -t "$($service.Name):latest" .
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  [OK] $($service.Name) construido exitosamente" -ForegroundColor Green
        $successCount++
    }
    else {
        Write-Host "  [ERROR] Error al construir $($service.Name)" -ForegroundColor Red
        $failCount++
    }
    
    Write-Host ""
}

# Resumen
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "RESUMEN DE CONSTRUCCION" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Exitosas: $successCount" -ForegroundColor Green
Write-Host "Fallidas:  $failCount" -ForegroundColor Red
Write-Host ""

# Listar imagenes creadas
Write-Host "Imagenes Docker disponibles:" -ForegroundColor Cyan
docker images | Select-String -Pattern "(api-gateway|product|user|delivery|cart|order|payment)-service"
Write-Host ""

if ($failCount -eq 0) {
    Write-Host "EXITO: Todas las imagenes fueron construidas exitosamente" -ForegroundColor Green
    Write-Host "Ahora puedes ejecutar: .\deploy.ps1" -ForegroundColor White
}
else {
    Write-Host "ADVERTENCIA: Algunas imagenes fallaron. Revisa los errores arriba." -ForegroundColor Yellow
}

Write-Host ""
