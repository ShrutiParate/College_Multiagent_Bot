# crew_runner.py
from crewai import Crew
from crew_tasks import router_task, student_task, support_task

def extract_clean_answer(result):
    # Robust extraction of textual output
    try:
        if hasattr(result, "tasks_output") and result.tasks_output:
            out = result.tasks_output[0]
            if hasattr(out, "raw_output") and out.raw_output:
                return out.raw_output.strip()
        if hasattr(result, "raw_output") and result.raw_output:
            return result.raw_output.strip()
    except Exception:
        pass
    return str(result).strip()

def safe_kickoff(crew, query):
    try:
        result = crew.kickoff(inputs={"user_query": query})
        return extract_clean_answer(result)
    except Exception as e:
        # log and fallback
        print("[safe_kickoff] Exception:", e)
        try:
            # old fallback: try task output
            to = crew.tasks[0].output
            return str(to).strip()
        except Exception:
            return "Task executed but no text output generated."

def extract_router_decision(text: str) -> str:
    if not text:
        return "SUPPORT"
    t = text.upper().strip()
    if "STUDENT" in t:
        return "STUDENT"
    if "SUPPORT" in t:
        return "SUPPORT"
    # Try to parse if the router returned JSON-like or quoted value
    if '"STUDENT"' in t or "'STUDENT'" in t:
        return "STUDENT"
    if '"SUPPORT"' in t or "'SUPPORT'" in t:
        return "SUPPORT"
    return "SUPPORT"

def route_query(user_input: str):
    # 1) Ask Router
    router_crew = Crew(tasks=[router_task], process="sequential", verbose=False)
    router_raw = safe_kickoff(router_crew, user_input)
    decision = extract_router_decision(router_raw)
    print(f"[Router Decision] → {decision}")

    # 2) Delegate
    if decision == "STUDENT":
        print("[Delegation] → Student Agent (RAG Tool)")
        crew = Crew(tasks=[student_task], process="sequential", verbose=True)
    else:
        print("[Delegation] → Support Agent (Web Search Tool)")
        crew = Crew(tasks=[support_task], process="sequential", verbose=True)

    answer = safe_kickoff(crew, user_input)
    return answer or "No answer generated."
