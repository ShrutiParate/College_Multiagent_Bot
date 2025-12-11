# web_search_tool.py
from duckduckgo_search import DDGS

# simple wrapper implementation
def _web_search_impl(query: str) -> str:
    with DDGS() as ddg:
        results = ddg.text(query, max_results=3)
    if not results:
        return "No web results found."
    out = "WEB SEARCH RESULTS:\n"
    for i, r in enumerate(results, 1):
        title = r.get("title") or ""
        body = r.get("body") or ""
        out += f"\n{i}. {title}\n{body}\n"
    return out.strip()

class ToolWrapper:
    def __init__(self, name: str, description: str, func):
        self.name = name
        self.description = description
        self._func = func

    def __call__(self, *args, **kwargs):
        return self._func(*args, **kwargs)

def web_search_tool_func(q: str) -> str:
    return _web_search_impl(q)

web_search_tool = ToolWrapper(
    name="web_search_tool",
    description="Perform a DuckDuckGo web search and summarize top hits.",
    func=web_search_tool_func
)
