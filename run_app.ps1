# Script para ejecutar Flux Pro Generator
Write-Host "🚀 Iniciando Flux Pro Generator..." -ForegroundColor Green
Write-Host ""

# Verificar entorno virtual
if (!(Test-Path "venv\Scripts\Activate.ps1")) {
    Write-Host "❌ Error: Entorno virtual no encontrado" -ForegroundColor Red
    Write-Host "📝 Por favor ejecuta: python -m venv venv" -ForegroundColor Yellow
    Read-Host "Presiona Enter para continuar"
    exit 1
}

Write-Host "✅ Usando entorno virtual..." -ForegroundColor Green

Write-Host "📦 Verificando dependencias..." -ForegroundColor Blue
& ".\venv\Scripts\python.exe" -m pip install -q -r requirements.txt

Write-Host "🌐 Abriendo aplicación web..." -ForegroundColor Magenta
Write-Host ""
Write-Host "🎯 La aplicación se abrirá en tu navegador" -ForegroundColor Cyan
Write-Host "🔗 URL local: http://localhost:8501" -ForegroundColor Cyan
Write-Host ""
Write-Host "⏹️  Para detener la aplicación presiona Ctrl+C" -ForegroundColor Yellow
Write-Host ""

& ".\venv\Scripts\python.exe" -m streamlit run app.py --server.headless true --browser.gatherUsageStats false
