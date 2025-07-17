# 🦷 AI Models Pro Generator

**Generador avanzado de imágenes y videos dentales con IA - by Ayoze Benítez**

Una aplicación web completa desarrollada con Streamlit que integra múltiples modelos de IA para generar contenido visual especializado en odontología y entretenimiento.

## ✨ Características Principales

### 🎯 **Modelos de IA Integrados**
- **🖼️ Flux Pro**: Generación de imágenes dentales hiperrealistas
- **🎬 Seedance 1-Pro**: Videos cinematográficos para clínicas
- **🎭 Pixverse v3.5**: Videos anime y contenido creativo

### 🎛️ **Interfaz Avanzada**
- **Sidebar dinámico** con parámetros específicos por modelo
- **Plantillas predefinidas** para cada tipo de contenido
- **Panel de control** con información en tiempo real
- **Pestañas organizadas** (Generar / Historial)

### 📊 **Sistema de Análisis y Estadísticas**
- **Resumen global** con métricas totales
- **Análisis de costos** en USD y EUR
- **Estadísticas detalladas** por generación:
  - Resolución, megapixeles, pasos de procesamiento
  - FPS, frames totales, duración
  - Estimaciones de costo precisas
- **Información temporal** (fecha, hora, antigüedad)

### 💾 **Gestión de Archivos**
- **Descarga automática** de contenido generado
- **Almacenamiento local** en carpeta `historial/`
- **Historial persistente** en formato JSON
- **Vista previa** integrada para imágenes
- **Información de archivos** para videos

### 🔐 **Seguridad y Configuración**
- **Tokens seguros** mediante archivo `config.py`
- **Configuración ejemplo** incluida
- **Validación de credenciales**

## 🚀 Instalación y Configuración

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
# Opción 1: Script automático
run_app.bat  # Windows
# run_app.ps1  # PowerShell

