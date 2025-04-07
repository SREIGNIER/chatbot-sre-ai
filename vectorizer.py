from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

def vectorize_documents(documents):
    splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_documents(documents)
    db = FAISS.from_documents(chunks, OpenAIEmbeddings())
    return db
