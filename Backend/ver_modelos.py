import os
from google import genai
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    print("❌ No hay llave de Gemini")
else:
    print("🔍 Buscando modelos disponibles para tu API Key...")
    client = genai.Client(api_key=GEMINI_API_KEY)
    
    # Listamos todos los modelos que tu llave puede usar
    for m in client.models.list():
        # Filtramos para mostrar solo los de la familia Gemini
        if "gemini" in m.name:
            print(f"✅ Modelo disponible: {m.name}")