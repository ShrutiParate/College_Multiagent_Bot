import os
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

DATA_PATH = "data/private_data.txt"
DB_DIR = "chroma_db"


def build_vector_store():
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError("private_data.txt missing!")

    text = open(DATA_PATH, "r", encoding="utf-8").read()

    splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=20)
    chunks = splitter.split_text(text)

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    vectordb = Chroma.from_texts(
        texts=chunks,
        embedding=embeddings,
        persist_directory=DB_DIR
    )

    vectordb.persist()
    print("✅ Vector DB built successfully!")


if __name__ == "__main__":
    build_vector_store()
