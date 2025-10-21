# =============================================================================
# Script de Pruebas de Integración - E-commerce Microservices
# =============================================================================
# Este script ejecuta todas las pruebas de integración del sistema
# Uso: .\run-integration-tests.ps1 [-Verbose] [-Coverage] [-Service <nombre>]

param(
    [switch]$Verbose,
    [switch]$Coverage,
    [string]$Service = ""
)

Write-Host ""
Write-Host "🧪 Iniciando Pruebas de Integración - E-commerce Microservices" -ForegroundColor Cyan
Write-Host "=" -ForegroundColor Cyan -NoNewline
Write-Host ("=" * 69) -ForegroundColor Cyan
Write-Host ""

# Verificar que estamos en el directorio correcto
if (-not (Test-Path "Backend")) {
    Write-Host "❌ Error: Este script debe ejecutarse desde la raíz del proyecto" -ForegroundColor Red
    Write-Host "   Directorio actual: $(Get-Location)" -ForegroundColor Yellow
    Write-Host "   Esperado: Directorio que contenga la carpeta 'Backend'" -ForegroundColor Yellow
    exit 1
}

# Verificar que Python está instalado
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python detectado: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Error: Python no está instalado o no está en el PATH" -ForegroundColor Red
    exit 1
}

# Verificar que pip está disponible
try {
    $pipVersion = pip --version 2>&1
    Write-Host "✅ pip detectado: $pipVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Error: pip no está disponible" -ForegroundColor Red
    exit 1
}

# Cambiar al directorio Backend
Set-Location "Backend"

Write-Host ""
Write-Host "📦 Instalando dependencias..." -ForegroundColor Yellow

# Instalar dependencias
try {
    if ($Verbose) {
        pip install -e .[dev]
    } else {
        pip install -e .[dev] | Out-Null
    }
    Write-Host "✅ Dependencias instaladas correctamente" -ForegroundColor Green
} catch {
    Write-Host "❌ Error al instalar dependencias" -ForegroundColor Red
    exit 1
}

# Verificar que pytest está instalado
try {
    $pytestVersion = python -m pytest --version 2>&1
    Write-Host "✅ pytest detectado: $pytestVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Error: pytest no está instalado correctamente" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "🧪 Ejecutando pruebas de integración..." -ForegroundColor Yellow

# Construir comando pytest
$pytestCmd = "python -m pytest tests/integration/"

if ($Service) {
    $pytestCmd += "test_$Service`_service.py"
    Write-Host "🎯 Ejecutando pruebas solo para: $Service" -ForegroundColor Cyan
}

if ($Verbose) {
    $pytestCmd += " -v"
}

if ($Coverage) {
    $pytestCmd += " --cov=src --cov-report=html --cov-report=term-missing"
    Write-Host "📊 Generando reporte de cobertura..." -ForegroundColor Cyan
}

# Ejecutar las pruebas
Write-Host ""
Write-Host "Comando: $pytestCmd" -ForegroundColor Gray
Write-Host ""

try {
    Invoke-Expression $pytestCmd
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "✅ Todas las pruebas pasaron exitosamente" -ForegroundColor Green
    } else {
        Write-Host ""
        Write-Host "❌ Algunas pruebas fallaron" -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host ""
    Write-Host "❌ Error al ejecutar las pruebas: $_" -ForegroundColor Red
    exit 1
}

# Mostrar resumen
Write-Host ""
Write-Host "=" -ForegroundColor Cyan -NoNewline
Write-Host ("=" * 69) -ForegroundColor Cyan
Write-Host "📋 RESUMEN DE PRUEBAS DE INTEGRACIÓN" -ForegroundColor Cyan
Write-Host "=" -ForegroundColor Cyan -NoNewline
Write-Host ("=" * 69) -ForegroundColor Cyan
Write-Host ""

$services = @(
    "Product Service",
    "User Service", 
    "Cart Service",
    "Order Service",
    "Payment Service",
    "Delivery Service"
)

Write-Host "✅ Servicios probados:" -ForegroundColor Green
foreach ($service in $services) {
    if (-not $Service -or $Service -eq $service.Replace(" Service", "").ToLower()) {
        Write-Host "   • $service" -ForegroundColor White
    }
}

Write-Host ""
Write-Host "🔍 Tipos de pruebas ejecutadas:" -ForegroundColor Green
Write-Host "   • Creación de entidades en base de datos" -ForegroundColor White
Write-Host "   • Recuperación de entidades por ID" -ForegroundColor White
Write-Host "   • Listado de entidades" -ForegroundColor White
Write-Host "   • Actualización de entidades" -ForegroundColor White
Write-Host "   • Eliminación de entidades" -ForegroundColor White
Write-Host "   • Validación de enums y estados" -ForegroundColor White
Write-Host "   • Pruebas de restricciones de base de datos" -ForegroundColor White
Write-Host "   • Pruebas de precisión de datos" -ForegroundColor White
Write-Host "   • Pruebas de relaciones entre entidades" -ForegroundColor White

if ($Coverage) {
    Write-Host ""
    Write-Host "📊 Reporte de cobertura generado en: Backend\htmlcov\index.html" -ForegroundColor Cyan
}

Write-Host ""
Write-Host "🎉 ¡Todas las pruebas de integración completadas exitosamente!" -ForegroundColor Green
Write-Host ""
Write-Host "💡 Próximos pasos:" -ForegroundColor Yellow
Write-Host "   • Revisar el reporte de cobertura (si se generó)" -ForegroundColor White
Write-Host "   • Ejecutar las pruebas en el pipeline de CI/CD" -ForegroundColor White
Write-Host "   • Considerar agregar pruebas de carga" -ForegroundColor White
Write-Host "   • Implementar pruebas de integración end-to-end" -ForegroundColor White

# Volver al directorio original
Set-Location ".."

Write-Host ""
Write-Host "✨ Script completado" -ForegroundColor Green