# Opción 2: Manual
streamlit run app.py --server.port=8505
```

## 📋 Uso de la Aplicación

### 🖼️ **Generación de Imágenes (Flux Pro)**

**Parámetros disponibles:**
- **Pasos**: 10-50 (calidad vs velocidad)
- **Dimensiones**: 512x512 hasta 1280x1280
- **Guidance**: 1-10 (fuerza de guidance)
- **Formato**: WebP, JPG, PNG
- **Calidad**: 60-100%

**Plantillas incluidas:**
- 🦷 **Dental Clásico**: Ilustraciones 3D hiperrealistas
- 🔬 **Instrumental Dental**: Fotografía macro de instrumentos
- 🏥 **Consultorio Moderno**: Interiores de clínicas contemporáneas

### 🎬 **Generación de Videos (Seedance)**

**Parámetros disponibles:**
- **FPS**: 12, 24, 30
- **Duración**: 3-10 segundos
- **Resolución**: 720p, 1080p, 1440p
- **Relación de aspecto**: 16:9, 9:16, 1:1
- **Cámara fija**: Opcional

**Plantillas incluidas:**
- 🌊 **Clínica Oceánica**: Ambientes cinematográficos
- 🦷 **Procedimiento Dental**: Tomas clínicas profesionales

### 🎭 **Generación de Videos Anime (Pixverse)**

**Parámetros disponibles:**
- **Estilo**: Anime, Realistic, Cartoon
- **Calidad**: 540p, 720p, 1080p
- **Efectos**: Zoom In/Out, Pan Left/Right
- **Modo de movimiento**: Normal, Slow, Fast
- **Prompt negativo**: Opcional
- **Efectos de sonido**: Activable

**Plantillas incluidas:**
- 🎭 **Escena de Acción**: Batallas épicas
- 🌸 **Personaje Kawaii**: Estilo cute
- 🏯 **Paisaje Japonés**: Ambientes tradicionales
- ⚔️ **Batalla Épica**: Combates dinámicos
- 🌙 **Noche Mágica**: Magical girls

## 📊 Sistema de Estadísticas

### **Resumen Global**
- Contador de generaciones por tipo
- Costo total acumulado en USD/EUR
- Métricas de uso histórico

### **Análisis Individual**
- **Imágenes**: Resolución, megapixeles, costo estimado
- **Videos**: Duración, FPS, frames totales, tamaño de archivo
- **Temporales**: Fecha, hora, antigüedad

### **Estimaciones de Costo**
- **Flux Pro**: ~$0.05 por imagen (ajustado por resolución)
- **Seedance**: ~$0.10 por segundo (ajustado por calidad)
- **Pixverse**: ~$0.08 por segundo (ajustado por calidad)

## 📁 Estructura del Proyecto

```
flux-pro-dental/
├── 📄 app.py                 # Aplicación principal Streamlit
├── 📄 config.py              # Configuración de tokens (no en git)
├── 📄 config.example.py      # Plantilla de configuración
├── 📄 generate_imagen.py     # Script CLI para imágenes
├── 📄 video.py              # Script CLI para videos Seedance  
├── 📄 anime.py              # Script CLI para videos anime
├── 📄 requirements.txt       # Dependencias Python
├── 📄 run_app.bat           # Script de inicio Windows
├── 📄 run_app.ps1           # Script de inicio PowerShell
├── 📁 assets/               # Recursos de la aplicación
│   └── 🖼️ logo22.jpg        # Logo personalizado
├── 📁 historial/            # Archivos generados y metadatos
│   ├── 📄 history.json      # Historial persistente
│   ├── 🖼️ imagen_*.webp     # Imágenes generadas
│   └── 🎬 video_*.mp4       # Videos generados
├── 📁 venv/                 # Entorno virtual Python
└── 📄 .gitignore           # Archivos excluidos de git
```

## 🛠️ Scripts Independientes

### **Generación de Imágenes**
```bash
python generate_imagen.py
```

### **Generación de Videos Seedance**
```bash
python video.py
```

### **Generación de Videos Anime**
```bash
python anime.py
```

## 🔧 Tecnologías Utilizadas

- **Frontend**: Streamlit
- **Backend**: Python 3.10+
- **IA**: Replicate API
- **Almacenamiento**: JSON + Sistema de archivos
- **Estilo**: CSS personalizado
- **Control de versiones**: Git

## 📦 Dependencias Principales

```
streamlit>=1.47.0
replicate>=0.15.0
requests>=2.31.0
pathlib>=1.0.1
```

## 🎨 Características de Diseño

- **Logo personalizado** en sidebar (170px, bordes redondeados)
- **Tipografía manuscrita** para el nombre del autor
- **Interfaz responsiva** con layout amplio
- **Iconos temáticos** para cada función
- **Colores diferenciados** por tipo de contenido
- **Sidebar persistente** con todos los controles

## 🔒 Seguridad

- **Tokens externos** no incluidos en el repositorio
- **Archivo `.gitignore`** configurado correctamente
- **Validación de configuración** antes de usar la API
- **Historial local** sin exposición de datos sensibles

## 📈 Métricas de Rendimiento

- **Tiempo de generación**: Variable según modelo y parámetros
- **Almacenamiento**: Optimizado con límite de 100 elementos en historial
- **Interfaz**: Respuesta inmediata en controles
- **Descarga**: Automática con verificación de archivos existentes

## 🤝 Contribuciones

Este proyecto está en desarrollo activo. Las mejoras y sugerencias son bienvenidas.

## 📄 Licencia

Proyecto desarrollado por **Ayoze Benítez** para uso educativo y profesional en el ámbito odontológico.

## 🌐 Enlaces

- **GitHub**: [AransDino/flux-pro-dental](https://github.com/AransDino/flux-pro-dental)
- **Replicate**: [replicate.com](https://replicate.com)
- **Streamlit**: [streamlit.io](https://streamlit.io)

---

**© 2025 Ayoze Benítez - AI Models Pro Generator**
