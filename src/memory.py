from typing import List, Dict

class ShortTermMemory:
    def __init__(self, k: int = 8):
        self.k = k
        self.buf: List[Dict[str, str]] = []

    def add(self, role: str, content: str):
        self.buf.append({"role": role, "content": content})
        self.buf = self.buf[-self.k:]

    def context(self) -> str:
        return "\n".join(f"{m['role'].upper()}: {m['content']}" for m in self.buf)
