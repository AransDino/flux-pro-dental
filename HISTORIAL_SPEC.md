# ESPECIFICACIÓN DEL SISTEMA DE HISTORIAL
# =====================================
# GRABADO A FUEGO - NO CAMBIAR SIN AUTORIZACIÓN EXPLÍCITA

## 1. ARCHIVO DE HISTORIAL
ARCHIVO_HISTORIAL = "historial/history.json"
# - ÚNICO archivo de historial
# - Formato: JSON array
# - Encoding: UTF-8
# - Ubicación: carpeta historial/

## 2. ESTRUCTURA DE DATOS
# Cada elemento del historial DEBE contener:
CAMPOS_OBLIGATORIOS = [
    "tipo",           # "imagen", "video_seedance", "video_anime"
    "fecha",          # ISO format: "2025-07-17T19:23:54.123456"
    "prompt",         # COMPLETO, sin truncar
    "plantilla",      # Nombre de plantilla usada
    "url",            # URL original de Replicate o "archivo_local:filename"
    "archivo_local",  # Nombre del archivo descargado
    "parametros"      # Objeto con parámetros de generación
]

CAMPOS_OPCIONALES = [
    "id_prediccion",  # ID de Replicate (solo imágenes)
    "recuperado",     # true si fue recuperado de archivo
    "nota"           # Información adicional
]

## 3. REGLAS DE FUNCIONAMIENTO
# - Orden: Cronológico inverso (más reciente primero)
# - Límite: 100 elementos máximo
# - Prompts: SIEMPRE completos, NUNCA truncados
# - Serialización: Limpiar objetos no serializables
# - Backup: NO crear múltiples archivos JSON

## 4. FUNCIONES CRÍTICAS
# - load_history(): Cargar desde history.json
# - save_to_history(item): Guardar nuevo elemento al principio
# - Limpieza automática de objetos FileOutput a string

## 5. TIPOS DE CONTENIDO
TIPOS_VALIDOS = {
    "imagen": {
        "prefijo_archivo": "imagen_",
        "extensiones": [".webp", ".jpg", ".png"]
    },
    "video_seedance": {
        "prefijo_archivo": "video_seedance_",
        "extensiones": [".mp4"]
    },
    "video_anime": {
        "prefijo_archivo": "video_anime_",
        "extensiones": [".mp4"]
    }
}

## 6. NOMBRE DE ARCHIVOS
# Formato: {tipo}_{YYYYMMDD_HHMMSS}.{ext}
# Ejemplo: imagen_20250717_192354.webp
# Ejemplo: video_seedance_20250717_192354.mp4

## 7. RECUPERACIÓN DE VIDEOS
# - Buscar archivos .mp4 huérfanos
# - Crear entradas con recuperado=true
# - Prompt descriptivo basado en plantilla
# - Fechas extraídas del nombre de archivo

## 8. REGLAS DE COHERENCIA
# - UN SOLO archivo JSON de historial
# - NO crear historial.json, backup.json, etc.
# - SIEMPRE usar history.json
# - Mantener compatibilidad hacia atrás

# =====================================
# ESTA ESPECIFICACIÓN ES DEFINITIVA
# CUALQUIER CAMBIO DEBE ACTUALIZARLA
# =====================================
