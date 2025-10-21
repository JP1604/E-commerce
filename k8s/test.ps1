# =============================================================================
# Script de Pruebas Automatizadas - E-commerce en Kubernetes
# =============================================================================
# Este script verifica que todo funciona correctamente después del despliegue
# Uso: .\test.ps1

Write-Host ""
Write-Host "🧪 Iniciando Pruebas Automatizadas de E-commerce..." -ForegroundColor Cyan
Write-Host "=" -ForegroundColor Cyan -NoNewline
Write-Host ("=" * 79) -ForegroundColor Cyan
Write-Host ""

$passedTests = 0
$failedTests = 0
$totalTests = 0

# Función para mostrar resultado de test
function Test-Result {
    param(
        [string]$TestName,
        [bool]$Passed,
        [string]$Message = ""
    )
    
    $script:totalTests++
    
    if ($Passed) {
        Write-Host "  ✅ PASS: $TestName" -ForegroundColor Green
        $script:passedTests++
    } else {
        Write-Host "  ❌ FAIL: $TestName" -ForegroundColor Red
        if ($Message) {
            Write-Host "     └─ $Message" -ForegroundColor Yellow
        }
        $script:failedTests++
    }
}

# =============================================================================
# 1. Verificar Pre-requisitos
# =============================================================================
Write-Host "📋 Test Suite 1: Pre-requisitos" -ForegroundColor Cyan
Write-Host ""

# Test 1.1: kubectl
try {
    $null = kubectl version --client --short 2>&1
    Test-Result "kubectl instalado" ($LASTEXITCODE -eq 0)
} catch {
    Test-Result "kubectl instalado" $false "kubectl no está disponible"
}

# Test 1.2: Conexión al cluster
try {
    $null = kubectl cluster-info 2>&1
    Test-Result "Conexión al cluster K8s" ($LASTEXITCODE -eq 0)
} catch {
    Test-Result "Conexión al cluster K8s" $false "No se puede conectar al cluster"
}

Write-Host ""

# =============================================================================
# 2. Verificar Recursos Desplegados
# =============================================================================
Write-Host "📋 Test Suite 2: Recursos Desplegados" -ForegroundColor Cyan
Write-Host ""

# Test 2.1: ConfigMaps
$null = kubectl get configmap ecommerce-config 2>&1
Test-Result "ConfigMap existe" ($LASTEXITCODE -eq 0) "Ejecuta deploy.ps1 primero"

# Test 2.2: Secrets
$null = kubectl get secret ecommerce-secrets 2>&1
Test-Result "Secrets existen" ($LASTEXITCODE -eq 0) "Ejecuta deploy.ps1 primero"

# Test 2.3: PVCs
$pvcCount = (kubectl get pvc 2>&1 | Measure-Object -Line).Lines - 1
Test-Result "PersistentVolumeClaims - 6 esperados" ($pvcCount -eq 6) "Encontrados: $pvcCount"

# Test 2.4: Servicios
$serviceCount = (kubectl get services 2>&1 | Where-Object { $_ -match "product|user|delivery|cart|order|payment" } | Measure-Object -Line).Lines
Test-Result "Services desplegados - 13 esperados" ($serviceCount -eq 13) "Encontrados: $serviceCount"

Write-Host ""

# =============================================================================
# 3. Verificar Estado de Pods
# =============================================================================
Write-Host "📋 Test Suite 3: Estado de Pods" -ForegroundColor Cyan
Write-Host ""

# Lista de servicios esperados
$services = @(
    "product-db",
    "user-db",
    "delivery-db",
    "cart-db",
    "order-db",
    "payment-db",
    "product-service",
    "user-service",
    "delivery-service",
    "cart-service",
    "order-service",
    "order-validation-service",
    "payment-service"
)

foreach ($service in $services) {
    $pods = kubectl get pods -l app=$service -o jsonpath='{.items[*].status.phase}' 2>&1
    $allRunning = ($pods -split " " | Where-Object { $_ -ne "Running" }).Count -eq 0 -and $pods -ne ""
    Test-Result "Pod $service en estado Running" $allRunning "Estado: $pods"
}

Write-Host ""

# =============================================================================
# 4. Verificar Acceso Web (Swagger UI)
# =============================================================================
Write-Host "📋 Test Suite 4: Acceso Web a Servicios" -ForegroundColor Cyan
Write-Host ""

