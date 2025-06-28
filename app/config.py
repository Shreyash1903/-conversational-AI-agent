# app/config.py

import os
from dotenv import load_dotenv

load_dotenv()  # This loads the .env file

# Load Gemini API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
print("🔐 Loaded GEMINI API Key :", GEMINI_API_KEY)

SCOPES = ["https://www.googleapis.com/auth/calendar"]
CREDENTIALS_FILE = "credentials.json"
