import pandas as pd

# Carichiamo il catalogo una sola volta, all'avvio
_df_catalogo = pd.read_csv("Catalogo_Aftermarket.csv")


def cerca_prezzo_aftermarket(marca: str, modello: str, componente: str) -> dict:
    """
    INTERFACCIA STABILE - stessa logica usata nel progetto ricambisti.
    In futuro, quando avrai un vero listino fornitore o TecDoc,
    sostituirai solo il "dentro" di questa funzione.

    INPUT:  marca, modello, componente (stringhe)
    OUTPUT: dizionario standard con risultati OEM + aftermarket trovati
    """

    if not marca or not modello or not componente:
        return {
            "trovato": False,
            "risultati": [],
            "errore": "Dati insufficienti per la ricerca (manca marca, modello o componente)."
        }

    match = _df_catalogo[
        (_df_catalogo["marca"].str.lower() == marca.lower()) &
        (_df_catalogo["modello"].str.lower().apply(lambda m: m in modello.lower())) &
        (_df_catalogo["componente"].str.lower() == componente.lower())
    ]

    if match.empty:
        return {
            "trovato": False,
            "risultati": [],
            "errore": "Nessun ricambio trovato nel catalogo per questo veicolo/componente."
        }

    risultati = []
    for _, riga in match.iterrows():
        risultati.append({
            "tipo": riga["tipo"],
            "brand": riga["brand"],
            "codice": riga["codice"],
            "prezzo_euro": float(riga["prezzo_euro"]),
            "disponibile": riga["disponibilita"].strip().lower() == "si",
            "note": riga["note"]
        })

    # Ordiniamo per mostrare sempre prima l'OEM, poi gli aftermarket
    risultati.sort(key=lambda r: r["tipo"] != "OEM")

    return {
        "trovato": True,
        "risultati": risultati,
        "errore": None
    }


# --- TEST (nessun costo, è solo lettura del CSV locale) ---
if __name__ == "__main__":
    import json
    risultato = cerca_prezzo_aftermarket("Fiat", "Panda", "Pastiglie freno")
    print(json.dumps(risultato, indent=2, ensure_ascii=False))