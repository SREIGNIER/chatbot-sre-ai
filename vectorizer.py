from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
import streamlit as st

def vectorize_documents(docs):
    # Vérifie que la clé API est présente
    if "OPENAI_API_KEY" not in st.secrets:
        st.error("❌ Clé API OpenAI manquante dans les secrets Streamlit.")
        return None

    # Découpe les documents en morceaux
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = text_splitter.split_documents(docs)

    # Initialise les embeddings avec la clé sécurisée
    embeddings = OpenAIEmbeddings(openai_api_key=st.secrets["OPENAI_API_KEY"])

    # Crée l’index vectoriel
    db = FAISS.from_documents(chunks, embeddings)
    return db
