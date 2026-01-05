import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
print("Using key:", api_key[:6] + "****" if api_key else None)

client = genai.Client(api_key=api_key)

print("\n📦 AVAILABLE MODELS:\n")

for m in client.models.list():
    print(m.name)
