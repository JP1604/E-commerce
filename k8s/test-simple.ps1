# Script de Pruebas Simple para E-commerce en Kubernetes
# Uso: .\test-simple.ps1

Write-Host ""
Write-Host "==============================================================================" -ForegroundColor Cyan
Write-Host "  PRUEBAS AUTOMATIZADAS - E-commerce en Kubernetes" -ForegroundColor Cyan
Write-Host "==============================================================================" -ForegroundColor Cyan
Write-Host ""

$passedTests = 0
$failedTests = 0

function Show-TestResult {
    param(
        [string]$TestName,
        [bool]$Passed
    )
    
    if ($Passed) {
        Write-Host "  [OK] $TestName" -ForegroundColor Green
        $script:passedTests++
    } else {
        Write-Host "  [FAIL] $TestName" -ForegroundColor Red
        $script:failedTests++
    }
}

# =============================================================================
# 1. Verificar Pre-requisitos
# =============================================================================
Write-Host "Test Suite 1: Pre-requisitos" -ForegroundColor Yellow
Write-Host ""

# kubectl
$null = kubectl version --client 2>&1
Show-TestResult "kubectl instalado" ($LASTEXITCODE -eq 0)

# Conexión al cluster
$null = kubectl cluster-info 2>&1
Show-TestResult "Conexion al cluster K8s" ($LASTEXITCODE -eq 0)

Write-Host ""

# =============================================================================
# 2. Verificar Recursos
# =============================================================================
Write-Host "Test Suite 2: Recursos Desplegados" -ForegroundColor Yellow
Write-Host ""

# ConfigMap
$null = kubectl get configmap ecommerce-config 2>&1
Show-TestResult "ConfigMap existe" ($LASTEXITCODE -eq 0)

# Secrets
$null = kubectl get secret ecommerce-secrets 2>&1
Show-TestResult "Secrets existen" ($LASTEXITCODE -eq 0)

Write-Host ""

# =============================================================================
# 3. Verificar Pods
# =============================================================================
Write-Host "Test Suite 3: Estado de Pods" -ForegroundColor Yellow
Write-Host ""

$services = @(
    "product-db",
    "user-db",
    "cart-db",
    "order-db",
    "payment-db",
    "product-service",
    "user-service",
    "cart-service",
    "order-service",
    "payment-service"
)

foreach ($service in $services) {
    $pods = kubectl get pods -l app=$service -o jsonpath='{.items[*].status.phase}' 2>&1 | Out-String
    $isRunning = [bool]($pods -like "*Running*")
    Show-TestResult "Pod $service Running" $isRunning
}

Write-Host ""

# =============================================================================
# 4. Verificar Acceso Web
# =============================================================================
Write-Host "Test Suite 4: Acceso a Servicios Web" -ForegroundColor Yellow
Write-Host ""

$ports = @{
    "Product Service" = 30000
    "User Service" = 30001
    "Cart Service" = 30003
    "Order Service" = 30005
    "Payment Service" = 30007
}

foreach ($serviceName in $ports.Keys) {
    $port = $ports[$serviceName]
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:$port/docs" -TimeoutSec 5 -UseBasicParsing -ErrorAction Stop
        Show-TestResult "$serviceName accesible" ($response.StatusCode -eq 200)
    } catch {
        Show-TestResult "$serviceName accesible" $false
    }
}

Write-Host ""

# =============================================================================
# 5. Verificar Health Checks
# =============================================================================
Write-Host "Test Suite 5: Health Checks" -ForegroundColor Yellow
Write-Host ""

foreach ($serviceName in $ports.Keys) {
    $port = $ports[$serviceName]
    try {
        $response = Invoke-RestMethod -Uri "http://localhost:$port/health" -TimeoutSec 5 -ErrorAction Stop
        Show-TestResult "$serviceName health OK" $true
    } catch {
        Show-TestResult "$serviceName health OK" $false
    }
}

Write-Host ""

# =============================================================================
# 6. Prueba de Integracion Basica
# =============================================================================
Write-Host "Test Suite 6: Integracion Basica" -ForegroundColor Yellow
Write-Host ""

# Crear producto
try {
    $productBody = @{
        name = "Test Product"
        description = "Product for testing"
        price = 99.99
        stock_quantity = 10
    } | ConvertTo-Json

    $product = Invoke-RestMethod -Uri "http://localhost:30000/api/v1/products/" -Method POST -Body $productBody -ContentType "application/json" -TimeoutSec 10 -ErrorAction Stop
    
    $productCreated = ($null -ne $product.id)
    Show-TestResult "Crear producto via API" $productCreated
    
    if ($productCreated) {
        Write-Host "     Producto ID: $($product.id)" -ForegroundColor Gray
    }
} catch {
    Show-TestResult "Crear producto via API" $false
}

# Crear usuario
try {
    $userBody = @{
        name = "Test User"
        email = "test@example.com"
        phone = "+34612345678"
    } | ConvertTo-Json

    $user = Invoke-RestMethod -Uri "http://localhost:30001/api/v1/users/" -Method POST -Body $userBody -ContentType "application/json" -TimeoutSec 10 -ErrorAction Stop
    
    $userCreated = ($null -ne $user.id)
    Show-TestResult "Crear usuario via API" $userCreated
    
    if ($userCreated) {
        Write-Host "     Usuario ID: $($user.id)" -ForegroundColor Gray
    }
} catch {
    Show-TestResult "Crear usuario via API" $false
}

Write-Host ""

# =============================================================================
# Resumen
# =============================================================================
$totalTests = $passedTests + $failedTests
$successRate = if ($totalTests -gt 0) { [math]::Round(($passedTests / $totalTests) * 100, 2) } else { 0 }

Write-Host ""
Write-Host "==============================================================================" -ForegroundColor Cyan
Write-Host "  RESUMEN DE PRUEBAS" -ForegroundColor Cyan
Write-Host "==============================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Total de pruebas:     $totalTests" -ForegroundColor White
Write-Host "Pruebas exitosas:     $passedTests" -ForegroundColor Green
Write-Host "Pruebas fallidas:     $failedTests" -ForegroundColor Red
Write-Host "Tasa de exito:        $successRate%" -ForegroundColor $(if ($successRate -eq 100) { "Green" } elseif ($successRate -ge 80) { "Yellow" } else { "Red" })
Write-Host ""

if ($failedTests -eq 0) {
    Write-Host "EXITO! Todas las pruebas pasaron!" -ForegroundColor Green
} elseif ($successRate -ge 80) {
    Write-Host "La mayoria de las pruebas pasaron" -ForegroundColor Yellow
} else {
    Write-Host "Varias pruebas fallaron - Verifica el despliegue" -ForegroundColor Red
    Write-Host "Comandos utiles:" -ForegroundColor White
    Write-Host "  kubectl get pods" -ForegroundColor Gray
    Write-Host "  kubectl logs -l app=product-service" -ForegroundColor Gray
}

Write-Host ""
Write-Host "==============================================================================" -ForegroundColor Cyan
Write-Host ""
