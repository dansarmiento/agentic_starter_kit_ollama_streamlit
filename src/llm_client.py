import httpx
from typing import Optional, Dict, Any

class OllamaClient:
    def __init__(self, base_url: str = "http://127.0.0.1:11434", model: str = "llama3.1:8b-instruct"):
        self.base_url = base_url.rstrip("/")
        self.model = model

    def generate(self, prompt: str, system: Optional[str] = None, stream: bool = False, **params) -> str:
        url = f"{self.base_url}/api/generate"
        payload: Dict[str, Any] = {"model": self.model, "prompt": prompt, "stream": stream}
        if system:
            payload["system"] = system
        if params:
            payload.update(params)

        if not stream:
            r = httpx.post(url, json=payload, timeout=120)
            r.raise_for_status()
            return r.json().get("response", "")

        # Streaming
        chunks = []
        with httpx.stream("POST", url, json=payload, timeout=120) as r:
            r.raise_for_status()
            for line in r.iter_lines():
                if not line:
                    continue
                part = httpx.Response(200, content=line).json()
                if "response" in part:
                    chunks.append(part["response"])
        return "".join(chunks)
