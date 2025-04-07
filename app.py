import streamlit as st
from loader import load_documents
from vectorizer import vectorize_documents

st.set_page_config(page_title="SRE AI – Assistant Méthodologique", page_icon="🤖")

st.title("🤖 SRE AI – Assistant Méthodologique")

if "vectorstore" not in st.session_state:
    with st.spinner("Chargement de la base de connaissances..."):
        docs = load_documents("docs")  # Charge tous les fichiers PDF/DOCX du dossier /docs
        st.session_state.vectorstore = vectorize_documents(docs)

question = st.text_input("Pose ta question sur une méthodologie SRE 👇")

if question:
    if st.session_state.vectorstore:
        docs = st.session_state.vectorstore.similarity_search(question, k=2)
        answer = docs[0].page_content if docs else "Je n'ai pas trouvé d'information."
    else:
        answer = "La base vectorielle n'est pas disponible."

    st.markdown("### Réponse :")
    st.write(answer)
