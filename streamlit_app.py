import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from src.workflows.main_workflow import ask_gaia_with_tool
import geocoder

# Configurazione del tema
st.set_page_config(page_title="Gaia - Security and Support", layout="wide", page_icon="logo.png",)

# Stile personalizzato
st.markdown(
    """
    <style>
    /* Sfondo e colore del testo */
    body {
        background-color: #ff0000; /* Rosso */
        color: #ffffff;           /* Bianco */
    }
    /* Sidebar */
    .stSidebar {
        background-color: #900; 
     
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
    /* chat */ 
    
    .st-emotion-cache-qdbtli {
     background-color: #900;
    
    }
    /* Bottoni nella sidebar */
    .menu-button {
        background-color: #ffffff; /* Bianco */
        color: #ff0000;            /* Rosso */
        border: 2px solid #ff0000;
        border-radius: 8px;
        padding: 10px;
        font-size: 16px;
        text-align: center;
        cursor: pointer;
        margin-bottom: 10px;
        font-weight: bold;
    }
    .menu-button:hover {
        background-color: #ffcccc; /* Rosso chiaro */
    }
    .stVerticalBlock {
    text-align: center;
    }
    .float-child{
    background-color: #900;
    display: flex;
    justify-content: center;
    
    }
    .st-emotion-cache-0{
    display: flex;
    justify-content: center;
    width: 100%;
    margin-block: auto
    }
    /* Testi generici */
    .stTextInput, .stButton, .stTextArea, .stChatMessage {
        color: #ffffff !important;
    }
    /* FontAwesome Icons */
    @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css');
    .icon {
        font-size: 20px;
        margin-right: 8px;
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
    st.session_state["current_page"] = "Home"

if st.sidebar.button("💬 Chatting with Gaia"):
    st.session_state["current_page"] = "Chatting with Gaia"

if st.sidebar.button("🗺️ Hazardous Areas Map"):
    st.session_state["current_page"] = "Hazardous Areas Map"

if st.sidebar.button("📞 Call 112"):
    st.session_state["current_page"] = "Emergency Call"
# Pagina 1: Nome e Descrizione dell'App
if st.session_state["current_page"] == "Home":

    st.title("Gaia - Security and Support")
    st.image("logo.png",   width=100)    
    st.write("""
        Gaia is a mobile application designed to provide emotional support and security for women.
        Through artificial intelligence, Gaia simulates a conversation to offer companionship
        and can help you contact the emergency services in case of danger.
    """)
    
    st.write("Navigate through the menu to access the different functionalities.")

# Pagina 2: Chat con Gaia
elif st.session_state["current_page"] == "Chatting with Gaia":
    st.title("Chatting with Gaia")
    st.write("Talk to Gaia to feel safe or contact the emergency services directly.")

    # Inizializza la history nella sessione
    if "history" not in st.session_state:
        st.session_state["history"] = []

    # Input dell'utente
    if query := st.chat_input("Write a message..."):
        st.session_state["history"].append({"role": "user", "content": query})
        response, last_response = ask_gaia_with_tool(st.session_state["history"])
        st.session_state["history"].append({"role": "assistant", "content": last_response})

    # Mostra la chat
    for message in st.session_state["history"]:
        st.chat_message(message["role"]).write(message["content"])



# Pagina 3: Mappa delle Aree Rischiose
elif st.session_state["current_page"] == "Hazardous Areas Map":
    # Dati iniziali delle aree pericolose
    data = {
        "Area": ["Termini", "Trastevere", "San Lorenzo", "Piazza Venezia", "Tor Bella Monaca"],
        "Lat": [41.901, 41.881, 41.893, 41.897, 41.867],
        "Lon": [12.501, 12.469, 12.518, 12.482, 12.592],
        "Reports": [15, 8, 12, 20, 30],
        "Danger": ["Aggressions", "Theft", "", "Theft", "Drug Dealing"],
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
    st.title("Map of Hazardous Areas")
    st.write("Here you can view your location and whether or not you are close to a danger zone")
    mappa = folium.Map(location=[41.9028, 12.4964], zoom_start=12)

    for _, row in df.iterrows():
        folium.CircleMarker(
            location=(row["Lat"], row["Lon"]),
            radius=row["Reports"] / 2,  # Dimensione del cerchio
            color=get_risk_color(row["Reports"]),
            fill=True,
            fill_opacity=0.6,
            popup=f"<b>{row['Area']}</b><br>Danger: {row['Danger']}<br>Reports: {row['Reports']}",
        ).add_to(mappa)

    # Mostrare avviso se vicino a un'area pericolosa
    st.subheader("Security Warnings")
    user_location = geocoder.ip("me").latlng
    if user_location:
        for _, row in df.iterrows():
            distance = ((row["Lat"] - user_location[0])**2 + (row["Lon"] - user_location[1])**2)**0.5
            if distance < 0.01:  # Approssimativamente 1 km
                st.warning(f"⚠️ You are close to a dangerous area: {row['Area']} ({row['Pericolo']})")
    else:
        st.error("Unable to determine your current position.")

    # Visualizzare la mappa
    st_folium(mappa, width="100%", height=400)



# Pagina 4: Chiamata di Emergenza
elif st.session_state["current_page"] == "Emergency Call":
    st.title("Are you sure you want to call the emergency number?")

    # Bottone di conferma
    col1, col2 = st.columns(2)
    with col1:
        conferma = st.button("Confirmation", key="Confirmation")
    with col2:
        annulla = st.button("Cancel", key="Cancel")

    # Gestione dell'azione in base al bottone premuto
    if conferma:
        st.warning("Call in progress to the emergency number... 🚨")
        # Aggiungi qui il codice per effettuare la chiamata
    elif annulla:
        st.success("Call cancelled. Come back and stay safe!")