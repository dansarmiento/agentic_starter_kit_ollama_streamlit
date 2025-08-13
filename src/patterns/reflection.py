from src.llm_client import OllamaClient

REFLECT_SYS = (
    "You are a rigorous reviewer. Identify mistakes, missing cases, and unclear reasoning; "
    "propose concrete fixes."
)

def reflect(client: OllamaClient, question: str, attempt: str) -> str:
    critique = client.generate(
        prompt=(
            f"Question:\n{question}\n\n"
            f"Attempt:\n{attempt}\n\n"
            f"Critique this attempt and propose exact improvements."
        ),
        system=REFLECT_SYS,
    )
    improved = client.generate(
        prompt=(
            f"Original Question:\n{question}\n\n"
            f"Improvement Guidance:\n{critique}\n\n"
            f"Rewrite the answer with all improvements applied."
        ),
        system="You incorporate feedback completely and write a single, improved answer.",
    )
    return improved
