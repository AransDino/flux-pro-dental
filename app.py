import streamlit as st
import os
import time
import replicate
import requests
from datetime import datetime
from pathlib import Path
import tempfile
import json

# Configurar la página
st.set_page_config(
    page_title="🦷 Ai Models Pro Generator - by Ayoze Benítez",
    page_icon="🦷",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configuración de directorios
HISTORY_DIR = Path("historial")
HISTORY_FILE = HISTORY_DIR / "history.json"

# Crear directorio de historial si no existe
HISTORY_DIR.mkdir(exist_ok=True)

# Funciones de historial
def load_history():
    """Cargar historial desde archivo JSON"""
    if HISTORY_FILE.exists():
        try:
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return []
    return []

def save_to_history(item):
    """Guardar item al historial"""
    try:
        # Limpiar cualquier objeto no serializable del item
        clean_item = {}
        for key, value in item.items():
            try:
                # Intentar serializar cada valor individualmente
                json.dumps(value)
                clean_item[key] = value
            except (TypeError, ValueError):
                # Si no se puede serializar, convertir a string
                clean_item[key] = str(value)
        
        history = load_history()
        history.insert(0, clean_item)  # Añadir al principio
        
        # Mantener solo los últimos 100 elementos
        history = history[:100]
        
        with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
            
    except Exception as e:
        st.error(f"Error al guardar historial: {str(e)}")
        # Debug: mostrar más información sobre el error
        st.error(f"Tipo de error: {type(e).__name__}")
        st.error(f"Item que causó el error: {str(item)[:200]}...")

def download_and_save_file(url, filename, file_type):
    """Descargar archivo y guardarlo localmente"""
    try:
        local_path = HISTORY_DIR / filename
        
        # Si ya existe, no descargar de nuevo
        if local_path.exists():
            return str(local_path)
        
        response = requests.get(url, timeout=60)
        if response.status_code == 200:
            with open(local_path, 'wb') as f:
                f.write(response.content)
            return str(local_path)
        else:
            return None
    except Exception as e:
        st.error(f"Error al descargar {file_type}: {str(e)}")
        return None

# Función para cargar configuración
def load_config():
    try:
        from config import REPLICATE_API_TOKEN
        if REPLICATE_API_TOKEN == "tu_token_aqui":
            return None
        os.environ["REPLICATE_API_TOKEN"] = REPLICATE_API_TOKEN
        return REPLICATE_API_TOKEN
    except ImportError:
        return None

# Función para cargar logo en base64
def get_logo_base64():
    """Cargar el logo y convertirlo a base64 para embebido en HTML"""
    import base64
    logo_path = Path("assets/logo22.jpg")
    try:
        if logo_path.exists():
            with open(logo_path, "rb") as f:
                return base64.b64encode(f.read()).decode()
        else:
            return ""
    except Exception:
        return ""

# Función para generar imagen
def generate_image(prompt, **params):
    client = replicate.Client()
    
    prediction = client.predictions.create(
        version="black-forest-labs/flux-pro",
        input={
            "prompt": prompt,
            **params
        }
    )
    
    return prediction

# Función para generar video con Seedance
def generate_video_seedance(prompt, **params):
    output = replicate.run(
        "bytedance/seedance-1-pro",
        input={
            "prompt": prompt,
            **params
        }
    )
    return output

# Función para generar video anime con Pixverse
def generate_video_pixverse(prompt, **params):
    output = replicate.run(
        "pixverse/pixverse-v3.5",
        input={
            "prompt": prompt,
            **params
        }
    )
    return output

# Título principal
st.markdown("""
<div style="text-align: left;">
    <h1 style="margin-bottom: 0;">🦷 Ai Models Pro Generator</h1>
    <p style="font-family: 'Brush Script MT', 'Lucida Handwriting', 'Apple Chancery', cursive; 
              font-size: 24px; 
              color: #2E86AB; 
              margin-top: -10px; 
              font-style: italic;
              text-shadow: 1px 1px 2px rgba(0,0,0,0.1);">
        - by Ayoze Benítez
    </p>
</div>
""", unsafe_allow_html=True)
st.markdown("### Generador de contenido con modelos de IA avanzados")

# Verificar configuración
token = load_config()
if not token:
    st.error("❌ **Error de configuración**")
    st.markdown("""
    **Por favor configura tu token de Replicate:**
    1. Copia `config.example.py` como `config.py`
    2. Edita `config.py` y configura tu token real
    3. Reinicia la aplicación
    """)
    st.stop()

# Sidebar para configuración (SIEMPRE VISIBLE)
with st.sidebar:
    # Logo en la esquina superior izquierda
    st.markdown("""
    <div style="text-align: center; margin-bottom: 20px;">
        <img src="data:image/jpeg;base64,{}" 
             style="width: 170px; 
                    height: auto; 
                    max-width: 100%;
                    border-radius: 10px;">
    </div>
    """.format(get_logo_base64()), unsafe_allow_html=True)
    
    st.header("⚙️ Configuración")
    
    # Selector de tipo de contenido
    content_type = st.selectbox(
        "🎯 Tipo de contenido:",
        ["🖼️ Imagen (Flux Pro)", "🎬 Video (Seedance)", "🎭 Video Anime (Pixverse)"],
        help="Selecciona el tipo de contenido que quieres generar"
    )
    
    st.divider()
    
    # Configuración según el tipo
    if "Imagen" in content_type:
        st.subheader("📸 Parámetros de Imagen")
        
        col1, col2 = st.columns(2)
        with col1:
            steps = st.slider("Pasos", min_value=10, max_value=50, value=25, help="Calidad vs velocidad")
            width = st.selectbox("Ancho", [512, 768, 1024, 1280], index=2)
        
        with col2:
            guidance = st.slider("Guidance", min_value=1, max_value=10, value=3, help="Fuerza del guidance")
            height = st.selectbox("Alto", [512, 768, 1024, 1280], index=2)
        
        aspect_ratio = st.selectbox("Relación de aspecto", ["1:1", "16:9", "9:16", "4:3", "3:4"], index=0)
        output_format = st.selectbox("Formato", ["webp", "jpg", "png"], index=0)
        output_quality = st.slider("Calidad", min_value=60, max_value=100, value=80)
        
        # Parámetros avanzados
        with st.expander("🔧 Parámetros avanzados"):
            interval = st.slider("Intervalo", min_value=1, max_value=5, value=2)
            safety_tolerance = st.slider("Tolerancia de seguridad", min_value=1, max_value=5, value=2)
            prompt_upsampling = st.checkbox("Mejora de prompt", value=False)
        
        params = {
            "steps": steps,
            "width": width,
            "height": height,
            "guidance": guidance,
            "interval": interval,
            "aspect_ratio": aspect_ratio,
            "output_format": output_format,
            "output_quality": output_quality,
            "safety_tolerance": safety_tolerance,
            "prompt_upsampling": prompt_upsampling
        }
    
    elif "Seedance" in content_type:  # Video Seedance
        st.subheader("🎬 Parámetros de Video (Seedance)")
        
        col1, col2 = st.columns(2)
        with col1:
            fps = st.selectbox("FPS", [12, 24, 30], index=1)
            duration = st.slider("Duración (seg)", min_value=3, max_value=10, value=5)
        
        with col2:
            resolution = st.selectbox("Resolución", ["720p", "1080p", "1440p"], index=1)
            aspect_ratio = st.selectbox("Relación de aspecto", ["16:9", "9:16", "1:1"], index=0)
        
        camera_fixed = st.checkbox("Cámara fija", value=False, help="Si está marcado, la cámara no se mueve")
        
        params = {
            "fps": fps,
            "duration": duration,
            "resolution": resolution,
            "aspect_ratio": aspect_ratio,
            "camera_fixed": camera_fixed
        }
    
    else:  # Video Anime Pixverse
        st.subheader("🎭 Parámetros de Video Anime (Pixverse)")
        
        col1, col2 = st.columns(2)
        with col1:
            style = st.selectbox("Estilo", ["anime", "realistic", "cartoon"], index=0)
            quality = st.selectbox("Calidad", ["540p", "720p", "1080p"], index=1)
        
        with col2:
            duration = st.slider("Duración (seg)", min_value=3, max_value=10, value=5)
            aspect_ratio = st.selectbox("Relación de aspecto", ["16:9", "9:16", "1:1"], index=0)
        
        effect = st.selectbox("Efecto", ["None", "Zoom In", "Zoom Out", "Pan Left", "Pan Right"], index=0)
        motion_mode = st.selectbox("Modo de movimiento", ["normal", "slow", "fast"], index=0)
        sound_effect_switch = st.checkbox("Efectos de sonido", value=False)
        
        # Área para prompt negativo
        negative_prompt = st.text_area(
            "Prompt negativo (opcional):",
            height=60,
            placeholder="Describe lo que NO quieres en el video..."
        )
        
        params = {
            "style": style,
            "effect": effect,
            "quality": quality,
            "duration": duration,
            "motion_mode": motion_mode,
            "aspect_ratio": aspect_ratio,
            "negative_prompt": negative_prompt,
            "sound_effect_switch": sound_effect_switch
        }

# Pestañas principales
tab1, tab2 = st.tabs(["🚀 Generar", "📂 Historial"])

with tab1:
    # Área principal de generación
    st.subheader(f"✨ Generar {content_type}")
    
    # Área principal
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("📝 Prompt")
        
        # Plantillas predefinidas
        if "Imagen" in content_type:
            templates = {
                "🎨 Arte Digital": "A stunning digital artwork featuring vibrant colors and intricate details, masterpiece quality, trending on artstation, highly detailed, 8k resolution, professional digital art, cinematic lighting, beautiful composition.",
                "📸 Fotografía Realista": "Professional photography, hyperrealistic, award-winning photo, perfect lighting, high resolution, DSLR quality, studio lighting, crisp details, commercial photography style.",
                "🌈 Estilo Fantástico": "Fantasy art style, magical atmosphere, ethereal lighting, mystical elements, enchanted environment, otherworldly beauty, epic fantasy scene, dramatic composition.",
                "🤖 Futurista/Sci-Fi": "Futuristic design, cyberpunk aesthetic, neon lights, advanced technology, sleek modern architecture, sci-fi atmosphere, digital art style, high-tech environment.",
                "� Retrato Artístico": "Professional portrait, artistic lighting, emotional expression, fine art photography, dramatic shadows, captivating eyes, artistic composition, studio quality.",
                "✨ Personalizado": ""
            }
        elif "Seedance" in content_type:
            templates = {
                "� Amanecer Épico": "Golden hour sunrise over misty mountains, cinematic camera movement, slow dolly shot revealing majestic landscape, warm lighting casting long shadows, peaceful atmosphere, nature documentary style, breathtaking vista.",
                "🏙️ Ciudad Futurista": "Futuristic cityscape at night, neon lights reflecting on wet streets, slow camera pan across towering skyscrapers, cyberpunk atmosphere, dramatic lighting, urban cinematic scene.",
                "🌊 Océano Tranquilo": "Serene ocean waves gently rolling onto pristine beach, golden sunset lighting, smooth camera tracking shot along shoreline, peaceful coastal scene, relaxing atmosphere.",
                "🎬 Escena Cinematográfica": "Professional cinematic shot with dramatic lighting, smooth camera movement, film-quality composition, artistic framing, moody atmosphere, cinematic color grading.",
                "✨ Personalizado": ""
            }
        else:  # Pixverse Anime
            templates = {
                "🎭 Escena de Acción Anime": "an anime action scene, a woman looks around slowly, mountain landscape in the background",
                "🌸 Personaje Kawaii": "a cute anime girl with big eyes, pink hair, sitting in a cherry blossom garden, gentle breeze moving her hair",
                "🏯 Paisaje Japonés": "traditional Japanese temple in anime style, sunset lighting, dramatic clouds, peaceful atmosphere",
                "⚔️ Batalla Épica": "epic anime battle scene, warriors with glowing swords, dynamic camera movement, intense lighting effects",
                "🌙 Noche Mágica": "anime magical girl under moonlight, sparkles and magical effects, flowing dress, mystical atmosphere",
                "✨ Personalizado": ""
            }
        
        selected_template = st.selectbox("🎨 Plantillas predefinidas:", list(templates.keys()))
        
        # Área de texto para el prompt
        if selected_template == "✨ Personalizado":
            prompt = st.text_area(
                "Escribe tu prompt personalizado:",
                height=150,
                placeholder="Describe detalladamente lo que quieres generar..."
            )
        else:
            prompt = st.text_area(
                f"Prompt seleccionado ({selected_template}):",
                value=templates[selected_template],
                height=150
            )
    
    with col2:
        st.header("🎛️ Panel de Control")
        
        # Información de la configuración
        st.info(f"""
        **Configuración actual:**
        - 📊 Tipo: {content_type}
        - 🎯 Plantilla: {selected_template}
        - 📏 Caracteres: {len(prompt) if prompt else 0}
        """)
        
        # Botón de generación
        if st.button("🚀 **GENERAR**", type="primary", use_container_width=True):
            if not prompt.strip():
                st.error("❌ Por favor ingresa un prompt")
            else:
                with st.spinner("⏳ Generando contenido..."):
                    try:
                        start_time = time.time()
                        start_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        
                        if "Imagen" in content_type:
                            st.info(f"🖼️ Generando imagen... Iniciado a las {start_datetime}")
                            prediction = generate_image(prompt, **params)
                            
                            # Mostrar ID de predicción
                            st.code(f"ID de predicción: {prediction.id}")
                            
                            # Esperar resultado
                            progress_bar = st.progress(0)
                            status_text = st.empty()
                            
                            timeout = 300  # 5 minutos
                            
                            while prediction.status not in ["succeeded", "failed", "canceled"]:
                                elapsed = int(time.time() - start_time)
                                if elapsed > timeout:
                                    st.error("⛔ Tiempo de espera excedido (5 minutos)")
                                    break
                                    
                                progress = min(elapsed / 120, 0.95)  # Estimar progreso
                                progress_bar.progress(progress)
                                status_text.text(f"⏱ [{elapsed}s] Estado: {prediction.status}")
                                time.sleep(2)
                                
                                try:
                                    prediction.reload()
                                except Exception as reload_error:
                                    st.error(f"❌ Error al verificar estado: {str(reload_error)}")
                                    break
                            
                            progress_bar.progress(1.0)
                            
                            if prediction.status == "succeeded":
                                st.success("✅ ¡Imagen generada exitosamente!")
                                
                                # Mostrar imagen y enlaces
                                try:
                                    if prediction.output and len(prediction.output) > 0:
                                        # Obtener la URL (manejar si es string o lista)
                                        if isinstance(prediction.output, list):
                                            image_url = prediction.output[0]
                                        elif isinstance(prediction.output, str):
                                            image_url = prediction.output
                                        else:
                                            image_url = str(prediction.output)
                                        
                                        st.write(f"🔗 **URL de la imagen:** {image_url}")
                                        
                                        # Descargar y guardar localmente
                                        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                                        filename = f"imagen_{timestamp}.{params['output_format']}"
                                        local_path = download_and_save_file(image_url, filename, "imagen")
                                        
                                        # Guardar en historial
                                        history_item = {
                                            "tipo": "imagen",
                                            "fecha": datetime.now().isoformat(),
                                            "prompt": prompt,  # Guardar prompt completo
                                            "plantilla": selected_template,
                                            "url": image_url,
                                            "archivo_local": filename if local_path else None,
                                            "parametros": params,
                                            "id_prediccion": prediction.id
                                        }
                                        save_to_history(history_item)
                                        
                                        if local_path:
                                            st.success(f"💾 Imagen guardada localmente: `{filename}`")
                                        
                                        # Botón para abrir la imagen en nueva pestaña
                                        st.markdown(f"""
                                        <a href="{image_url}" target="_blank">
                                            <button style="
                                                background-color: #ff6b6b;
                                                color: white;
                                                padding: 10px 20px;
                                                border: none;
                                                border-radius: 5px;
                                                cursor: pointer;
                                                font-size: 16px;
                                                margin: 10px 0;
                                            ">🖼️ Ver Imagen en Nueva Pestaña</button>
                                        </a>
                                        """, unsafe_allow_html=True)
                                        
                                        # Intentar mostrar la imagen directamente
                                        try:
                                            st.image(image_url, caption="Imagen generada", use_container_width=True)
                                        except Exception as img_error:
                                            st.warning(f"⚠️ No se pudo mostrar la imagen directamente: {str(img_error)}")
                                            st.info("💡 Usa el botón de arriba para ver la imagen")
                                
                                except Exception as e:
                                    st.error(f"❌ Error al procesar la imagen: {str(e)}")
                            else:
                                st.error(f"❌ La generación falló. Estado: {prediction.status}")
                        
                        elif "Seedance" in content_type:
                            st.info(f"🎬 Generando video con Seedance... Iniciado a las {start_datetime}")
                            
                            with st.spinner("🎥 Procesando video..."):
                                output = generate_video_seedance(prompt, **params)
                            
                            if output:
                                st.success("✅ ¡Video generado exitosamente!")
                                
                                # Convertir output a string URL si es un objeto FileOutput
                                if hasattr(output, 'url'):
                                    video_url = output.url
                                elif isinstance(output, str):
                                    video_url = output
                                else:
                                    video_url = str(output)
                                
                                st.write(f"🔗 **URL del video:** {video_url}")
                                
                                # Descargar y guardar localmente
                                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                                filename = f"video_seedance_{timestamp}.mp4"
                                local_path = download_and_save_file(video_url, filename, "video")
                                
                                # Guardar en historial
                                history_item = {
                                    "tipo": "video_seedance",
                                    "fecha": datetime.now().isoformat(),
                                    "prompt": prompt,  # Guardar prompt completo
                                    "plantilla": selected_template,
                                    "url": video_url,
                                    "archivo_local": filename if local_path else None,
                                    "parametros": params
                                }
                                save_to_history(history_item)
                                
                                if local_path:
                                    st.success(f"💾 Video guardado localmente: `{filename}`")
                                
                                # Botón para ver video
                                st.markdown(f"""
                                <a href="{video_url}" target="_blank">
                                    <button style="
                                        background-color: #4CAF50;
                                        color: white;
                                        padding: 10px 20px;
                                        border: none;
                                        border-radius: 5px;
                                        cursor: pointer;
                                        font-size: 16px;
                                        margin: 10px 0;
                                    ">🎬 Ver Video en Nueva Pestaña</button>
                                </a>
                                """, unsafe_allow_html=True)
                                
                                # Intentar mostrar el video directamente
                                try:
                                    st.video(video_url)
                                except Exception as vid_error:
                                    st.warning(f"⚠️ No se pudo mostrar el video directamente: {str(vid_error)}")
                                    st.info("💡 Usa el botón de arriba para ver el video")
                            else:
                                st.error("❌ No se pudo generar el video")
                        
                        else:  # Video Anime Pixverse
                            st.info(f"🎭 Generando video anime con Pixverse... Iniciado a las {start_datetime}")
                            
                            with st.spinner("🎨 Procesando video anime..."):
                                output = generate_video_pixverse(prompt, **params)
                            
                            if output:
                                st.success("✅ ¡Video anime generado exitosamente!")
                                
                                # Convertir output a string URL si es un objeto FileOutput
                                if hasattr(output, 'url'):
                                    video_url = output.url
                                elif isinstance(output, str):
                                    video_url = output
                                else:
                                    video_url = str(output)
                                
                                st.write(f"🔗 **URL del video:** {video_url}")
                                
                                # Descargar y guardar localmente
                                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                                filename = f"video_anime_{timestamp}.mp4"
                                local_path = download_and_save_file(video_url, filename, "video")
                                
                                # Guardar en historial
                                history_item = {
                                    "tipo": "video_anime",
                                    "fecha": datetime.now().isoformat(),
                                    "prompt": prompt,  # Guardar prompt completo
                                    "plantilla": selected_template,
                                    "url": video_url,
                                    "archivo_local": filename if local_path else None,
                                    "parametros": params
                                }
                                save_to_history(history_item)
                                
                                if local_path:
                                    st.success(f"💾 Video guardado localmente: `{filename}`")
                                
                                # Botón para ver video
                                st.markdown(f"""
                                <a href="{video_url}" target="_blank">
                                    <button style="
                                        background-color: #FF69B4;
                                        color: white;
                                        padding: 10px 20px;
                                        border: none;
                                        border-radius: 5px;
                                        cursor: pointer;
                                        font-size: 16px;
                                        margin: 10px 0;
                                    ">🎭 Ver Video Anime en Nueva Pestaña</button>
                                </a>
                                """, unsafe_allow_html=True)
                                
                                # Intentar mostrar el video directamente
                                try:
                                    st.video(video_url)
                                except Exception as vid_error:
                                    st.warning(f"⚠️ No se pudo mostrar el video directamente: {str(vid_error)}")
                                    st.info("💡 Usa el botón de arriba para ver el video")
                            else:
                                st.error("❌ No se pudo generar el video anime")
                    
                    except Exception as e:
                        st.error(f"❌ Error durante la generación: {str(e)}")

with tab2:
    st.header("📂 Historial de Generaciones")
    
    # Cargar historial
    history = load_history()
    
    if not history:
        st.info("📭 No hay generaciones en el historial aún.")
        st.markdown("¡Genera tu primer contenido en la pestaña **Generar**!")
    else:
        # Resumen de estadísticas globales
        st.subheader("📊 Resumen General")
        
        # Calcular estadísticas globales
        total_imagenes = len([item for item in history if item.get('tipo') == 'imagen'])
        total_videos_seedance = len([item for item in history if item.get('tipo') == 'video_seedance'])
        total_videos_anime = len([item for item in history if item.get('tipo') == 'video_anime'])
        
        # Calcular costos totales estimados
        costo_total = 0
        for item in history:
            if item['tipo'] == 'imagen':
                params = item.get('parametros', {})
                width = params.get('width', 1024)
                height = params.get('height', 1024)
                megapixels = (width * height) / 1_000_000
                cost_multiplier = max(1.0, megapixels / 1.0)
                costo_total += 0.05 * cost_multiplier
            elif item['tipo'] == 'video_seedance':
                params = item.get('parametros', {})
                duration = params.get('duration', 5)
                resolution = params.get('resolution', '1080p')
                resolution_multiplier = {'720p': 0.8, '1080p': 1.0, '1440p': 1.5}.get(resolution, 1.0)
                costo_total += duration * 0.10 * resolution_multiplier
            elif item['tipo'] == 'video_anime':
                params = item.get('parametros', {})
                duration = params.get('duration', 5)
                quality = params.get('quality', '720p')
                quality_multiplier = {'540p': 0.7, '720p': 1.0, '1080p': 1.4}.get(quality, 1.0)
                costo_total += duration * 0.08 * quality_multiplier
        
        # Mostrar métricas globales
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric("🖼️ Imágenes", total_imagenes)
        with col2:
            st.metric("🎬 Videos Seedance", total_videos_seedance)
        with col3:
            st.metric("🎭 Videos Anime", total_videos_anime)
        with col4:
            st.metric("💰 Costo Total (USD)", f"${costo_total:.2f}")
        with col5:
            st.metric("💶 Costo Total (EUR)", f"€{costo_total * 0.92:.2f}")
        
        st.divider()
        
        # Filtros
        col1, col2, col3 = st.columns(3)
        
        with col1:
            filter_type = st.selectbox(
                "Filtrar por tipo:",
                ["Todos", "imagen", "video_seedance", "video_anime"]
            )
        
        with col2:
            search_term = st.text_input("Buscar en prompts:", placeholder="Escribe para buscar...")
        
        with col3:
            st.metric("Total de generaciones", len(history))
        
        # Filtrar historial
        filtered_history = history
        
        if filter_type != "Todos":
            filtered_history = [item for item in filtered_history if item.get("tipo") == filter_type]
        
        if search_term:
            filtered_history = [
                item for item in filtered_history 
                if search_term.lower() in item.get("prompt", "").lower()
            ]
        
        st.divider()
        
        # Mostrar historial filtrado
        for i, item in enumerate(filtered_history):
            with st.expander(f"{'🖼️' if item['tipo'] == 'imagen' else '🎬' if item['tipo'] == 'video_seedance' else '🎭'} {item.get('fecha', 'Sin fecha')[:16]} - {item.get('prompt', 'Sin prompt')[:50]}..."):
                
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.write(f"**Tipo:** {item.get('tipo', 'Desconocido')}")
                    st.write(f"**Prompt completo:**")
                    st.text_area("Prompt completo", value=item.get('prompt', ''), height=100, key=f"prompt_{i}", disabled=True, label_visibility="collapsed")
                    st.write(f"**Plantilla:** {item.get('plantilla', 'N/A')}")
                    
                    if item.get('parametros'):
                        with st.expander("Ver parámetros"):
                            st.json(item['parametros'])
                    
                    # Estadísticas y métricas
                    with st.expander("📊 Estadísticas y Costos"):
                        # Calcular estadísticas según el tipo
                        if item['tipo'] == 'imagen':
                            params = item.get('parametros', {})
                            width = params.get('width', 1024)
                            height = params.get('height', 1024)
                            steps = params.get('steps', 25)
                            
                            # Cálculos para imágenes (Flux Pro)
                            megapixels = (width * height) / 1_000_000
                            
                            # Estimación de costo (precios aproximados de Replicate)
                            # Flux Pro: ~$0.05 por imagen estándar
                            cost_base = 0.05
                            cost_multiplier = max(1.0, megapixels / 1.0)  # Ajuste por resolución
                            estimated_cost = cost_base * cost_multiplier
                            
                            col1_stats, col2_stats = st.columns(2)
                            with col1_stats:
                                st.metric("📐 Resolución", f"{width}x{height}")
                                st.metric("🔍 Megapixeles", f"{megapixels:.2f} MP")
                                st.metric("⚙️ Pasos de procesamiento", steps)
                            
                            with col2_stats:
                                st.metric("💰 Costo estimado", f"${estimated_cost:.3f}")
                                st.metric("💶 Costo en EUR", f"€{estimated_cost * 0.92:.3f}")
                                aspect = f"{width/height:.2f}:1" if width >= height else f"1:{height/width:.2f}"
                                st.metric("📏 Relación de aspecto", aspect)
                        
                        elif item['tipo'] in ['video_seedance', 'video_anime']:
                            params = item.get('parametros', {})
                            duration = params.get('duration', 5)
                            
                            if item['tipo'] == 'video_seedance':
                                # Seedance pricing (aproximado)
                                fps = params.get('fps', 24)
                                resolution = params.get('resolution', '1080p')
                                
                                # Cálculo de frames totales
                                total_frames = duration * fps
                                
                                # Estimación de costo para Seedance (~$0.10 por segundo)
                                cost_per_second = 0.10
                                resolution_multiplier = {'720p': 0.8, '1080p': 1.0, '1440p': 1.5}.get(resolution, 1.0)
                                estimated_cost = duration * cost_per_second * resolution_multiplier
                                
                                col1_stats, col2_stats = st.columns(2)
                                with col1_stats:
                                    st.metric("⏱️ Duración", f"{duration}s")
                                    st.metric("🎬 Frames por segundo", fps)
                                    st.metric("📹 Resolución", resolution)
                                
                                with col2_stats:
                                    st.metric("🖼️ Total de frames", total_frames)
                                    st.metric("💰 Costo estimado", f"${estimated_cost:.3f}")
                                    st.metric("💶 Costo en EUR", f"€{estimated_cost * 0.92:.3f}")
                            
                            else:  # video_anime (Pixverse)
                                quality = params.get('quality', '720p')
                                style = params.get('style', 'anime')
                                motion_mode = params.get('motion_mode', 'normal')
                                
                                # Estimación de costo para Pixverse (~$0.08 por segundo)
                                cost_per_second = 0.08
                                quality_multiplier = {'540p': 0.7, '720p': 1.0, '1080p': 1.4}.get(quality, 1.0)
                                estimated_cost = duration * cost_per_second * quality_multiplier
                                
                                col1_stats, col2_stats = st.columns(2)
                                with col1_stats:
                                    st.metric("⏱️ Duración", f"{duration}s")
                                    st.metric("🎨 Estilo", style.title())
                                    st.metric("📹 Calidad", quality)
                                
                                with col2_stats:
                                    st.metric("🏃 Modo de movimiento", motion_mode.title())
                                    st.metric("💰 Costo estimado", f"${estimated_cost:.3f}")
                                    st.metric("💶 Costo en EUR", f"€{estimated_cost * 0.92:.3f}")
                        
                        # Información adicional común
                        st.divider()
                        fecha_obj = datetime.fromisoformat(item.get('fecha', ''))
                        tiempo_transcurrido = datetime.now() - fecha_obj
                        
                        col1_time, col2_time, col3_time = st.columns(3)
                        with col1_time:
                            st.metric("📅 Fecha de creación", fecha_obj.strftime("%d/%m/%Y"))
                        with col2_time:
                            st.metric("🕐 Hora de creación", fecha_obj.strftime("%H:%M:%S"))
                        with col3_time:
                            if tiempo_transcurrido.days > 0:
                                st.metric("⏳ Antigüedad", f"{tiempo_transcurrido.days} días")
                            else:
                                horas = tiempo_transcurrido.seconds // 3600
                                st.metric("⏳ Antigüedad", f"{horas}h ago")
                        
                        # Advertencia sobre estimaciones
                        st.info("💡 **Nota:** Los costos son estimaciones basadas en precios públicos aproximados. Los costos reales pueden variar.")
                
                with col2:
                    # Botón para ver el enlace online (Replicate)
                    if item.get('url'):
                        st.markdown(f"""
                        <a href="{item['url']}" target="_blank">
                            <button style="background-color: #ff6b6b; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; width: 100%; margin: 5px 0;">🔗 Ver Online (Replicate)</button>
                        </a>
                        """, unsafe_allow_html=True)
                    # Botón para ver el archivo local
                    if item.get('archivo_local'):
                        local_file = HISTORY_DIR / item['archivo_local']
                        if local_file.exists():
                            st.markdown(f"""
                            <a href="file/{item['archivo_local']}" target="_blank">
                                <button style="background-color: #007BFF; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; width: 100%; margin: 5px 0;">💾 Ver Local</button>
                            </a>
                            """, unsafe_allow_html=True)
                            st.success("💾 Archivo disponible localmente")
                            # Mostrar preview si es imagen
                            if item['tipo'] == 'imagen':
                                try:
                                    st.image(str(local_file), caption="Preview", use_container_width=True)
                                except:
                                    st.info("No se puede mostrar preview")
                            # Para videos, mostrar información del archivo
                            elif item['tipo'] in ['video_seedance', 'video_anime']:
                                try:
                                    file_size = local_file.stat().st_size / (1024 * 1024)  # MB
                                    st.metric("📁 Tamaño del archivo", f"{file_size:.1f} MB")
                                    st.markdown(f"""
                                    <div style="margin: 10px 0;">
                                        <small>📂 Archivo local:</small><br>
                                        <code>{item['archivo_local']}</code>
                                    </div>
                                    """, unsafe_allow_html=True)
                                except:
                                    st.info("Información del archivo no disponible")
                        else:
                            st.warning("📁 Archivo local no encontrado")
