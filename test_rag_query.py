from rag_tool import rag_query

while True:
    q = input("\nAsk: ")
    if q.lower() in ("exit", "quit"):
        break

    print(rag_query(q))
