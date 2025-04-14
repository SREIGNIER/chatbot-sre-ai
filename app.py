import os
import streamlit as st
from datetime import datetime
from chatbot import vectorize_documents, get_chain_from_docs
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OllamaEmbeddings
from loader import download_docs_from_github  # <--- Ajouté ici

# --- Étape 1 : Télécharger les documents depuis GitHub ---
download_docs_from_github()

# Chemins
DOCS_PATH = "docs"
INDEX_PATH = "faiss_index"
UNRECOGNIZED_PATH = "questions_non_reconnues.txt"

# Config page
st.set_page_config(page_title="SRE AI – Assistant Méthodologique", page_icon="🤖", layout="centered")
st.title("🤖 SRE AI – Assistant Méthodologique")

# Fonction : enregistrer une question non reconnue
def enregistrer_question_non_reconnue(question):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    with open(UNRECOGNIZED_PATH, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {question.strip()}\n")

# Chargement vecteur FAISS
if "vectordb" not in st.session_state:
    if os.path.exists(INDEX_PATH):
        st.session_state.vectordb = FAISS.load_local(
            INDEX_PATH,
            OllamaEmbeddings(model="nomic-embed-text"),
            allow_dangerous_deserialization=True
        )
    else:
        st.session_state.vectordb = vectorize_documents()

qa_chain = get_chain_from_docs(st.session_state.vectordb)

# Saisie question
question = st.text_input("💬 Pose ta question métier :")

if question:
    with st.spinner("Recherche de réponse..."):
        response = qa_chain(question)
        if "❌" in response:
            st.error(response)
            enregistrer_question_non_reconnue(question)
        else:
            st.success("✅ Réponse :")
            st.markdown(response)

# Upload d’un document
st.markdown("### ➕ Ajouter une nouvelle procédure (.docx)")
uploaded_file = st.file_uploader("Uploader un fichier Word :", type="docx")

if uploaded_file:
    save_path = os.path.join(DOCS_PATH, uploaded_file.name)
    if not os.path.exists(DOCS_PATH):
        os.makedirs(DOCS_PATH)

    if os.path.exists(save_path):
        st.warning(f"⚠️ Le fichier '{uploaded_file.name}' existe déjà.")
    else:
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"✅ Fichier '{uploaded_file.name}' ajouté.")
        st.session_state.vectordb = vectorize_documents()
        qa_chain = get_chain_from_docs(st.session_state.vectordb)

# Gestion des questions non reconnues
st.markdown("---")
with st.expander("📋 Gérer les questions non reconnues enregistrées"):
    if os.path.exists(UNRECOGNIZED_PATH):
        with open(UNRECOGNIZED_PATH, "r", encoding="utf-8") as f:
            lines = f.readlines()

        if lines:
            for i, line in enumerate(lines):
                col1, col2, col3 = st.columns([6, 1, 1])
                with col1:
                    st.markdown(line.strip())
                with col2:
                    if st.button("✅ Traité", key=f"traiter_{i}"):
                        lines[i] = "✅ " + line if not line.startswith("✅") else line
                        with open(UNRECOGNIZED_PATH, "w", encoding="utf-8") as f:
                            f.writelines(lines)
                        st.experimental_rerun()
                with col3:
                    if st.button("🗑️ Supprimer", key=f"supprimer_{i}"):
                        lines.pop(i)
                        with open(UNRECOGNIZED_PATH, "w", encoding="utf-8") as f:
                            f.writelines(lines)
                        st.experimental_rerun()
        else:
            st.info("✅ Aucune question non reconnue à afficher.")
    else:
        st.info("✅ Le fichier de suivi n'existe pas encore.")
