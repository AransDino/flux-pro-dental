import replicate
import os
from datetime import datetime

# Configurar token de forma segura
def load_config():
    try:
        from config import REPLICATE_API_TOKEN
        if REPLICATE_API_TOKEN == "tu_token_aqui":
            print("❌ Error: Token no configurado. Edita config.py")
            return False
        os.environ["REPLICATE_API_TOKEN"] = REPLICATE_API_TOKEN
        return True
    except ImportError:
        print("❌ Error: Archivo config.py no encontrado")
        print("💡 Copia config.example.py como config.py y configura tu token")
        return False

# Función para generar video anime
def generate_anime_video(prompt, **params):
    if not load_config():
        return None
    
    try:
        print(f"🎭 Generando video anime...")
        print(f"📝 Prompt: {prompt}")
        print(f"⚙️ Parámetros: {params}")
        
        start_time = datetime.now()
        print(f"⏰ Iniciado a las: {start_time.strftime('%H:%M:%S')}")
        
        output = replicate.run(
            "pixverse/pixverse-v3.5",
            input={
                "prompt": prompt,
                **params
            }
        )
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        print(f"✅ Video generado exitosamente!")
        print(f"⏱️ Tiempo transcurrido: {duration:.2f} segundos")
        print(f"🔗 URL del video: {output}")
        
        return output
        
    except Exception as e:
        print(f"❌ Error durante la generación: {str(e)}")
        return None

# Configuración por defecto
if __name__ == "__main__":
    # Parámetros de ejemplo
    params = {
        "style": "anime",
        "effect": "None",
        "quality": "720p",
        "duration": 5,
        "motion_mode": "normal",
        "aspect_ratio": "16:9",
        "negative_prompt": "",
        "sound_effect_switch": False
    }
    
    # Prompt de ejemplo
    prompt = "an anime action scene, a woman looks around slowly, mountain landscape in the background"
    
    # Generar video
    result = generate_anime_video(prompt, **params)
    
    if result:
        print(f"\n🎉 ¡Proceso completado!")
        print(f"📱 Usa esta URL para ver tu video: {result}")
    else:
        print("\n💥 La generación falló. Revisa la configuración.")