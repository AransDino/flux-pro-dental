import json
from pathlib import Path

# Consolidar archivos de historial
HISTORY_DIR = Path("historial")
history_file = HISTORY_DIR / "history.json"
historial_file = HISTORY_DIR / "historial.json"

def consolidate_history():
    # Cargar ambos archivos
    history_data = []
    historial_data = []
    
    if history_file.exists():
        with open(history_file, 'r', encoding='utf-8') as f:
            history_data = json.load(f)
    
    if historial_file.exists():
        with open(historial_file, 'r', encoding='utf-8') as f:
            historial_data = json.load(f)
    
    # Combinar los datos (historial.json parece tener más datos)
    all_data = historial_data + [item for item in history_data if item not in historial_data]
    
    # Ordenar por fecha (más reciente primero)
    all_data.sort(key=lambda x: x.get('fecha', ''), reverse=True)
    
    # Guardar consolidado en history.json
    with open(history_file, 'w', encoding='utf-8') as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Consolidado: {len(all_data)} elementos en history.json")
    return all_data

if __name__ == "__main__":
    print("=== CONSOLIDANDO HISTORIAL ===")
    data = consolidate_history()
    for i, item in enumerate(data):
        print(f"{i+1}. {item['tipo']} - {item['fecha'][:19]} - {item['prompt'][:50]}...")
