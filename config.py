import os
from dotenv import load_dotenv

load_dotenv()  # legge il file .env

API_KEY = os.getenv("INFOTARGA_API_KEY")

if API_KEY:
    print("✅ Chiave caricata correttamente (non la mostro per sicurezza)")
else:
    print("❌ Chiave NON trovata. Controlla il file .env")