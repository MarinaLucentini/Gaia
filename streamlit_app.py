from openai import OpenAI
import streamlit as st
from llm import *
# Aggiungi il campo per l'inserimento della API key nella barra laterale
# with st.sidebar:
#     api_key = st.text_input("API Key", key="chatbot_api_key", type="password")

# Imposta il titolo dell'app con emoji
st.title("🌍 Llama Impact Hackathon - Roma")
st.caption("💡 Unisciti a noi per creare soluzioni innovative ad alto impatto sociale")


# Inizializza la history della chat, se non esiste già
if "history" not in st.session_state:
    st.session_state["history"] = []

# Gestisci l'inserimento di un nuovo messaggio da parte dell'utente
if query := st.chat_input():
    # Aggiungi il messaggio dell'utente alla history
    st.session_state["history"].append({"role": "user", "content": query})
    
    # Invia il messaggio e ottieni la risposta
    
    response,last_response=ask_gaia_with_tool(str(st.session_state["history"]))
    
    # Aggiungi la risposta dell'assistente alla history
    st.session_state["history"].append({"role": "assistant", "content": last_response})
    
    # Visualizza la history dei messaggi nella chat
    for message in st.session_state["history"]:
        st.chat_message(message["role"]).write(message["content"])

