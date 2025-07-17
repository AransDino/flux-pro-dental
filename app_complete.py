import streamlit as st
import os
import time
import replicate
import requests
from datetime import datetime
from pathlib import Path
import tempfile
import json
import base64
import traceback

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

# Función para generar stickers
def generate_sticker(prompt, **params):
    # Modificar el prompt para que sea más específico para stickers
    sticker_prompt = f"sticker design, {prompt}, clean background, cartoon style, simple design, bright colors, outlined, digital art"
    
    output = replicate.run(
        "black-forest-labs/flux-pro",
        input={
            "prompt": sticker_prompt,
            "width": 1024,
            "height": 1024,
            "num_outputs": 1,
            "guidance_scale": 7.5,
            "num_inference_steps": 50,
            "safety_tolerance": 2
        }
    )
    return output

# Función para generar imágenes con Kandinsky 2.2
def generate_kandinsky(prompt, **params):
    client = replicate.Client()
    
    prediction = client.predictions.create(
        version="ai-forever/kandinsky-2.2:ad9d7879fbffa2874e1d909d1d37d9bc682889cc65b31f7bb00d2362619f194a",
        input={
            "prompt": prompt,
            **params
        }
    )
    
    return prediction

# Función para generar con SSD-1B (LucaTaco)
def generate_ssd1b(prompt, **params):
    """
    Genera imágenes usando el modelo SSD-1B de lucataco
    """
    output = replicate.run(
        "lucataco/ssd-1b:b19e3639452c59ce8295b82aba70a231404cb062f2eb580ea894b31e8ce5bbb6",
        input={
            "prompt": prompt,
            **params
        }
    )
    return output

# Función para generar video con VEO 3 Fast
def generate_video_veo3(prompt, **params):
    """
    Genera videos usando el modelo VEO 3 Fast de Google
    """
    output = replicate.run(
        "google/veo-3-fast",
        input={
            "prompt": prompt,
            **params
        }
    )
    return output

