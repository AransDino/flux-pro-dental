#!/usr/bin/env python3
"""
Script para ejecutar las pruebas del proyecto de manera automática
"""
import subprocess
import sys
import os
from pathlib import Path


def run_command(command, description):
    """Ejecutar comando y mostrar resultado"""
    print(f"\n🔧 {description}")
    print("=" * 50)
    
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent
        )
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error ejecutando: {command}")
        print(f"Código de salida: {e.returncode}")
        print(f"STDOUT: {e.stdout}")
        print(f"STDERR: {e.stderr}")
        return False


def check_pytest_installation():
    """Verificar si pytest está instalado"""
    try:
        import pytest
        print(f"✅ pytest está instalado (versión: {pytest.__version__})")
        return True
    except ImportError:
        print("❌ pytest no está instalado")
        return False


def install_test_dependencies():
    """Instalar dependencias de testing"""
    print("📦 Instalando dependencias de testing...")
    
    dependencies = [
        "pytest>=7.4.0",
        "pytest-mock>=3.11.0",
        "pytest-cov>=4.1.0",
        "pytest-html>=3.2.0"
    ]
    
    for dep in dependencies:
        success = run_command(
            f"pip install {dep}",
            f"Instalando {dep}"
        )
        if not success:
            return False
    
    return True


def run_tests(test_type="all"):
    """Ejecutar diferentes tipos de pruebas"""
    
    if test_type == "all" or test_type == "unit":
        print("\n🧪 Ejecutando pruebas unitarias...")
        success = run_command(
            "python -m pytest tests/ -v --tb=short",
            "Pruebas unitarias básicas"
        )
        if not success:
            return False
    
    if test_type == "all" or test_type == "coverage":
        print("\n📊 Ejecutando pruebas con cobertura...")
        success = run_command(
            "python -m pytest tests/ --cov=. --cov-report=html --cov-report=term-missing --cov-exclude=tests/*",
            "Pruebas con análisis de cobertura"
        )
        if not success:
            return False
    
    if test_type == "all" or test_type == "report":
        print("\n📋 Generando reporte HTML...")
        success = run_command(
            "python -m pytest tests/ --html=test_report.html --self-contained-html",
            "Generación de reporte HTML"
        )
        if not success:
            return False
    
    return True


def main():
    """Función principal"""
    print("🚀 Sistema de Testing para AI Models Pro Generator")
    print("=" * 60)
    
    # Verificar si estamos en el directorio correcto
    if not Path("app.py").exists():
        print("❌ Error: Ejecutar desde el directorio raíz del proyecto")
        sys.exit(1)
    
    # Verificar instalación de pytest
    if not check_pytest_installation():
        print("📦 Instalando pytest...")
        if not install_test_dependencies():
            print("❌ Error al instalar dependencias de testing")
            sys.exit(1)
    
    # Determinar tipo de prueba
    test_type = "all"
    if len(sys.argv) > 1:
        test_type = sys.argv[1].lower()
        if test_type not in ["all", "unit", "coverage", "report"]:
            print("❌ Tipo de prueba inválido. Usar: all, unit, coverage, report")
            sys.exit(1)
    
    # Ejecutar pruebas
    print(f"\n🎯 Ejecutando pruebas tipo: {test_type}")
    
    if run_tests(test_type):
        print("\n✅ ¡Todas las pruebas completadas exitosamente!")
        
        # Mostrar ubicación de reportes
        if test_type in ["all", "coverage"]:
            print("📊 Reporte de cobertura: htmlcov/index.html")
        if test_type in ["all", "report"]:
            print("📋 Reporte de pruebas: test_report.html")
        
    else:
        print("\n❌ Algunas pruebas fallaron")
        sys.exit(1)


if __name__ == "__main__":
    main()
