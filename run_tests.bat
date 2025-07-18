@echo off
REM Script para ejecutar las pruebas en Windows
REM Parte del sistema de testing para AI Models Pro Generator

setlocal enabledelayedexpansion

echo.
echo ======================================================
echo   🚀 AI Models Pro Generator - Sistema de Testing
echo ======================================================
echo.

REM Verificar si estamos en el directorio correcto
if not exist app.py (
    echo ❌ Error: Ejecutar desde el directorio raiz del proyecto
    echo    Debe existir el archivo app.py
    pause
    exit /b 1
)

REM Función para mostrar ayuda
if "%1"=="help" (
    echo Uso: run_tests.bat [tipo_de_prueba]
    echo.
    echo Tipos de prueba disponibles:
    echo   all        - Ejecutar todas las pruebas ^(por defecto^)
    echo   unit       - Solo pruebas unitarias
    echo   coverage   - Pruebas con análisis de cobertura
    echo   report     - Generar reporte HTML
    echo   install    - Solo instalar dependencias
    echo   quick      - Pruebas rápidas sin cobertura
    echo   help       - Mostrar esta ayuda
    echo.
    echo Ejemplos:
    echo   run_tests.bat
    echo   run_tests.bat coverage
    echo   run_tests.bat unit
    pause
    exit /b 0
)

set TEST_TYPE=all
if not "%1"=="" set TEST_TYPE=%1

echo 🎯 Tipo de prueba: %TEST_TYPE%
echo.

REM Verificar si pytest está instalado
python -c "import pytest" 2>nul
if errorlevel 1 (
    echo 📦 pytest no está instalado. Instalando dependencias...
    goto :install_deps
) else (
    echo ✅ pytest está disponible
)

REM Saltar instalación si ya está disponible
goto :run_tests

:install_deps
echo 📦 Instalando dependencias de testing...
echo =====================================

REM Instalar pytest y dependencias
echo Instalando pytest...
pip install pytest>=7.4.0
if errorlevel 1 (
    echo ❌ Error instalando pytest
    pause
    exit /b 1
)

echo Instalando pytest-mock...
pip install pytest-mock>=3.11.0
if errorlevel 1 (
    echo ❌ Error instalando pytest-mock
    pause
    exit /b 1
)

echo Instalando pytest-cov...
pip install pytest-cov>=4.1.0
if errorlevel 1 (
    echo ❌ Error instalando pytest-cov
    pause
    exit /b 1
)

echo Instalando pytest-html...
pip install pytest-html>=3.2.0
if errorlevel 1 (
    echo ❌ Error instalando pytest-html
    pause
    exit /b 1
)

echo ✅ Dependencias instaladas correctamente
echo.

if "%TEST_TYPE%"=="install" (
    echo 🎉 Instalación completada
    pause
    exit /b 0
)

:run_tests
echo 🧪 Ejecutando pruebas tipo: %TEST_TYPE%
echo =====================================

if "%TEST_TYPE%"=="unit" (
    echo Ejecutando pruebas unitarias...
    python -m pytest tests/ -v --tb=short
    goto :check_result
)

if "%TEST_TYPE%"=="coverage" (
    echo Ejecutando pruebas con cobertura...
    python -m pytest tests/ --cov=. --cov-report=html --cov-report=term-missing
    goto :show_coverage_info
)

if "%TEST_TYPE%"=="report" (
    echo Generando reporte HTML...
    python -m pytest tests/ --html=test_report.html --self-contained-html
    goto :show_report_info
)

if "%TEST_TYPE%"=="quick" (
    echo Ejecutando pruebas rápidas...
    python -m pytest tests/ -x --tb=short
    goto :check_result
)

if "%TEST_TYPE%"=="all" (
    echo Ejecutando todas las pruebas...
    python -m pytest tests/ -v --tb=short --cov=. --cov-report=html --cov-report=term-missing --html=test_report.html --self-contained-html
    goto :show_all_info
)

echo ❌ Tipo de prueba desconocido: %TEST_TYPE%
echo Use 'run_tests.bat help' para ver opciones disponibles
pause
exit /b 1

:check_result
if errorlevel 1 (
    echo.
    echo ❌ Algunas pruebas fallaron
    pause
    exit /b 1
) else (
    echo.
    echo ✅ ¡Todas las pruebas pasaron correctamente!
)
goto :end

:show_coverage_info
if errorlevel 1 (
    echo.
    echo ❌ Algunas pruebas fallaron
    pause
    exit /b 1
) else (
    echo.
    echo ✅ ¡Pruebas completadas!
    echo 📊 Reporte de cobertura generado: htmlcov\index.html
)
goto :end

:show_report_info
if errorlevel 1 (
    echo.
    echo ❌ Error generando el reporte
    pause
    exit /b 1
) else (
    echo.
    echo ✅ ¡Reporte generado!
    echo 📋 Reporte HTML: test_report.html
)
goto :end

:show_all_info
if errorlevel 1 (
    echo.
    echo ❌ Algunas pruebas fallaron
    pause
    exit /b 1
) else (
    echo.
    echo ✅ ¡Todas las pruebas completadas exitosamente!
    echo.
    echo 📊 Reportes generados:
    echo    • Cobertura: htmlcov\index.html
    echo    • Pruebas: test_report.html
)
goto :end

:end
echo.
echo 🎉 Proceso completado
echo ======================================================
pause