def update_generation_stats(model, time_taken, success):
    """
    Actualiza las estadísticas de generación
    """
    stats_file = "generation_stats.json"
    
    # Cargar estadísticas existentes
    if os.path.exists(stats_file):
        with open(stats_file, "r", encoding="utf-8") as f:
            stats = json.load(f)
    else:
        stats = {}
    
    # Inicializar modelo si no existe
    if model not in stats:
        stats[model] = {
            "total": 0,
            "exitosas": 0,
            "tiempo_promedio": 0
        }
    
    # Actualizar estadísticas
    stats[model]["total"] += 1
    if success:
        stats[model]["exitosas"] += 1
    
    # Calcular tiempo promedio
    if stats[model]["tiempo_promedio"] == 0:
        stats[model]["tiempo_promedio"] = time_taken
    else:
        stats[model]["tiempo_promedio"] = (stats[model]["tiempo_promedio"] + time_taken) / 2
    
    # Guardar estadísticas
    with open(stats_file, "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)

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
        ["🖼️ Imagen (Flux Pro)", "🎨 Imagen (Kandinsky 2.2)", "⚡ Imagen (SSD-1B)", "🎬 Video (Seedance)", "🎭 Video Anime (Pixverse)", "🚀 Video (VEO 3 Fast)", "🏷️ Sticker (Flux Pro)"],
        help="Selecciona el tipo de contenido que quieres generar"
    )
    
    st.divider()
    
    # Configuración según el tipo
    if "Flux Pro" in content_type:
        st.subheader("📸 Parámetros de Imagen (Flux Pro)")
        
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
    
    elif "Kandinsky" in content_type:
        st.subheader("🎨 Parámetros de Imagen (Kandinsky 2.2)")
        
        col1, col2 = st.columns(2)
        with col1:
            width = st.selectbox("Ancho", [512, 768, 1024, 1280], index=2)
            num_inference_steps = st.slider("Pasos de inferencia", min_value=10, max_value=100, value=75, help="Más pasos = mejor calidad")
        
        with col2:
            height = st.selectbox("Alto", [512, 768, 1024, 1280], index=2)
            num_inference_steps_prior = st.slider("Pasos prior", min_value=10, max_value=50, value=25, help="Pasos del modelo prior")
        
        output_format = st.selectbox("Formato de salida", ["webp", "png", "jpg"], index=0)
        
        params = {
            "width": width,
            "height": height,
            "num_outputs": 1,
            "output_format": output_format,
            "num_inference_steps": num_inference_steps,
            "num_inference_steps_prior": num_inference_steps_prior
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
    
    elif "Pixverse" in content_type:  # Video Anime Pixverse
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
    
    elif "SSD-1B" in content_type:
        st.subheader("⚡ Parámetros de Imagen (SSD-1B)")
        
        col1, col2 = st.columns(2)
        with col1:
            width = st.selectbox("Ancho", [512, 768, 1024, 1280], index=1)  # Default 768
            seed = st.number_input("Seed", min_value=0, max_value=999999999999, value=36446545872, help="Semilla para reproducibilidad")
            scheduler = st.selectbox("Scheduler", ["K_EULER", "DPMSolverMultistep", "HeunDiscrete", "DDIM"], index=0)
        
        with col2:
            height = st.selectbox("Alto", [512, 768, 1024, 1280], index=1)  # Default 768
            guidance_scale = st.slider("Guidance Scale", min_value=1, max_value=20, value=9, help="Fuerza del guidance")
            num_inference_steps = st.slider("Pasos de inferencia", min_value=10, max_value=50, value=25, help="Más pasos = mejor calidad")
        
        col3, col4 = st.columns(2)
        with col3:
            lora_scale = st.slider("LoRA Scale", min_value=0.0, max_value=1.0, value=0.6, step=0.1, help="Intensidad del LoRA")
            prompt_strength = st.slider("Prompt Strength", min_value=0.0, max_value=1.0, value=0.8, step=0.1, help="Fuerza del prompt")
        
        with col4:
            apply_watermark = st.checkbox("Aplicar marca de agua", value=True)
            batched_prompt = st.checkbox("Prompt por lotes", value=False)
        
        # Prompt negativo
        negative_prompt = st.text_area("Prompt negativo (opcional):", 
                                     value="scary, cartoon, painting", 
                                     height=60,
                                     help="Elementos que NO quieres en la imagen")
        
        params = {
            "seed": seed,
            "width": width,
            "height": height,
            "scheduler": scheduler,
            "lora_scale": lora_scale,
            "num_outputs": 1,
            "batched_prompt": batched_prompt,
            "guidance_scale": guidance_scale,
            "apply_watermark": apply_watermark,
            "negative_prompt": negative_prompt,
            "prompt_strength": prompt_strength,
            "num_inference_steps": num_inference_steps
        }
        
    elif "VEO 3 Fast" in content_type:  # Video VEO 3 Fast
        st.subheader("🚀 Parámetros de Video (VEO 3 Fast)")
        
        col1, col2 = st.columns(2)
        with col1:
            duration = st.slider("Duración (seg)", min_value=2, max_value=8, value=5, help="Duración del video")
            aspect_ratio = st.selectbox("Relación de aspecto", ["16:9", "9:16", "1:1"], index=0)
        
        with col2:
            enhance_prompt = st.checkbox("Mejorar prompt automáticamente", value=True, help="VEO 3 Fast mejorará automáticamente tu prompt")
            quality = st.selectbox("Calidad", ["standard", "high"], index=1)
        
        # Configuraciones avanzadas
        with st.expander("🔧 Configuraciones avanzadas"):
            camera_motion = st.selectbox("Movimiento de cámara", ["static", "pan", "zoom", "dolly"], index=0)
            motion_intensity = st.slider("Intensidad de movimiento", min_value=0.1, max_value=1.0, value=0.5, step=0.1)
        
        params = {
            "duration": duration,
            "aspect_ratio": aspect_ratio,
            "enhance_prompt": enhance_prompt,
            "quality": quality,
            "camera_motion": camera_motion,
            "motion_intensity": motion_intensity
        }
        
    else:  # Stickers Flux Pro
        st.subheader("📎 Parámetros de Sticker")
        
        # Parámetros fijos para stickers
        params = {
            "width": 1024,
            "height": 1024,
            "num_outputs": 1,
            "guidance_scale": 7.5,
            "num_inference_steps": 50,
            "safety_tolerance": 2
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
        if "Flux Pro" in content_type:
            templates = {
                "🎨 Arte Digital": "A stunning digital artwork featuring vibrant colors and intricate details, masterpiece quality, trending on artstation, highly detailed, 8k resolution, professional digital art, cinematic lighting, beautiful composition.",
                "📸 Fotografía Realista": "Professional photography, hyperrealistic, award-winning photo, perfect lighting, high resolution, DSLR quality, studio lighting, crisp details, commercial photography style.",
                "🌈 Estilo Fantástico": "Fantasy art style, magical atmosphere, ethereal lighting, mystical elements, enchanted environment, otherworldly beauty, epic fantasy scene, dramatic composition.",
                "🤖 Futurista/Sci-Fi": "Futuristic design, cyberpunk aesthetic, neon lights, advanced technology, sleek modern architecture, sci-fi atmosphere, digital art style, high-tech environment.",
                "👤 Retrato Artístico": "Professional portrait, artistic lighting, emotional expression, fine art photography, dramatic shadows, captivating eyes, artistic composition, studio quality.",
                "✨ Personalizado": ""
            }
        elif "Kandinsky" in content_type:
            templates = {
                "🎨 Arte Abstracto": "Abstract art with flowing forms, vivid colors, dynamic composition, expressive brushstrokes, modern art style, contemporary aesthetic, artistic masterpiece.",
                "🌈 Paisaje Onírico": "Dreamlike landscape with surreal elements, soft pastel colors, floating objects, magical atmosphere, fantastical environment, artistic interpretation.",
                "🖼️ Estilo Clásico": "Classical art style, renaissance painting technique, detailed composition, traditional art, museum quality, masterful brushwork, timeless beauty.",
                "🌸 Arte Japonés": "Japanese art style, traditional aesthetic, delicate details, harmonious composition, zen atmosphere, cultural elements, artistic elegance.",
                "🌟 Surrealismo": "Surrealist art style, impossible scenes, dream-like imagery, unexpected combinations, artistic vision, creative interpretation, imaginative composition.",
                "✨ Personalizado": ""
            }
        elif "Seedance" in content_type:
            templates = {
                "🌅 Amanecer Épico": "Golden hour sunrise over misty mountains, cinematic camera movement, slow dolly shot revealing majestic landscape, warm lighting casting long shadows, peaceful atmosphere, nature documentary style, breathtaking vista.",
                "🏙️ Ciudad Futurista": "Futuristic cityscape at night, neon lights reflecting on wet streets, slow camera pan across towering skyscrapers, cyberpunk atmosphere, dramatic lighting, urban cinematic scene.",
                "🌊 Océano Tranquilo": "Serene ocean waves gently rolling onto pristine beach, golden sunset lighting, smooth camera tracking shot along shoreline, peaceful coastal scene, relaxing atmosphere.",
                "🎬 Escena Cinematográfica": "Professional cinematic shot with dramatic lighting, smooth camera movement, film-quality composition, artistic framing, moody atmosphere, cinematic color grading.",
                "✨ Personalizado": ""
            }
        elif "Pixverse" in content_type:
            templates = {
                "🎭 Escena de Acción Anime": "an anime action scene, a woman looks around slowly, mountain landscape in the background",
                "🌸 Personaje Kawaii": "a cute anime girl with big eyes, pink hair, sitting in a cherry blossom garden, gentle breeze moving her hair",
                "🏯 Paisaje Japonés": "traditional Japanese temple in anime style, sunset lighting, dramatic clouds, peaceful atmosphere",
                "⚔️ Batalla Épica": "epic anime battle scene, warriors with glowing swords, dynamic camera movement, intense lighting effects",
                "🌙 Noche Mágica": "anime magical girl under moonlight, sparkles and magical effects, flowing dress, mystical atmosphere",
                "✨ Personalizado": ""
            }
        elif "SSD-1B" in content_type:
            templates = {
                "🔥 Fantasía Épica": "epic fantasy creature, dramatic lighting, ultra realistic details, cinematic composition, dark fantasy atmosphere, vibrant colors, professional digital art",
                "🌪️ Elementos Naturales": "with smoke, half ice and half fire and ultra realistic in detail, dramatic contrast, elemental powers, cinematic lighting, vibrant effects",
                "🦅 Vida Salvaje": "majestic wild animal, ultra realistic detail, wildlife photography style, natural habitat, dramatic lighting, vibrant colors, cinematic composition",
                "🖤 Arte Oscuro": "dark fantasy art, mysterious atmosphere, dramatic shadows, gothic elements, ultra realistic details, cinematic lighting, professional artwork",
                "⚡ Efectos Dinámicos": "dynamic energy effects, lightning, fire, smoke, ultra realistic rendering, cinematic composition, vibrant colors, dramatic atmosphere",
                "✨ Personalizado": ""
            }
        elif "VEO 3 Fast" in content_type:
            templates = {
                "🏃 Acción Épica": "A superhero running at incredible speed through a bustling city, leaving trails of light behind, cars and people blur as the hero moves, dynamic camera following the action, cinematic lighting, epic scale",
                "🌊 Naturaleza Cinematográfica": "Ocean waves crashing against dramatic cliffs during golden hour, seagulls flying overhead, camera slowly panning to reveal the vast coastline, breathtaking natural beauty, cinematic quality",
                "🚗 Persecución Urbana": "High-speed chase through neon-lit streets at night, cars weaving through traffic, dramatic lighting from street lamps, rain reflecting on wet pavement, action movie style",
                "🦋 Transformación Mágica": "A caterpillar transforming into a butterfly in extreme slow motion, magical particles floating around, nature documentary style with macro cinematography",
                "🎭 Drama Emocional": "Close-up of a person's face showing deep emotion, tears slowly falling, soft lighting, intimate moment captured with cinematic depth",
                "✨ Personalizado": ""
            }
        else:  # Stickers Flux Pro
            templates = {
                "🌟 Sticker Brillante": "a shiny, colorful star sticker, cartoon style, bright and cheerful, with a glossy finish",
                "❤️ Corazón Colorido": "a vibrant, multi-colored heart sticker, cartoon style, with a glossy shine",
                "🐶 Perro Kawaii": "a cute, cartoon-style dog sticker, big eyes, smiling, with a colorful collar",
                "🍕 Pizza Divertida": "a fun, cartoon-style pizza slice sticker, with exaggerated toppings and a smiling face",
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
                        
                        if "Flux Pro" in content_type:
                            st.info(f"🖼️ Generando imagen con Flux Pro... Iniciado a las {start_datetime}")
                            prediction = generate_image(prompt, **params)
                            
                            # Mostrar ID de predicción
                            st.code(f"ID de predicción: {prediction.id}")
                            
                            # Esperar resultado con progress bar
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
                                            "prompt": prompt,
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
                        
                        elif "Kandinsky" in content_type:
                            st.info(f"🎨 Generando imagen con Kandinsky 2.2... Iniciado a las {start_datetime}")
                            prediction = generate_kandinsky(prompt, **params)
                            
                            # Mostrar ID de predicción
                            st.code(f"ID de predicción: {prediction.id}")
                            
                            # Esperar resultado con progress bar
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
                                
                                # Procesar resultado
                                try:
                                    if prediction.output:
                                        image_url = prediction.output[0] if isinstance(prediction.output, list) else prediction.output
                                        st.write(f"🔗 **URL de la imagen:** {image_url}")
                                        
                                        # Descargar y guardar localmente
                                        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                                        filename = f"kandinsky_{timestamp}.jpg"
                                        local_path = download_and_save_file(image_url, filename, "imagen")
                                        
                                        # Guardar en historial
                                        history_item = {
                                            "tipo": "imagen",
                                            "fecha": datetime.now().isoformat(),
                                            "prompt": prompt,
                                            "plantilla": selected_template,
                                            "url": image_url,
                                            "archivo_local": filename if local_path else None,
                                            "parametros": params,
                                            "id_prediccion": prediction.id
                                        }
                                        save_to_history(history_item)
                                        
                                        if local_path:
                                            st.success(f"💾 Imagen guardada localmente: `{filename}`")
                                        
                                        # Botón para abrir en nueva pestaña
                                        st.markdown(f"""
                                        <a href="{image_url}" target="_blank">
                                            <button style="
                                                background-color: #4CAF50;
                                                color: white;
                                                padding: 10px 20px;
                                                border: none;
                                                border-radius: 5px;
                                                cursor: pointer;
                                                font-size: 16px;
                                                margin: 10px 0;
                                            ">🎨 Ver Imagen en Nueva Pestaña</button>
                                        </a>
                                        """, unsafe_allow_html=True)
                                        
                                        # Mostrar imagen
                                        try:
                                            st.image(image_url, caption="Imagen generada con Kandinsky", use_container_width=True)
                                        except Exception as img_error:
                                            st.warning(f"⚠️ No se pudo mostrar la imagen directamente: {str(img_error)}")
                                            st.info("💡 Usa el botón de arriba para ver la imagen")
                                
                                except Exception as e:
                                    st.error(f"❌ Error al procesar la imagen: {str(e)}")
                            else:
                                st.error(f"❌ La generación falló. Estado: {prediction.status}")
                        
                        elif "SSD-1B" in content_type:
                            st.info(f"⚡ Generando imagen rápida con SSD-1B... Iniciado a las {start_datetime}")
                            
                            # SSD-1B es muy rápido, no necesita progress bar compleja
                            with st.spinner("🚀 Generando imagen rápida..."):
                                try:
                                    prediction = generate_ssd1b(prompt, **params)
                                    st.code(f"ID de predicción: {prediction.id}")
                                    
                                    # Esperar resultado (debería ser muy rápido)
                                    timeout = 60  # 1 minuto
                                    while prediction.status not in ["succeeded", "failed", "canceled"]:
                                        elapsed = int(time.time() - start_time)
                                        if elapsed > timeout:
                                            st.error("⛔ Tiempo de espera excedido")
                                            break
                                        time.sleep(1)
                                        prediction.reload()
                                    
                                    if prediction.status == "succeeded":
                                        st.success("⚡ ¡Imagen generada exitosamente!")
                                        
                                        if prediction.output:
                                            image_url = prediction.output[0] if isinstance(prediction.output, list) else prediction.output
                                            st.write(f"🔗 **URL de la imagen:** {image_url}")
                                            
                                            # Descargar y guardar
                                            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                                            filename = f"ssd_{timestamp}.jpg"
                                            local_path = download_and_save_file(image_url, filename, "imagen")
                                            
                                            # Guardar en historial
                                            history_item = {
                                                "tipo": "imagen",
                                                "fecha": datetime.now().isoformat(),
                                                "prompt": prompt,
                                                "plantilla": selected_template,
                                                "url": image_url,
                                                "archivo_local": filename if local_path else None,
                                                "parametros": params,
                                                "id_prediccion": prediction.id
                                            }
                                            save_to_history(history_item)
                                            
                                            if local_path:
                                                st.success(f"💾 Imagen guardada: `{filename}`")
                                            
                                            # Mostrar imagen
                                            st.image(image_url, caption="Imagen SSD-1B", use_container_width=True)
                                    else:
                                        st.error(f"❌ Error en SSD-1B: {prediction.status}")
                                
                                except Exception as e:
                                    st.error(f"❌ Error con SSD-1B: {str(e)}")
                        
                        elif "Seedance" in content_type:
                            st.info(f"💃 Generando con Seedance... Iniciado a las {start_datetime}")
                            
                            with st.spinner("💃 Procesando con Seedance..."):
                                try:
                                    prediction = generate_video_seedance(prompt, **params)
                                    st.code(f"ID de predicción: {prediction.id}")
                                    
                                    timeout = 180  # 3 minutos
                                    while prediction.status not in ["succeeded", "failed", "canceled"]:
                                        elapsed = int(time.time() - start_time)
                                        if elapsed > timeout:
                                            st.error("⛔ Tiempo de espera excedido")
                                            break
                                        time.sleep(2)
                                        prediction.reload()
                                    
                                    if prediction.status == "succeeded":
                                        st.success("💃 ¡Generación exitosa!")
                                        
                                        if prediction.output:
                                            result_url = prediction.output[0] if isinstance(prediction.output, list) else prediction.output
                                            st.write(f"🔗 **URL del resultado:** {result_url}")
                                            
                                            # Determinar tipo de archivo
                                            file_ext = "jpg"
                                            if result_url.lower().endswith(('.mp4', '.mov')):
                                                file_ext = "mp4"
                                            
                                            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                                            filename = f"seedance_{timestamp}.{file_ext}"
                                            local_path = download_and_save_file(result_url, filename, "media")
                                            
                                            # Guardar en historial
                                            history_item = {
                                                "tipo": "media",
                                                "fecha": datetime.now().isoformat(),
                                                "prompt": prompt,
                                                "plantilla": selected_template,
                                                "url": result_url,
                                                "archivo_local": filename if local_path else None,
                                                "parametros": params,
                                                "id_prediccion": prediction.id
                                            }
                                            save_to_history(history_item)
                                            
                                            if local_path:
                                                st.success(f"💾 Archivo guardado: `{filename}`")
                                            
                                            # Mostrar según tipo
                                            if file_ext == "mp4":
                                                st.video(result_url)
                                            else:
                                                st.image(result_url, caption="Resultado Seedance", use_container_width=True)
                                    else:
                                        st.error(f"❌ Error en Seedance: {prediction.status}")
                                
                                except Exception as e:
                                    st.error(f"❌ Error con Seedance: {str(e)}")
                        
                        elif "Pixverse" in content_type:
                            st.info(f"🎬 Generando video con Pixverse... Iniciado a las {start_datetime}")
                            
                            progress_bar = st.progress(0)
                            status_text = st.empty()
                            
                            try:
                                prediction = generate_video_pixverse(prompt, **params)
                                st.code(f"ID de predicción: {prediction.id}")
                                
                                timeout = 600  # 10 minutos para video
                                
                                while prediction.status not in ["succeeded", "failed", "canceled"]:
                                    elapsed = int(time.time() - start_time)
                                    if elapsed > timeout:
                                        st.error("⛔ Tiempo de espera excedido (10 minutos)")
                                        break
                                        
                                    progress = min(elapsed / 300, 0.95)  # Estimar progreso
                                    progress_bar.progress(progress)
                                    status_text.text(f"⏱ [{elapsed}s] Estado: {prediction.status}")
                                    time.sleep(3)
                                    
                                    try:
                                        prediction.reload()
                                    except Exception as reload_error:
                                        st.error(f"❌ Error al verificar estado: {str(reload_error)}")
                                        break
                                
                                progress_bar.progress(1.0)
                                
                                if prediction.status == "succeeded":
                                    st.success("🎬 ¡Video generado exitosamente!")
                                    
                                    if prediction.output:
                                        video_url = prediction.output[0] if isinstance(prediction.output, list) else prediction.output
                                        st.write(f"🔗 **URL del video:** {video_url}")
                                        
                                        # Descargar video
                                        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                                        filename = f"pixverse_{timestamp}.mp4"
                                        local_path = download_and_save_file(video_url, filename, "video")
                                        
                                        # Guardar en historial
                                        history_item = {
                                            "tipo": "video",
                                            "fecha": datetime.now().isoformat(),
                                            "prompt": prompt,
                                            "plantilla": selected_template,
                                            "url": video_url,
                                            "archivo_local": filename if local_path else None,
                                            "parametros": params,
                                            "id_prediccion": prediction.id
                                        }
                                        save_to_history(history_item)
                                        
                                        if local_path:
                                            st.success(f"💾 Video guardado: `{filename}`")
                                        
                                        # Mostrar video
                                        st.video(video_url)
                                else:
                                    st.error(f"❌ Error en Pixverse: {prediction.status}")
                            
                            except Exception as e:
                                st.error(f"❌ Error con Pixverse: {str(e)}")
                        
                        elif "VEO 3 Fast" in content_type:
                            st.info(f"🚀 Generando video con VEO 3 Fast... Iniciado a las {start_datetime}")
                            
                            progress_bar = st.progress(0)
                            status_text = st.empty()
                            
                            try:
                                prediction = generate_video_veo3(prompt, **params)
                                st.code(f"ID de predicción: {prediction.id}")
                                
                                timeout = 600  # 10 minutos para video
                                
                                while prediction.status not in ["succeeded", "failed", "canceled"]:
                                    elapsed = int(time.time() - start_time)
                                    if elapsed > timeout:
                                        st.error("⛔ Tiempo de espera excedido (10 minutos)")
                                        break
                                        
                                    progress = min(elapsed / 240, 0.95)  # VEO 3 Fast es más rápido
                                    progress_bar.progress(progress)
                                    status_text.text(f"⏱ [{elapsed}s] Estado: {prediction.status}")
                                    time.sleep(3)
                                    
                                    try:
                                        prediction.reload()
                                    except Exception as reload_error:
                                        st.error(f"❌ Error al verificar estado: {str(reload_error)}")
                                        break
                                
                                progress_bar.progress(1.0)
                                
                                if prediction.status == "succeeded":
                                    st.success("🚀 ¡Video VEO 3 Fast generado exitosamente!")
                                    
                                    if prediction.output:
                                        video_url = prediction.output
                                        st.write(f"🔗 **URL del video:** {video_url}")
                                        
                                        # Descargar video
                                        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                                        filename = f"veo3_{timestamp}.mp4"
                                        local_path = download_and_save_file(video_url, filename, "video")
                                        
                                        # Guardar en historial
                                        history_item = {
                                            "tipo": "video",
                                            "fecha": datetime.now().isoformat(),
                                            "prompt": prompt,
                                            "plantilla": selected_template,
                                            "url": video_url,
                                            "archivo_local": filename if local_path else None,
                                            "parametros": params,
                                            "id_prediccion": prediction.id,
                                            "modelo": "VEO 3 Fast"
                                        }
                                        save_to_history(history_item)
                                        
                                        if local_path:
                                            st.success(f"💾 Video guardado: `{filename}`")
                                        
                                        # Mostrar video con información adicional
                                        st.video(video_url)
                                        
                                        # Información técnica
                                        st.info("📊 **VEO 3 Fast**: Modelo de última generación para generación rápida de videos de alta calidad")
                                        
                                else:
                                    st.error(f"❌ Error en VEO 3 Fast: {prediction.status}")
                            
                            except Exception as e:
                                st.error(f"❌ Error con VEO 3 Fast: {str(e)}")
                        
                        elif "Stickers" in content_type:
                            st.info(f"🏷️ Generando sticker... Iniciado a las {start_datetime}")
                            
                            with st.spinner("🏷️ Generando sticker..."):
                                try:
                                    prediction = generate_sticker(prompt, **params)
                                    st.code(f"ID de predicción: {prediction.id}")
                                    
                                    timeout = 120  # 2 minutos
                                    while prediction.status not in ["succeeded", "failed", "canceled"]:
                                        elapsed = int(time.time() - start_time)
                                        if elapsed > timeout:
                                            st.error("⛔ Tiempo de espera excedido")
                                            break
                                        time.sleep(2)
                                        prediction.reload()
                                    
                                    if prediction.status == "succeeded":
                                        st.success("🏷️ ¡Sticker generado exitosamente!")
                                        
                                        if prediction.output:
                                            sticker_url = prediction.output[0] if isinstance(prediction.output, list) else prediction.output
                                            st.write(f"🔗 **URL del sticker:** {sticker_url}")
                                            
                                            # Descargar sticker
                                            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                                            filename = f"sticker_{timestamp}.png"
                                            local_path = download_and_save_file(sticker_url, filename, "sticker")
                                            
                                            # Guardar en historial
                                            history_item = {
                                                "tipo": "sticker",
                                                "fecha": datetime.now().isoformat(),
                                                "prompt": prompt,
                                                "plantilla": selected_template,
                                                "url": sticker_url,
                                                "archivo_local": filename if local_path else None,
                                                "parametros": params,
                                                "id_prediccion": prediction.id
                                            }
                                            save_to_history(history_item)
                                            
                                            if local_path:
                                                st.success(f"💾 Sticker guardado: `{filename}`")
                                            
                                            # Mostrar sticker
                                            st.image(sticker_url, caption="Sticker generado", use_container_width=True)
                                    else:
                                        st.error(f"❌ Error en Stickers: {prediction.status}")
                                
                                except Exception as e:
                                    st.error(f"❌ Error con Stickers: {str(e)}")
                        
                        # Estadísticas finales
                        end_time = time.time()
                        total_time = end_time - start_time
                        end_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        
                        st.success(f"⏱️ **Proceso completado en {total_time:.1f} segundos**")
                        st.info(f"🕐 **Inicio:** {start_datetime} | **Fin:** {end_datetime}")
                        
                        # Actualizar estadísticas globales
                        update_generation_stats(content_type, total_time, prediction.status == "succeeded")

                    except Exception as e:
                        st.error(f"❌ Error durante la generación: {str(e)}")
                        st.error(f"🔍 Detalles del error: {type(e).__name__}")
                        st.code(traceback.format_exc())

        # Información adicional en la barra lateral
        with st.sidebar:
            st.header("📊 Información")
            
            # Estadísticas de uso
            if os.path.exists("generation_stats.json"):
                with open("generation_stats.json", "r", encoding="utf-8") as f:
                    stats = json.load(f)
                
                st.subheader("📈 Estadísticas")
                for model, data in stats.items():
                    success_rate = (data["exitosas"] / data["total"] * 100) if data["total"] > 0 else 0
                    st.write(f"**{model}:**")
                    st.write(f"- Total: {data['total']}")
                    st.write(f"- Exitosas: {data['exitosas']}")
                    st.write(f"- Éxito: {success_rate:.1f}%")
                    if data["tiempo_promedio"] > 0:
                        st.write(f"- Tiempo promedio: {data['tiempo_promedio']:.1f}s")
                    st.write("---")
            
            # Enlaces útiles
            st.subheader("🔗 Enlaces")
            st.markdown("[📚 Documentación Flux Pro](https://replicate.com/black-forest-labs/flux-pro)")
            st.markdown("[🎨 Documentación Kandinsky](https://replicate.com/ai-forever/kandinsky-2.2)")
            st.markdown("[⚡ Documentación SSD-1B](https://replicate.com/lucataco/realvisxl-v4.0-lightning)")
            st.markdown("[💃 Documentación Seedance](https://replicate.com/fofr/realvisxl-v4.0)")
            st.markdown("[🎬 Documentación Pixverse](https://replicate.com/pixverse/pixverse-v1.8)")
            st.markdown("[🚀 Documentación VEO 3 Fast](https://replicate.com/fofr/veo-3-fast)")
            st.markdown("[🏷️ Documentación Stickers](https://replicate.com/fofr/sticker-maker)")

# Sección de historial
with tab2:
    st.header("📚 Historial de Generaciones")
    
    history = load_history()
    
    if history:
        # Opciones de filtrado
        col1, col2, col3 = st.columns(3)
        with col1:
            filter_type = st.selectbox("Filtrar por tipo:", ["Todos", "imagen", "video", "sticker", "media"])
        with col2:
            filter_date = st.date_input("Filtrar por fecha:", value=None)
        with col3:
            show_count = st.slider("Mostrar últimos:", 5, 50, 20)
        
        # Aplicar filtros
        filtered_history = history.copy()
        
        if filter_type != "Todos":
            filtered_history = [item for item in filtered_history if item.get("tipo") == filter_type]
        
        if filter_date:
            filter_date_str = filter_date.strftime('%Y-%m-%d')
            filtered_history = [item for item in filtered_history if item.get("fecha", "").startswith(filter_date_str)]
        
        # Ordenar por fecha (más reciente primero)
        filtered_history.sort(key=lambda x: x.get("fecha", ""), reverse=True)
        
        # Mostrar elementos del historial
        for i, item in enumerate(filtered_history[:show_count]):
            with st.expander(f"{i+1}. {item.get('tipo', 'Unknown').title()} - {item.get('fecha', 'Sin fecha')[:16]}"):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.write(f"**Prompt:** {item.get('prompt', 'Sin prompt')}")
                    st.write(f"**Plantilla:** {item.get('plantilla', 'Sin plantilla')}")
                    if item.get('url'):
                        st.write(f"**URL:** {item['url']}")
                    if item.get('archivo_local'):
                        st.write(f"**Archivo local:** `{item['archivo_local']}`")
                    if item.get('id_prediccion'):
                        st.code(f"ID: {item['id_prediccion']}")
                
                with col2:
                    # Mostrar preview si es posible
                    if item.get('url'):
                        try:
                            if item.get('tipo') in ['imagen', 'sticker']:
                                st.image(item['url'], width=150)
                            elif item.get('tipo') in ['video']:
                                st.video(item['url'])
                        except:
                            st.write("🖼️ Preview no disponible")
                    
                    # Botón para abrir en nueva pestaña
                    if item.get('url'):
                        st.markdown(f"""
                        <a href="{item['url']}" target="_blank">
                            <button style="
                                background-color: #007bff;
                                color: white;
                                padding: 5px 10px;
                                border: none;
                                border-radius: 3px;
                                cursor: pointer;
                                font-size: 12px;
                            ">🔗 Abrir</button>
                        </a>
                        """, unsafe_allow_html=True)
    else:
        st.info("📝 No hay elementos en el historial aún.")
