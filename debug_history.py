import json
from pathlib import Path

# Configuración de directorios
HISTORY_DIR = Path("historial")
HISTORY_FILE = HISTORY_DIR / "history.json"

def load_history():
    """Cargar historial desde archivo JSON"""
    print(f"🔍 Verificando archivo: {HISTORY_FILE}")
    print(f"🔍 Existe archivo: {HISTORY_FILE.exists()}")
    
    if HISTORY_FILE.exists():
        try:
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                print(f"🔍 Datos cargados: {len(data)} elementos")
                print(f"🔍 Primer elemento: {data[0] if data else 'N/A'}")
                return data
        except Exception as e:
            print(f"❌ Error al cargar: {e}")
            return []
    return []

if __name__ == "__main__":
    print("=== DIAGNÓSTICO DEL HISTORIAL ===")
    history = load_history()
    print(f"Total elementos: {len(history)}")
