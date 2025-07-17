import json
from pathlib import Path
from datetime import datetime

# Configuración
HISTORY_DIR = Path("historial")
history_file = HISTORY_DIR / "history.json"

def clean_and_rebuild_history():
    print("=== LIMPIANDO Y RECONSTRUYENDO HISTORIAL ===")
    
    # Cargar historial actual
    with open(history_file, 'r', encoding='utf-8') as f:
        all_data = json.load(f)
    
    print(f"📋 Elementos actuales: {len(all_data)}")
    
    # Filtrar solo elementos que NO sean recuperados o que tengan fechas válidas
    clean_data = []
    videos_to_recover = []
    
    for item in all_data:
        if item.get('recuperado'):
            # Es un elemento recuperado, vamos a re-procesarlo
            if item.get('archivo_local'):
                videos_to_recover.append(item['archivo_local'])
            print(f"   🔄 Marcando para re-procesar: {item.get('archivo_local', 'N/A')}")
        elif item.get('fecha') != "2025-07-17T::":
            # Elemento válido, mantener
            clean_data.append(item)
            print(f"   ✅ Manteniendo: {item.get('tipo', 'N/A')} - {item.get('fecha', 'N/A')[:19]}")
    
    print(f"\n📋 Elementos limpios: {len(clean_data)}")
    print(f"🎬 Videos para recuperar: {len(videos_to_recover)}")
    
    # Re-procesar videos con fechas correctas
    for video_file in videos_to_recover:
        filename = video_file
        print(f"\n🔧 Re-procesando: {filename}")
        
        # Determinar tipo
        if "anime" in filename:
            tipo = "video_anime"
            plantilla = "🎭 Escena de Acción Anime"
        else:
            tipo = "video_seedance" 
            plantilla = "🌅 Amanecer Épico"
        
        # Parsear fecha correctamente
        try:
            parts = filename.split('_')
            if len(parts) >= 4:
                date_part = parts[2]  # 20250717
                time_part = parts[3].split('.')[0]  # 181836
                date_str = f"{date_part[:4]}-{date_part[4:6]}-{date_part[6:8]}T{time_part[:2]}:{time_part[2:4]}:{time_part[4:6]}"
                print(f"   📅 Fecha parseada: {date_str}")
            else:
                date_str = datetime.now().isoformat()
                print(f"   ⚠️  Usando fecha actual: {date_str}")
        except Exception as e:
            print(f"   ❌ Error parseando fecha: {e}")
            date_str = datetime.now().isoformat()
        
        # Crear entrada corregida
        recovery_item = {
            "tipo": tipo,
            "fecha": date_str,
            "prompt": f"Video generado anteriormente (recuperado del archivo {filename})",
            "plantilla": plantilla,
            "url": f"archivo_local:{filename}",
            "archivo_local": filename,
            "parametros": {
                "duration": 5,
                "fps": 24 if tipo == "video_seedance" else None,
                "quality": "720p" if tipo == "video_anime" else None,
                "resolution": "1080p" if tipo == "video_seedance" else None
            },
            "recuperado": True
        }
        clean_data.append(recovery_item)
        print(f"   ✅ Agregado con fecha correcta")
    
    # Ordenar por fecha
    clean_data.sort(key=lambda x: x.get('fecha', ''), reverse=True)
    
    # Guardar
    with open(history_file, 'w', encoding='utf-8') as f:
        json.dump(clean_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Historial reconstruido: {len(clean_data)} elementos")
    
    # Mostrar resumen
    tipos = {}
    for item in clean_data:
        tipo = item['tipo']
        tipos[tipo] = tipos.get(tipo, 0) + 1
    
    print("\n📊 Resumen final:")
    for tipo, count in tipos.items():
        print(f"   {tipo}: {count}")
    
    return clean_data

if __name__ == "__main__":
    clean_and_rebuild_history()
