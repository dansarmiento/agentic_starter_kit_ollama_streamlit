from src.llm_client import OllamaClient

PLANNER_SYS = "Plan precise, verifiable steps to solve the task. Numbered, minimal, executable."
EXECUTOR_SYS = "Execute given steps exactly. If a step is ambiguous, state the ambiguity and propose a fix."

def plan(client: OllamaClient, task: str) -> str:
    prompt = f"Task: {task}\nProduce a numbered plan with 3–8 steps."
    return client.generate(prompt, system=PLANNER_SYS)

def execute(client: OllamaClient, plan_text: str) -> str:
    prompt = f"Follow this plan step-by-step and produce the final result.\nPLAN:\n{plan_text}"
    return client.generate(prompt, system=EXECUTOR_SYS)

def planner_executor(client: OllamaClient, task: str) -> str:
    p = plan(client, task)
    return execute(client, p)
