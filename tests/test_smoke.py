# Mocked tests; no Ollama needed
class DummyClient:
    def generate(self, prompt: str, system: str = None, **kwargs) -> str:
        if system and "FINAL" in prompt:
            return "DRAFT: x\n\nCRITIQUE: y\n\nFINAL: done"
        if system and "Numbered" in system:
            return "1) Do a\n2) Do b\n3) Do c"
        if system and "Execute" in system:
            return "result: executed"
        return "ok"

def test_self_check_flow():
    from src.patterns.self_check import self_check
    out = self_check(DummyClient(), "test")
    assert "FINAL" in out

def test_planner_executor_flow():
    from src.patterns.planner_executor import planner_executor
    out = planner_executor(DummyClient(), "anything")
    assert "executed" in out

def test_react_contract():
    from src.patterns.react import react
    out = react(DummyClient(), "what time is it?", max_steps=1)
    assert isinstance(out, str)
