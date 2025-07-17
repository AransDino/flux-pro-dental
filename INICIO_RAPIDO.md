# 🚀 Guía de Inicio Rápido

## 📋 Formas de ejecutar la aplicación

### **Opción 1: PowerShell (Recomendado para Windows)**
```powershell
# Desde PowerShell
.\run_app.ps1
```

### **Opción 2: Command Prompt (CMD)**
```bash
# Desde CMD
run_app.bat
```

### **Opción 3: Doble clic**
- Hacer doble clic en `run_app.bat` desde el explorador de archivos

## 🔧 ¿Qué hacen los scripts automáticamente?

1. **Verifican Python** - Si no está instalado, te avisan
2. **Crean el entorno virtual** - Si no existe, lo crean automáticamente
3. **Activan el entorno virtual** - Para usar las dependencias correctas
4. **Instalan dependencias** - Desde `requirements.txt`
5. **Verifican configuración** - Si no existe `config.py`, copian la plantilla
6. **Inician Streamlit** - Abren la aplicación en el navegador

## ⚠️ Primera ejecución

### Si es la primera vez:
1. El script creará automáticamente el entorno virtual
2. Te copiará `config.example.py` como `config.py`
3. **IMPORTANTE**: Edita `config.py` y añade tu token de Replicate:

```python
# En config.py
REPLICATE_API_TOKEN = "tu_token_real_aqui"
```

4. Obtén tu token en: https://replicate.com/account/api-tokens

## 🌐 Acceso a la aplicación

Una vez iniciada:
- **URL local**: http://localhost:8501
- Se abrirá automáticamente en tu navegador
- Para detener: **Ctrl+C** en la terminal

## 🐛 Solución de problemas

### Error: "No se reconoce el comando"
```powershell
# En lugar de:
run_app.bat

# Usa:
.\run_app.bat
```

### Error: "No se puede ejecutar scripts"
```powershell
# Habilitar ejecución de scripts en PowerShell:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Error: "Python no encontrado"
1. Instala Python desde: https://www.python.org/downloads/
2. Asegúrate de marcar "Add Python to PATH" durante la instalación

### Error: "Token no configurado"
1. Edita `config.py`
2. Reemplaza `"tu_token_aqui"` con tu token real de Replicate
3. Reinicia la aplicación

## 📁 Estructura después del primer inicio

```
flux-pro/
├── venv/              # Entorno virtual (creado automáticamente)
├── config.py          # Tu configuración (creado automáticamente)
├── historial/         # Archivos generados
├── run_app.bat        # Script de Windows
├── run_app.ps1        # Script de PowerShell
└── app.py            # Aplicación principal
```
