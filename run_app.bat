@echo off
echo 🚀 Iniciando Flux Pro Generator...
echo.
echo 📋 Verificando entorno virtual...

if not exist "venv\Scripts\python.exe" (
    echo ❌ Error: Entorno virtual no encontrado
    echo � Creando entorno virtual...
    python -m venv venv
    if errorlevel 1 (
        echo ❌ Error al crear entorno virtual
        echo 📝 Por favor instala Python primero
        pause
        exit /b 1
    )
    echo ✅ Entorno virtual creado
)

echo ✅ Activando entorno virtual...
call venv\Scripts\activate.bat

echo 📦 Instalando/actualizando dependencias...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

echo 🔧 Verificando configuración...
if not exist "config.py" (
    echo ⚠️  Archivo config.py no encontrado
    echo 📝 Copiando plantilla de configuración...
    copy config.example.py config.py
    echo.
    echo ❗ IMPORTANTE: Edita config.py y configura tu token de Replicate
    echo 🔗 Obtén tu token en: https://replicate.com/account/api-tokens
    echo.
    pause
)

echo 🌐 Iniciando aplicación web...
echo.
echo 🎯 La aplicación se abrirá en tu navegador
echo 🔗 URL local: http://localhost:8501
echo.
echo ⏹️  Para detener la aplicación presiona Ctrl+C
echo.
python -m streamlit run app.py --server.headless true --browser.gatherUsageStats false
