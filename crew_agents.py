from crewai import Agent
from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq

load_dotenv()

# ✅ Groq LLM for ALL agents
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    groq_api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.2
)

# ✅ ROUTER AGENT (NEW - REPLACES IF/ELSE)
router_agent = Agent(
    role="Query Router Agent",
    goal="Decide which specialist agent should handle the user's query",
    backstory=(
        "You analyze the user's message and decide ONLY ONE of the following:\n"
        "1. SUPPORT → if the query is about fees, login, password, portal, payment.\n"
        "2. STUDENT → if the query is about exams, syllabus, attendance, results, timetable.\n\n"
        "You MUST reply with exactly ONE word only:\n"
        "SUPPORT or STUDENT.\n"
        "No explanation. No extra words."
    ),
    allow_delegation=False,
    verbose=False,
    llm=llm
)

# ✅ SUPPORT AGENT
support_agent = Agent(
    role="Support Agent",
    goal="Handle all college IT, fees, and portal-related issues",
    backstory=(
        "You are a professional college IT and administration support assistant.\n"
        "Only answer questions related to:\n"
        "- fees\n- login\n- password\n- payment\n- id card\n- portal\n"
        "Be short and direct."
    ),
    allow_delegation=False,
    verbose=True,
    llm=llm
)

# ✅ STUDENT AGENT
student_agent = Agent(
    role="Student Information Agent",
    goal="Handle all academic-related student queries",
    backstory=(
        "You are a professional academic assistant.\n"
        "Only answer questions related to:\n"
        "- exams\n- attendance\n- syllabus\n- timetable\n- results\n"
        "Be short and formal."
    ),
    allow_delegation=False,
    verbose=True,
    llm=llm
)

