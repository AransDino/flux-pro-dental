# 📁 Sistema de Acceso a Archivos Locales

## 🎯 Objetivo del Sistema Dual

El **AI Models Pro Generator** implementa un sistema robusto de doble acceso que permite:

- **🌐 Acceso Online**: Enlaces directos a Replicate para ver/descargar contenido
- **💾 Acceso Local**: Archivos descargados automáticamente en tu ordenador
- **🔄 Redundancia**: Garantía de acceso incluso si un método falla
- **⚡ Velocidad**: Archivos locales para acceso instantáneo

---

## 📊 Cómo Funciona

### 🔗 **Enlaces en el Historial**

Cada elemento generado incluye **dos botones diferenciados**:

| Botón | Color | Función | Disponibilidad |
|-------|-------|---------|----------------|
| **🔗 Ver en Replicate** | Rojo | Abre URL original en Replicate | Siempre disponible |
| **📁 Archivo Local** | Azul | Abre archivo descargado localmente | Solo si el archivo existe |

### 📁 **Estructura de Almacenamiento Local**

```
flux-pro-dental/
├── 📁 historial/
│   ├── 📄 history.json           # ← Historial unificado
│   ├── 🖼️ imagen_20250118_*.webp  # ← Imágenes Flux Pro
│   ├── 🎨 kandinsky_20250118_*.jpg # ← Imágenes Kandinsky
│   ├── ⚡ ssd_20250118_*.jpg       # ← Imágenes SSD-1B
│   ├── 🎬 seedance_20250118_*.mp4  # ← Videos Seedance
│   ├── 🎭 pixverse_20250118_*.mp4  # ← Videos Pixverse
│   └── 🎥 veo_20250118_*.mp4       # ← Videos VEO 3 Fast
```

---

## ⚙️ Comportamiento del Sistema

### ✅ **Descarga Automática**

- **Al generar contenido** → Descarga automática a carpeta `historial/`
- **Nombres únicos** → Timestamp para evitar conflictos
- **Verificación** → Solo muestra botón local si el archivo existe
- **Formato preservado** → Mantiene formato original (WebP, MP4, etc.)

### 🔍 **Detección Inteligente**

El sistema identifica automáticamente:

```python
# Ejemplo de lógica de detección
if archivo_local and local_path.exists():
    mostrar_boton_local = True
    color_boton = "azul"
else:
    mostrar_boton_local = False
    mostrar_mensaje = "Solo disponible en Replicate"
```

### 🚀 **Apertura de Archivos**

Cuando haces clic en **"📁 Archivo Local"**:

- **Windows**: `os.startfile()` → Abre con programa predeterminado
- **macOS**: `open` command → Abre con aplicación asociada  
- **Linux**: `xdg-open` → Abre con aplicación predeterminada

---

## 📈 Ventajas del Sistema Dual

### 🌐 **Acceso Online (Replicate)**
- ✅ Siempre disponible (mientras Replicate mantenga el archivo)
- ✅ No ocupa espacio local
- ✅ Compartible mediante URL
- ❌ Requiere conexión a internet
- ❌ Puede desaparecer tras cierto tiempo

### 💾 **Acceso Local**
- ✅ Acceso instantáneo sin internet
- ✅ Control total sobre el archivo
- ✅ Permanente en tu ordenador
- ✅ Mejor para edición/procesamiento
- ❌ Ocupa espacio en disco
- ❌ Solo disponible en tu ordenador

---

## 🛠️ Gestión de Archivos

### 📊 **Información en el Historial**

Cada elemento muestra:

```
🖼️ 2025-01-18 15:30 - Imagen dental profesional...
├── 📄 Archivo: imagen_20250118_153045.webp
├── 🟢 Archivo disponible localmente  
├── 💰 Costo: $0.055
└── 🔗 Enlaces: [Ver en Replicate] [Archivo Local]
```

### 🧹 **Limpieza de Archivos**

Para gestionar el espacio en disco:

```bash
# Ver tamaño total de historial
du -sh historial/

# Limpiar archivos antiguos (manual)
# Eliminar archivos de hace más de 30 días
find historial/ -name "*.webp" -mtime +30 -delete
find historial/ -name "*.mp4" -mtime +30 -delete
```

### 🔧 **Recuperación de Archivos**

Si un archivo local se pierde:

1. **Archivo aún disponible** → Copiar URL de Replicate y descargar manualmente
2. **Conservar nombre original** → Mantener formato `tipo_fecha_hora.extension`
3. **Actualizar historial** → El sistema detectará automáticamente el archivo

---

## 💡 Casos de Uso Recomendados

### 🎨 **Para Diseñadores**
- Usar **archivos locales** para edición y procesamiento
- Mantener **enlaces de Replicate** para compartir con clientes

### 📊 **Para Análisis**
- **Archivos locales** → Análisis de metadatos y procesamiento
- **URLs de Replicate** → Referencias y documentación

### 🔄 **Para Backup**
- **Sistema dual** como backup automático
- **Historial JSON** para recuperar metadatos

---

## ⚠️ Consideraciones Importantes

### 🔒 **Seguridad**
- Los archivos locales se almacenan sin cifrado
- URLs de Replicate son públicas (temporal)
- No incluir información sensible en prompts

### 💾 **Espacio en Disco**
- Videos ocupan más espacio que imágenes
- Considerar límites de almacenamiento
- Implementar limpieza periódica si es necesario

### 🌐 **Conectividad**
- Sistema funciona **offline** para archivos locales
- URLs de Replicate requieren **conexión a internet**
- Historial se carga desde archivo local (no requiere internet)

---

## 🚀 Estado Actual del Sistema

### ✅ **Implementado y Funcionando**
- ✅ Descarga automática de todos los tipos de contenido
- ✅ Detección inteligente de archivos existentes
- ✅ Botones diferenciados por color y función
- ✅ Apertura automática con programas predeterminados
- ✅ Historial unificado con referencias duales
- ✅ Verificación de integridad de archivos

### 🎯 **Optimizado Para**
- **Flujo de trabajo profesional** con acceso dual
- **Gestión eficiente** de grandes volúmenes de contenido
- **Recuperación robusta** ante fallos de conectividad
- **Integración perfecta** con el ecosistema de la aplicación