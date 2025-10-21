# Script de Diagnostico para E-commerce en Kubernetes
# Uso: .\diagnose.ps1

Write-Host ""
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "  DIAGNOSTICO DE DESPLIEGUE - E-commerce" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""

# 1. Verificar pods
Write-Host "1. Estado de los Pods:" -ForegroundColor Yellow
Write-Host ""
kubectl get pods
Write-Host ""

$runningPods = (kubectl get pods --no-headers 2>&1 | Select-String "Running" | Measure-Object).Count
$totalPods = (kubectl get pods --no-headers 2>&1 | Measure-Object).Count

Write-Host "Pods Running: $runningPods / $totalPods" -ForegroundColor $(if ($runningPods -eq $totalPods) { "Green" } else { "Yellow" })
Write-Host ""

# 2. Verificar servicios
Write-Host "2. Servicios Expuestos:" -ForegroundColor Yellow
Write-Host ""
kubectl get services | Select-String -Pattern "product|user|cart|order|payment|delivery"
Write-Host ""

# 3. Verificar product-service especificamente
Write-Host "3. Detalles de Product Service:" -ForegroundColor Yellow
Write-Host ""

$productPods = kubectl get pods -l app=product-service -o jsonpath='{.items[*].status.phase}' 2>&1
Write-Host "  Estado: $productPods" -ForegroundColor White

if ($productPods -like "*Running*") {
    Write-Host "  [OK] Product Service esta Running" -ForegroundColor Green
    
    Write-Host ""
    Write-Host "  Ultimos logs:" -ForegroundColor White
    kubectl logs -l app=product-service --tail=10 2>&1 | ForEach-Object { Write-Host "    $_" -ForegroundColor Gray }
}
else {
    Write-Host "  [PROBLEMA] Product Service NO esta Running" -ForegroundColor Red
    Write-Host ""
    Write-Host "  Detalles del problema:" -ForegroundColor White
    kubectl describe pod -l app=product-service 2>&1 | Select-Object -Last 20 | ForEach-Object { Write-Host "    $_" -ForegroundColor Gray }
}

Write-Host ""

# 4. Probar acceso HTTP
Write-Host "4. Prueba de Acceso HTTP:" -ForegroundColor Yellow
Write-Host ""

$endpoints = @{
    "Product Service Health" = "http://localhost:30000/health"
    "Product Service Docs" = "http://localhost:30000/docs"
}

foreach ($name in $endpoints.Keys) {
    $url = $endpoints[$name]
    try {
        $response = Invoke-WebRequest -Uri $url -TimeoutSec 3 -UseBasicParsing -ErrorAction Stop
        Write-Host "  [OK] $name - Accesible (Status: $($response.StatusCode))" -ForegroundColor Green
    }
    catch {
        Write-Host "  [FAIL] $name - No accesible" -ForegroundColor Red
        Write-Host "         URL: $url" -ForegroundColor Gray
        Write-Host "         Error: $($_.Exception.Message)" -ForegroundColor Gray
    }
}

Write-Host ""

# 5. Verificar bases de datos
Write-Host "5. Estado de Bases de Datos:" -ForegroundColor Yellow
Write-Host ""

$databases = @("product-db", "user-db", "cart-db", "order-db", "payment-db", "delivery-db")
$dbsReady = 0

foreach ($db in $databases) {
    $ready = kubectl get pods -l app=$db -o jsonpath='{.items[0].status.containerStatuses[0].ready}' 2>&1
    if ($ready -eq "true") {
        Write-Host "  [OK] $db esta listo" -ForegroundColor Green
        $dbsReady++
    }
    else {
        Write-Host "  [PROBLEMA] $db NO esta listo (Estado: $ready)" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "Bases de datos listas: $dbsReady / $($databases.Count)" -ForegroundColor $(if ($dbsReady -eq $databases.Count) { "Green" } else { "Yellow" })
Write-Host ""

# 6. Resumen y recomendaciones
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "  RESUMEN Y RECOMENDACIONES" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""

if ($runningPods -lt $totalPods) {
    Write-Host "[ACCION REQUERIDA] No todos los pods estan Running" -ForegroundColor Yellow
    Write-Host "  1. Espera 2-3 minutos mas para que se inicien" -ForegroundColor White
    Write-Host "  2. Si siguen en Pending/Error, ejecuta:" -ForegroundColor White
    Write-Host "     kubectl describe pod NOMBRE-POD" -ForegroundColor Gray
    Write-Host "     kubectl logs NOMBRE-POD" -ForegroundColor Gray
}
elseif ($dbsReady -lt $databases.Count) {
    Write-Host "[ACCION REQUERIDA] Bases de datos no estan listas" -ForegroundColor Yellow
    Write-Host "  Las bases de datos PostgreSQL tardan 1-2 minutos en iniciar" -ForegroundColor White
    Write-Host "  Espera un poco mas y ejecuta este diagnostico de nuevo" -ForegroundColor White
}
else {
    Write-Host "[ESTADO] Todo parece estar funcionando correctamente" -ForegroundColor Green
    Write-Host ""
    Write-Host "Si aun no puedes acceder a http://localhost:30000/docs:" -ForegroundColor White
    Write-Host "  1. Verifica que el pod product-service este Running" -ForegroundColor White
    Write-Host "  2. Revisa los logs: kubectl logs -l app=product-service" -ForegroundColor White
    Write-Host "  3. Prueba el health endpoint: http://localhost:30000/health" -ForegroundColor White
}

Write-Host ""
Write-Host "Para ejecutar este diagnostico de nuevo: .\diagnose.ps1" -ForegroundColor Cyan
Write-Host ""
