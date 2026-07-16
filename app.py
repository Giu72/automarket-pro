import streamlit as st
from vehicle_api import get_vehicle_data_infotarga

st.set_page_config(page_title="Automarket Pro", page_icon="🚗")

st.title("🚗 Automarket Pro")
st.subheader("Ricerca dati veicolo da targa")

targa = st.text_input("Inserisci la targa", placeholder="es. AB123CD")

if st.button("Cerca veicolo") and targa:
   with st.spinner("Interrogazione in corso..."):
        risultato = get_vehicle_data_infotarga(targa)

    if risultato["trovato"]:
        st.success(f"Veicolo trovato (fonte: {risultato['fonte']})")

        col1, col2 = st.columns(2)
        col1.metric("Marca", risultato["marca"] or "—")
        col2.metric("Cilindrata", f"{risultato['cilindrata']} cc" if risultato["cilindrata"] else "—")

        st.markdown(f"**Modello:** {risultato['modello'] or '—'}")
    else:
        st.error(f"⚠️ {risultato['errore']}")