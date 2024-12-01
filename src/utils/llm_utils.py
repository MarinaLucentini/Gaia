import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq

# Carica le variabili dal file .env
load_dotenv()


chat = ChatGroq(
    temperature=0,
    groq_api_key=os.getenv("GROQ_API"),
    model_name="llama-3.1-70b-versatile",
)
