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
        history = load_history()
        history.insert(0, item)  # Añadir al principio
        
        # Mantener solo los últimos 100 elementos
        history = history[:100]
        
        with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
    except Exception as e:
        st.error(f"Error al guardar historial: {str(e)}")

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
st.title("🦷 Flux Pro Generator")
st.markdown("### Generador de imágenes y videos dentales con IA")

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
                "🦷 Dental Clásico": "A hyper-realistic 3D dental illustration showing a top view of the lower dental arch with multiple inlays and onlays placed in molars. The gum tissue and all surrounding teeth are anatomically accurate with realistic textures. Several premolars and molars have visible ceramic restorations perfectly fitted into prepared cavities — demonstrating different types of indirect dental restorations. High detail on enamel, restoration surfaces, and gum tissue. Clean white or neutral background. Medical-grade rendering, ideal for dental education and clinical presentations.",
                "🔬 Instrumental Dental": "Close-up macro photography of dental instruments on a sterile stainless steel tray. Gleaming dental mirrors, probes, and scalers arranged precisely. Soft medical lighting creates blue and silver reflections on the polished surfaces. Shallow depth of field with a clean, clinical background.",
                "🏥 Consultorio Moderno": "Modern dental office interior with sleek orange dental chairs, large windows with natural light, contemporary design elements, clean white surfaces, advanced dental equipment, professional medical atmosphere, architectural photography style.",
                "✨ Personalizado": ""
            }
        elif "Seedance" in content_type:
            templates = {
                "🌊 Clínica Oceánica": "El sol de la mañana entra en cascada a través de enormes cristaleras con vistas al océano. [Toma en travelling suave a ras de suelo] El reflejo dorado del amanecer se desliza sobre el suelo pulido mientras la cámara sigue las ruedas de un taburete dental que se empuja lentamente hacia un sillón naranja. [Dolly lento hacia arriba] El sillón se ilumina con luz cálida; gotas microscópicas de desinfectante brillan como rocío.",
                "🦷 Procedimiento Dental": "Close-up cinematic shot of a dental procedure. Slow motion water droplets from dental cleaning equipment. Professional hands working with precision instruments. Dramatic lighting highlighting the medical precision.",
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
                                            "prompt": prompt[:100] + "..." if len(prompt) > 100 else prompt,
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
                                video_url = output
                                st.write(f"🔗 **URL del video:** {video_url}")
                                
                                # Descargar y guardar localmente
                                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                                filename = f"video_seedance_{timestamp}.mp4"
                                local_path = download_and_save_file(video_url, filename, "video")
                                
                                # Guardar en historial
                                history_item = {
                                    "tipo": "video_seedance",
                                    "fecha": datetime.now().isoformat(),
                                    "prompt": prompt[:100] + "..." if len(prompt) > 100 else prompt,
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
                                video_url = output
                                st.write(f"🔗 **URL del video:** {video_url}")
                                
                                # Descargar y guardar localmente
                                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                                filename = f"video_anime_{timestamp}.mp4"
                                local_path = download_and_save_file(video_url, filename, "video")
                                
                                # Guardar en historial
                                history_item = {
                                    "tipo": "video_anime",
                                    "fecha": datetime.now().isoformat(),
                                    "prompt": prompt[:100] + "..." if len(prompt) > 100 else prompt,
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
                    st.text_area("", value=item.get('prompt', ''), height=100, key=f"prompt_{i}", disabled=True)
                    st.write(f"**Plantilla:** {item.get('plantilla', 'N/A')}")
                    
                    if item.get('parametros'):
                        with st.expander("Ver parámetros"):
                            st.json(item['parametros'])
                
                with col2:
                    if item.get('url'):
                        st.markdown(f"""
                        <a href="{item['url']}" target="_blank">
                            <button style="
                                background-color: #007BFF;
                                color: white;
                                padding: 8px 16px;
                                border: none;
                                border-radius: 5px;
                                cursor: pointer;
                                width: 100%;
                                margin: 5px 0;
                            ">🔗 Ver Original</button>
                        </a>
                        """, unsafe_allow_html=True)
                    
                    if item.get('archivo_local'):
                        local_file = HISTORY_DIR / item['archivo_local']
                        if local_file.exists():
                            st.success("💾 Archivo disponible localmente")
                            
                            # Mostrar preview si es imagen
                            if item['tipo'] == 'imagen':
                                try:
                                    st.image(str(local_file), caption="Preview", use_container_width=True)
                                except:
                                    st.info("No se puede mostrar preview")
                        else:
                            st.warning("📁 Archivo local no encontrado")
