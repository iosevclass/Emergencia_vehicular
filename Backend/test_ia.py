import asyncio
import httpx
import os
from dotenv import load_dotenv

# Cargamos el .env para sacar tu GROQ_API_KEY
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

async def probar_texto():
    print("⏳ PROBANDO LLaMA 3.1 (SOLO TEXTO)...")
    async with httpx.AsyncClient(timeout=15.0) as client:
        response = await client.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {GROQ_API_KEY}"},
            json={
                "model": "llama-3.1-8b-instant",
                "messages": [{"role": "user", "content": "Hola, actúa como mecánico. ¿Qué significa si sale humo azul del escape?"}]
            }
        )
        if response.status_code == 200:
            print("✅ ÉXITO TEXTO:")
            print(response.json()['choices'][0]['message']['content'])
        else:
            print(f"❌ ERROR TEXTO ({response.status_code}): {response.text}")
    print("-" * 50)

async def probar_vision():
    print("⏳ PROBANDO LLaMA 3.2 VISION (TEXTO + FOTO)...")
    async with httpx.AsyncClient(timeout=15.0) as client:
        response = await client.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {GROQ_API_KEY}"},
            json={
                # --- NUEVO MODELO MULTIMODAL ACTIVO EN GROQ ---
                "model": "meta-llama/llama-4-scout-17b-16e-instruct",
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "Eres un mecánico. Describe brevemente el daño en este auto."},
                            {"type": "image_url", "image_url": {"url": "https://upload.wikimedia.org/wikipedia/commons/e/e1/Car_crash_1.jpg"}}
                        ]
                    }
                ]
            }
        )
        if response.status_code == 200:
            print("✅ ÉXITO VISIÓN:")
            print(response.json()['choices'][0]['message']['content'])
        else:
            print(f"❌ ERROR VISIÓN ({response.status_code}): {response.text}")
    print("-" * 50)

async def main():
    if not GROQ_API_KEY:
        print("❌ No se encontró la GROQ_API_KEY en el archivo .env")
        return
    
    await probar_texto()
    await probar_vision()

if __name__ == "__main__":
    asyncio.run(main())