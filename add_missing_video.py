import json
from pathlib import Path
from datetime import datetime

# Cargar datos actuales
HISTORY_DIR = Path("historial")
history_file = HISTORY_DIR / "history.json"

with open(history_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"📋 Datos actuales: {len(data)} elementos")

# Verificar si falta el video más reciente
video_file = "video_seedance_20250717_192354.mp4"
found = any(item.get('archivo_local') == video_file for item in data)

if not found:
    print(f"⚠️  Video faltante: {video_file}")
    
    # Crear entrada para el video faltante
    new_entry = {
        "tipo": "video_seedance",
        "fecha": "2025-07-17T19:23:54",  # Hora estimada basada en el nombre del archivo
        "prompt": "Futuristic cityscape at night, neon lights reflecting on wet streets, slow camera pan across towering skyscrapers, cyberpunk atmosphere, dramatic lighting, urban cinematic scene.",
        "plantilla": "🏙️ Ciudad Futurista",
        "url": f"archivo_local:{video_file}",
        "archivo_local": video_file,
        "parametros": {
            "fps": 24,
            "duration": 5,
            "resolution": "1080p",
            "aspect_ratio": "16:9",
            "camera_fixed": False
        },
        "recuperado": True,
        "nota": "Video recuperado - generado recientemente"
    }
    
    # Agregar al principio
    data.insert(0, new_entry)
    
    # Guardar
    with open(history_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Video agregado. Total: {len(data)} elementos")
else:
    print(f"✅ Video ya está en el historial")

print("\n📊 Resumen:")
tipos = {}
for item in data:
    tipo = item['tipo']
    tipos[tipo] = tipos.get(tipo, 0) + 1

for tipo, count in tipos.items():
    print(f"   {tipo}: {count}")
