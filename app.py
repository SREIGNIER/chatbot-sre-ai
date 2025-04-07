import streamlit as st

st.set_page_config(page_title="SRE AI", page_icon="🤖")

st.title("Bienvenue sur le chatbot SRE AI")
question = st.text_input("Pose ta question :")

if question:
    st.write(f"Tu as demandé : {question}")
    st.write("Je suis encore en phase de configuration.")