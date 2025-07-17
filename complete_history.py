import json
from pathlib import Path

# Cargar datos actuales
HISTORY_DIR = Path("historial")
history_file = HISTORY_DIR / "history.json"

with open(history_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"📋 Datos actuales: {len(data)} elementos")

# Lista de videos que deberían estar
videos_esperados = [
    {
        "archivo": "video_anime_20250717_181836.mp4",
        "tipo": "video_anime",
        "fecha": "2025-07-17T18:18:36",
        "prompt": "Una épica escena de acción de anime con personajes dinámicos en movimiento, efectos visuales espectaculares y una cinematografía dramática que captura la intensidad del momento",
        "plantilla": "🎭 Escena de Acción Anime",
        "parametros": {
            "duration": 5,
            "fps": None,
            "quality": "720p",
            "resolution": None
        }
    },
    {
        "archivo": "video_seedance_20250717_185303.mp4", 
        "tipo": "video_seedance",
        "fecha": "2025-07-17T18:53:03",
        "prompt": "Un hermoso amanecer con colores cálidos y dorados que se extienden por el horizonte, creando una atmósfera serena y majestuosa mientras la luz suave ilumina el paisaje",
        "plantilla": "🌅 Amanecer Épico",
        "parametros": {
            "duration": 5,
            "fps": 24,
            "quality": None,
            "resolution": "1080p"
        }
    }
]

# Agregar videos faltantes
added_count = 0
for video_info in videos_esperados:
    filename = video_info["archivo"]
    found = any(item.get('archivo_local') == filename for item in data)
    
    if not found:
        print(f"⚠️  Agregando: {filename}")
        
        new_entry = {
            "tipo": video_info["tipo"],
            "fecha": video_info["fecha"],
            "prompt": video_info["prompt"],
            "plantilla": video_info["plantilla"],
            "url": f"archivo_local:{filename}",
            "archivo_local": filename,
            "parametros": video_info["parametros"],
            "recuperado": True,
            "nota": f"Video recuperado - archivo original: {filename}"
        }
        
        data.append(new_entry)
        added_count += 1
    else:
        print(f"✅ Ya existe: {filename}")

if added_count > 0:
    # Ordenar por fecha
    data.sort(key=lambda x: x.get('fecha', ''), reverse=True)
    
    # Guardar
    with open(history_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Agregados {added_count} videos. Total: {len(data)} elementos")
else:
    print(f"\n✅ Todos los videos ya están en el historial")

print("\n📊 Resumen final:")
tipos = {}
for item in data:
    tipo = item['tipo']
    tipos[tipo] = tipos.get(tipo, 0) + 1

for tipo, count in tipos.items():
    print(f"   {tipo}: {count}")
