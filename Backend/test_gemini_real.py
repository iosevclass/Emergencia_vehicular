import asyncio
import httpx
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Cargamos el .env
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

async def probar_gemini_vision():
    if not GEMINI_API_KEY:
        print("❌ No se encontró GEMINI_API_KEY en el .env")
        return

    # Inicializamos el cliente oficial de Google
    client = genai.Client(api_key=GEMINI_API_KEY)
    
    # Usamos el modelo exacto que nos devolvió tu script
    modelo_gemini = 'gemini-2.5-flash' 

    print(f"🚀 INICIANDO PRUEBA REAL CON GEMINI ({modelo_gemini})...")

    # ==========================================
    # PRUEBA DE IMAGEN (Usando tu URL real de Cloudinary)
    # ==========================================
    print("\n📸 Descargando imagen de Cloudinary...")
    url_foto = "https://res.cloudinary.com/dh8zaedgv/image/upload/v1777322111/bc87189f-aad2-45ec-98ab-893e95ca27d7.png"
    
    async with httpx.AsyncClient(timeout=30.0) as client_http:
        try:
            resp = await client_http.get(url_foto)
            if resp.status_code == 200:
                print("📥 Imagen descargada correctamente (Bytes OK).")
                print("🧠 Enviando a Gemini para análisis...")
                
                # Preparamos la imagen para el nuevo SDK
                imagen_part = types.Part.from_bytes(
                    data=resp.content,
                    mime_type='image/jpeg'
                )
                
                # Le pasamos la descripción real de tu emergencia #33
                prompt_vision = "Eres un mecánico experto. Analiza esta foto y la descripción: 'mi auto se trabó está goteando aceite por debajo y no avanza pero sí enciende'. Redacta un diagnóstico breve sin usar emojis y clasifica la prioridad estrictamente como: 'alta', 'media' o 'baja'."
                
                # Llamada a la IA
                res_vision = await client.aio.models.generate_content(
                    model=modelo_gemini,
                    contents=[prompt_vision, imagen_part]
                )
                
                print("\n" + "="*50)
                print("✅ RESULTADO VISIÓN:")
                print("="*50)
                print(res_vision.text)
                print("="*50)
            else:
                print(f"❌ Error al descargar imagen: {resp.status_code}")
        except Exception as e:
            print(f"❌ Error en la descarga o proceso: {e}")

if __name__ == "__main__":
    asyncio.run(probar_gemini_vision())