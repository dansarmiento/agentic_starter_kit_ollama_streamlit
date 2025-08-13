from typing import List
from src.llm_client import OllamaClient
from src.tools import TOOLS

REACT_SYS = (
    "You can reason step-by-step and call tools.\n"
    "When you need a tool, output exactly:\n"
    "ACTION: <tool_name>\n"
    "INPUT: <json input or string>\n"
    "Then wait for OBSERVATION. Repeat as needed. Finish with:\n"
    "FINAL: <answer>"
)

def react(client: OllamaClient, question: str, max_steps: int = 6) -> str:
    transcript: List[str] = []
    prefix = f"QUESTION: {question}\n"

    for _ in range(max_steps):
        out = client.generate(system=REACT_SYS, prompt="\n".join(transcript) + prefix)
        transcript.append(out)

        # Look for tool call
        action, arg = None, None
        lines = [l.strip() for l in out.splitlines()]
        for i, ln in enumerate(lines):
            if ln.startswith("ACTION:"):
                action = ln.replace("ACTION:", "").strip()
                if i + 1 < len(lines) and lines[i + 1].startswith("INPUT:"):
                    arg = lines[i + 1].replace("INPUT:", "").strip()
                break

        if action:
            if action not in TOOLS:
                obs = f"Tool '{action}' not found."
            else:
                try:
                    obs = TOOLS[action]["fn"]()  # simple 0-arg tools
                except Exception as e:
                    obs = f"Tool error: {e}"
            transcript.append(f"OBSERVATION: {obs}")
            continue

        # Look for FINAL
        for ln in reversed(lines):
            if ln.startswith("FINAL:"):
                return ln.replace("FINAL:", "").strip()

    return "Reached max steps without FINAL."
