# test_gemini.py
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()  # Load .env file

# Set your API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# List available models
models = genai.list_models()
print("📦 Available Models:")
for model in models:
    print("🧠", model.name)

# Use a valid model (check your console above)
model = genai.GenerativeModel("gemini-1.5-flash")

# Generate content
response = model.generate_content("What's the capital of Japan?")
print("\n Response :", response.text)
