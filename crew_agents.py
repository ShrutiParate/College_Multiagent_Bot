# crew_agents.py
from crewai import Agent
from crewai.llm import LLM
from dotenv import load_dotenv
import os

load_dotenv()

# import tool wrappers
from rag_tool import rag_tool
from web_search_tool import web_search_tool

# Shared Groq LLM configured via CrewAI's native LLM wrapper to avoid OpenAI fallback
groq_llm = LLM(
    model="llama-3.1-8b-instant",
    provider="groq",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.2,
)

# Router Agent (no tools)
router_agent = Agent(
    name="Router Agent",
    role="Query Classifier",
    goal="Return exactly one word: STUDENT or SUPPORT.",
    backstory="Classifies queries strictly and returns only STUDENT or SUPPORT.",
    llm=groq_llm,
    tools=[],
)

# Student Agent -> RAG tool
student_agent = Agent(
    name="Student Agent",
    role="Academic Assistant",
    goal="Answer academic queries using the RAG tool (Chroma DB).",
    backstory="If RAG data exists, prefer it. Otherwise use LLM.",
    llm=groq_llm,
    tools=[rag_tool],
)

# Support Agent -> Web Search tool
support_agent = Agent(
    name="Support Agent",
    role="Technical Support Assistant",
    goal="Handle portal, payment, login, and other support queries. Use web search tool.",
    backstory="Use web search tool for live support info and summarise results.",
    llm=groq_llm,
    tools=[web_search_tool],
)
