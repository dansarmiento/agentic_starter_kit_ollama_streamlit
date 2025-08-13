import httpx
import logging
from typing import Optional, Dict, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

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

        try:
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
        except httpx.RequestError as e:
            logger.error(f"RequestError: Could not connect to Ollama at {self.base_url}. Is it running? Error: {e}")
            return f"Error: Could not connect to Ollama at {self.base_url}. Please ensure Ollama is running and accessible."
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTPStatusError: Received status code {e.response.status_code}. Response: {e.response.text}")
            if e.response.status_code == 404:
                return f"Error: Model '{self.model}' not found. Please pull the model with 'ollama pull {self.model}'."
            return f"Error: Received status code {e.response.status_code} from Ollama. {e.response.text}"
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}", exc_info=True)
            return f"An unexpected error occurred: {e}"
