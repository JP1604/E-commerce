# Script para probar el chatbot de n8n con el backend de E-commerce
# Autor: Sistema de E-commerce
# Fecha: 2025

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  Test de Chatbot E-commerce con n8n" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Variables
$WEBHOOK_URL = "http://localhost:5678/webhook-test/chatbot"
$USER_ID = "123e4567-e89b-12d3-a456-426614174000"

# Función para enviar mensaje al chatbot
function Send-ChatMessage {
    param(
        [string]$Message,
        [string]$UserId = $USER_ID
    )
    
    $body = @{
        user_id = $UserId
        message = $Message
    } | ConvertTo-Json

    try {
        Write-Host "> Usuario: " -NoNewline -ForegroundColor Yellow
        Write-Host $Message -ForegroundColor White
        
        $response = Invoke-RestMethod -Uri $WEBHOOK_URL -Method Post -Body $body -ContentType "application/json"
        
        Write-Host "> Chatbot: " -NoNewline -ForegroundColor Green
        Write-Host $response.response -ForegroundColor White
        Write-Host ""
        
        return $response
    }
    catch {
        Write-Host "Error al comunicarse con el chatbot: $_" -ForegroundColor Red
        Write-Host "Asegúrate de que n8n esté corriendo y el workflow esté activo" -ForegroundColor Yellow
        return $null
    }
}

# Verificar si n8n está corriendo
Write-Host "Paso 1: Verificando n8n..." -ForegroundColor Cyan
try {
    $n8nStatus = Invoke-WebRequest -Uri "http://localhost:5678" -Method Get -TimeoutSec 5 -UseBasicParsing
    Write-Host "[OK] n8n está corriendo" -ForegroundColor Green
}
catch {
    Write-Host "[ERROR] n8n no está disponible en http://localhost:5678" -ForegroundColor Red
    Write-Host "Por favor ejecuta: docker-compose up -d n8n" -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  Iniciando pruebas del chatbot" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Prueba 1: Comando de ayuda
Write-Host "Test 1: Comando de ayuda" -ForegroundColor Magenta
Write-Host "----------------------------------------" -ForegroundColor Gray
Send-ChatMessage -Message "ayuda"
Start-Sleep -Seconds 2

# Prueba 2: Ver productos
Write-Host "Test 2: Ver productos disponibles" -ForegroundColor Magenta
Write-Host "----------------------------------------" -ForegroundColor Gray
Send-ChatMessage -Message "ver productos"
Start-Sleep -Seconds 2

# Prueba 3: Ver carrito
Write-Host "Test 3: Ver carrito" -ForegroundColor Magenta
Write-Host "----------------------------------------" -ForegroundColor Gray
Send-ChatMessage -Message "ver mi carrito"
Start-Sleep -Seconds 2

# Prueba 4: Ver órdenes
Write-Host "Test 4: Ver mis órdenes" -ForegroundColor Magenta
Write-Host "----------------------------------------" -ForegroundColor Gray
Send-ChatMessage -Message "mis órdenes"
Start-Sleep -Seconds 2

# Prueba 5: Información de pago
Write-Host "Test 5: Información de pago" -ForegroundColor Magenta
Write-Host "----------------------------------------" -ForegroundColor Gray
Send-ChatMessage -Message "pagar"
Start-Sleep -Seconds 2

# Prueba 6: Comando no reconocido
Write-Host "Test 6: Comando no reconocido" -ForegroundColor Magenta
Write-Host "----------------------------------------" -ForegroundColor Gray
Send-ChatMessage -Message "comando inexistente"
Start-Sleep -Seconds 2

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  Resumen de Pruebas" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "✅ Todas las pruebas completadas" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Información adicional:" -ForegroundColor Cyan
Write-Host "  - n8n Dashboard: http://localhost:5678" -ForegroundColor White
Write-Host "  - Usuario: admin" -ForegroundColor White
Write-Host "  - Contraseña: admin123" -ForegroundColor White
Write-Host "  - Webhook URL: $WEBHOOK_URL" -ForegroundColor White
Write-Host ""
Write-Host "💡 Próximos pasos:" -ForegroundColor Cyan
Write-Host "  1. Abre n8n en tu navegador" -ForegroundColor White
Write-Host "  2. Importa el workflow desde n8n/workflows/chatbot-ecommerce.json" -ForegroundColor White
Write-Host "  3. Activa el workflow" -ForegroundColor White
Write-Host "  4. Prueba enviando mensajes personalizados" -ForegroundColor White
Write-Host ""

# Opción interactiva
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  Modo Interactivo" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "¿Quieres probar el chatbot de forma interactiva? (S/N): " -NoNewline -ForegroundColor Yellow
$respuesta = Read-Host

if ($respuesta -eq "S" -or $respuesta -eq "s") {
    Write-Host ""
    Write-Host "Modo interactivo activado. Escribe 'salir' para terminar." -ForegroundColor Green
    Write-Host ""
    
    while ($true) {
        Write-Host "Tú: " -NoNewline -ForegroundColor Yellow
        $mensaje = Read-Host
        
        if ($mensaje -eq "salir" -or $mensaje -eq "exit") {
            Write-Host "¡Hasta luego! 👋" -ForegroundColor Cyan
            break
        }
        
        if ($mensaje) {
            Send-ChatMessage -Message $mensaje
        }
    }
}

Write-Host ""
Write-Host "Script finalizado. ¡Gracias por usar el chatbot! 🤖" -ForegroundColor Cyan
