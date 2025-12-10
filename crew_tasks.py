from crewai import Task
from crew_agents import router_agent, support_agent, student_agent

# ✅ ROUTER TASK (LLM DECIDES THE ROUTE)
router_task = Task(
    description=(
        "Analyze the following user query and decide the route.\n"
        "Reply with ONLY ONE WORD:\n"
        "SUPPORT or STUDENT.\n\n"
        "User Query: {user_query}"
    ),
    expected_output="Either SUPPORT or STUDENT only.",
    agent=router_agent
)

# ✅ SUPPORT TASK
support_task = Task(
    description=(
        "Answer ONLY what the user asked about support.\n"
        "Do NOT include academic content.\n\n"
        "User Query: {user_query}"
    ),
    expected_output="A short and clear support-related answer.",
    agent=support_agent
)

# ✅ STUDENT TASK
student_task = Task(
    description=(
        "Answer ONLY what the user asked about academics.\n"
        "Do NOT include fees, login, or portal topics.\n\n"
        "User Query: {user_query}"
    ),
    expected_output="A short and clear academic-related answer.",
    agent=student_agent
)
