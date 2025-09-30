"""
Script simple para verificar que todos los servicios están funcionando.
"""

import requests
import sys

def check_service(name, url):
    """Verifica si un servicio está funcionando."""
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            print(f"✅ {name}: OK")
            return True
        else:
            print(f"⚠️ {name}: HTTP {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ {name}: No disponible ({e})")
        return False

def main():
    """Función principal."""
    print("🏥 Verificando salud de microservicios...")
    print("=" * 50)
    
    services = [
        ("Order Service", "http://localhost:8005/"),
        ("Order Validation Service", "http://localhost:8006/"),
        ("Payment Service", "http://localhost:8007/"),
        ("User Service", "http://localhost:8001/"),
        ("Product Service", "http://localhost:8000/")
    ]
    
    all_healthy = True
    
    for name, url in services:
        if not check_service(name, url):
            all_healthy = False
    
    print("=" * 50)
    
    if all_healthy:
        print("🎉 Todos los servicios están funcionando correctamente!")
        
        # Mostrar URLs de documentación
        print("\n📚 URLs de documentación:")
        print("- Order Service: http://localhost:8005/docs")
        print("- Order Validation: http://localhost:8006/docs")
        print("- Payment Service: http://localhost:8007/docs")
        print("- User Service: http://localhost:8001/docs")
        print("- Product Service: http://localhost:8000/docs")
        
        return 0
    else:
        print("❌ Algunos servicios no están disponibles.")
        print("\n🔧 Soluciones:")
        print("1. Ejecutar: docker-compose up -d")
        print("2. Verificar logs: docker-compose logs")
        print("3. Reiniciar servicios: docker-compose restart")
        return 1

if __name__ == "__main__":
    sys.exit(main())
