# 🦷 AI Models Pro Generator

**Generador avanzado de imágenes y videos con IA - by Ayoze Benítez**

Una aplicación web completa desarrollada con Streamlit que integra múltiples modelos de IA para generar contenido visual de alta calidad. Sistema robusto con historial dual (online/local) y gestión avanzada de archivos.

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

### 💾 **Gestión de Archivos y Sistema Dual**

- **Descarga automática** de contenido generado
- **Almacenamiento local** en carpeta `historial/`
- **Sistema dual de enlaces**: Online (Replicate) y Local
- **Historial unificado** en archivo `history.json`
- **Vista previa** integrada para imágenes
- **Información de archivos** para videos
- **Botones diferenciados**: Rojo para online, azul para local
- **Verificación de archivos** antes de mostrar enlaces locales

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

- 🎨 **Arte Digital**: Composiciones vibrantes y detalladas
- � **Fotografía Realista**: Estilo fotográfico profesional
- 🌈 **Estilo Fantástico**: Ambientes mágicos y místicos
- 🤖 **Futurista/Sci-Fi**: Diseños cyberpunk y tecnológicos
- 🎭 **Retrato Artístico**: Retratos con iluminación dramática

### 🎬 **Generación de Videos (Seedance)**

**Parámetros disponibles:**
- **FPS**: 12, 24, 30
- **Duración**: 3-10 segundos
- **Resolución**: 720p, 1080p, 1440p
- **Relación de aspecto**: 16:9, 9:16, 1:1
- **Cámara fija**: Opcional

**Plantillas incluidas:**

- 🌊 **Amanecer Épico**: Paisajes cinematográficos dramáticos
- 🏙️ **Ciudad Futurista**: Escenas urbanas nocturnas
- 🌊 **Océano Tranquilo**: Ambientes costeros serenos
- 🎬 **Escena Cinematográfica**: Tomas profesionales de cine

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

## � Sistema Dual de Enlaces

### **Acceso Online y Local**
La aplicación implementa un sistema robusto de doble acceso a los archivos generados:

- **🔗 Ver Online (Replicate)** - Botón rojo que abre la URL original en Replicate
- **💾 Ver Local** - Botón azul para acceder al archivo descargado localmente

### **Características del Sistema Dual**
- **Almacenamiento redundante**: Cada generación se guarda con ambas referencias
- **Verificación automática**: Los botones solo aparecen si los recursos están disponibles
- **Interfaz diferenciada**: Colores distintos para identificar fácilmente cada tipo de acceso
- **Persistencia**: El historial mantiene ambos enlaces indefinidamente
- **Recuperación**: Sistema robusto que permite recuperar elementos faltantes

### **Estructura del Historial**
```json
{
  "tipo": "imagen",
  "fecha": "2025-01-17T10:30:00",
  "prompt": "Prompt completo preservado",
  "url": "https://replicate.delivery/...",
  "archivo_local": "imagen_20250117_103000.webp",
  "parametros": {...}
}
```

## �📊 Sistema de Estadísticas

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
├── � HISTORIAL_SPEC.md     # Especificación del sistema de historial
├── �📁 assets/               # Recursos de la aplicación
│   └── 🖼️ logo22.jpg        # Logo personalizado
├── 📁 historial/            # Sistema unificado de archivos
│   ├── 📄 history.json      # Historial único con enlaces duales
│   ├── 🖼️ imagen_*.webp     # Imágenes generadas (descarga local)
│   └── 🎬 video_*.mp4       # Videos generados (descarga local)
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
