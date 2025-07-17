@echo off
echo 🚀 Iniciando Flux Pro Generator...
echo.
echo 📋 Verificando entorno virtual...

if not exist "venv\Scripts\python.exe" (
    echo ❌ Error: Entorno virtual no encontrado
    echo 📝 Por favor ejecuta: python -m venv venv
    pause
    exit /b 1
)

echo ✅ Usando entorno virtual...

echo 📦 Verificando dependencias...
venv\Scripts\python.exe -m pip install -q -r requirements.txt

echo 🌐 Abriendo aplicación web...
echo.
echo 🎯 La aplicación se abrirá en tu navegador
echo 🔗 URL local: http://localhost:8501
echo.
echo ⏹️  Para detener la aplicación presiona Ctrl+C
echo.
venv\Scripts\python.exe -m streamlit run app.py --server.headless true --browser.gatherUsageStats false
