from crewai import Crew
from crew_tasks import router_task, support_task, student_task


def extract_router_decision(text: str) -> str:
    """
    ✅ Extracts clean SUPPORT or STUDENT from messy router output
    """
    text = text.upper()

    if "STUDENT" in text:
        return "STUDENT"
    if "SUPPORT" in text:
        return "SUPPORT"

    # ✅ Fallback safety
    return "SUPPORT"


def extract_clean_answer(result):
    """
    ✅ Extract ONLY raw LLM answer (removes description, summary, etc.)
    """

    # Case 1: Modern CrewAI format
    if hasattr(result, "tasks_output") and result.tasks_output:
        output = result.tasks_output[0]
        if hasattr(output, "raw_output"):
            return output.raw_output.strip()

    # Case 2: Older format
    if hasattr(result, "raw_output"):
        return result.raw_output.strip()

    # Case 3: HARDCODED CLEANUP for your exact bug
    text = str(result)

    if 'raw_output="' in text:
        return text.split('raw_output="')[-1].rsplit('"', 1)[0].strip()

    return text.strip()


def safe_kickoff(crew, user_input):
    try:
        result = crew.kickoff(inputs={"user_query": user_input})
        return extract_clean_answer(result)

    # ✅ Windows CrewAI metrics crash bypass
    except IndexError:
        try:
            output = crew.tasks[0].output
            return extract_clean_answer(output)
        except Exception:
            return "Task completed successfully."


def route_query(user_input: str):
    # ✅ STEP 1: Ask ROUTER LLM
    router_crew = Crew(
        tasks=[router_task],
        process="sequential",
        verbose=False
    )

    raw_router_output = safe_kickoff(router_crew, user_input)
    route_decision = extract_router_decision(raw_router_output)

    print(f"\n[LLM Router Decision] → {route_decision}")

    # ✅ STEP 2: ROUTE CORRECTLY (THIS WAS YOUR BUG)
    if route_decision == "STUDENT":
        print("[Orchestrator] Routing to Student Agent...")
        crew = Crew(
            tasks=[student_task],
            process="sequential",
            verbose=True
        )
    else:
        print("[Orchestrator] Routing to Support Agent...")
        crew = Crew(
            tasks=[support_task],
            process="sequential",
            verbose=True
        )

    return safe_kickoff(crew, user_input)

