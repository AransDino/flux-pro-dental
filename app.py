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

# Importar funciones utilitarias centralizadas
from utils import (
    load_history, save_to_history, calculate_item_cost, 
    load_replicate_token, download_and_save_file, get_logo_base64,
    HISTORY_DIR, HISTORY_FILE, COST_RATES
)

# Configurar la página
st.set_page_config(
    page_title="🦷 Ai Models Pro Generator - by Ayoze Benítez",
    page_icon="🦷",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Funciones eliminadas - ahora importadas de utils.py:
# - load_history()
# - save_to_history() 
# - download_and_save_file()
# - calculate_item_cost()
# - load_config() -> load_replicate_token()

# Función eliminada - load_config() ahora es load_replicate_token() en utils.py

# Función eliminada - get_logo_base64() ahora en utils.py

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

# Tarifas eliminadas - ahora importadas de utils.py

# Función calculate_item_cost eliminada - ahora importada de utils.py

# Inicializar estado de sesión para navegación
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'generator'

if 'selected_item_index' not in st.session_state:
    st.session_state.selected_item_index = None

# Header con título y botón de biblioteca
header_col1, header_col2 = st.columns([4, 1])

with header_col1:
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
    
    if st.session_state.current_page == 'generator':
        st.markdown("### Generador de contenido con modelos de IA avanzados")
    else:
        st.markdown("### Biblioteca de contenido generado")

with header_col2:
    st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
    
    if st.session_state.current_page == 'generator':
        if st.button("📚 Biblioteca", type="secondary", use_container_width=True):
            st.session_state.current_page = 'biblioteca'
            st.rerun()
    else:
        if st.button("🚀 Generador", type="secondary", use_container_width=True):
            st.session_state.current_page = 'generator'
            st.rerun()

# Verificar configuración
token = load_replicate_token()
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
            style = st.selectbox("Estilo", ["None", "anime", "3d_animation", "clay", "cyberpunk", "comic"], index=1)
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

# Navegación por páginas
if st.session_state.current_page == 'generator':
    # PÁGINA DEL GENERADOR (contenido original)
    # Pestañas principales para el generador
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
                "🏞️ Paisaje Natural": "Breathtaking natural landscape, golden hour lighting, majestic mountains, pristine wilderness, dramatic sky, professional nature photography, epic vista, serene beauty.",
                "🌃 Ciudad Nocturna": "Urban cityscape at night, neon reflections on wet streets, dramatic lighting, architectural photography, bustling metropolis, vibrant nightlife, modern skyline.",
                "🦋 Macro Naturaleza": "Extreme macro photography, intricate details, morning dew drops, delicate textures, shallow depth of field, professional wildlife photography, natural beauty.",
                "🎭 Retrato Dramático": "Dramatic portrait with intense lighting, deep shadows, emotional expression, cinematic style, fine art photography, powerful mood, artistic vision.",
                "🌺 Estilo Vintage": "Vintage aesthetic, retro color palette, nostalgic atmosphere, classic composition, aged film look, timeless beauty, artistic vintage style.",
                "🔥 Acción Épica": "Epic action scene, dynamic movement, explosive energy, cinematic composition, dramatic lighting, intense atmosphere, superhero style, powerful imagery.",
                "✨ Personalizado": ""
            }
        elif "Kandinsky" in content_type:
            templates = {
                "🎨 Arte Abstracto": "Abstract art with flowing forms, vivid colors, dynamic composition, expressive brushstrokes, modern art style, contemporary aesthetic, artistic masterpiece.",
                "🌈 Paisaje Onírico": "Dreamlike landscape with surreal elements, soft pastel colors, floating objects, magical atmosphere, fantastical environment, artistic interpretation.",
                "🖼️ Estilo Clásico": "Classical art style, renaissance painting technique, detailed composition, traditional art, museum quality, masterful brushwork, timeless beauty.",
                "🌸 Arte Japonés": "Japanese art style, traditional aesthetic, delicate details, harmonious composition, zen atmosphere, cultural elements, artistic elegance.",
                "🌟 Surrealismo": "Surrealist art style, impossible scenes, dream-like imagery, unexpected combinations, artistic vision, creative interpretation, imaginative composition.",
                "🎭 Expresionismo": "Expressionist art style, bold colors, emotional intensity, distorted forms, powerful brushstrokes, psychological depth, dramatic mood.",
                "🌊 Impresionismo": "Impressionist painting style, soft brush strokes, natural lighting, outdoor scenes, color harmony, atmospheric effects, gentle beauty.",
                "🎪 Pop Art": "Pop art style, bright bold colors, graphic elements, contemporary culture, commercial aesthetic, vibrant imagery, modern art movement.",
                "🌙 Arte Místico": "Mystical art with spiritual elements, cosmic themes, ethereal atmosphere, transcendent beauty, sacred geometry, divine inspiration.",
                "🏛️ Arte Neoclásico": "Neoclassical art style, elegant proportions, refined details, historical themes, marble textures, classical beauty, timeless sophistication.",
                "✨ Personalizado": ""
            }
        elif "Seedance" in content_type:
            templates = {
                "🌅 Amanecer Épico": "Golden hour sunrise over misty mountains, cinematic camera movement, slow dolly shot revealing majestic landscape, warm lighting casting long shadows, peaceful atmosphere, nature documentary style, breathtaking vista.",
                "🏙️ Ciudad Futurista": "Futuristic cityscape at night, neon lights reflecting on wet streets, slow camera pan across towering skyscrapers, cyberpunk atmosphere, dramatic lighting, urban cinematic scene.",
                "🌊 Océano Tranquilo": "Serene ocean waves gently rolling onto pristine beach, golden sunset lighting, smooth camera tracking shot along shoreline, peaceful coastal scene, relaxing atmosphere.",
                "🎬 Escena Cinematográfica": "Professional cinematic shot with dramatic lighting, smooth camera movement, film-quality composition, artistic framing, moody atmosphere, cinematic color grading.",
                "🌲 Bosque Místico": "Enchanted forest with magical particles floating, cinematic tracking shot through ancient trees, ethereal lighting filtering through canopy, mystical atmosphere, fantasy documentary style.",
                "🌆 Timelapse Urbano": "Urban timelapse with fast-moving clouds, bustling street traffic, dynamic lighting changes from day to night, cinematic urban documentary, modern city rhythm.",
                "🦅 Vuelo Épico": "Aerial cinematography following majestic eagle soaring over vast landscape, smooth camera tracking, nature documentary style, epic wide shots, dramatic sky.",
                "🔥 Elementos Dramáticos": "Dramatic scene with fire and smoke effects, cinematic lighting, intense atmosphere, action movie style, dynamic camera movement.",
                "🌙 Noche Estrellada": "Starry night sky timelapse, Milky Way rotating overhead, peaceful landscape silhouette, astronomical cinematography, cosmic beauty.",
                "⚡ Tormenta Épica": "Epic thunderstorm with lightning strikes, dramatic weather cinematography, dark storm clouds, nature's raw power, cinematic storm documentation.",
                "✨ Personalizado": ""
            }
        elif "Pixverse" in content_type:
            templates = {
                "🎭 Escena de Acción Anime": "an anime action scene, a woman looks around slowly, mountain landscape in the background",
                "🌸 Personaje Kawaii": "a cute anime girl with big eyes, pink hair, sitting in a cherry blossom garden, gentle breeze moving her hair",
                "🏯 Paisaje Japonés": "traditional Japanese temple in anime style, sunset lighting, dramatic clouds, peaceful atmosphere",
                "⚔️ Batalla Épica": "epic anime battle scene, warriors with glowing swords, dynamic camera movement, intense lighting effects",
                "🌙 Noche Mágica": "anime magical girl under moonlight, sparkles and magical effects, flowing dress, mystical atmosphere",
                "🦊 Espíritu del Bosque": "anime fox spirit in enchanted forest, glowing eyes, magical aura, mystical atmosphere, nature spirits dancing",
                "🏫 Escuela Anime": "anime school scene, students in uniform, cherry blossoms falling, warm afternoon light, slice of life atmosphere",
                "🌊 Playa Tropical": "anime beach scene, crystal clear water, palm trees swaying, sunset colors, peaceful vacation atmosphere",
                "🎪 Festival Matsuri": "anime summer festival, paper lanterns, fireworks in background, traditional yukata, festive atmosphere",
                "🚀 Aventura Espacial": "anime space adventure, starship cockpit, cosmic background, dramatic lighting, sci-fi atmosphere",
                "✨ Personalizado": ""
            }
        elif "SSD-1B" in content_type:
            templates = {
                "🔥 Fantasía Épica": "epic fantasy creature, dramatic lighting, ultra realistic details, cinematic composition, dark fantasy atmosphere, vibrant colors, professional digital art",
                "🌪️ Elementos Naturales": "with smoke, half ice and half fire and ultra realistic in detail, dramatic contrast, elemental powers, cinematic lighting, vibrant effects",
                "🦅 Vida Salvaje": "majestic wild animal, ultra realistic detail, wildlife photography style, natural habitat, dramatic lighting, vibrant colors, cinematic composition",
                "🖤 Arte Oscuro": "dark fantasy art, mysterious atmosphere, dramatic shadows, gothic elements, ultra realistic details, cinematic lighting, professional artwork",
                "⚡ Efectos Dinámicos": "dynamic energy effects, lightning, fire, smoke, ultra realistic rendering, cinematic composition, vibrant colors, dramatic atmosphere",
                "🌌 Espacio Cósmico": "cosmic space scene, nebulae, stars, galaxies, ultra realistic space photography, dramatic celestial lighting, vibrant cosmic colors, epic scale",
                "🏰 Arquitectura Épica": "majestic ancient castle, dramatic architecture, ultra realistic stonework, cinematic lighting, medieval atmosphere, epic fortress design",
                "🌋 Paisaje Volcánico": "volcanic landscape, lava flows, dramatic geological formations, ultra realistic terrain, cinematic lighting, powerful natural forces",
                "🐉 Criatura Mítica": "mythical dragon, ultra realistic scales and textures, dramatic pose, cinematic lighting, fantasy atmosphere, epic creature design",
                "⚔️ Guerrero Épico": "epic warrior in battle armor, ultra realistic metal textures, dramatic pose, cinematic lighting, heroic atmosphere, fantasy warrior design",
                "✨ Personalizado": ""
            }
        elif "VEO 3 Fast" in content_type:
            templates = {
                "🏃 Acción Épica": "A superhero running at incredible speed through a bustling city, leaving trails of light behind, cars and people blur as the hero moves, dynamic camera following the action, cinematic lighting, epic scale",
                "🌊 Naturaleza Cinematográfica": "Ocean waves crashing against dramatic cliffs during golden hour, seagulls flying overhead, camera slowly panning to reveal the vast coastline, breathtaking natural beauty, cinematic quality",
                "🚗 Persecución Urbana": "High-speed chase through neon-lit streets at night, cars weaving through traffic, dramatic lighting from street lamps, rain reflecting on wet pavement, action movie style",
                "🦋 Transformación Mágica": "A caterpillar transforming into a butterfly in extreme slow motion, magical particles floating around, nature documentary style with macro cinematography",
                "🎭 Drama Emocional": "Close-up of a person's face showing deep emotion, tears slowly falling, soft lighting, intimate moment captured with cinematic depth",
                "🌪️ Tormenta Épica": "Massive tornado approaching across open plains, dark storm clouds swirling, lightning illuminating the scene, dramatic weather phenomenon, nature's raw power",
                "🏔️ Montaña Majestuosa": "Drone shot over snow-capped mountain peaks, morning mist clearing to reveal breathtaking alpine vista, golden sunrise light, cinematic landscape",
                "🌃 Metrópolis Futurista": "Futuristic city with flying cars, holographic billboards, neon lights reflecting on glass buildings, cyberpunk atmosphere, sci-fi urban landscape",
                "🔥 Volcán en Erupción": "Active volcano erupting, lava flows cascading down mountainside, dramatic geological event, cinematic documentation of earth's power",
                "🌈 Aurora Boreal": "Northern lights dancing across arctic sky, ethereal green and purple colors, time-lapse photography, magical atmospheric phenomenon",
                "✨ Personalizado": ""
            }
        else:  # Stickers Flux Pro
            templates = {
                "🌟 Sticker Brillante": "a shiny, colorful star sticker, cartoon style, bright and cheerful, with a glossy finish",
                "❤️ Corazón Colorido": "a vibrant, multi-colored heart sticker, cartoon style, with a glossy shine",
                "🐶 Perro Kawaii": "a cute, cartoon-style dog sticker, big eyes, smiling, with a colorful collar",
                "🍕 Pizza Divertida": "a fun, cartoon-style pizza slice sticker, with exaggerated toppings and a smiling face",
                "🌈 Arcoíris Feliz": "a cheerful rainbow sticker with clouds, cartoon style, bright colors, glossy finish, kawaii aesthetic",
                "🎃 Halloween Spooky": "a cute Halloween pumpkin sticker, cartoon style, friendly face, orange and black colors, glossy finish",
                "🦄 Unicornio Mágico": "a magical unicorn sticker, cartoon style, pastel colors, rainbow mane, sparkles, glossy finish",
                "🌮 Taco Divertido": "a funny taco character sticker, cartoon style, smiling face, vibrant colors, Mexican food theme",
                "🐱 Gato Adorable": "an adorable cat sticker, cartoon style, big eyes, cute pose, colorful fur, glossy finish",
                "🎮 Gaming Retro": "a retro gaming console sticker, pixel art style, nostalgic colors, classic gaming aesthetic, glossy finish",
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
                            
                            # SSD-1B usa replicate.run() que devuelve resultados directamente
                            with st.spinner("🚀 Generando imagen rápida..."):
                                try:
                                    output = generate_ssd1b(prompt, **params)
                                    
                                    # SSD-1B devuelve directamente el resultado
                                    if output:
                                        st.success("⚡ ¡Imagen generada exitosamente!")
                                        
                                        # Manejar diferentes tipos de output
                                        try:
                                            if isinstance(output, list):
                                                # Si es una lista, tomar el primer elemento
                                                first_output = output[0]
                                                if hasattr(first_output, 'url'):
                                                    # Es un objeto FileOutput
                                                    image_url = first_output.url
                                                else:
                                                    # Es una URL directa
                                                    image_url = str(first_output)
                                            elif hasattr(output, 'url'):
                                                # Es un objeto FileOutput directo
                                                image_url = output.url
                                            else:
                                                # Es una URL directa
                                                image_url = str(output)
                                            
                                            st.write(f"🔗 **URL de la imagen:** {image_url}")
                                            st.code(f"Tipo de output: {type(output).__name__}")
                                            
                                            # Descargar y guardar
                                            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                                            filename = f"ssd_{timestamp}.jpg"
                                            local_path = download_and_save_file(image_url, filename, "imagen")
                                            
                                        except Exception as url_error:
                                            st.error(f"❌ Error al procesar URL: {str(url_error)}")
                                            st.code(f"Output recibido: {type(output)} - {str(output)[:200]}")
                                            image_url = None
                                            local_path = None
                                        
                                        # Guardar en historial solo si tenemos URL válida
                                        if image_url:
                                            history_item = {
                                                "tipo": "imagen",
                                                "fecha": datetime.now().isoformat(),
                                                "prompt": prompt,
                                                "plantilla": selected_template,
                                                "url": image_url,
                                                "archivo_local": filename if local_path else None,
                                                "parametros": params,
                                                "modelo": "SSD-1B",
                                                "id_prediccion": "N/A (output directo)"
                                            }
                                            save_to_history(history_item)
                                            
                                            if local_path:
                                                st.success(f"💾 Imagen guardada: `{filename}`")
                                            
                                            # Mostrar imagen
                                            try:
                                                st.image(image_url, caption="Imagen SSD-1B", use_container_width=True)
                                            except Exception as img_error:
                                                st.warning(f"⚠️ No se pudo mostrar la imagen: {str(img_error)}")
                                                st.markdown(f'<a href="{image_url}" target="_blank">🔗 Ver imagen en nueva pestaña</a>', unsafe_allow_html=True)
                                        else:
                                            st.error("❌ No se pudo obtener URL de la imagen")
                                    else:
                                        st.error("❌ SSD-1B no devolvió output")
                                
                                except Exception as e:
                                    st.error(f"❌ Error con SSD-1B: {str(e)}")
                                    st.error(f"🔍 Tipo de error: {type(e).__name__}")
                                    st.code(f"Output recibido: {type(output) if 'output' in locals() else 'No definido'}")
                        
                        elif "Seedance" in content_type:
                            st.info(f"💃 Generando con Seedance... Iniciado a las {start_datetime}")
                            
                            with st.spinner("💃 Procesando con Seedance..."):
                                try:
                                    # Seedance usa replicate.run() que devuelve el resultado directamente
                                    output = generate_video_seedance(prompt, **params)
                                    
                                    if output:
                                        st.success("💃 ¡Generación exitosa!")
                                        
                                        # Manejar diferentes tipos de output
                                        try:
                                            if isinstance(output, list):
                                                result_url = output[0]
                                            elif hasattr(output, 'url'):
                                                result_url = output.url
                                            else:
                                                result_url = str(output)
                                            
                                            st.write(f"🔗 **URL del resultado:** {result_url}")
                                            
                                            # Determinar tipo de archivo
                                            file_ext = "mp4"
                                            if result_url.lower().endswith(('.jpg', '.jpeg', '.png')):
                                                file_ext = "jpg"
                                            
                                            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                                            filename = f"seedance_{timestamp}.{file_ext}"
                                            local_path = download_and_save_file(result_url, filename, "video")
                                            
                                            # Guardar en historial
                                            history_item = {
                                                "tipo": "video",
                                                "modelo": "seedance",
                                                "fecha": datetime.now().isoformat(),
                                                "prompt": prompt,
                                                "plantilla": selected_template,
                                                "url": result_url,
                                                "archivo_local": filename if local_path else None,
                                                "parametros": params,
                                                "video_duration": params.get('duration', 5),
                                                "processing_time": int(time.time() - start_time)
                                            }
                                            save_to_history(history_item)
                                            
                                            if local_path:
                                                st.success(f"💾 Video guardado: `{filename}`")
                                            
                                            # Mostrar según tipo
                                            if file_ext == "mp4":
                                                st.video(result_url)
                                            else:
                                                st.image(result_url, caption="Resultado Seedance", use_container_width=True)
                                        
                                        except Exception as url_error:
                                            st.error(f"❌ Error procesando URL: {str(url_error)}")
                                            st.code(f"Output recibido: {type(output).__name__}")
                                    else:
                                        st.error("❌ Seedance no devolvió output")
                                
                                except Exception as e:
                                    st.error(f"❌ Error con Seedance: {str(e)}")
                                    st.code(f"Tipo de error: {type(e).__name__}")
                        
                        elif "Pixverse" in content_type:
                            st.info(f"🎬 Generando video con Pixverse... Iniciado a las {start_datetime}")
                            
                            # Pixverse usa replicate.run() que devuelve resultados directamente
                            with st.spinner("🎬 Generando video con Pixverse..."):
                                try:
                                    output = generate_video_pixverse(prompt, **params)
                                    
                                    # Pixverse devuelve directamente el resultado
                                    if output:
                                        st.success("🎬 ¡Video generado exitosamente!")
                                        
                                        # Manejar diferentes tipos de output
                                        video_url = None
                                        local_path = None
                                        
                                        try:
                                            if isinstance(output, list):
                                                # Si es una lista, tomar el primer elemento
                                                first_output = output[0]
                                                if hasattr(first_output, 'url'):
                                                    # Es un objeto FileOutput
                                                    video_url = first_output.url
                                                else:
                                                    # Es una URL directa
                                                    video_url = str(first_output)
                                            elif hasattr(output, 'url'):
                                                # Es un objeto FileOutput directo
                                                video_url = output.url
                                            else:
                                                # Es una URL directa
                                                video_url = str(output)
                                            
                                            # Descargar inmediatamente para evitar que expire la URL
                                            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                                            filename = f"pixverse_{timestamp}.mp4"
                                            
                                            if video_url:
                                                st.write(f"🔗 **URL del video:** {video_url}")
                                                st.info("💾 Descargando video para conservar acceso...")
                                                local_path = download_and_save_file(video_url, filename, "video")
                                                
                                                if local_path:
                                                    st.success(f"✅ Video guardado: `{filename}`")
                                                else:
                                                    st.warning("⚠️ La descarga falló, pero la URL puede funcionar temporalmente")
                                            
                                        except Exception as url_error:
                                            st.error(f"❌ Error al procesar URL: {str(url_error)}")
                                            st.code(f"Output recibido: {type(output)} - {str(output)[:200]}")
                                        
                                        # Calcular units estimadas para Pixverse basado en duración y resolución
                                        duration_num = params.get('duration', 5)
                                        quality = params.get('quality', '720p')
                                        
                                        # Estimar units basado en duración y resolución
                                        base_units = duration_num * 6  # Base: 6 units por segundo
                                        if '1080p' in quality:
                                            estimated_units = base_units * 1.5  # 50% más para 1080p
                                        elif '540p' in quality:
                                            estimated_units = base_units * 0.7  # 30% menos para 540p
                                        else:  # 720p
                                            estimated_units = base_units
                                        
                                        estimated_units = round(estimated_units, 1)
                                        
                                        # Guardar en historial con prioridad al archivo local
                                        if video_url or local_path:
                                            history_item = {
                                                "tipo": "video",
                                                "fecha": datetime.now().isoformat(),
                                                "prompt": prompt,
                                                "plantilla": selected_template,
                                                "url": video_url,
                                                "archivo_local": filename if local_path else None,
                                                "parametros": params,
                                                "modelo": "Pixverse",
                                                "id_prediccion": "N/A (output directo)",
                                                "video_duration": duration_num,  # Duración real del video
                                                "pixverse_units": estimated_units,  # Units estimadas para cálculo de costo
                                                "processing_time": None  # No disponible para Pixverse (output directo)
                                            }
                                            save_to_history(history_item)
                                            
                                            # Mostrar video priorizando archivo local
                                            try:
                                                if local_path and local_path.exists():
                                                    st.info("🎬 Reproduciendo desde archivo local (más confiable)")
                                                    st.video(str(local_path))
                                                elif video_url:
                                                    st.warning("⚠️ Reproduciendo desde URL externa (puede expirar)")
                                                    st.video(video_url)
                                                else:
                                                    st.error("❌ No hay fuente disponible para reproducir")
                                            except Exception as video_error:
                                                st.warning(f"⚠️ Error al reproducir: {str(video_error)}")
                                                if video_url:
                                                    st.markdown(f'<a href="{video_url}" target="_blank">🔗 Intentar ver en nueva pestaña</a>', unsafe_allow_html=True)
                                        else:
                                            st.error("❌ No se pudo obtener URL del video")
                                    else:
                                        st.error("❌ Pixverse no devolvió output")
                                
                                except Exception as e:
                                    st.error(f"❌ Error con Pixverse: {str(e)}")
                                    st.error(f"🔍 Tipo de error: {type(e).__name__}")
                                    st.code(f"Output recibido: {type(output) if 'output' in locals() else 'No definido'}")
                        
                        elif "VEO 3 Fast" in content_type:
                            st.info(f"🚀 Generando video con VEO 3 Fast... Iniciado a las {start_datetime}")
                            
                            with st.spinner("🚀 Generando video con VEO 3 Fast..."):
                                try:
                                    output = generate_video_veo3(prompt, **params)
                                    
                                    # VEO 3 Fast devuelve directamente el resultado
                                    if output:
                                        # Manejar el output que puede ser FileOutput o URL directa
                                        try:
                                            if hasattr(output, 'url'):
                                                video_url = output.url
                                            elif isinstance(output, str):
                                                video_url = output
                                            else:
                                                video_url = str(output)
                                            
                                            st.success("🚀 ¡Video VEO 3 Fast generado exitosamente!")
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
                                                "modelo": "VEO 3 Fast"
                                            }
                                            save_to_history(history_item)
                                            
                                            if local_path:
                                                st.success(f"💾 Video guardado: `{filename}`")
                                            
                                            # Mostrar video
                                            st.video(video_url)
                                            
                                            # Información técnica
                                            st.info("📊 **VEO 3 Fast**: Modelo de última generación para generación rápida de videos de alta calidad")
                                            
                                        except Exception as output_error:
                                            st.error(f"❌ Error al procesar output de VEO 3 Fast: {str(output_error)}")
                                            st.write(f"🔍 **Tipo de output:** {type(output)}")
                                            st.write(f"🔍 **Output raw:** {output}")
                                    else:
                                        st.error("❌ VEO 3 Fast no devolvió output")
                                        
                                except Exception as e:
                                    st.error(f"❌ Error con VEO 3 Fast: {str(e)}")
                                    st.error(f"🔍 Detalles: {type(e).__name__}")
                                    st.code(traceback.format_exc())
                        
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
                                            
                                            # Calcular tiempo de procesamiento
                                            processing_time = time.time() - start_time
                                            
                                            # Guardar en historial con información adicional para cálculo de costos
                                            history_item = {
                                                "tipo": "sticker",
                                                "fecha": datetime.now().isoformat(),
                                                "prompt": prompt,
                                                "plantilla": selected_template,
                                                "url": sticker_url,
                                                "archivo_local": filename if local_path else None,
                                                "parametros": params,
                                                "id_prediccion": prediction.id,
                                                "processing_time": processing_time,  # Tiempo real de procesamiento
                                                "modelo": "Flux Pro Stickers"  # Modelo específico para identificación
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
                        # Para VEO 3 Fast, asumimos éxito si llegamos aquí sin excepción
                        if "VEO 3 Fast" in content_type:
                            success = True  # Si llegamos aquí, fue exitoso
                        else:
                            success = hasattr(locals(), 'prediction') and prediction.status == "succeeded"
                        
                        update_generation_stats(content_type, total_time, success)

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
                
                st.subheader("📈 Estadísticas de Rendimiento")
                
                # Crear métricas visuales compactas y modernas para cada modelo
                models_data = list(stats.items())
                
                for i, (model, data) in enumerate(models_data):
                    success_rate = (data["exitosas"] / data["total"] * 100) if data["total"] > 0 else 0
                    avg_time = data.get("tiempo_promedio", 0)
                    
                    # Determinar icono basado en el modelo
                    if "flux" in model.lower():
                        model_icon = "🖼️"
                        model_name = "Flux Pro"
                        bg_color = "#667eea"
                    elif "kandinsky" in model.lower():
                        model_icon = "🎨"
                        model_name = "Kandinsky"
                        bg_color = "#f093fb"
                    elif "ssd" in model.lower():
                        model_icon = "🎥"
                        model_name = "SSD-1B"
                        bg_color = "#ffc107"
                    elif "veo" in model.lower():
                        model_icon = "🎥"
                        model_name = "VEO 3"
                        bg_color = "#4ECDC4"
                    elif "pixverse" in model.lower():
                        model_icon = "🎭"
                        model_name = "Pixverse"
                        bg_color = "#A8E6CF"
                    elif "seedance" in model.lower():
                        model_icon = "🎬"
                        model_name = "Seedance"
                        bg_color = "#FF6B6B"
                    elif "sticker" in model.lower():
                        model_icon = "🏷️"
                        model_name = "Stickers"
                        bg_color = "#84fab0"
                    else:
                        model_icon = "📊"
                        model_name = model.title()
                        bg_color = "#667eea"
                    
                    # Determinar color de la tasa de éxito
                    if success_rate >= 90:
                        success_color = "#28a745"
                        success_emoji = "🟢"
                    elif success_rate >= 70:
                        success_color = "#fd7e14"
                        success_emoji = "🟡"
                    else:
                        success_color = "#dc3545"
                        success_emoji = "🔴"
                    
                    # Crear la tarjeta usando columnas de Streamlit
                    with st.container():
                        st.markdown(f"""
                        <div style="background: {bg_color}; padding: 12px; border-radius: 10px; margin: 8px 0; color: white;">
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <span style="font-weight: bold;">{model_icon} {model_name}</span>
                                <span style="font-size: 20px; font-weight: bold;">{data["total"]}</span>
                            </div>
                            <div style="margin-top: 8px; display: flex; justify-content: space-between; font-size: 12px;">
                                <span>{success_emoji} {success_rate:.1f}% éxito</span>
                                <span>⏱️ {avg_time:.1f}s</span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
            
            # Enlaces útiles
            st.subheader("🔗 Enlaces")
            st.markdown("[📚 Documentación Flux Pro](https://replicate.com/black-forest-labs/flux-pro)")
            st.markdown("[🎨 Documentación Kandinsky](https://replicate.com/ai-forever/kandinsky-2.2)")
            st.markdown("[⚡ Documentación SSD-1B](https://replicate.com/lucataco/realvisxl-v4.0-lightning)")
            st.markdown("[💃 Documentación Seedance](https://replicate.com/fofr/realvisxl-v4.0)")
            st.markdown("[🎬 Documentación Pixverse](https://replicate.com/pixverse/pixverse-v1.8)")
            st.markdown("[🚀 Documentación VEO 3 Fast](https://replicate.com/fofr/veo-3-fast)")
            st.markdown("[🏷️ Documentación Stickers](https://replicate.com/fofr/sticker-maker)")

    # Sección de historial avanzado
    with tab2:
        st.header("📊 Historial de Generaciones")
        
        history = load_history()
        
        if history:
            # Calcular estadísticas generales - corregir detección de tipos de video
            total_items = len(history)
            total_imagenes = len([h for h in history if h.get('tipo') == 'imagen'])
            
            # Detectar videos por tipo o archivo_local (algunos tienen tipo "video_seedance" incorrecto)
            total_videos_seedance = len([h for h in history if 
                (h.get('tipo') == 'video' and ('seedance' in h.get('archivo_local', '').lower() or 'seedance' in h.get('modelo', '').lower())) or
                h.get('tipo') == 'video_seedance'
            ])
            total_videos_anime = len([h for h in history if 
                h.get('tipo') == 'video' and ('pixverse' in h.get('archivo_local', '').lower() or 'pixverse' in h.get('modelo', '').lower())
            ])
            total_videos_veo = len([h for h in history if 
                h.get('tipo') == 'video' and ('veo3' in h.get('archivo_local', '').lower() or 'veo' in h.get('modelo', '').lower())
            ])
            total_stickers = len([h for h in history if h.get('tipo') == 'sticker'])
            
            # Tarifas reales por unidad extraídas de la factura de Replicate
            cost_rates = {
                'imagen': {
                    'flux_pro': {'rate': 0.055, 'unit': 'imagen'},      # $0.055 por imagen
                    'kandinsky': {'rate': 0.0014, 'unit': 'segundo'},   # $0.0014 por segundo  
                    'ssd_1b': {'rate': 0.000975, 'unit': 'segundo'}     # $0.000975 por segundo
                },
                'video': {
                    'seedance': {'rate': 0.15, 'unit': 'segundo'},      # $0.15 por segundo
                    'pixverse': {'rate': 0.010, 'unit': 'unit'},        # $0.010 por unit (calculado por duración/resolución)
                    'veo3': {'rate': 0.40, 'unit': 'segundo'}           # $0.40 por segundo
                },
                'sticker': {'rate': 0.055, 'unit': 'sticker'}           # $0.055 por sticker
            }
            
            # Usar la función calculate_item_cost de utils.py
            # (eliminada función duplicada)
            
            # Calcular costo total
            total_cost_usd = 0
            cost_breakdown = []
            
            for item in history:
                item_cost, model_info, calculation_details = calculate_item_cost(item)
                total_cost_usd += item_cost
                cost_breakdown.append({
                    'fecha': item.get('fecha', ''),
                    'modelo': model_info,
                    'costo': item_cost,
                    'calculo': calculation_details
                })
            
            total_cost_eur = total_cost_usd * 0.92  # Conversión aproximada
            
            # Mostrar métricas de resumen con diseño visual mejorado
            st.markdown("### 📊 Resumen de Actividad")
            
            # Primera fila de métricas principales
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"""
                <div style="
                    background: linear-gradient(135deg, #FF6B6B, #FF8E8E);
                    padding: 25px;
                    border-radius: 15px;
                    text-align: center;
                    color: white;
                    box-shadow: 0 4px 15px rgba(255,107,107,0.3);
                ">
                    <div style="font-size: 14px; margin-bottom: 5px;">🖼️ IMÁGENES</div>
                    <div style="font-size: 36px; font-weight: bold; margin: 10px 0;">{total_imagenes}</div>
                    <div style="font-size: 12px; opacity: 0.9;">Generadas</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                total_videos = total_videos_seedance + total_videos_anime + total_videos_veo
                st.markdown(f"""
                <div style="
                    background: linear-gradient(135deg, #4ECDC4, #44A08D);
                    padding: 25px;
                    border-radius: 15px;
                    text-align: center;
                    color: white;
                    box-shadow: 0 4px 15px rgba(78,205,196,0.3);
                ">
                    <div style="font-size: 14px; margin-bottom: 5px;">🎬 VIDEOS</div>
                    <div style="font-size: 36px; font-weight: bold; margin: 10px 0;">{total_videos}</div>
                    <div style="font-size: 12px; opacity: 0.9;">Generados</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div style="
                    background: linear-gradient(135deg, #A8E6CF, #7FB069);
                    padding: 25px;
                    border-radius: 15px;
                    text-align: center;
                    color: white;
                    box-shadow: 0 4px 15px rgba(168,230,207,0.3);
                ">
                    <div style="font-size: 14px; margin-bottom: 5px;">🏷️ STICKERS</div>
                    <div style="font-size: 36px; font-weight: bold; margin: 10px 0;">{total_stickers}</div>
                    <div style="font-size: 12px; opacity: 0.9;">Generados</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Segunda fila con costos y total
            col4, col5, col6 = st.columns(3)
            
            with col4:
                st.markdown(f"""
                <div style="
                    background: linear-gradient(135deg, #667eea, #764ba2);
                    padding: 25px;
                    border-radius: 15px;
                    text-align: center;
                    color: white;
                    box-shadow: 0 4px 15px rgba(102,126,234,0.3);
                ">
                    <div style="font-size: 14px; margin-bottom: 5px;">📈 TOTAL</div>
                    <div style="font-size: 36px; font-weight: bold; margin: 10px 0;">{total_items}</div>
                    <div style="font-size: 12px; opacity: 0.9;">Generaciones</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col5:
                st.markdown(f"""
                <div style="
                    background: linear-gradient(135deg, #f093fb, #f5576c);
                    padding: 25px;
                    border-radius: 15px;
                    text-align: center;
                    color: white;
                    box-shadow: 0 4px 15px rgba(240,147,251,0.3);
                ">
                    <div style="font-size: 16px; margin-bottom: 5px; font-weight: bold;">💰 COSTO USD</div>
                    <div style="font-size: 42px; font-weight: bold; margin: 15px 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">${total_cost_usd:.2f}</div>
                    <div style="font-size: 14px; opacity: 0.9;">Costo Total Estimado</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col6:
                st.markdown(f"""
                <div style="
                    background: linear-gradient(135deg, #ffecd2, #fcb69f);
                    padding: 25px;
                    border-radius: 15px;
                    text-align: center;
                    color: #8B4513;
                    box-shadow: 0 4px 15px rgba(255,236,210,0.3);
                ">
                    <div style="font-size: 16px; margin-bottom: 5px; font-weight: bold;">💶 COSTO EUR</div>
                    <div style="font-size: 42px; font-weight: bold; margin: 15px 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">€{total_cost_eur:.2f}</div>
                    <div style="font-size: 14px; opacity: 0.9;">Costo Total Estimado</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("<br><br>", unsafe_allow_html=True)
            
            # Filtros avanzados
            st.subheader("🔍 Filtros")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                filter_type = st.selectbox(
                    "Filtrar por tipo:",
                    ["Todos", "imagen", "video", "sticker", "media"]
                )
            
            with col2:
                search_prompt = st.text_input(
                    "Buscar en prompts:",
                    placeholder="Escribe palabras clave..."
                )
            
            with col3:
                show_count = st.selectbox(
                    "Total de generaciones",
                    [10, 20, 50, 100, "Todos"],
                    index=1
                )
            
            # Aplicar filtros
            filtered_history = history.copy()
            
            # Filtro por tipo
            if filter_type != "Todos":
                filtered_history = [item for item in filtered_history if item.get("tipo") == filter_type]
            
            # Filtro por búsqueda en prompt
            if search_prompt:
                search_terms = search_prompt.lower().split()
                filtered_history = [
                    item for item in filtered_history 
                    if any(term in item.get('prompt', '').lower() for term in search_terms)
                ]
            
            # Ordenar por fecha (más reciente primero)
            filtered_history.sort(key=lambda x: x.get("fecha", ""), reverse=True)
            
            # Limitar cantidad si no es "Todos"
            if show_count != "Todos":
                filtered_history = filtered_history[:show_count]
            
            st.subheader(f"📋 Resultados ({len(filtered_history)} elementos)")
            
            # Mostrar elementos del historial con diseño avanzado
            for i, item in enumerate(filtered_history):
                # Obtener información del elemento
                fecha = item.get('fecha', 'Sin fecha')
                prompt = item.get('prompt', 'Sin prompt')
                plantilla = item.get('plantilla', 'Sin plantilla')
                tipo = item.get('tipo', 'Unknown').title()
                url = item.get('url', '')
                archivo_local = item.get('archivo_local', '')
                parametros = item.get('parametros', {})
                id_prediccion = item.get('id_prediccion', '')
                modelo = item.get('modelo', '')
                
                # Asignar icono según el tipo y modelo
                if tipo.lower() == 'imagen':
                    if 'kandinsky' in archivo_local.lower() if archivo_local else False or 'kandinsky' in modelo.lower():
                        icon = "🎨"
                    elif 'ssd' in archivo_local.lower() if archivo_local else False or 'ssd' in modelo.lower():
                        icon = "⚡"
                    else:
                        icon = "🖼️"  # Flux Pro por defecto
                elif tipo.lower() == 'video':
                    if 'seedance' in archivo_local.lower() if archivo_local else False or 'seedance' in modelo.lower():
                        icon = "🎬"  # Seedance - clapperboard profesional
                    elif 'pixverse' in archivo_local.lower() if archivo_local else False or 'pixverse' in modelo.lower():
                        icon = "🎭"  # Pixverse - anime/artístico
                    elif 'veo' in modelo.lower() or 'veo3' in archivo_local.lower() if archivo_local else False:
                        icon = "🎥"  # VEO 3 Fast - cámara profesional
                    else:
                        icon = "📹"  # Video genérico - videocámara
                elif tipo.lower() == 'sticker':
                    icon = "🏷️"
                elif tipo.lower() == 'media':
                    icon = "📄"
                else:
                    icon = "📄"  # Por defecto
                
                # Crear expandible con información resumida
                fecha_formatted = fecha[:16] if len(fecha) > 16 else fecha
                prompt_preview = prompt[:50] + "..." if len(prompt) > 50 else prompt
                
                with st.expander(f"{icon} {fecha_formatted} - {prompt_preview}", expanded=False):
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        # Información básica
                        st.write(f"**Tipo:** {tipo}")
                        
                        # Prompt completo en área expandible
                        with st.expander("📝 Prompt completo", expanded=False):
                            st.text_area("Prompt:", value=prompt, height=100, disabled=True, key=f"prompt_{i}", label_visibility="collapsed")
                        
                        st.write(f"**Plantilla:** {plantilla}")
                        
                        # Parámetros técnicos
                        if parametros:
                            with st.expander("⚙️ Ver parámetros", expanded=False):
                                for key, value in parametros.items():
                                    st.write(f"**{key}:** {value}")
                        
                        # Estadísticas y costos
                        with st.expander("📊 Estadísticas y Costos", expanded=True):
                            # Calcular costo específico del item usando la función mejorada
                            item_cost, model_info, calculation_details = calculate_item_cost(item)
                            
                            col_stats1, col_stats2 = st.columns(2)
                            with col_stats1:
                                # Información técnica específica por tipo
                                if 'width' in parametros and 'height' in parametros:
                                    resolution = f"{parametros['width']}x{parametros['height']}"
                                    megapixels = (parametros['width'] * parametros['height']) / 1_000_000
                                    st.write(f"🔍 **Resolución:** {resolution}")
                                    st.write(f"🔢 **Megapíxeles:** {megapixels:.2f} MP")
                                
                                # Información de video - duración y quality
                                if tipo.lower() == 'video':
                                    if 'duration' in parametros:
                                        st.write(f"⏱️ **Duración:** {parametros['duration']}s")
                                    elif item.get('video_duration'):
                                        st.write(f"⏱️ **Duración:** {item.get('video_duration')}s")
                                    
                                    if 'quality' in parametros:
                                        st.write(f"📺 **Calidad:** {parametros['quality']}")
                                    
                                    # Mostrar units de Pixverse si están disponibles
                                    if item.get('pixverse_units'):
                                        st.write(f"🎯 **Pixverse Units:** {item.get('pixverse_units')}")
                                
                                # Información de procesamiento
                                if item.get('processing_time'):
                                    st.write(f"⚡ **Tiempo de procesamiento:** {item.get('processing_time'):.1f}s")
                                
                                if 'steps' in parametros:
                                    st.write(f"⚙️ **Pasos de procesamiento:** {parametros['steps']}")
                                elif 'num_inference_steps' in parametros:
                                    st.write(f"⚙️ **Pasos de procesamiento:** {parametros['num_inference_steps']}")
                            
                            with col_stats2:
                                st.markdown(f"### 💰 **${item_cost:.3f}**")
                                st.caption("Costo estimado USD")
                                st.markdown(f"### 💶 **€{item_cost * 0.92:.3f}**")
                                st.caption("Costo estimado EUR")
                                
                                # Mostrar detalles del cálculo
                                st.caption(f"🔢 **Modelo:** {model_info}")
                                st.caption(f"📊 **Cálculo:** {calculation_details}")
                                
                                if 'aspect_ratio' in parametros:
                                    st.write(f"📐 **Relación de aspecto:** {parametros['aspect_ratio']}")
                        
                        # Información técnica
                        col_tech1, col_tech2 = st.columns(2)
                        with col_tech1:
                            st.write(f"📅 **Fecha de creación:** {fecha[:10]}")
                            st.write(f"🕐 **Hora de creación:** {fecha[11:19] if len(fecha) > 11 else 'N/A'}")
                        
                        with col_tech2:
                            if fecha:
                                try:
                                    fecha_obj = datetime.fromisoformat(fecha.replace('Z', '+00:00'))
                                    ahora = datetime.now()
                                    diferencia = ahora - fecha_obj.replace(tzinfo=None)
                                    
                                    if diferencia.days > 0:
                                        antiguedad = f"{diferencia.days} días"
                                    elif diferencia.seconds > 3600:
                                        antiguedad = f"{diferencia.seconds // 3600} horas"
                                    else:
                                        antiguedad = f"{diferencia.seconds // 60} minutos"
                                    
                                    st.write(f"⏰ **Antigüedad:** {antiguedad}")
                                except:
                                    st.write(f"⏰ **Antigüedad:** No calculable")
                        
                        if id_prediccion:
                            st.code(f"🆔 ID de predicción: {id_prediccion}")
                    
                    with col2:
                        # Preview y botones de acción - priorizar archivo local para videos
                        archivo_local = item.get('archivo_local')
                        local_path = HISTORY_DIR / archivo_local if archivo_local else None
                        
                        # Mostrar preview priorizando archivo local
                        preview_shown = False
                        if archivo_local and local_path and local_path.exists():
                            try:
                                if tipo.lower() in ['imagen', 'sticker']:
                                    st.image(str(local_path), caption="Preview (Local)", use_container_width=True)
                                elif tipo.lower() == 'video':
                                    st.video(str(local_path))
                                    st.caption("🎬 Reproduciendo desde archivo local")
                                preview_shown = True
                            except Exception as e:
                                st.warning(f"⚠️ Error con archivo local: {str(e)[:30]}...")
                        
                        # Si no se pudo mostrar desde archivo local, intentar URL
                        if not preview_shown and url:
                            try:
                                if tipo.lower() in ['imagen', 'sticker']:
                                    st.image(url, caption="Preview", use_container_width=True)
                                elif tipo.lower() == 'video':
                                    # Mejor visualización para videos en el historial
                                    st.markdown(f"""
                                    <div style="text-align: center; margin: 10px 0;">
                                        <video width="100%" height="250" controls style="border-radius: 8px;">
                                            <source src="{url}" type="video/mp4">
                                            <source src="{url}" type="video/webm">
                                            Tu navegador no soporta el elemento video.
                                        </video>
                                    </div>
                                    """, unsafe_allow_html=True)
                                    st.caption("🌐 Reproduciendo desde URL externa")
                            except Exception as e:
                                st.warning("🖼️ Preview no disponible")
                                st.caption(f"Error: {str(e)[:50]}...")
                        
                        # Botones de acción estandarizados - siempre dos botones
                        col_btn1, col_btn2 = st.columns(2)
                        
                        with col_btn1:
                            # Botón archivo local
                            if archivo_local:
                                local_path = HISTORY_DIR / archivo_local
                                if local_path.exists():
                                    if st.button("📁 Archivo Local", key=f"local_{i}", use_container_width=True, type="primary"):
                                        import subprocess
                                        import os
                                        # Abrir el archivo con el programa predeterminado del sistema
                                        if os.name == 'nt':  # Windows
                                            os.startfile(str(local_path))
                                        elif os.name == 'posix':  # macOS y Linux
                                            subprocess.call(['open' if 'darwin' in os.uname().sysname.lower() else 'xdg-open', str(local_path)])
                                else:
                                    st.button("📁 Local No Disponible", disabled=True, use_container_width=True, help="El archivo local no existe")
                            else:
                                st.button("� Sin Archivo Local", disabled=True, use_container_width=True, help="No hay archivo local guardado")
                        
                        with col_btn2:
                            # Botón URL Replicate
                            if url:
                                # Determinar el texto del botón según el tipo
                                if tipo.lower() == 'video':
                                    st.link_button("🔗 Ver en Replicate", url, use_container_width=True)
                                else:
                                    st.link_button("🔗 Ver en Replicate", url, use_container_width=True)
                            else:
                                st.button("🔗 Sin URL Replicate", disabled=True, use_container_width=True, help="No hay URL de Replicate disponible")
                        
                        # Indicadores de estado
                        if archivo_local and (HISTORY_DIR / archivo_local).exists():
                            st.success("🟢 Archivo disponible localmente")
                        else:
                            st.info("� Solo disponible en Replicate")
                        
                        # Información del archivo
                        if archivo_local:
                            st.caption(f"📄 **Archivo:** {archivo_local}")
                    
                    st.divider()
            
            # Información adicional
            if filtered_history:
                st.info(f"📈 **Total mostrado:** {len(filtered_history)} de {total_items} generaciones")
            
        else:
            st.info("📝 No hay elementos en el historial aún. ¡Genera tu primer contenido!")

elif st.session_state.current_page == 'biblioteca':
    # PÁGINA DE LA BIBLIOTECA
    # Cargar historial para la biblioteca
    history = load_history()
    
    if history:
        # CONTENIDO PRINCIPAL
        # Estadísticas rápidas en la parte superior
        stats_col1, stats_col2, stats_col3, stats_col4 = st.columns(4)
        total_items = len(history)
        total_imagenes = len([h for h in history if h.get('tipo') == 'imagen'])
        total_videos = len([h for h in history if h.get('tipo') == 'video'])
        total_stickers = len([h for h in history if h.get('tipo') == 'sticker'])
        total_cost_usd = sum(calculate_item_cost(h)[0] for h in history)
        
        with stats_col1:
            st.metric("📊 Total", total_items)
        with stats_col2:
            st.metric("🖼️ Imágenes", total_imagenes)
        with stats_col3:
            st.metric("🎬 Videos", total_videos)
        with stats_col4:
            st.markdown(f"""
            <div style="text-align: center; padding: 15px; background: linear-gradient(135deg, #28a745, #20c997); border-radius: 10px; color: white;">
                <div style="font-size: 14px; opacity: 0.9;">💰 COSTO TOTAL</div>
                <div style="font-size: 32px; font-weight: bold; margin: 8px 0;">${total_cost_usd:.2f}</div>
                <div style="font-size: 12px; opacity: 0.8;">Estimado USD</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.divider()
        
        # Filtros rápidos
        filter_col1, filter_col2, filter_col3, filter_col4 = st.columns(4)
        
        with filter_col1:
            filter_type = st.selectbox("Filtrar por tipo:", ["Todos", "imagen", "video", "sticker"])
        
        with filter_col2:
            sort_order = st.selectbox("Ordenar por:", ["Más reciente", "Más antiguo", "Tipo"])
        
        with filter_col3:
            items_per_row = st.slider("Items por fila:", 2, 6, 3)
        
        with filter_col4:
            image_size = st.selectbox("Tamaño de vista previa:", ["Pequeño", "Mediano", "Grande", "Extra Grande"], index=1)
        
        # Aplicar filtros
        filtered_items = history.copy()
        
        if filter_type != "Todos":
            filtered_items = [item for item in filtered_items if item.get('tipo') == filter_type]
        
        # Ordenar
        if sort_order == "Más reciente":
            filtered_items.sort(key=lambda x: x.get("fecha", ""), reverse=True)
        elif sort_order == "Más antiguo":
            filtered_items.sort(key=lambda x: x.get("fecha", ""))
        elif sort_order == "Tipo":
            filtered_items.sort(key=lambda x: x.get("tipo", ""))
        
        # Mostrar items en grid
        if filtered_items:
            # Dividir en filas
            for i in range(0, len(filtered_items), items_per_row):
                cols = st.columns(items_per_row)
                
                for j in range(items_per_row):
                    if i + j < len(filtered_items):
                        item = filtered_items[i + j]
                        original_index = history.index(item)
                        
                        with cols[j]:
                            # Card del item
                            st.markdown(f"""
                            <div style="
                                border: 2px solid #e0e0e0;
                                border-radius: 10px;
                                padding: 10px;
                                margin: 5px 0;
                                background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
                                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                            ">
                                <div style="display: flex; flex-direction: column; gap: 4px;">
                                    <h6 style="margin: 0; color: #2c3e50; font-size: 14px; font-weight: 600;">
                                        {item.get('tipo', 'Item').title()} #{original_index + 1}
                                    </h6>
                                    <p style="margin: 0; font-size: 11px; color: #666;">
                                        📅 {item.get('fecha', 'N/A')[:10]} | 🔗 {item.get('modelo', 'Modelo desconocido')[:15]}{'...' if len(item.get('modelo', 'Modelo desconocido')) > 15 else ''}
                                    </p>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Mostrar preview de la imagen/video
                            url = item.get('url')
                            archivo_local = item.get('archivo_local')
                            
                            # Priorizar archivo local para videos de Pixverse y VEO que pueden tener URLs expiradas
                            if archivo_local:
                                local_path = HISTORY_DIR / archivo_local
                                if local_path.exists():
                                    try:
                                        if item.get('tipo') == 'video':
                                            # Para archivos locales, usar st.video funciona mejor
                                            st.video(str(local_path))
                                            st.success(f"🎬 Reproduciendo desde archivo local: {archivo_local}")
                                        else:
                                            st.image(str(local_path), use_container_width=True)
                                    except Exception as e:
                                        st.markdown(f"""
                                        <div style="
                                            background: #f8f9fa;
                                            border: 2px dashed #dee2e6;
                                            border-radius: 10px;
                                            padding: 20px;
                                            text-align: center;
                                        ">
                                            <div style="font-size: 48px; margin-bottom: 10px;">🎬</div>
                                            <div style="color: #6c757d;">Video local: {archivo_local}</div>
                                            <div style="color: #dc3545; font-size: 12px;">Error: {str(e)[:50]}</div>
                                        </div>
                                        """, unsafe_allow_html=True)
                                else:
                                    # Archivo local no existe, intentar con URL
                                    if url:
                                        st.warning(f"⚠️ Archivo local no encontrado: {archivo_local}")
                                        st.info("🔗 Intentando cargar desde URL externa...")
                                        try:
                                            if item.get('tipo') == 'video':
                                                st.markdown(f"""
                                                <div style="text-align: center; margin: 20px 0;">
                                                    <video width="100%" height="400" controls style="border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.2);">
                                                        <source src="{url}" type="video/mp4">
                                                        <source src="{url}" type="video/webm">
                                                        <source src="{url}" type="video/quicktime">
                                                        Tu navegador no soporta el elemento video.
                                                    </video>
                                                </div>
                                                """, unsafe_allow_html=True)
                                            else:
                                                st.image(url, use_container_width=True)
                                        except:
                                            st.error("❌ Tanto el archivo local como la URL externa fallaron")
                                    else:
                                        st.warning(f"⚠️ Archivo local no encontrado: {archivo_local}")
                                        st.error("❌ No hay URL de respaldo disponible")
                            elif url:
                                try:
                                    if item.get('tipo') == 'video':
                                        # Para videos, usar HTML personalizado para mejor compatibilidad
                                        st.markdown(f"""
                                        <div style="text-align: center; margin: 20px 0;">
                                            <video width="100%" height="400" controls style="border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.2);">
                                                <source src="{url}" type="video/mp4">
                                                <source src="{url}" type="video/webm">
                                                <source src="{url}" type="video/quicktime">
                                                Tu navegador no soporta el elemento video.
                                                <br><br>
                                                <a href="{url}" target="_blank" style="color: #1f77b4; text-decoration: none;">
                                                    🔗 Abrir video en nueva pestaña
                                                </a>
                                            </video>
                                        </div>
                                        """, unsafe_allow_html=True)
                                        
                                        # Advertencia específica para el botón de nueva pestaña
                                        st.markdown(f"""
                                        <div style="text-align: center; margin: 10px 0;">
                                            <a href="{url}" target="_blank" style="
                                                background: linear-gradient(135deg, #667eea, #764ba2);
                                                color: white;
                                                padding: 8px 16px;
                                                text-decoration: none;
                                                border-radius: 6px;
                                                font-size: 14px;
                                            ">
                                                🎬 Abrir video en nueva pestaña
                                            </a>
                                        </div>
                                        """, unsafe_allow_html=True)
                                    else:
                                        st.image(url, use_container_width=True)
                                except Exception as e:
                                    st.markdown(f"""
                                    <div style="
                                        background: #f8f9fa;
                                        border: 2px dashed #dee2e6;
                                        border-radius: 10px;
                                        padding: 20px;
                                        text-align: center;
                                        margin: 20px 0;
                                    ">
                                        <div style="font-size: 48px; margin-bottom: 10px;">🎬</div>
                                        <div style="color: #6c757d; margin-bottom: 15px;">Vista previa no disponible</div>
                                        <div style="color: #dc3545; font-size: 12px; margin-bottom: 15px;">Error: {str(e)[:50]}</div>
                                        <a href="{url}" target="_blank" style="
                                            background: #007bff;
                                            color: white;
                                            padding: 10px 20px;
                                            text-decoration: none;
                                            border-radius: 6px;
                                        ">
                                            Ver contenido original
                                        </a>
                                    </div>
                                    """, unsafe_allow_html=True)
                            else:
                                st.markdown("❌ Sin preview disponible")
                            
                            # Prompt truncado
                            prompt = item.get('prompt', '')
                            if prompt:
                                prompt_preview = prompt[:80] + "..." if len(prompt) > 80 else prompt
                                st.caption(f"💬 {prompt_preview}")
                            
                            # Botón Ver detalles
                            if st.button("👁️ Ver detalles", key=f"details_{original_index}", use_container_width=True):
                                st.session_state.selected_item_index = original_index
                                st.rerun()
            
            st.markdown(f"---")
            st.info(f"📊 Mostrando {len(filtered_items)} de {len(history)} items")
            
        else:
            st.info("🔍 No se encontraron items con los filtros seleccionados")
        
        # POPUP DE DETALLES
        if st.session_state.selected_item_index is not None and st.session_state.selected_item_index < len(history):
            selected_item = history[st.session_state.selected_item_index]
            
            # Crear popup con st.dialog
            @st.dialog("📋 Detalles del Item", width="large")
            def show_item_details():
                # Fila superior: Info básica + Botón cerrar
                col1, col2, col3 = st.columns([3, 3, 1])
                with col1:
                    st.markdown(f"<div style='text-align: center; padding: 8px;'><h5 style='margin: 0; color: #2c3e50;'>🎯 {selected_item.get('tipo', 'N/A').title()}</h5><small style='color: #6c757d;'>📅 {selected_item.get('fecha', 'N/A')[:10]}</small></div>", unsafe_allow_html=True)
                with col2:
                    # Usar la función de cálculo real en lugar del hardcodeado
                    cost_usd, model_info, calculation_details = calculate_item_cost(selected_item)
                    st.markdown(f"<div style='text-align: center; padding: 8px;'><h5 style='margin: 0; color: #495057;'>🔗 {selected_item.get('modelo', 'N/A')[:15]}</h5><div style='font-size: 18px; font-weight: bold; color: #28a745; margin-top: 5px;'>💰 ${cost_usd:.3f}</div></div>", unsafe_allow_html=True)
                with col3:
                    st.markdown("<div style='text-align: center; padding: 8px;'>", unsafe_allow_html=True)
                    if st.button("❌", key="close_popup", help="Cerrar"):
                        st.session_state.selected_item_index = None
                        st.rerun()
                    st.markdown("</div>", unsafe_allow_html=True)
                
                # Separador visual
                st.markdown("<hr style='margin: 10px 0; border: 1px solid #e9ecef;'>", unsafe_allow_html=True)
                
                # Fila de datos económicos con fuente más grande y simétrica
                eco_col1, eco_col2, eco_col3, eco_col4 = st.columns(4)
                with eco_col1:
                    cost_eur = cost_usd * 0.92
                    st.markdown(f"""
                    <div style='text-align: center; padding: 12px; background: #f8f9fa; border-radius: 8px; margin: 4px;'>
                        <h2 style='margin: 0; color: #28a745; font-weight: bold;'>💵 ${cost_usd:.3f}</h2>
                        <small style='color: #6c757d; font-weight: 500;'>Costo USD</small>
                    </div>
                    """, unsafe_allow_html=True)
                with eco_col2:
                    st.markdown(f"""
                    <div style='text-align: center; padding: 12px; background: #f8f9fa; border-radius: 8px; margin: 4px;'>
                        <h2 style='margin: 0; color: #007bff; font-weight: bold;'>💶 €{cost_eur:.3f}</h2>
                        <small style='color: #6c757d; font-weight: 500;'>Costo EUR</small>
                    </div>
                    """, unsafe_allow_html=True)
                with eco_col3:
                    plantilla = selected_item.get('plantilla', 'Sin plantilla')
                    plantilla_short = plantilla[:10] + "..." if len(plantilla) > 10 else plantilla
                    st.markdown(f"""
                    <div style='text-align: center; padding: 12px; background: #f8f9fa; border-radius: 8px; margin: 4px;'>
                        <h5 style='margin: 0; color: #6c757d; font-weight: bold;'>🎨 {plantilla_short}</h5>
                        <small style='color: #6c757d; font-weight: 500;'>Plantilla</small>
                    </div>
                    """, unsafe_allow_html=True)
                with eco_col4:
                    fecha = selected_item.get('fecha', '')
                    if fecha:
                        try:
                            fecha_obj = datetime.fromisoformat(fecha.replace('Z', '+00:00'))
                            ahora = datetime.now()
                            diferencia = ahora - fecha_obj.replace(tzinfo=None)
                            if diferencia.days > 0:
                                antiguedad = f"{diferencia.days}d"
                            elif diferencia.seconds > 3600:
                                antiguedad = f"{diferencia.seconds // 3600}h"
                            else:
                                antiguedad = f"{diferencia.seconds // 60}m"
                            st.markdown(f"""
                            <div style='text-align: center; padding: 12px; background: #f8f9fa; border-radius: 8px; margin: 4px;'>
                                <h5 style='margin: 0; color: #fd7e14; font-weight: bold;'>⏰ {antiguedad}</h5>
                                <small style='color: #6c757d; font-weight: 500;'>Antigüedad</small>
                            </div>
                            """, unsafe_allow_html=True)
                        except:
                            st.markdown(f"""
                            <div style='text-align: center; padding: 12px; background: #f8f9fa; border-radius: 8px; margin: 4px;'>
                                <h5 style='margin: 0; color: #6c757d; font-weight: bold;'>⏰ N/A</h5>
                                <small style='color: #6c757d; font-weight: 500;'>Antigüedad</small>
                            </div>
                            """, unsafe_allow_html=True)
                
                # Separador visual
                st.markdown("<hr style='margin: 10px 0; border: 1px solid #e9ecef;'>", unsafe_allow_html=True)
                
                # Prompt en área más pequeña
                st.markdown("**📝 Prompt:**")
                st.text_area("", value=selected_item.get('prompt', 'Sin prompt disponible'), height=80, disabled=True, label_visibility="collapsed")
                
                # Detalles del cálculo de costo
                st.markdown("**💰 Detalles del Costo:**")
                st.caption(f"🔢 **Modelo:** {model_info}")
                st.caption(f"📊 **Cálculo:** {calculation_details}")
                
                # Fila inferior: Botones de acceso estandarizados
                archivo_local = selected_item.get('archivo_local', '')
                url = selected_item.get('url', '')
                
                col1, col2 = st.columns(2)
                with col1:
                    # Botón archivo local
                    if archivo_local:
                        local_path = HISTORY_DIR / archivo_local
                        if local_path.exists():
                            if st.button("📁 Abrir Archivo Local", key="popup_local", use_container_width=True, type="primary"):
                                import subprocess
                                import os
                                # Abrir el archivo con el programa predeterminado del sistema
                                if os.name == 'nt':  # Windows
                                    os.startfile(str(local_path))
                                elif os.name == 'posix':  # macOS y Linux
                                    subprocess.call(['open' if 'darwin' in os.uname().sysname.lower() else 'xdg-open', str(local_path)])
                            file_size = local_path.stat().st_size / (1024 * 1024)
                            st.success(f"📁 Disponible • {file_size:.1f}MB")
                        else:
                            st.button("📁 Local No Disponible", disabled=True, use_container_width=True, help="El archivo local no existe")
                            st.error("❌ Archivo no encontrado")
                    else:
                        st.button("📁 Sin Archivo Local", disabled=True, use_container_width=True, help="No hay archivo local guardado")
                        st.info("📁 No guardado localmente")
                
                with col2:
                    # Botón URL Replicate
                    if url:
                        st.link_button("� Ver en Replicate", url, use_container_width=True)
                        st.success("🔗 URL disponible")
                    else:
                        st.button("🔗 Sin URL Replicate", disabled=True, use_container_width=True, help="No hay URL de Replicate disponible")
                        st.info("🔗 URL no disponible")
                
                # Botón de cerrar compacto
                if st.button("✅ Cerrar", key="close_bottom", use_container_width=True, type="primary"):
                    st.session_state.selected_item_index = None
                    st.rerun()
            
            # Mostrar el popup
            show_item_details()
    
    else:
        st.info("📝 No hay contenido en la biblioteca aún. ¡Genera tu primer contenido en el Generador!")
        
        if st.button("🚀 Ir al Generador"):
            st.session_state.current_page = 'generator'
            st.rerun()


