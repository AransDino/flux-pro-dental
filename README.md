# 🦷 Flux Pro Dental Image Generator

Un generador de imágenes dentales hiperrealistas usando el modelo Flux Pro de Replicate. Este proyecto permite crear ilustraciones 3D de alta calidad para educación dental y presentaciones clínicas.

## 🚀 Características

- **Generación de imágenes dentales hiperrealistas** usando Flux Pro
- **Progreso en tiempo real** con contador de segundos actualizable
- **Configuración personalizable** de parámetros de generación
- **Descarga automática** de imágenes generadas
- **Timeouts configurables** para evitar esperas infinitas

## 🛠️ Instalación

### Prerrequisitos

- Python 3.7 o superior
- Cuenta en [Replicate](https://replicate.com/)
- Token de API de Replicate

### Configuración del entorno

1. **Clona este repositorio:**
   ```bash
   git clone https://github.com/tu-usuario/flux-pro-dental.git
   cd flux-pro-dental
   ```

2. **Crea un entorno virtual:**
   ```bash
   python -m venv venv
   ```

3. **Activa el entorno virtual:**
   
   **Windows (PowerShell):**
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```
   
   **macOS/Linux:**
   ```bash
   source venv/bin/activate
   ```

4. **Instala las dependencias:**
   ```bash
   pip install replicate requests
   ```

## 🔧 Configuración

1. **Obtén tu token de API de Replicate:**
   - Ve a [Replicate](https://replicate.com/)
   - Inicia sesión y ve a tu perfil
   - Copia tu token de API

2. **Configura el token:**
   
   **Copia el archivo de configuración:**
   ```bash
   cp config.example.py config.py
   ```
   
   **Edita el archivo `config.py` y reemplaza el token:**
   ```python
   REPLICATE_API_TOKEN = "tu_token_real_aqui"
   ```

   **⚠️ Importante:** El archivo `config.py` está en `.gitignore` y no se subirá a GitHub por seguridad.

## 📖 Uso

1. **Ejecuta el script:**
   ```bash
   python generate_imagen.py
   ```

2. **El script te mostrará:**
   - Hora de inicio del proceso
   - ID de la predicción
   - Progreso en tiempo real con contador de segundos
   - Estado del proceso de generación

3. **La imagen se guardará como:**
   ```
   dental_crown.webp
   ```

## ⚙️ Configuración de parámetros

Puedes modificar los siguientes parámetros en el código:

```python
input={
    "steps": 25,              # Pasos de inferencia (calidad vs velocidad)
    "width": 1024,            # Ancho de la imagen
    "height": 1024,           # Alto de la imagen
    "guidance": 3,            # Fuerza del guidance
    "interval": 2,            # Intervalo de guidance
    "aspect_ratio": "1:1",    # Relación de aspecto
    "output_format": "webp",  # Formato de salida
    "output_quality": 80,     # Calidad de compresión
    "safety_tolerance": 2,    # Tolerancia de seguridad
    "prompt_upsampling": False # Mejora del prompt
}
```

## 📝 Personalización del prompt

El prompt actual está optimizado para generar ilustraciones dentales. Puedes modificarlo en la variable `prompt_text`:

```python
prompt_text = """
Tu prompt personalizado aquí...
"""
```

### Ejemplo de prompt incluido:
- Vista superior del arco dental inferior
- Múltiples inlays y onlays en molares
- Tejido gingival anatómicamente correcto
- Texturas realistas
- Restauraciones cerámicas detalladas
- Fondo limpio y neutral
- Calidad de grado médico

## 🔄 Funcionamiento

1. **Inicialización**: Se configura el cliente de Replicate y se registra la hora de inicio
2. **Envío**: Se envía la solicitud de generación con los parámetros especificados
3. **Monitoreo**: Se muestra el progreso en tiempo real con actualización cada 2 segundos
4. **Finalización**: Una vez completado, se descarga y guarda la imagen

## ⏱️ Tiempos esperados

- **Tiempo típico**: 2-5 minutos
- **Timeout configurado**: 40 minutos
- **Actualización de estado**: Cada 2 segundos

## 🚨 Manejo de errores

El script incluye manejo para:
- Timeouts de conexión
- Errores de generación
- Estados cancelados
- Fallos de descarga

## 📋 Estados posibles

- `starting` → `waiting response`
- `processing` → `processing`
- `succeeded` → ✅ Imagen generada
- `failed` → ❌ Error en la generación
- `canceled` → ⚠️ Proceso cancelado

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## 🔗 Enlaces útiles

- [Replicate API Documentation](https://replicate.com/docs)
- [Flux Pro Model](https://replicate.com/black-forest-labs/flux-pro)
- [Python Replicate Client](https://github.com/replicate/replicate-python)

## ⚠️ Nota de seguridad

**No subas tu token de API a GitHub.** Considera usar variables de entorno o archivos de configuración locales para manejar credenciales sensibles.

---

**Desarrollado para generar contenido educativo dental de alta calidad** 🦷✨
