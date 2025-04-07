from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
import os

def vectorize_documents(documents):
    # Découpe les documents en morceaux de 1000 caractères avec un chevauchement de 100
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = text_splitter.split_documents(documents)

    # Récupère la clé OpenAI depuis les secrets (via Streamlit Cloud)
    openai_key = os.environ["OPENAI_API_KEY"]
    embeddings = OpenAIEmbeddings(openai_api_key=openai_key)

    # Création de la base vectorielle
    db = FAISS.from_documents(chunks, embeddings)

    return db
