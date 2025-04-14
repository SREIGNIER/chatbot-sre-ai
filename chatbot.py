import os
import shutil
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import Docx2txtLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import Ollama

DOCS_PATH = "docs"
INDEX_PATH = "faiss_index"

def remove_readonly(func, path, _):
    os.chmod(path, 0o777)
    func(path)

def load_documents():
    documents = []
    for filename in os.listdir(DOCS_PATH):
        if filename.endswith(".docx"):
            path = os.path.join(DOCS_PATH, filename)
            loader = Docx2txtLoader(path)
            documents.extend(loader.load())
    return documents

def vectorize_documents():
    if os.path.exists(INDEX_PATH):
        shutil.rmtree(INDEX_PATH, onerror=remove_readonly)

    documents = load_documents()
    if not documents:
        return None

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = splitter.split_documents(documents)

    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    db = FAISS.from_documents(chunks, embeddings)
    db.save_local(INDEX_PATH)
    return db

def get_chain_from_docs(db):
    llm = Ollama(model="mistral", temperature=0.1)
    chain = load_qa_chain(llm, chain_type="stuff")

    def ask(question):
        docs = db.similarity_search(question, k=3)
        if not docs:
            return "❌ Je ne connais pas encore la réponse à cette question."
        response = chain.run(input_documents=docs, question=question)
        return str(response).strip()
    return ask
