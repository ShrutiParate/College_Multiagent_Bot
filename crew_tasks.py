from crewai import Task
from crew_agents import router_agent, student_agent, support_agent

router_task = Task(
    description=(
        "Classify the user's query.\n"
        "Return ONLY one word: STUDENT or SUPPORT.\n\n"
        "User Query: {user_query}"
    ),
    expected_output="STUDENT or SUPPORT",
    agent=router_agent
)

student_task = Task(
    description=(
        "Use your RAG tool to answer the academic query.\n"
        "If RAG has no information, fallback to LLM.\n\n"
        "User Query: {user_query}"
    ),
    expected_output="Academic answer.",
    agent=student_agent
)

support_task = Task(
    description=(
        "Use your web search tool to answer support-related queries.\n\n"
        "User Query: {user_query}"
    ),
    expected_output="Support answer.",
    agent=support_agent
)

