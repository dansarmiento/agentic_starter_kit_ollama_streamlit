from src.llm_client import OllamaClient

SELF_CHECK_SYS = (
    "You are a careful reasoner. Produce a DRAFT answer, then CRITIQUE it, then FINAL. "
    "Keep critique concise and specific."
)

def self_check(client: OllamaClient, task: str) -> str:
    prompt = f"""Task: {task}

Respond in three sections:
DRAFT:
[Write your first attempt.]

CRITIQUE:
[List concrete issues, missing steps, errors, ambiguities.]

FINAL:
[Fix every issue. Provide a clean, correct solution.]
"""
    return client.generate(prompt, system=SELF_CHECK_SYS)
