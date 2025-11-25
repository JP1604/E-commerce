# Script para agregar productos de prueba

Write-Host "Agregando productos de prueba al backend..." -ForegroundColor Cyan

$products = @(
    @{
        name = "Laptop HP Pavilion"
        description = "Laptop HP Pavilion 15.6 pulgadas, Intel Core i5, 8GB RAM, 256GB SSD"
        price = 799.99
        category = "Electronics"
        stock_quantity = 15
    },
    @{
        name = "Mouse Logitech MX Master 3"
        description = "Mouse inalambrico ergonomico con precision avanzada"
        price = 99.99
        category = "Electronics"
        stock_quantity = 50
    },
    @{
        name = "Teclado Mecanico RGB"
        description = "Teclado mecanico gaming con iluminacion RGB personalizable"
        price = 129.99
        category = "Electronics"
        stock_quantity = 30
    },
    @{
        name = "Monitor LG 27 pulgadas 4K"
        description = "Monitor LG UltraFine 4K con HDR10"
        price = 449.99
        category = "Electronics"
        stock_quantity = 20
    },
    @{
        name = "Audifonos Sony WH-1000XM5"
        description = "Audifonos inalambricos con cancelacion de ruido premium"
        price = 399.99
        category = "Electronics"
        stock_quantity = 25
    },
    @{
        name = "Webcam Logitech C920"
        description = "Webcam HD 1080p para videoconferencias"
        price = 79.99
        category = "Electronics"
        stock_quantity = 40
    },
    @{
        name = "Disco Duro Externo 2TB"
        description = "Disco duro externo portatil USB 3.0"
        price = 89.99
        category = "Storage"
        stock_quantity = 35
    },
    @{
        name = "SSD Samsung 1TB"
        description = "SSD NVMe M.2 de alta velocidad"
        price = 149.99
        category = "Storage"
        stock_quantity = 45
    },
    @{
        name = "Cable USB-C a HDMI"
        description = "Cable adaptador USB-C a HDMI 4K"
        price = 19.99
        category = "Accessories"
        stock_quantity = 100
    },
    @{
        name = "Hub USB 3.0 de 7 Puertos"
        description = "Hub USB con alimentacion externa"
        price = 34.99
        category = "Accessories"
        stock_quantity = 60
    }
)

foreach ($product in $products) {
    $body = $product | ConvertTo-Json
    
    try {
        $response = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/products/" `
            -Method Post `
            -Body $body `
            -ContentType "application/json"
        
        Write-Host "Producto creado: $($product.name)" -ForegroundColor Green
    }
    catch {
        Write-Host "Error creando $($product.name): $_" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "Productos agregados exitosamente!" -ForegroundColor Green
Write-Host "Puedes ver los productos en: http://localhost:8000/api/v1/products" -ForegroundColor Cyan
