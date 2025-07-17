import os
import replicate
from datetime import datetime

# Importar configuración del token
try:
    from config import REPLICATE_API_TOKEN
    if REPLICATE_API_TOKEN == "tu_token_aqui":
        print("❌ Error: Token no configurado")
        print("📝 Por favor edita 'config.py' y configura tu token real de Replicate")
        exit(1)
    os.environ["REPLICATE_API_TOKEN"] = REPLICATE_API_TOKEN
except ImportError:
    print("❌ Error: No se encontró el archivo 'config.py'")
    print("📝 Por favor:")
    print("   1. Copia 'config.example.py' como 'config.py'")
    print("   2. Edita 'config.py' y configura tu token de Replicate")
    print("   3. Vuelve a ejecutar el script")
    exit(1)

# Registro de hora inicial
start_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print(f"🎬 Generación de video iniciada a las {start_datetime}")

output = replicate.run(
    "bytedance/seedance-1-pro",
    input={
        "fps": 24,
        "prompt": "El sol de la mañana entra en cascada a través de enormes cristaleras con vistas al océano. [Toma en travelling suave a ras de suelo] El reflejo dorado del amanecer se desliza sobre el suelo pulido mientras la cámara sigue las ruedas de un taburete dental que se empuja lentamente hacia un sillón naranja. [Dolly lento hacia arriba] El sillón se ilumina con luz cálida; gotas microscópicas de desinfectante brillan como rocío. [Paneo lateral amplio] Más allá del vidrio, el mar centellea y barcos lejanos cruzan el horizonte. [Close macro de instrumental sobre bandeja inox] Las piezas relucen con destellos azules mientras un higienista ajusta guantes. [Jib ascendiendo por detrás del sillón] Entra el primer paciente; la luz marina baña su rostro. [Rack focus: vista mar → rostro paciente → sillón naranja] La clínica despierta suavemente: pantallas encendiéndose, luces de equipo dental, un zumbido bajo de aspiración. La escena termina con un encuadre amplio donde los sillones naranjas se alinean frente al paisaje oceánico, simbolizando un comienzo fresco del día.",
        "duration": 5,
        "resolution": "1080p",
        "aspect_ratio": "16:9",
        "camera_fixed": False
    }
)

print("✅ Video generado exitosamente:")
print(output)