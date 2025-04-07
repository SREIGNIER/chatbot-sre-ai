import os
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader

def load_documents(path="docs"):
    documents = []
    for filename in os.listdir(path):
        filepath = os.path.join(path, filename)
        if filename.endswith(".pdf"):
            documents += PyPDFLoader(filepath).load()
        elif filename.endswith(".docx"):
            documents += Docx2txtLoader(filepath).load()
        elif filename.endswith(".txt"):
            documents += TextLoader(filepath).load()
    return documents
