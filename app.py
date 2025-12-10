import streamlit as st
from crew_runner import route_query

# ------------------ PAGE CONFIG ------------------

st.set_page_config(
    page_title="College AI Assistant",
    page_icon="🎓",
    layout="centered"
)

# ------------------ FAINT, CLEAN CSS (VERY LIGHT) ------------------

st.markdown("""
<style>
/* Light background tint */
.stApp {
    background-color: #f9fafb;
}

/* Title soft color */
h1 {
    color: #1e3a8a;
}

/* Input box - soft border */
.stTextInput > div > div > input {
    border-radius: 8px;
    border: 1px solid #c7d2fe;
}

/* Send button - soft blue */
.stButton > button {
    background-color: #3b82f6;
    color: white;
    border-radius: 8px;
    border: none;
}

.stButton > button:hover {
    background-color: #2563eb;
}

/* Sidebar faint */
section[data-testid="stSidebar"] {
    background-color: #f1f5f9;
}
</style>
""", unsafe_allow_html=True)

# ------------------ TITLE ------------------

st.title("🎓 College Multi-Agent Bot")
st.caption("Groq + CrewAI + LLM Router")

# ------------------ SESSION MEMORY ------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

# ------------------ SIDEBAR ------------------

st.sidebar.header("⚙️ Controls")

if st.sidebar.button("🧹 Clear Chat"):
    st.session_state.messages = []
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.markdown("### ℹ️ About This Assistant")
st.sidebar.markdown(
    "This is a **Multi-Agent College AI Assistant** that helps students with:\n\n"
    "• 📘 Academic queries (syllabus, exams, results)\n\n"
    "• 💳 Support queries (fees, login, portal issues)\n\n"
    "Feel free to ask any questions related to support and academics"
)

# ------------------ CHAT HISTORY ------------------

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ------------------ INPUT FORM (BASIC + CLEAN) ------------------

with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input(
        "💬 Ask your question:",
        placeholder="e.g. Where can I see my results? / How to pay fees?"
    )
    send = st.form_submit_button("Send")

if send and user_input.strip():
    # Save user message
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    # Get AI response
    with st.spinner("🤖 AI is thinking..."):
        response = route_query(user_input)

    # Save assistant response
    st.session_state.messages.append(
        {"role": "assistant", "content": response}
    )

    st.rerun()
