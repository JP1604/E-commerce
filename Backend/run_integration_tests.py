#!/usr/bin/env python3
"""
Script para ejecutar todas las pruebas de integración del sistema de e-commerce.

Este script:
1. Instala las dependencias necesarias
2. Ejecuta todas las pruebas de integración
3. Genera reportes de cobertura
4. Muestra un resumen de resultados

Uso:
    python run_integration_tests.py
    python run_integration_tests.py --verbose
    python run_integration_tests.py --coverage
"""

import subprocess
import sys
import os
import argparse
from pathlib import Path


def run_command(command, description, verbose=False):
    """Ejecuta un comando y muestra el resultado."""
    if verbose:
        print(f"\n🔧 {description}")
        print(f"Comando: {command}")
    
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent
        )
        
        if result.returncode == 0:
            print(f"✅ {description} - ÉXITO")
            if verbose and result.stdout:
                print(result.stdout)
        else:
            print(f"❌ {description} - ERROR")
            print(f"Error: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ {description} - EXCEPCIÓN: {e}")
        return False
    
    return True


def main():
    """Función principal del script."""
    parser = argparse.ArgumentParser(description="Ejecutar pruebas de integración del e-commerce")
    parser.add_argument("--verbose", "-v", action="store_true", help="Mostrar salida detallada")
    parser.add_argument("--coverage", "-c", action="store_true", help="Generar reporte de cobertura")
    parser.add_argument("--service", "-s", help="Ejecutar pruebas solo para un servicio específico")
    
    args = parser.parse_args()
    
    print("🧪 Iniciando Pruebas de Integración - E-commerce Microservices")
    print("=" * 70)
    
    # Verificar que estamos en el directorio correcto
    if not Path("Backend").exists():
        print("❌ Error: Este script debe ejecutarse desde la raíz del proyecto")
        sys.exit(1)
    
    # Cambiar al directorio Backend
    os.chdir("Backend")
    
    # 1. Instalar dependencias de desarrollo
    print("\n📦 Instalando dependencias...")
    if not run_command("pip install -e .[dev]", "Instalación de dependencias", args.verbose):
        print("❌ Error al instalar dependencias")
        sys.exit(1)
    
    # 2. Verificar que pytest está instalado
    if not run_command("pytest --version", "Verificación de pytest", args.verbose):
        print("❌ Error: pytest no está instalado correctamente")
        sys.exit(1)
    
    # 3. Ejecutar pruebas de integración
    print("\n🧪 Ejecutando pruebas de integración...")
    
    # Construir comando pytest
    pytest_cmd = "pytest tests/integration/"
    
    if args.service:
        pytest_cmd += f"test_{args.service}_service.py"
        print(f"🎯 Ejecutando pruebas solo para: {args.service}")
    
    if args.verbose:
        pytest_cmd += " -v"
    
    if args.coverage:
        pytest_cmd += " --cov=src --cov-report=html --cov-report=term-missing"
        print("📊 Generando reporte de cobertura...")
    
    # Ejecutar las pruebas
    if not run_command(pytest_cmd, "Ejecución de pruebas de integración", args.verbose):
        print("❌ Algunas pruebas fallaron")
        sys.exit(1)
    
    # 4. Mostrar resumen
    print("\n" + "=" * 70)
    print("📋 RESUMEN DE PRUEBAS DE INTEGRACIÓN")
    print("=" * 70)
    
    services = [
        "product_service",
        "user_service", 
        "cart_service",
        "order_service",
        "payment_service",
        "delivery_service"
    ]
    
    print("\n✅ Servicios probados:")
    for service in services:
        if not args.service or args.service == service.replace("_service", ""):
            print(f"   • {service.replace('_', ' ').title()}")
    
    print("\n🔍 Tipos de pruebas ejecutadas:")
    print("   • Creación de entidades en base de datos")
    print("   • Recuperación de entidades por ID")
    print("   • Listado de entidades")
    print("   • Actualización de entidades")
    print("   • Eliminación de entidades")
    print("   • Validación de enums y estados")
    print("   • Pruebas de restricciones de base de datos")
    print("   • Pruebas de precisión de datos")
    print("   • Pruebas de relaciones entre entidades")
    
    if args.coverage:
        print(f"\n📊 Reporte de cobertura generado en: Backend/htmlcov/index.html")
    
    print("\n🎉 ¡Todas las pruebas de integración completadas exitosamente!")
    print("\n💡 Próximos pasos:")
    print("   • Revisar el reporte de cobertura (si se generó)")
    print("   • Ejecutar las pruebas en el pipeline de CI/CD")
    print("   • Considerar agregar pruebas de carga")
    print("   • Implementar pruebas de integración end-to-end")


if __name__ == "__main__":
    main()
