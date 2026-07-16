# Simula la risposta di InfoTarga per una targa NON trovata,
# senza fare nessuna chiamata reale (0 costo)

def simula_risposta_targa_non_trovata():
    return {
        "trovato": False,
        "marca": None,
        "modello": None,
        "cilindrata": None,
        "errore": "Targa non trovata nel database InfoTarga",
        "fonte": "InfoTarga (simulato)"
    }

risultato = simula_risposta_targa_non_trovata()
print(risultato)