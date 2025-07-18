# 🦷 AI Models Pro Generator - **by Ayoze Benítez**

**Generador avanzado de imágenes y videos con IA - Sistema completo con backup y restauración integrados**

Una aplicación web completa desarrollada con Streamlit que integra múltiples modelos de IA para generar contenido visual de alta calidad. Sistema robusto con historial dual (online/local), gestión avanzada de archivos y **funcionalidad completa de backup y restauración**.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.24+-red.svg)](https://streamlit.io)
[![Replicate](https://img.shields.io/badge/Replicate-API-green.svg)](https://replicate.com)

## 📚 Documentación del Proyecto

### 📖 **Guías de Usuario**
- **[🚀 INICIO_RAPIDO.md](./INICIO_RAPIDO.md)** - Guía de instalación y configuración rápida
- **[📋 HISTORIAL_SPEC.md](./HISTORIAL_SPEC.md)** - Especificación técnica del sistema de historial
- **[💰 CORRECCIONES_COSTOS.md](./CORRECCIONES_COSTOS.md)** - Tarifas reales de Replicate y cálculos de costos
- **[📁 ACCESO_ARCHIVOS_LOCALES.md](./ACCESO_ARCHIVOS_LOCALES.md)** - Sistema de archivos locales y enlaces duales

### 🗂️ **Navegación Rápida**
- [⚡ Instalación Automática](#-instalación-y-ejecución-automática) - Scripts de inicio automático
- [🎯 Modelos de IA](#-modelos-de-ia-integrados) - Flux Pro, Kandinsky, VEO 3 Fast y más
- [💾 Sistema de Backup](#-sistema-de-backup-y-restauración-nuevo) - **NUEVO: Backup completo**
- [📊 Sistema de Estadísticas](#-sistema-de-estadísticas) - Análisis de costos y métricas
- [💾 Gestión de Archivos](#-gestión-de-archivos-y-sistema-dual) - Sistema dual online/local
- [🛠️ Solución de Problemas](#-solución-de-problemas) - Errores comunes y soluciones
- [📁 Estructura del Proyecto](#-estructura-del-proyecto) - Organización de archivos

---

## ✨ Características Principales

### 🎯 **Modelos de IA Integrados**
- **🖼️ Flux Pro**: Generación de imágenes dentales hiperrealistas
- **🎨 Kandinsky 2.2**: Arte abstracto y creativo de alta calidad
- **⚡ SSD-1B**: Generación rápida de imágenes fotorrealistas
- **🎬 Seedance 1-Pro**: Videos cinematográficos para clínicas
- **🎭 Pixverse v3.5**: Videos anime y contenido creativo
- **🚀 VEO 3 Fast**: Videos de Google con calidad cinematográfica

### 🎛️ **Interfaz Avanzada**
- **Sidebar dinámico** con parámetros específicos por modelo
- **Plantillas predefinidas** para cada tipo de contenido (11+ por modelo)
- **Panel de control** con información en tiempo real
- **Pestañas organizadas** (Generar / Historial)
- **Modal de configuración** con pestañas para control y backup

### 💾 **Sistema de Backup y Restauración (NUEVO)**
- **🔄 Backup automático** - Crea copias completas de todos los datos
- **📦 Compresión ZIP** - Archivos optimizados con metadatos incluidos
- **🛡️ Backup de seguridad** - Se crea automáticamente antes de restaurar
- **📁 Gestión de backups** - Lista, restaura y elimina backups existentes
- **📤 Import/Export** - Sube archivos de backup desde cualquier ubicación
- **✅ Validación completa** - Verificación de integridad de archivos

#### **¿Qué incluye cada backup?**
```
ai_models_backup_YYYYMMDD_HHMMSS.zip
├── generation_stats.json           # Estadísticas globales
├── historial/
│   ├── history.json                # Historial de generaciones
│   ├── imagen_*.webp               # Imágenes generadas
│   ├── video_*.mp4                 # Videos generados
│   └── ...                         # Otros archivos multimedia
└── backup_metadata.json            # Información del backup
```

### 📊 **Sistema de Análisis y Estadísticas**
- **Resumen global** con métricas totales de rendimiento
- **Análisis de costos** precisos en USD y EUR por modelo
- **Estadísticas detalladas** por generación:
  - Resolución, megapixeles, pasos de procesamiento
  - FPS, frames totales, duración para videos
  - Estimaciones de costo en tiempo real
- **Información temporal** (fecha, hora, antigüedad relativa)
- **Métricas visuales** con tarjetas coloridas por modelo

### 💾 **Gestión de Archivos y Sistema Dual**
- **Descarga automática** de contenido generado desde Replicate
- **Almacenamiento local** organizado en carpeta `historial/`
- **Sistema dual de enlaces**: Online (Replicate) y Local
- **Historial unificado** en archivo `history.json`
- **Vista previa integrada** para imágenes y videos
- **Información detallada** de archivos (tamaño, formato, duración)
- **Botones diferenciados**: 🔗 para online, 📁 para local
- **Verificación automática** de archivos antes de mostrar enlaces

### 🔐 **Seguridad y Configuración**
- **Tokens seguros** mediante archivo `config.py` (excluido de Git)
- **Configuración ejemplo** incluida como plantilla
- **Validación de credenciales** en tiempo real
- **Variables de entorno** para mayor seguridad

---

## 🚀 Instalación y Ejecución (AUTOMÁTICA)

### **Método Rápido (Recomendado)**

#### **Opción 1: PowerShell (Windows)**
```powershell
# 1. Clonar el repositorio
git clone https://github.com/AransDino/flux-pro-dental.git
cd flux-pro-dental

# 2. Ejecutar script automático
.\run_app.ps1
```

#### **Opción 2: Command Prompt (Windows)**
```bash
# 1. Clonar el repositorio
git clone https://github.com/AransDino/flux-pro-dental.git
cd flux-pro-dental

# 2. Ejecutar script automático
run_app.bat
```

#### **Opción 3: Doble clic**
1. Clonar el repositorio
2. Hacer doble clic en `run_app.bat`

### **¿Qué hace automáticamente el script?**
✅ **Verifica Python** (te avisa si no está instalado)  
✅ **Crea entorno virtual** (automático si no existe)  
✅ **Activa el entorno virtual** (automático)  
✅ **Instala dependencias** (desde requirements.txt)  
✅ **Crea config.py** (desde plantilla si no existe)  
✅ **Inicia Streamlit** (abre en navegador automáticamente)  

### **Primera ejecución - Configurar token:**
1. El script copiará automáticamente `config.example.py` como `config.py`
2. **Edita `config.py`** y reemplaza:
```python
REPLICATE_API_TOKEN = "tu_token_de_replicate_aqui"
```
3. Obtén tu token en: https://replicate.com/account/api-tokens
4. Reinicia el script

---

## 💾 Sistema de Backup y Restauración (NUEVO)

### **🔄 Crear Backup**
1. Abre la aplicación y ve a **Configuración** (⚙️ en la sidebar)
2. Selecciona la pestaña **"💾 Backup y Restauración"**
3. Haz clic en **"💾 Crear Backup"**
4. El archivo se guardará automáticamente como `ai_models_backup_YYYYMMDD_HHMMSS.zip`

### **📥 Restaurar Backup**

#### **Desde backup local:**
1. Ve a **Configuración → Backup y Restauración**
2. En la sección **"📂 Backups Disponibles"**, selecciona un backup
3. Haz clic en **"🔄 Restaurar"**
4. Reinicia la aplicación para ver los cambios

#### **Desde archivo externo:**
1. Ve a **Configuración → Backup y Restauración**
2. En **"📁 Restaurar desde Archivo"**, sube tu archivo `.zip`
3. Haz clic en **"🔄 Restaurar Archivo"**
4. Reinicia la aplicación

### **🛡️ Funciones de Seguridad**
- **Backup automático** se crea antes de cualquier restauración
- **Validación completa** de archivos ZIP
- **Metadatos incluidos** en cada backup
- **Limpieza automática** de archivos temporales

### **📋 Gestión de Backups**
- **Ver información detallada** (fecha, tamaño, contenido)
- **Eliminar backups antiguos** con confirmación
- **Lista ordenada** por fecha (más recientes primero)

---

## 🎯 Modelos de IA Integrados

### **🖼️ Flux Pro - Imágenes Hiperrealistas**
- **Resoluciones**: Hasta 1280x1280 píxeles
- **Formatos**: WebP, JPG, PNG
- **Parámetros avanzados**: Steps, Guidance, Aspect Ratio
- **Plantillas**: 11 estilos predefinidos (Arte Digital, Fotografía, Fantasía, etc.)

### **🎨 Kandinsky 2.2 - Arte Abstracto**
- **Resoluciones**: Hasta 1280x1280 píxeles
- **Estilo**: Arte abstracto y creativo de alta calidad
- **Parámetros**: Pasos de inferencia, modelo prior
- **Plantillas**: 10 estilos artísticos (Abstracto, Surrealismo, Impresionismo, etc.)

### **⚡ SSD-1B - Generación Rápida**
- **Velocidad**: Generación ultrarrápida (15-25 pasos)
- **Calidad**: Imágenes fotorrealistas de alta calidad
- **Parámetros**: LoRA Scale, Scheduler, Guidance Scale
- **Plantillas**: 10 estilos dinámicos (Fantasía Épica, Elementos Naturales, etc.)

### **🎬 Seedance 1-Pro - Videos Cinematográficos**
- **Duración**: 3-10 segundos
- **Resoluciones**: 720p, 1080p, 1440p
- **FPS**: 12, 24, 30 fps
- **Plantillas**: 10 estilos cinematográficos (Amanecer Épico, Ciudad Futurista, etc.)

### **🎭 Pixverse v3.5 - Videos Anime**
- **Duración**: 3-10 segundos
- **Estilos**: Anime, 3D Animation, Clay, Cyberpunk
- **Efectos**: Zoom, Pan, efectos de sonido
- **Plantillas**: 10 estilos anime (Acción, Kawaii, Batalla Épica, etc.)

### **🚀 VEO 3 Fast - Videos de Google**
- **Duración**: 2-8 segundos
- **Calidad**: Standard y High
- **Características**: Mejora automática de prompts
- **Plantillas**: 10 estilos épicos (Acción, Naturaleza, Persecución, etc.)

---

## 📊 Sistema de Estadísticas

### **📈 Métricas Globales**
- **Total de generaciones** por modelo
- **Tasa de éxito** en tiempo real
- **Tiempo promedio** de procesamiento
- **Costo acumulado** en USD y EUR

### **💰 Análisis de Costos**
```python
# Tarifas actualizadas (2024)
COST_RATES = {
    'imagen': {
        'flux_pro': 0.055,      # $0.055 por imagen
        'kandinsky': 0.005,     # $0.005 por imagen
        'ssd1b': 0.003          # $0.003 por imagen
    },
    'video': {
        'seedance': 0.02,       # $0.02 por segundo
        'pixverse': 0.016,      # $0.016 por segundo
        'veo3_fast': 0.125      # $0.125 por segundo
    }
}
```

### **📋 Información Detallada**
- **Por generación**: Resolución, megapixeles, parámetros
- **Por video**: FPS, frames totales, duración
- **Temporal**: Fecha/hora exacta, antigüedad relativa
- **Técnica**: ID de predicción, modelo específico

---

## 💾 Gestión de Archivos y Sistema Dual

### **📁 Estructura de Archivos**
```
flux-pro-dental/
├── historial/                     # Archivos descargados
│   ├── history.json               # Historial principal
│   ├── imagen_20240718_123456.webp
│   ├── video_20240718_123457.mp4
│   └── ...
├── generation_stats.json          # Estadísticas globales
├── ai_models_backup_*.zip          # Backups automáticos
├── app.py                         # Aplicación principal
├── utils.py                       # Funciones centralizadas
└── config.py                      # Configuración (no en Git)
```

### **🔗 Sistema Dual de Enlaces**
- **🔗 Enlaces Online (Replicate)**: Acceso directo desde Replicate
- **📁 Enlaces Locales**: Archivos descargados automáticamente
- **Verificación automática**: Solo muestra enlaces si los archivos existen
- **Botones diferenciados**: Colores distintos para cada tipo

### **💾 Descarga Automática**
- **Detección de formato**: Automática según el tipo de archivo
- **Nomenclatura estándar**: `tipo_YYYYMMDD_HHMMSS.ext`
- **Verificación de integridad**: Validación antes de guardar
- **Gestión de errores**: Reintentos automáticos

---

## 🛠️ Instalación Manual (Opcional)

Si prefieres hacer todo manualmente:

### 1. Clonar el repositorio
```bash
git clone https://github.com/AransDino/flux-pro-dental.git
cd flux-pro-dental
```

### 2. Crear entorno virtual
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar token de Replicate
```bash
# Copiar archivo de configuración
copy config.example.py config.py

# Editar config.py y añadir tu token real
REPLICATE_API_TOKEN = "tu_token_de_replicate_aqui"
```

### 5. Ejecutar la aplicación
```bash
# Recomendado: Scripts automáticos
.\run_app.ps1  # PowerShell
run_app.bat    # Command Prompt

# Manual (si el entorno virtual ya está activado)
streamlit run app.py --server.port=8501
```

---

## 🔧 Solución de Problemas

### **Error: "No se reconoce el comando"**
```powershell
# En PowerShell, usar:
.\run_app.ps1
# En lugar de:
run_app.ps1
```

### **Error: "No se puede ejecutar scripts"**
```powershell
# Habilitar ejecución de scripts en PowerShell:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### **Error: "Python no encontrado"**
1. Instala Python desde: https://www.python.org/downloads/
2. Asegúrate de marcar "Add Python to PATH" durante la instalación

### **Error: "Token de Replicate inválido"**
1. Verifica tu token en: https://replicate.com/account/api-tokens
2. Asegúrate de que `config.py` contiene el token correcto
3. Reinicia la aplicación después de cambiar el token

### **Error: "Archivo de backup corrupto"**
1. Verifica que el archivo ZIP no esté dañado
2. Usa **"📂 Backups Disponibles"** para archivos locales
3. Crea un nuevo backup si el problema persiste

---

## 📁 Estructura del Proyecto

```
flux-pro-dental/
├── 📄 app.py                      # Aplicación Streamlit principal
├── 📄 utils.py                    # Funciones centralizadas y utilities
├── 📄 config.example.py           # Plantilla de configuración
├── 📄 config.py                   # Configuración real (Git ignored)
├── 📄 requirements.txt            # Dependencias Python
├── 📄 generation_stats.json       # Estadísticas globales
├── 🔧 run_app.bat                 # Script Windows (Command Prompt)
├── 🔧 run_app.ps1                 # Script Windows (PowerShell)
├── 📁 historial/                  # Archivos generados y datos
│   ├── 📄 history.json            # Historial de generaciones
│   ├── 🖼️ imagen_*.webp           # Imágenes generadas
│   ├── 🎬 video_*.mp4             # Videos generados
│   └── ...                        # Otros archivos multimedia
├── 📁 assets/                     # Recursos estáticos
│   └── 🖼️ logo.jpg               # Logo de la aplicación
├── 📁 tests/                      # Tests unitarios
├── 💾 ai_models_backup_*.zip      # Backups automáticos
├── 📚 README.md                   # Esta documentación
├── 📚 INICIO_RAPIDO.md            # Guía de inicio rápido
├── 📚 HISTORIAL_SPEC.md           # Especificación técnica
├── 📚 CORRECCIONES_COSTOS.md      # Información de costos
└── 📚 ACCESO_ARCHIVOS_LOCALES.md  # Sistema de archivos
```

---

## 📝 Historial de Cambios Recientes

### **v2.1.0 - Sistema de Backup (2024-07-19)**
- ✅ **Nueva funcionalidad de backup completo**
- ✅ **Compresión ZIP con metadatos**
- ✅ **Restauración desde archivos externos**
- ✅ **Backup de seguridad automático**
- ✅ **Gestión completa de backups existentes**
- ✅ **Validación de integridad de archivos**

### **v2.0.0 - Restructuración Completa (2024-07-18)**
- ✅ **Funciones centralizadas en utils.py**
- ✅ **Modal de configuración con pestañas**
- ✅ **Sistema dual mejorado (online/local)**
- ✅ **Estadísticas visuales por modelo**
- ✅ **Cálculos de costo actualizados**

---

## 🤝 Contribuir

1. **Fork** el proyecto
2. **Crea** una branch para tu feature (`git checkout -b feature/AmazingFeature`)
3. **Commit** tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. **Push** a la branch (`git push origin feature/AmazingFeature`)
5. **Abre** un Pull Request

---

## 📧 Contacto

**Ayoze Benítez** - Desarrollador Principal

- 🌐 **GitHub**: [@AransDino](https://github.com/AransDino)
- 📧 **Email**: [Contacto directo via GitHub Issues](https://github.com/AransDino/flux-pro-dental/issues)

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

---

## ⭐ Agradecimientos

- **[Replicate](https://replicate.com)** - Por proporcionar la API de modelos de IA
- **[Streamlit](https://streamlit.io)** - Por el framework de aplicaciones web
- **[Black Forest Labs](https://huggingface.co/black-forest-labs)** - Por el modelo Flux Pro
- **Comunidad Open Source** - Por las librerías y herramientas utilizadas

---

<div align="center">

**⭐ Si este proyecto te es útil, considera darle una estrella ⭐**

**🔧 Hecho con ❤️ por Ayoze Benítez**

</div>
