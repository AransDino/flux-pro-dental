import os
import time
import replicate
import requests
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

client = replicate.Client()

prompt_text = """
A hyper-realistic 3D dental illustration showing a top view of the lower dental arch with multiple inlays and onlays placed in molars. The gum tissue and all surrounding teeth are anatomically accurate with realistic textures. Several premolars and molars have visible ceramic restorations perfectly fitted into prepared cavities — demonstrating different types of indirect dental restorations. High detail on enamel, restoration surfaces, and gum tissue. Clean white or neutral background. Medical-grade rendering, ideal for dental education and clinical presentations. --ar 3:2 --v 6 --style raw --quality 2

"""

# Registro de hora inicial
start_time = time.time()
start_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print(f"🟡 Proceso iniciado a las {start_datetime}")

# Lanza la predicción
prediction = client.predictions.create(
    version="black-forest-labs/flux-pro",
    input={
        "steps": 25,
        "width": 1024,
        "height": 1024,
        "prompt": prompt_text,
        "guidance": 3,
        "interval": 2,
        "aspect_ratio": "1:1",
        "output_format": "webp",
        "output_quality": 80,
        "safety_tolerance": 2,
        "prompt_upsampling": False
    }
)

print(f"🔁 ID de predicción: {prediction.id}")
print("⏳ Esperando respuesta del modelo...")

# Temporizador
timeout = 2400  # 40 minutos

# Bucle de espera con contador en segundos
while prediction.status not in ["succeeded", "failed", "canceled"]:
    elapsed = int(time.time() - start_time)
    estado_legible = "waiting response" if prediction.status == "starting" else prediction.status
    print(f"\r⏱ [{elapsed}s] Estado: {estado_legible}...", end="", flush=True)
    if elapsed > timeout:
        print("\n⛔ Tiempo de espera excedido. Abortando.")
        break
    time.sleep(2)
    prediction.reload()

# Resultado final
print()  # Salto de línea después del bucle
if prediction.status == "succeeded":
    image_url = prediction.output[0]
    response = requests.get(image_url)
    output_path = os.path.join(os.path.dirname(__file__), "dental_crown.webp")
    with open(output_path, "wb") as f:
        f.write(response.content)
    print(f"✅ Imagen generada y guardada como '{output_path}'")
elif prediction.status == "failed":
    print("❌ La generación falló:")
    print(prediction.error)
else:
    print(f"⚠️ Finalizó con estado: {prediction.status}")