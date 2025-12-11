import platform
import signal

# Provide fallbacks for signals that are missing on Windows before other imports rely on them.
if platform.system() != "Linux":
    if not hasattr(signal, "SIGHUP"):
        signal.SIGHUP = 1
    if not hasattr(signal, "SIGTSTP"):
        signal.SIGTSTP = getattr(signal, "SIGBREAK", 18)
    if not hasattr(signal, "SIGCONT"):
        signal.SIGCONT = 19

import streamlit as st
from crew_runner import route_query

st.set_page_config(page_title="College AI Assistant", layout="wide")

st.title("🎓 College AI Assistant")

with st.sidebar:
    st.header("ℹ️ About This Assistant")
    st.markdown("""
This is a **Multi-Agent AI Assistant** powered by:

- 🧠 Groq LLM  
- 🤖 CrewAI Agents  
- 📚 RAG (for academic queries)  
- 🌐 Web Search (for support queries)  

Ask anything related to syllabus, exams, fees, login, portal, school timings, etc.
""")
    if st.button("Clear Chat"):
        st.session_state.messages = []

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

query = st.chat_input("Ask your question...")

if query:
    st.session_state.messages.append({"role": "user", "content": query})

    response = route_query(query)

    st.session_state.messages.append({"role": "assistant", "content": response})

    st.chat_message("assistant").write(response)

