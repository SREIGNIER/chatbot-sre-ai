import streamlit as st
from loader import load_documents
from vectorizer import vectorize_documents
from chatbot import ask_question

st.set_page_config(page_title="SRE AI", page_icon="🤖")
st.markdown("<style>body {background-color: black; color: white;}</style>", unsafe_allow_html=True)
st.title("🤖 SRE AI – Assistant Méthodologique")

if "vectorstore" not in st.session_state:
    with st.spinner("Chargement de la base de documents..."):
        docs = load_documents("docs")
        st.session_state.vectorstore = vectorize_documents(docs)

question = st.text_input("Pose ta question 👇")

if question:
    with st.spinner("Recherche en cours..."):
        reponse = ask_question(question, st.session_state.vectorstore)
        st.markdown(f"**Réponse :** {reponse}")