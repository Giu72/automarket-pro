import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("INFOTARGA_API_KEY")
BASE_URL = "https://api.infotarga.com/v2/query"


def get_vehicle_data_infotarga(plate: str) -> dict:
    """
    Interroga InfoTarga e restituisce un formato STANDARD, uguale per
    qualsiasi fonte dati futura (OEM, aftermarket, ecc.).
    """
    if not API_KEY:
        return {"trovato": False, "marca": None, "modello": None,
                "cilindrata": None, "errore": "Chiave API mancante nel .env", "fonte": "InfoTarga"}

    headers = {"x-api-key": API_KEY, "Content-Type": "application/json"}
    payload = {"plate": plate.strip().upper(), "type": "car", "details": True}

    try:
        response = requests.post(BASE_URL, headers=headers, json=payload, timeout=10)
        body = response.json()
    except requests.exceptions.RequestException as e:
        return {"trovato": False, "marca": None, "modello": None,
                "cilindrata": None, "errore": f"Errore di connessione: {e}", "fonte": "InfoTarga"}

    if not body.get("success", False):
        return {"trovato": False, "marca": None, "modello": None,
                "cilindrata": None, "errore": body.get("message", "Errore sconosciuto"), "fonte": "InfoTarga"}

    data = body.get("data", {})
    engine = data.get("engine", {})

    return {
        "trovato": True,
        "marca": data.get("brand"),
        "modello": data.get("model"),
        "cilindrata": engine.get("cc"),
        "errore": None,
        "fonte": "InfoTarga"
    }