from src.llm_client import OllamaClient
from src.patterns.self_check import self_check
from src.patterns.react import react
from src.patterns.planner_executor import planner_executor
from src.patterns.reflection import reflect
from src.patterns.rag import answer_with_rag

if __name__ == "__main__":
    client = OllamaClient(model="llama3.1:8b-instruct")

    print("\n== Self-Check ==")
    print(self_check(client, "Write a Python function to check if a number is prime; include edge cases."))

    print("\n== ReAct ==")
    print(react(client, "What time is it right now?", max_steps=3))

    print("\n== Planner–Executor ==")
    print(planner_executor(client, "Generate a bash one-liner to count unique IPs in access.log"))

    print("\n== Reflection ==")
    attempt = "Use a loop to test divisibility up to n."
    print(reflect(client, "How to check primality efficiently?", attempt))

    print("\n== RAG ==")
    print(answer_with_rag(client, "Summarize the key ideas in our local docs."))