$webServices = @{
    "Product Service"           = "http://localhost:30000/docs"
    "User Service"              = "http://localhost:30001/docs"
    "Delivery Service"          = "http://localhost:30002/docs"
    "Cart Service"              = "http://localhost:30003/docs"
    "Order Service"             = "http://localhost:30005/docs"
    "Order Validation Service"  = "http://localhost:30006/docs"
    "Payment Service"           = "http://localhost:30007/docs"
}

foreach ($serviceName in $webServices.Keys) {
    $url = $webServices[$serviceName]
    try {
        $response = Invoke-WebRequest -Uri $url -TimeoutSec 5 -UseBasicParsing -ErrorAction SilentlyContinue
        $accessible = ($response.StatusCode -eq 200)
        Test-Result "Acceso a $serviceName" $accessible "URL: $url"
    } catch {
        Test-Result "Acceso a $serviceName" $false "$url no responde"
    }
}

Write-Host ""

# =============================================================================
# 5. Verificar Health Checks
# =============================================================================
Write-Host "📋 Test Suite 5: Health Checks" -ForegroundColor Cyan
Write-Host ""

$healthEndpoints = @{
    "Product Service"           = "http://localhost:30000/health"
    "User Service"              = "http://localhost:30001/health"
    "Delivery Service"          = "http://localhost:30002/health"
    "Cart Service"              = "http://localhost:30003/health"
    "Order Service"             = "http://localhost:30005/health"
    "Order Validation Service"  = "http://localhost:30006/health"
    "Payment Service"           = "http://localhost:30007/health"
}

foreach ($serviceName in $healthEndpoints.Keys) {
    $url = $healthEndpoints[$serviceName]
    try {
        $response = Invoke-RestMethod -Uri $url -TimeoutSec 5 -ErrorAction SilentlyContinue
        $healthy = $true
        Test-Result "Health check $serviceName" $healthy
    } catch {
        Test-Result "Health check $serviceName" $false "No responde"
    }
}

Write-Host ""

# =============================================================================
# 6. Prueba de Integración Básica
# =============================================================================
Write-Host "📋 Test Suite 6: Integración Básica" -ForegroundColor Cyan
Write-Host ""

# Test 6.1: Crear un producto
try {
    $productBody = @{
        name = "Test Product"
        description = "Product for automated testing"
        price = 99.99
        stock_quantity = 10
    } | ConvertTo-Json

    $product = Invoke-RestMethod -Uri "http://localhost:30000/api/v1/products/" -Method POST -Body $productBody -ContentType "application/json" -TimeoutSec 10 -ErrorAction SilentlyContinue
    
    $productCreated = ($null -ne $product.id)
    Test-Result "Crear producto vía API" $productCreated
    
    if ($productCreated) {
        $productId = $product.id
        Write-Host "     └─ Producto creado con ID: $productId" -ForegroundColor Gray
        
        # Test 6.2: Obtener el producto
        try {
            $retrievedProduct = Invoke-RestMethod -Uri "http://localhost:30000/api/v1/products/$productId" -Method GET -TimeoutSec 10 -ErrorAction SilentlyContinue
            
            Test-Result "Obtener producto por ID" ($retrievedProduct.id -eq $productId)
        } catch {
            Test-Result "Obtener producto por ID" $false
        }
        
        # Test 6.3: Listar productos
        try {
            $products = Invoke-RestMethod -Uri "http://localhost:30000/api/v1/products/" -Method GET -TimeoutSec 10 -ErrorAction SilentlyContinue
            
            Test-Result "Listar productos" ($products.Count -gt 0)
        } catch {
            Test-Result "Listar productos" $false
        }
    }
} catch {
    Test-Result "Crear producto vía API" $false "Error al crear producto"
}

# Test 6.4: Crear un usuario
try {
    $userBody = @{
        name = "Test User"
        email = "test@example.com"
        phone = "+34612345678"
    } | ConvertTo-Json

    $user = Invoke-RestMethod -Uri "http://localhost:30001/api/v1/users/" -Method POST -Body $userBody -ContentType "application/json" -TimeoutSec 10 -ErrorAction SilentlyContinue
    
    $userCreated = ($null -ne $user.id)
    Test-Result "Crear usuario vía API" $userCreated
    
    if ($userCreated) {
        Write-Host "     └─ Usuario creado con ID: $($user.id)" -ForegroundColor Gray
    }
} catch {
    Test-Result "Crear usuario vía API" $false
}

