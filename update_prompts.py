import json
from pathlib import Path
from datetime import datetime

# Configuración
HISTORY_DIR = Path("historial")
history_file = HISTORY_DIR / "history.json"

def update_video_prompts():
    print("=== ACTUALIZANDO PROMPTS DE VIDEOS RECUPERADOS ===")
    
    # Cargar historial actual
    with open(history_file, 'r', encoding='utf-8') as f:
        all_data = json.load(f)
    
    print(f"📋 Elementos actuales: {len(all_data)}")
    
    # Actualizar elementos recuperados con prompts mejorados
    updated_count = 0
    for item in all_data:
        if item.get('recuperado') and item.get('archivo_local'):
            filename = item['archivo_local']
            print(f"\n🔄 Actualizando: {filename}")
            
            # Prompts mejorados basados en el tipo
            if item['tipo'] == "video_anime":
                new_prompt = "Una épica escena de acción de anime con personajes dinámicos en movimiento, efectos visuales espectaculares y una cinematografía dramática que captura la intensidad del momento"
                print(f"   📝 Nuevo prompt (Anime): {new_prompt[:60]}...")
            elif item['tipo'] == "video_seedance":
                new_prompt = "Un hermoso amanecer con colores cálidos y dorados que se extienden por el horizonte, creando una atmósfera serena y majestuosa mientras la luz suave ilumina el paisaje"
                print(f"   📝 Nuevo prompt (Amanecer): {new_prompt[:60]}...")
            else:
                continue
            
            # Actualizar el prompt
            item['prompt'] = new_prompt
            item['nota'] = f"Prompt recuperado de plantilla - archivo original: {filename}"
            updated_count += 1
            print(f"   ✅ Actualizado")
    
    # Guardar cambios
    with open(history_file, 'w', encoding='utf-8') as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Prompts actualizados: {updated_count} videos")
    print(f"📋 Total elementos: {len(all_data)}")
    
    return all_data

if __name__ == "__main__":
    update_video_prompts()
