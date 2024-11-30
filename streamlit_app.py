import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from llm import *

# Configurazione del tema
st.set_page_config(page_title="Gaia - Sicurezza e Supporto", layout="centered")

# Stile personalizzato per sfondo rosso e scritte bianche
st.markdown(
    """
    <style>
    body {
        background-color: #ff0000; /* Rosso */
        color: #ffffff;           /* Bianco */
    }
    .stTextInput label, .stButton button, .stTextArea label, .stChatMessage {
        color: #ffffff !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Navigazione tra le pagine
menu = st.sidebar.selectbox("Naviga tra le pagine", ["Home", "Chat con Gaia", "Mappa Aree Rischiose"])

# Pagina 1: Nome e Descrizione dell'App
if menu == "Home":
    st.title("Gaia - Sicurezza e Supporto")
    st.write(
        """
        Gaia è un'applicazione mobile progettata per fornire supporto emotivo e sicurezza alle donne.
        Attraverso l'intelligenza artificiale, Gaia simula una conversazione per offrire compagnia
        e può aiutarti a contattare i servizi di emergenza in caso di pericolo.
        """
    )
 


# Pagina 2: Chat con Gaia
# Verifica se la sessione contiene una "history" dei messaggi, altrimenti la crea
history = []

if "history" not in st.session_state:
    st.session_state["history"] = []

# Pagina Chat con Gaia
if menu == "Chat con Gaia":
    st.title("Chat con Gaia")
    st.write("Parla con Gaia per sentirti al sicuro o contatta direttamente i servizi di emergenza.")
    
    # Input dell'utente per inviare un messaggio
    if query := st.chat_input():  # Ensure this line is indented properly
        # Aggiungi il messaggio dell'utente alla history
        st.session_state["history"].append({"role": "user", "content": query})
        
        # Invia il messaggio e ottieni la risposta
        print(f"st.session_state['history']: {str(st.session_state['history'])}")
        
        history.append({"USER": query})
        response, last_response = ask_gaia_with_tool(history)
        
        # Aggiungi la risposta dell'assistente alla history
        st.session_state["history"].append({"role": "assistant", "content": (last_response)})
        
        # Visualizza la history dei messaggi nella chat
        for message in st.session_state["history"]:
            st.chat_message(message["role"]).write(message["content"])
            history[-1]["AI"] = message["content"]

# Pagina 3: Mappa delle Aree Rischiose
elif menu == "Mappa Aree Rischiose":
    st.title("Mappa delle Aree Rischiose")
    st.write("Consulta la mappa per identificare le aree con maggiori segnalazioni di emergenza a Roma.")

    # Dataset di esempio per la mappa
    data = {
        "Area": ["Termini", "Trastevere", "San Lorenzo", "Piazza Venezia", "Tor Bella Monaca"],
        "Lat": [41.901, 41.881, 41.893, 41.897, 41.867],
        "Lon": [12.501, 12.469, 12.518, 12.482, 12.592],
        "Segnalazioni": [15, 8, 12, 20, 30],
    }
    df = pd.DataFrame(data)

    # Creazione della mappa
    mappa = folium.Map(location=[41.9028, 12.4964], zoom_start=12)

    for index, row in df.iterrows():
        folium.CircleMarker(
            location=(row["Lat"], row["Lon"]),
            radius=row["Segnalazioni"] / 2,  # Dimensione basata sulle segnalazioni
            color="red",
            fill=True,
            fill_opacity=0.6,
            popup=f"{row['Area']}: {row['Segnalazioni']} segnalazioni",
        ).add_to(mappa)

    # Visualizzazione della mappa
    st_folium(mappa, width=700, height=500)



