# Script para Probar la Comunicación del API Gateway
# Uso: .\test-api-gateway.ps1

Write-Host ""
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "  Probando Comunicación del API Gateway" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""

# Verificar que kubectl está disponible
$null = kubectl version --client 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] kubectl no está instalado" -ForegroundColor Red
    exit 1
}

# Verificar que el API Gateway está desplegado
Write-Host "Paso 1: Verificando estado del API Gateway..." -ForegroundColor Yellow
$gatewayPod = kubectl get pods -l app=api-gateway -o jsonpath='{.items[0].metadata.name}' 2>&1
if ($LASTEXITCODE -ne 0 -or $gatewayPod -eq "") {
    Write-Host "[ERROR] API Gateway no está desplegado" -ForegroundColor Red
    Write-Host "Ejecuta primero: .\deploy.ps1" -ForegroundColor Yellow
    exit 1
}

$gatewayStatus = kubectl get pods -l app=api-gateway -o jsonpath='{.items[0].status.phase}' 2>&1
if ($gatewayStatus -ne "Running") {
    Write-Host "[ADVERTENCIA] API Gateway no está en estado Running (Estado: $gatewayStatus)" -ForegroundColor Yellow
    Write-Host "Esperando a que esté listo..." -ForegroundColor White
    
    # Esperar hasta 2 minutos
    $maxWait = 120
    $elapsed = 0
    while ($elapsed -lt $maxWait) {
        $status = kubectl get pods -l app=api-gateway -o jsonpath='{.items[0].status.phase}' 2>&1
        if ($status -eq "Running") {
            Write-Host "[OK] API Gateway está listo" -ForegroundColor Green
            break
        }
        Write-Host "  Esperando... ($elapsed/$maxWait segundos)" -ForegroundColor White
        Start-Sleep -Seconds 5
        $elapsed += 5
    }
    
    if ($elapsed -ge $maxWait) {
        Write-Host "[ERROR] Timeout esperando API Gateway" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "[OK] API Gateway está ejecutándose" -ForegroundColor Green
}

Write-Host ""

# Obtener la URL del API Gateway
$gatewayUrl = "http://localhost:30080"
Write-Host "Paso 2: Probando endpoints del API Gateway..." -ForegroundColor Yellow
Write-Host "URL: $gatewayUrl" -ForegroundColor White
Write-Host ""

# Función para probar un endpoint
function Test-Endpoint {
    param(
        [string]$Name,
        [string]$Url,
        [string]$ExpectedStatus = "200"
    )
    
    Write-Host "  Probando $Name..." -ForegroundColor Cyan
    try {
        $response = Invoke-WebRequest -Uri $Url -Method GET -TimeoutSec 10 -UseBasicParsing
        if ($response.StatusCode -eq $ExpectedStatus) {
            Write-Host "    [OK] $Name - Status: $($response.StatusCode)" -ForegroundColor Green
            return $true
        } else {
            Write-Host "    [ERROR] $Name - Status: $($response.StatusCode) (esperado: $ExpectedStatus)" -ForegroundColor Red
            return $false
        }
    }
    catch {
        Write-Host "    [ERROR] $Name - Error: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

# Probar endpoints
$tests = @(
    @{Name="Health Check"; Url="$gatewayUrl/"; ExpectedStatus="200"},
    @{Name="API Docs"; Url="$gatewayUrl/docs"; ExpectedStatus="200"},
    @{Name="Products API"; Url="$gatewayUrl/api/products/"; ExpectedStatus="200"},
    @{Name="Users API"; Url="$gatewayUrl/api/users/"; ExpectedStatus="200"},
    @{Name="Orders API"; Url="$gatewayUrl/api/orders/"; ExpectedStatus="200"}
)

$successCount = 0
$totalTests = $tests.Count

foreach ($test in $tests) {
    if (Test-Endpoint -Name $test.Name -Url $test.Url -ExpectedStatus $test.ExpectedStatus) {
        $successCount++
    }
    Write-Host ""
}

# Probar endpoints específicos de carritos (que requieren parámetros)
Write-Host "  Probando endpoints específicos de carritos..." -ForegroundColor Cyan
try {
    # Probar obtener carrito por usuario (usando un UUID válido)
    $testUserId = "123e4567-e89b-12d3-a456-426614174000"  # UUID válido de prueba
    $cartResponse = Invoke-WebRequest -Uri "$gatewayUrl/api/carts/user/$testUserId" -Method GET -TimeoutSec 10 -UseBasicParsing
    if ($cartResponse.StatusCode -eq 404) {
        Write-Host "    [OK] Carts API (user endpoint) - Status: 404 (Not Found - esperado)" -ForegroundColor Green
        $successCount++
    } else {
        Write-Host "    [OK] Carts API (user endpoint) - Status: $($cartResponse.StatusCode)" -ForegroundColor Green
        $successCount++
    }
} catch {
    if ($_.Exception.Response.StatusCode -eq 404) {
        Write-Host "    [OK] Carts API (user endpoint) - Status: 404 (Not Found - esperado)" -ForegroundColor Green
        $successCount++
    } elseif ($_.Exception.Response.StatusCode -eq 422) {
        Write-Host "    [OK] Carts API (user endpoint) - Status: 422 (Validation Error - esperado para UUID inválido)" -ForegroundColor Green
        $successCount++
    } else {
        Write-Host "    [ERROR] Carts API (user endpoint) - Error: $($_.Exception.Message)" -ForegroundColor Red
    }
}
Write-Host ""

$totalTests++

# Resumen
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "  RESUMEN DE PRUEBAS" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Pruebas exitosas: $successCount/$totalTests" -ForegroundColor $(if ($successCount -eq $totalTests) { "Green" } else { "Yellow" })
Write-Host ""

if ($successCount -eq $totalTests) {
    Write-Host "🎉 ¡TODAS LAS PRUEBAS PASARON!" -ForegroundColor Green
    Write-Host ""
    Write-Host "El API Gateway está funcionando correctamente y puede comunicarse con todos los microservicios." -ForegroundColor Green
    Write-Host ""
    Write-Host "Puedes acceder a:" -ForegroundColor Cyan
    Write-Host "  🚀 API Gateway: $gatewayUrl/docs" -ForegroundColor Green
    Write-Host "  📚 Documentación: $gatewayUrl/docs" -ForegroundColor White
    Write-Host "  🔍 API Base: $gatewayUrl/api/" -ForegroundColor White
} else {
    Write-Host "⚠️  ALGUNAS PRUEBAS FALLARON" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Posibles causas:" -ForegroundColor Yellow
    Write-Host "  - Los microservicios no están ejecutándose" -ForegroundColor White
    Write-Host "  - Problemas de red en Kubernetes" -ForegroundColor White
    Write-Host "  - Configuración incorrecta" -ForegroundColor White
    Write-Host ""
    Write-Host "Comandos para diagnosticar:" -ForegroundColor Cyan
    Write-Host "  kubectl get pods" -ForegroundColor White
    Write-Host "  kubectl logs -l app=api-gateway" -ForegroundColor White
    Write-Host "  kubectl get services" -ForegroundColor White
}

Write-Host ""
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""