Write-Host ""

# =============================================================================
# 7. Verificar Alta Disponibilidad
# =============================================================================
Write-Host "📋 Test Suite 7: Alta Disponibilidad" -ForegroundColor Cyan
Write-Host ""

# Test 7.1: Verificar réplicas
$services = @("product-service", "user-service", "cart-service", "order-service", "payment-service")

foreach ($service in $services) {
    $replicaCount = (kubectl get pods -l app=$service 2>&1 | Measure-Object -Line).Lines - 1
    Test-Result "Réplicas de $service - 2 esperadas" ($replicaCount -eq 2) "Encontradas: $replicaCount"
}

Write-Host ""

# =============================================================================
# 8. Verificar Persistencia
# =============================================================================
Write-Host "📋 Test Suite 8: Persistencia de Datos" -ForegroundColor Cyan
Write-Host ""

# Test 8.1: Verificar que PVCs están Bound
$pvcsBound = kubectl get pvc -o jsonpath='{.items[*].status.phase}' 2>&1
$allBound = ($pvcsBound -split " " | Where-Object { $_ -ne "Bound" }).Count -eq 0 -and $pvcsBound -ne ""
Test-Result "Todos los PVCs están Bound" $allBound

Write-Host ""

# =============================================================================
# Resumen de Resultados
# =============================================================================
Write-Host ""
Write-Host "=" -ForegroundColor Cyan -NoNewline
Write-Host ("=" * 79) -ForegroundColor Cyan
Write-Host "📊 RESUMEN DE PRUEBAS" -ForegroundColor Cyan
Write-Host "=" -ForegroundColor Cyan -NoNewline
Write-Host ("=" * 79) -ForegroundColor Cyan
Write-Host ""

$successRate = if ($totalTests -gt 0) { [math]::Round(($passedTests / $totalTests) * 100, 2) } else { 0 }

Write-Host "Total de pruebas:     $totalTests" -ForegroundColor White
Write-Host "Pruebas exitosas:     $passedTests" -ForegroundColor Green
Write-Host "Pruebas fallidas:     $failedTests" -ForegroundColor Red
Write-Host "Tasa de éxito:        $successRate%" -ForegroundColor $(if ($successRate -eq 100) { "Green" } else { "Yellow" })
Write-Host ""

if ($failedTests -eq 0) {
    Write-Host "🎉 ¡TODAS LAS PRUEBAS PASARON!" -ForegroundColor Green
    Write-Host "   Tu aplicación está funcionando correctamente en Kubernetes" -ForegroundColor Green
} elseif ($successRate -ge 80) {
    Write-Host "⚠️  LA MAYORÍA DE LAS PRUEBAS PASARON" -ForegroundColor Yellow
    Write-Host "   Revisa las pruebas fallidas arriba" -ForegroundColor Yellow
} else {
    Write-Host "❌ VARIAS PRUEBAS FALLARON" -ForegroundColor Red
    Write-Host "   Verifica el despliegue y revisa los logs:" -ForegroundColor Red
    Write-Host "   kubectl get pods" -ForegroundColor White
    Write-Host "   kubectl logs <nombre-pod>" -ForegroundColor White
}

Write-Host ""
Write-Host "=" -ForegroundColor Cyan -NoNewline
Write-Host ("=" * 79) -ForegroundColor Cyan
Write-Host ""

# Comandos útiles
Write-Host "💡 Comandos útiles:" -ForegroundColor Cyan
Write-Host ""
Write-Host "  Ver pods:              kubectl get pods" -ForegroundColor White
Write-Host "  Ver servicios:         kubectl get services" -ForegroundColor White
Write-Host "  Ver logs:              kubectl logs -l app=product-service -f" -ForegroundColor White
Write-Host "  Ver eventos:           kubectl get events --sort-by='.lastTimestamp'" -ForegroundColor White
Write-Host "  Describir pod:         kubectl describe pod <nombre-pod>" -ForegroundColor White
Write-Host "  Acceder a Swagger:     http://localhost:30000/docs" -ForegroundColor White
Write-Host ""

exit $failedTests
