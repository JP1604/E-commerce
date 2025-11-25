# Script para iniciar el Frontend del E-Commerce
# Encoding: UTF-8

Write-Host "Iniciando Frontend E-Commerce..." -ForegroundColor Cyan
Write-Host ""

# Verificar que estamos en el directorio correcto
$frontendPath = "c:\Users\afperez\E-commerce\Frontend"

if (-not (Test-Path $frontendPath)) {
    Write-Host "Error: No se encuentra el directorio Frontend" -ForegroundColor Red
    exit 1
}

Set-Location $frontendPath

# Verificar que node_modules existe
if (-not (Test-Path "node_modules")) {
    Write-Host "Instalando dependencias..." -ForegroundColor Yellow
    npm install
    Write-Host ""
}

# Mostrar información importante
Write-Host "Informacion del Frontend:" -ForegroundColor Green
Write-Host "  - URL: http://localhost:3000" -ForegroundColor White
Write-Host "  - Backend API: http://localhost:8000" -ForegroundColor White
Write-Host "  - Chatbot n8n: http://localhost:5678/webhook/chatbot" -ForegroundColor White
Write-Host ""

Write-Host "Asegurate de que los siguientes servicios esten corriendo:" -ForegroundColor Yellow
Write-Host "  - Backend (puerto 8000)" -ForegroundColor White
Write-Host "  - n8n (puerto 5678)" -ForegroundColor White
Write-Host "  - Workflow de n8n activado" -ForegroundColor White
Write-Host ""

# Iniciar el servidor de desarrollo
Write-Host "Iniciando servidor de desarrollo..." -ForegroundColor Cyan
npm run dev
