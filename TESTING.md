# 🧪 Sistema de Testing - AI Models Pro Generator

Este documento describe el sistema de testing automatizado implementado para el proyecto AI Models Pro Generator.

## 📋 Índice

- [Visión General](#visión-general)
- [Instalación](#instalación)
- [Ejecución de Pruebas](#ejecución-de-pruebas)
- [Estructura de Testing](#estructura-de-testing)
- [Reportes y Cobertura](#reportes-y-cobertura)
- [Configuración Avanzada](#configuración-avanzada)
- [Desarrollo de Nuevas Pruebas](#desarrollo-de-nuevas-pruebas)

## 🎯 Visión General

El sistema de testing está construido con **pytest** y proporciona:

- ✅ **40 pruebas automatizadas** cubriendo todos los componentes críticos
- 📊 **Análisis de cobertura** con reportes HTML y terminal
- 🔧 **Mocks y fixtures** para pruebas aisladas y confiables
- 📱 **Múltiples formas de ejecución** (Python, batch, Makefile)
- 🚀 **Integración continua** preparada para CI/CD

### Componentes Probados

| Componente | Archivo de Pruebas | Cobertura | Descripción |
|------------|-------------------|-----------|-------------|
| **Sistema de Historial** | `test_historial.py` | 96% | Carga, guardado, filtrado y validación |
| **Cálculos de Costo** | `test_cost_calculation.py` | 96% | Costos por modelo, conversiones, validaciones |
| **Integración Replicate** | `test_replicate_integration.py` | 88% | API, generación, manejo de errores |
| **Utilidades** | `test_utils.py` | 94% | Archivos, configuración, helpers |

## 🚀 Instalación

### Instalación Automática

Para instalar todas las dependencias de testing automáticamente:

```bash
# Windows (Batch)
run_tests.bat install

# Windows (PowerShell) o Linux/Mac
python run_tests.py install

# Usando Makefile
make dev
```

### Instalación Manual

```bash
pip install pytest>=7.4.0 pytest-mock>=3.11.0 pytest-cov>=4.1.0 pytest-html>=3.2.0
```

## 🧪 Ejecución de Pruebas

### Métodos de Ejecución

#### 1. Script Python (Multiplataforma)
```bash
# Todas las pruebas
python run_tests.py

# Solo pruebas unitarias
python run_tests.py unit

# Con análisis de cobertura
python run_tests.py coverage

# Solo generar reporte HTML
python run_tests.py report
```

#### 2. Script Batch (Windows)
```batch
# Todas las pruebas
run_tests.bat

# Pruebas específicas
run_tests.bat unit
run_tests.bat coverage
run_tests.bat quick
```

#### 3. Makefile (Linux/Mac/Windows con make)
```bash
# Pruebas básicas
make test

# Solo unitarias
make test-unit

# Con cobertura
make test-coverage

# Reporte HTML
make test-report

# Verificación completa
make check
```

#### 4. Pytest Directo
```bash
# Básico
pytest tests/

# Con cobertura
pytest tests/ --cov=. --cov-report=html

# Solo un archivo
pytest tests/test_historial.py -v

# Solo una prueba específica
pytest tests/test_cost_calculation.py::TestCostCalculation::test_calculate_flux_pro_cost
```

### Comandos Rápidos

```bash
# Pruebas rápidas (para en el primer fallo)
pytest tests/ -x

# Pruebas paralelas (si tienes pytest-xdist)
pytest tests/ -n auto

# Modo verboso con traceback corto
pytest tests/ -v --tb=short

# Solo pruebas que contengan "cost" en el nombre
pytest tests/ -k "cost"
```

## 📁 Estructura de Testing

```
tests/
├── __init__.py                     # Marcador de paquete
├── conftest.py                     # Fixtures globales y configuración
├── pytest.ini                     # Configuración de pytest
├── test_cost_calculation.py        # Pruebas de cálculos de costo
├── test_historial.py              # Pruebas del sistema de historial
├── test_replicate_integration.py  # Pruebas de integración con Replicate
└── test_utils.py                  # Pruebas de funciones utilitarias
```

### Fixtures Disponibles

```python
# En conftest.py
@pytest.fixture
def temp_dir():          # Directorio temporal para pruebas
def sample_history():    # Datos de historial de prueba
def mock_replicate():    # Mock del cliente de Replicate
def test_config():       # Configuración de prueba
def cleanup_files():     # Limpieza automática de archivos
```

## 📊 Reportes y Cobertura

### Reportes Generados

1. **Reporte HTML de Pruebas**: `test_report.html`
   - Estado de cada prueba
   - Tiempos de ejecución
   - Logs y capturas de errores

2. **Reporte de Cobertura HTML**: `htmlcov/index.html`
   - Cobertura por archivo
   - Líneas cubiertas/no cubiertas
   - Análisis detallado

3. **Reporte de Terminal**: Salida directa en consola

### Visualización de Reportes

```bash
# Abrir reporte de pruebas
start test_report.html        # Windows
open test_report.html         # Mac
xdg-open test_report.html     # Linux

# Abrir reporte de cobertura
start htmlcov/index.html      # Windows
open htmlcov/index.html       # Mac
xdg-open htmlcov/index.html   # Linux
```

## ⚙️ Configuración Avanzada

### pytest.ini

El archivo `pytest.ini` contiene configuraciones como:

```ini
[tool:pytest]
testpaths = tests
addopts = 
    --verbose
    --tb=short
    --cov=.
    --cov-report=html:htmlcov
    --cov-report=term-missing
    --maxfail=3
    --durations=10
filterwarnings =
    ignore::DeprecationWarning
markers =
    unit: pruebas unitarias
    integration: pruebas de integración
    slow: pruebas lentas
    api: pruebas que requieren API
```

### Marcadores de Pruebas

```bash
# Solo pruebas unitarias
pytest -m unit

# Solo pruebas de integración
pytest -m integration

# Excluir pruebas lentas
pytest -m "not slow"

# Solo pruebas de API
pytest -m api
```

### Variables de Entorno

```bash
# Configurar para testing
export TESTING=true
export REPLICATE_API_TOKEN=test_token

# Ejecutar con configuración específica
PYTEST_CURRENT_TEST=true pytest tests/
```

## 🔧 Desarrollo de Nuevas Pruebas

### Estructura de una Prueba

```python
import pytest
from unittest.mock import Mock, patch

class TestNuevoComponente:
    """Pruebas para nuevo componente"""
    
    def test_funcionalidad_basica(self, temp_dir):
        """Probar funcionalidad básica"""
        # Arrange
        input_data = "test_input"
        expected = "expected_output"
        
        # Act
        result = nueva_funcion(input_data)
        
        # Assert
        assert result == expected
    
    @pytest.mark.api
    def test_integracion_api(self, mock_replicate):
        """Probar integración con API externa"""
        # Configurar mock
        mock_replicate.run.return_value = {"status": "success"}
        
        # Ejecutar
        result = funcion_que_usa_api()
        
        # Verificar
        assert result["status"] == "success"
        mock_replicate.run.assert_called_once()
    
    @pytest.mark.slow
    def test_operacion_lenta(self):
        """Probar operación que tarda tiempo"""
        # Esta prueba se puede saltar con -m "not slow"
        result = operacion_lenta()
        assert result is not None
```

### Mejores Prácticas

1. **Nombres Descriptivos**: `test_calculate_cost_for_flux_pro_model`
2. **AAA Pattern**: Arrange, Act, Assert
3. **Un Assert por Prueba**: Enfoque en una sola verificación
4. **Mocks para Dependencias**: Aislar la funcionalidad bajo prueba
5. **Datos de Prueba Realistas**: Usar fixtures con datos representativos

### Agregar Nueva Fixture

```python
# En conftest.py
@pytest.fixture
def mi_nueva_fixture():
    """Descripción de la fixture"""
    # Configuración
    data = setup_test_data()
    yield data
    # Limpieza (opcional)
    cleanup_test_data(data)
```

## 🐛 Depuración de Pruebas

### Debugging con Pytest

```bash
# Ejecutar con pdb
pytest tests/test_archivo.py --pdb

# Mostrar prints
pytest tests/ -s

# Capturar solo las pruebas que fallan
pytest tests/ --tb=long --capture=no

# Ejecutar prueba específica con máximo detalle
pytest tests/test_archivo.py::test_funcion -v -s --tb=long
```

### Logging en Pruebas

```python
import logging

def test_con_logging(caplog):
    """Prueba que captura logs"""
    with caplog.at_level(logging.INFO):
        funcion_que_genera_logs()
    
    assert "mensaje esperado" in caplog.text
```

## 🚨 Solución de Problemas

### Problemas Comunes

1. **ImportError**: Verificar que pytest esté instalado en el entorno correcto
2. **Fallos de Mock**: Asegurarse de que los mocks coincidan con la API real
3. **Archivos Temporales**: Usar fixtures de limpieza para evitar conflictos
4. **Dependencias Faltantes**: Ejecutar `pip install -r requirements.txt`

### Verificación de Salud

```bash
# Verificar instalación
python -c "import pytest; print(pytest.__version__)"

# Verificar configuración
pytest --collect-only

# Ejecutar una prueba simple
pytest tests/test_utils.py::TestUtilityFunctions::test_format_file_size -v
```

## 📈 Métricas de Calidad

### Objetivos de Cobertura

- **Objetivo mínimo**: 80% de cobertura de código
- **Objetivo ideal**: 90%+ en componentes críticos
- **Archivos críticos**: `app.py`, módulos de cálculo de costos

### Monitoreo Continuo

```bash
# Ejecutar y generar badge de cobertura
pytest tests/ --cov=. --cov-fail-under=80

# Reporte de cobertura en formato XML (para CI)
pytest tests/ --cov=. --cov-report=xml
```

## 🔄 Integración Continua

### GitHub Actions Example

```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.10
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pytest pytest-cov
    - name: Run tests
      run: pytest tests/ --cov=. --cov-report=xml
    - name: Upload coverage
      uses: codecov/codecov-action@v1
```

---

## 🎉 Conclusión

El sistema de testing proporciona una base sólida para mantener la calidad del código y detectar regresiones tempranamente. Con **40 pruebas automatizadas** y múltiples opciones de ejecución, garantiza que el proyecto mantenga su robustez a medida que evoluciona.

**¿Preguntas o problemas?** Consulta la documentación de [pytest](https://docs.pytest.org/) o revisa los logs de las pruebas para más detalles.

---
*Última actualización: Diciembre 2024*
