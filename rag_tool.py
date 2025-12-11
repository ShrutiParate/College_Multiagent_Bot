# rag_tool.py
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()

DB_DIR = "chroma_db"
EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL)

# load vectordb lazily to avoid heavy import cost on Streamlit startup
_vectordb = None
def _get_vectordb():
    global _vectordb
    if _vectordb is None:
        _vectordb = Chroma(persist_directory=DB_DIR, embedding_function=embeddings)
    return _vectordb

# Groq LLM
_llm = ChatGroq(
    model="llama-3.1-8b-instant",
    groq_api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.2
)

def _rag_query_impl(query: str) -> str | None:
    db = _get_vectordb()
    docs = db.similarity_search(query, k=3)
    if not docs:
        return None
    context = "\n".join([d.page_content for d in docs])
    prompt = f"""
Use ONLY the context below to answer the user's question.

Context:
{context}

User Question:
{query}

If the answer is not present in the context, reply: No relevant RAG data found.
"""
    res = _llm.invoke(prompt)
    return res.content.strip()

# Tool wrapper object that CrewAI / LangChain will accept
class ToolWrapper:
    def __init__(self, name: str, description: str, func):
        self.name = name
        self.description = description
        self._func = func

    def __call__(self, *args, **kwargs):
        return self._func(*args, **kwargs)

def rag_tool_func(q: str) -> str:
    out = _rag_query_impl(q)
    return f"[SOURCE: RAG]\n{out}" if out else "No relevant RAG data found."

rag_tool = ToolWrapper(
    name="rag_tool",
    description="Retrieve domain-specific info from ChromaDB and return summarized answer.",
    func=rag_tool_func
)
