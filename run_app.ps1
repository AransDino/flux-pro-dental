# Flux Pro Generator - PowerShell Launcher
# ========================================

Write-Host "🚀 Iniciando Flux Pro Generator..." -ForegroundColor Green
Write-Host ""

# Verificar Python
Write-Host "🐍 Verificando Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python encontrado: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Error: Python no encontrado" -ForegroundColor Red
    Write-Host "📝 Por favor instala Python desde: https://www.python.org/downloads/" -ForegroundColor Cyan
    Read-Host "Presiona Enter para salir"
    exit 1
}

# Verificar/crear entorno virtual
Write-Host "� Verificando entorno virtual..." -ForegroundColor Yellow
if (!(Test-Path "venv\Scripts\python.exe")) {
    Write-Host "🔧 Creando entorno virtual..." -ForegroundColor Cyan
    python -m venv venv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Error al crear entorno virtual" -ForegroundColor Red
        Read-Host "Presiona Enter para salir"
        exit 1
    }
    Write-Host "✅ Entorno virtual creado" -ForegroundColor Green
}

# Activar entorno virtual
Write-Host "✅ Activando entorno virtual..." -ForegroundColor Green
& ".\venv\Scripts\Activate.ps1"

# Actualizar pip e instalar dependencias
Write-Host "📦 Instalando/actualizando dependencias..." -ForegroundColor Yellow
& ".\venv\Scripts\python.exe" -m pip install --upgrade pip --quiet
& ".\venv\Scripts\python.exe" -m pip install -r requirements.txt --quiet

# Verificar configuración
Write-Host "🔧 Verificando configuración..." -ForegroundColor Yellow
if (!(Test-Path "config.py")) {
    Write-Host "⚠️  Archivo config.py no encontrado" -ForegroundColor Yellow
    Write-Host "📝 Copiando plantilla de configuración..." -ForegroundColor Cyan
    Copy-Item "config.example.py" "config.py"
    Write-Host ""
    Write-Host "❗ IMPORTANTE: Edita config.py y configura tu token de Replicate" -ForegroundColor Red
    Write-Host "🔗 Obtén tu token en: https://replicate.com/account/api-tokens" -ForegroundColor Cyan
    Write-Host ""
    Read-Host "Presiona Enter para continuar"
}

# Iniciar aplicación
Write-Host "🌐 Iniciando aplicación web..." -ForegroundColor Green
Write-Host ""
Write-Host "🎯 La aplicación se abrirá en tu navegador" -ForegroundColor Cyan
Write-Host "🔗 URL local: http://localhost:8501" -ForegroundColor Cyan
Write-Host ""
Write-Host "⏹️  Para detener la aplicación presiona Ctrl+C" -ForegroundColor Yellow
Write-Host ""

& ".\venv\Scripts\python.exe" -m streamlit run app.py --server.headless true --browser.gatherUsageStats false
