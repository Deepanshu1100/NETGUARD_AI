import google.generativeai as genai
import os
from dotenv import load_dotenv

# API Key load karo
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

print("🔍 Checking available Gemini models for your API Key...")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"✅ Found Model: {m.name}")
except Exception as e:
    print(f"❌ Error: {e}")