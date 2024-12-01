import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from llm import ask_gaia_with_tool
import geocoder

# Configurazione del tema
st.set_page_config(page_title="Gaia - Sicurezza e Supporto", layout="wide", page_icon="logo.png" )

st.markdown(
    """
    <style>
    /* Sfondo generale */
    .css-18e3th9 {
        background-color: #ff0000 !important; /* Rosso */
        color: #ffffff !important;           /* Bianco */
    }
    .stMain{
        background-color: #900; /* Rosso */
        color: #ffffff !important; 
        height: 100vh;
        display: flex; 
        justify-content: center;
        align-items: center;
    
    }
    /* Testo generico */
    .css-10trblm {
        color: #ffffff !important; /* Colore testo */
    }
    /* Header */
    .css-1v3fvcr {
        background-color: #900 !important; /* Rosso scuro */
        color: #ffffff !important;
    }
    /* Sidebar */
    .css-1d391kg {
        background-color: #900 !important; /* Rosso scuro */
        color: #ffffff !important;
    }
    /* Sidebar */
    .stSidebar {
        background-color: #900; 
        display: flex; 
        align-items: center;
     
    }
    .st-emotion-cache-n5r31u {
     background-color: black; 
     color: white;
    }
    /* header */ 
    .stAppHeader {
     background-color: #900; 
    }
    /* main container */
      .stMainBlockContainer{
    background-color: #900; 
    height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    width: 75%;
    }
    /* Bottoni nella sidebar */
    .css-1v0mbdj {
        background-color: #ffffff !important; /* Bianco */
        color: #ff0000 !important;            /* Rosso */
        border: 2px solid #ff0000 !important;
        border-radius: 8px !important;
        font-size: 16px !important;
        font-weight: bold !important;
    }
    .css-1v0mbdj:hover {
        background-color: #ffcccc !important; /* Rosso chiaro */
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Variabile per gestire la pagina attuale
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "Home"

# Logica per cambiare pagina
if st.sidebar.button("🏠 Home"):
    st.sidebar.button.markdown(
        """
        <style> 
        background-color: "black"
        </style>
         """,
    unsafe_allow_html=True,
    )
    st.session_state["current_page"] = "Home"

if st.sidebar.button("💬 Chat con Gaia"):
    st.session_state["current_page"] = "Chat con Gaia"

if st.sidebar.button("🗺️ Mappa Aree Rischiose"):
    st.session_state["current_page"] = "Mappa Aree Rischiose"

if st.sidebar.button("📞 Chiama il 112"):
    st.session_state["current_page"] = "Chiamata di emergenza"
# Pagina 1: Nome e Descrizione dell'App
if st.session_state["current_page"] == "Home":

    st.title("Gaia - Sicurezza e Supporto")
    st.image("logo.png",   width=100)    
    st.write("""
        Gaia è un'applicazione mobile progettata per fornire supporto emotivo e sicurezza alle donne.
        Attraverso l'intelligenza artificiale, Gaia simula una conversazione per offrire compagnia
        e può aiutarti a contattare i servizi di emergenza in caso di pericolo.
    """)
    
    st.write("Naviga attraverso il menu per accedere alle diverse funzionalità.")

# Pagina 2: Chat con Gaia
elif st.session_state["current_page"] == "Chat con Gaia":
    st.title("Chat con Gaia")
    st.write("Parla con Gaia per sentirti al sicuro o contatta direttamente i servizi di emergenza.")

    # Inizializza la history nella sessione
    if "history" not in st.session_state:
        st.session_state["history"] = []

    # Input dell'utente
    if query := st.chat_input("Scrivi un messaggio..."):
        st.session_state["history"].append({"role": "user", "content": query})
        response, last_response = ask_gaia_with_tool(st.session_state["history"])
        st.session_state["history"].append({"role": "assistant", "content": last_response})

    # Mostra la chat
    for message in st.session_state["history"]:
        st.chat_message(message["role"]).write(message["content"])



# Pagina 3: Mappa delle Aree Rischiose
elif st.session_state["current_page"] == "Mappa Aree Rischiose":
    # Dati iniziali delle aree pericolose
    data = {
        "Area": ["Termini", "Trastevere", "San Lorenzo", "Piazza Venezia", "Tor Bella Monaca"],
        "Lat": [41.901, 41.881, 41.893, 41.897, 41.867],
        "Lon": [12.501, 12.469, 12.518, 12.482, 12.592],
        "Segnalazioni": [15, 8, 12, 20, 30],
        "Pericolo": ["Aggressioni", "Furti", "Atti vandalici", "Furti", "Spaccio"],
    }

    # Converti i dati in DataFrame
    df = pd.DataFrame(data)

    # Funzione per classificare i rischi in base al numero di segnalazioni
    def get_risk_color(segnalazioni):
        if segnalazioni >= 20:
            return "red"
        elif 10 <= segnalazioni < 20:
            return "orange"
        else:
            return "yellow"

    # Mappa interattiva
    st.title("Mappa delle Aree Rischiose")
    st.write("Qui puoi visualizzare la tua posizione e se sei vicino o meno a un'area pericolosa")
    mappa = folium.Map(location=[41.9028, 12.4964], zoom_start=12)

    for _, row in df.iterrows():
        folium.CircleMarker(
            location=(row["Lat"], row["Lon"]),
            radius=row["Segnalazioni"] / 2,  # Dimensione del cerchio
            color=get_risk_color(row["Segnalazioni"]),
            fill=True,
            fill_opacity=0.6,
            popup=f"<b>{row['Area']}</b><br>Pericolo: {row['Pericolo']}<br>Segnalazioni: {row['Segnalazioni']}",
        ).add_to(mappa)

    # Mostrare avviso se vicino a un'area pericolosa
    st.subheader("Avvisi di sicurezza")
    user_location = geocoder.ip("me").latlng
    if user_location:
        for _, row in df.iterrows():
            distance = ((row["Lat"] - user_location[0])**2 + (row["Lon"] - user_location[1])**2)**0.5
            if distance < 0.01:  # Approssimativamente 1 km
                st.warning(f"⚠️ Sei vicino a una zona pericolosa: {row['Area']} ({row['Pericolo']})")
    else:
        st.error("Impossibile determinare la tua posizione attuale.")

    # Visualizzare la mappa
    st_folium(mappa, width="100%", height=400)



# Pagina 4: Chiamata di Emergenza
elif st.session_state["current_page"] == "Chiamata di emergenza":
    st.title("Sei sicuro di voler chiamare il numero di emergenza?")

    # Bottone di conferma
    col1, col2 = st.columns(2)
    with col1:
        conferma = st.button("Conferma", key="conferma")
    with col2:
        annulla = st.button("Annulla", key="annulla")

    # Gestione dell'azione in base al bottone premuto
    if conferma:
        st.warning("Chiamata in corso al numero di emergenza... 🚨")
        # Aggiungi qui il codice per effettuare la chiamata
    elif annulla:
        st.success("Chiamata annullata. Torna indietro e resta al sicuro!")