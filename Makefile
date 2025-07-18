# Makefile para AI Models Pro Generator
# Automatiza tareas comunes de desarrollo y testing

.PHONY: help install test test-unit test-coverage test-report clean setup dev lint format check

# Variables
PYTHON = python
PIP = pip
PYTEST = python -m pytest
TEST_DIR = tests
SRC_DIR = .
VENV_DIR = venv

# Colores para output
RED = \033[31m
GREEN = \033[32m
YELLOW = \033[33m
BLUE = \033[34m
RESET = \033[0m

# Ayuda por defecto
help:
	@echo "$(BLUE)AI Models Pro Generator - Comandos Disponibles$(RESET)"
	@echo "=================================================="
	@echo ""
	@echo "$(GREEN)Configuración:$(RESET)"
	@echo "  make setup          - Configuración inicial del proyecto"
	@echo "  make install        - Instalar todas las dependencias"
	@echo "  make dev            - Instalar dependencias de desarrollo"
	@echo ""
	@echo "$(GREEN)Testing:$(RESET)"
	@echo "  make test           - Ejecutar todas las pruebas"
	@echo "  make test-unit      - Ejecutar solo pruebas unitarias"
	@echo "  make test-coverage  - Ejecutar pruebas con cobertura"
	@echo "  make test-report    - Generar reporte HTML de pruebas"
	@echo ""
	@echo "$(GREEN)Calidad de Código:$(RESET)"
	@echo "  make lint           - Análisis de código con flake8"
	@echo "  make format         - Formatear código con black"
	@echo "  make check          - Verificación completa (lint + tests)"
	@echo ""
	@echo "$(GREEN)Utilidades:$(RESET)"
	@echo "  make clean          - Limpiar archivos temporales"
	@echo "  make run            - Ejecutar la aplicación Streamlit"
	@echo ""
	@echo "$(YELLOW)Ejemplo: make test-coverage$(RESET)"

# Configuración inicial
setup:
	@echo "$(BLUE)🔧 Configuración inicial del proyecto$(RESET)"
	@echo "======================================"
	@$(PYTHON) -m venv $(VENV_DIR) || echo "$(YELLOW)Virtual environment ya existe$(RESET)"
	@echo "$(GREEN)✅ Entorno virtual configurado$(RESET)"
	@echo "$(YELLOW)💡 Activar con: $(VENV_DIR)\Scripts\activate (Windows) o source $(VENV_DIR)/bin/activate (Linux/Mac)$(RESET)"

# Instalar dependencias principales
install:
	@echo "$(BLUE)📦 Instalando dependencias principales$(RESET)"
	@$(PIP) install -r requirements.txt
	@echo "$(GREEN)✅ Dependencias principales instaladas$(RESET)"

# Instalar dependencias de desarrollo
dev:
	@echo "$(BLUE)🛠️ Instalando dependencias de desarrollo$(RESET)"
	@$(PIP) install pytest>=7.4.0 pytest-mock>=3.11.0 pytest-cov>=4.1.0 pytest-html>=3.2.0
	@$(PIP) install black flake8 isort
	@echo "$(GREEN)✅ Dependencias de desarrollo instaladas$(RESET)"

# Ejecutar todas las pruebas
test:
	@echo "$(BLUE)🧪 Ejecutando todas las pruebas$(RESET)"
	@$(PYTEST) $(TEST_DIR) -v --tb=short --cov=$(SRC_DIR) --cov-report=html --cov-report=term-missing --cov-exclude=tests/*
	@echo "$(GREEN)✅ Pruebas completadas$(RESET)"
	@echo "$(YELLOW)📊 Reporte de cobertura: htmlcov/index.html$(RESET)"

# Ejecutar solo pruebas unitarias
test-unit:
	@echo "$(BLUE)🧪 Ejecutando pruebas unitarias$(RESET)"
	@$(PYTEST) $(TEST_DIR) -v --tb=short
	@echo "$(GREEN)✅ Pruebas unitarias completadas$(RESET)"

# Ejecutar pruebas con cobertura detallada
test-coverage:
	@echo "$(BLUE)📊 Ejecutando pruebas con análisis de cobertura$(RESET)"
	@$(PYTEST) $(TEST_DIR) --cov=$(SRC_DIR) --cov-report=html --cov-report=term-missing --cov-exclude=tests/* --cov-exclude=venv/* --cov-exclude=run_tests.py
	@echo "$(GREEN)✅ Análisis de cobertura completado$(RESET)"
	@echo "$(YELLOW)📊 Reporte HTML: htmlcov/index.html$(RESET)"

# Generar reporte HTML de pruebas
test-report:
	@echo "$(BLUE)📋 Generando reporte HTML de pruebas$(RESET)"
	@$(PYTEST) $(TEST_DIR) --html=test_report.html --self-contained-html
	@echo "$(GREEN)✅ Reporte HTML generado$(RESET)"
	@echo "$(YELLOW)📋 Reporte: test_report.html$(RESET)"

# Análisis de código
lint:
	@echo "$(BLUE)🔍 Ejecutando análisis de código$(RESET)"
	@flake8 $(SRC_DIR) --exclude=venv,htmlcov,tests/__pycache__ --max-line-length=88 --ignore=E203,W503
	@echo "$(GREEN)✅ Análisis de código completado$(RESET)"

# Formatear código
format:
	@echo "$(BLUE)🎨 Formateando código$(RESET)"
	@black $(SRC_DIR) --exclude="/(venv|htmlcov|\.git)/"
	@isort $(SRC_DIR) --skip=venv --skip=htmlcov
	@echo "$(GREEN)✅ Código formateado$(RESET)"

# Verificación completa
check: lint test
	@echo "$(GREEN)✅ Verificación completa finalizada$(RESET)"

# Limpiar archivos temporales
clean:
	@echo "$(BLUE)🧹 Limpiando archivos temporales$(RESET)"
	@rm -rf __pycache__ .pytest_cache htmlcov test_report.html .coverage
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@echo "$(GREEN)✅ Limpieza completada$(RESET)"

# Ejecutar aplicación
run:
	@echo "$(BLUE)🚀 Ejecutando aplicación Streamlit$(RESET)"
	@streamlit run app.py

# Comandos de testing rápido para desarrollo
test-quick:
	@echo "$(BLUE)⚡ Pruebas rápidas (sin cobertura)$(RESET)"
	@$(PYTEST) $(TEST_DIR) -x --tb=short
	@echo "$(GREEN)✅ Pruebas rápidas completadas$(RESET)"

# Instalar todo (dependencias + desarrollo)
install-all: install dev
	@echo "$(GREEN)✅ Todas las dependencias instaladas$(RESET)"

# Verificar que todo esté funcionando
health-check:
	@echo "$(BLUE)🏥 Verificación de salud del proyecto$(RESET)"
	@echo "======================================="
	@echo "$(YELLOW)Verificando Python...$(RESET)"
	@$(PYTHON) --version
	@echo "$(YELLOW)Verificando pip...$(RESET)"
	@$(PIP) --version
	@echo "$(YELLOW)Verificando dependencias principales...$(RESET)"
	@$(PIP) list | grep -E "(streamlit|replicate|requests)" || echo "$(RED)⚠️ Faltan dependencias principales$(RESET)"
	@echo "$(YELLOW)Verificando dependencias de testing...$(RESET)"
	@$(PIP) list | grep pytest || echo "$(RED)⚠️ Faltan dependencias de testing$(RESET)"
	@echo "$(GREEN)✅ Verificación de salud completada$(RESET)"
