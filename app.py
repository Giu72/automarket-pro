import streamlit as st
from vehicle_api import get_vehicle_data_infotarga
from aftermarket_catalog import cerca_prezzo_aftermarket

st.set_page_config(page_title="Automarket Pro", page_icon="🚗")

st.title("🚗 Automarket Pro")
st.subheader("Ricerca dati veicolo da targa")

# Inizializziamo la "memoria" della pagina, se non esiste ancora
if "risultato_veicolo" not in st.session_state:
    st.session_state.risultato_veicolo = None

targa = st.text_input("Inserisci la targa", placeholder="es. AB123CD")

if st.button("Cerca veicolo") and targa:
    with st.spinner("Interrogazione in corso..."):
        st.session_state.risultato_veicolo = get_vehicle_data_infotarga(targa)

# Da qui in poi leggiamo sempre dalla "memoria", non dal risultato del click
risultato = st.session_state.risultato_veicolo

if risultato is not None:
    if risultato["trovato"]:
        st.success(f"Veicolo trovato (fonte: {risultato['fonte']})")

        col1, col2 = st.columns(2)
        col1.metric("Marca", risultato["marca"] or "—")
        col2.metric("Cilindrata", f"{risultato['cilindrata']} cc" if risultato["cilindrata"] else "—")

        st.markdown(f"**Modello:** {risultato['modello'] or '—'}")

        # --- Sezione ricerca prezzi aftermarket ---
        st.divider()
        st.subheader("💰 Ricerca prezzi aftermarket")
        componente = st.text_input("Che componente ti serve?", placeholder="es. Pastiglie freno")

        if st.button("Cerca prezzo") and componente:
            risultato_aftermarket = cerca_prezzo_aftermarket(
                risultato["marca"], risultato["modello"], componente
            )
            if risultato_aftermarket["trovato"]:
                for r in risultato_aftermarket["risultati"]:
                    disp_str = "✅ Disponibile" if r["disponibile"] else "❌ Su richiesta"
                    tipo_str = "🔧 Originale" if r["tipo"] == "OEM" else "⚙️ Equivalente"
                    st.write(f"{tipo_str} — **{r['brand']}** — Codice: `{r['codice']}` — **{r['prezzo_euro']}€** — {disp_str}")
                    st.caption(r["note"])
            else:
                st.warning(f"⚠️ {risultato_aftermarket['errore']}")