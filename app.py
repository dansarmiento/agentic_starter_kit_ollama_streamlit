import os
import streamlit as st
from dotenv import load_dotenv
import logging
from logging.handlers import RotatingFileHandler

from src.llm_client import OllamaClient
from src.patterns.self_check import self_check
from src.patterns.react import react
from src.patterns.planner_executor import planner_executor
from src.patterns.reflection import reflect
from src.patterns.rag import answer_with_rag
import re

def is_valid_url(url):
    """Simple URL validation."""
    return re.match(r"https?://", url) is not None

def validate_inputs(base_url, model, *tasks):
    """Validate user inputs."""
    if not is_valid_url(base_url):
        st.error("Please enter a valid Ollama base URL (e.g., http://localhost:11434).")
        return False
    if not model.strip():
        st.error("Please enter a model name.")
        return False
    for task in tasks:
        if not task.strip():
            st.error("Please ensure all text fields are filled.")
            return False
    return True

load_dotenv()

# Setup logging
log_directory = "log"
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

log_file = os.path.join(log_directory, "app.log")

# Use a rotating file handler to keep log files from growing too large
handler = RotatingFileHandler(log_file, maxBytes=10*1024*1024, backupCount=5)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[handler, logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

st.set_page_config(page_title="Agentic AI Starter", layout="wide")
st.title("Agentic AI Starter — Streamlit UI")

with st.sidebar:
    st.header("Model & Connection")
    base_url = st.text_input("Ollama base URL", os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434"))
    model = st.text_input("Model", os.getenv("MODEL", "llama3.1:8b-instruct"))
    temperature = st.slider("Temperature", 0.0, 1.0, 0.2, 0.05)
    max_tokens = st.number_input("Max tokens", min_value=128, max_value=8192, value=2048, step=64)

    st.markdown("---")
    st.caption("Tip: Pull models in your terminal, e.g.:")
    st.code("ollama pull llama3.1:8b-instruct", language="bash")

tabs = st.tabs(["Self-Check", "ReAct", "Planner–Executor", "Reflection", "RAG"])

# Self-Check
with tabs[0]:
    st.subheader("Self-Check")
    task = st.text_area("Task", "Write a Python function to check if a number is prime; include edge cases.")
    if st.button("Run Self-Check", key="btn_sc"):
        if validate_inputs(base_url, model, task):
            with st.spinner("Running..."):
                try:
                    client = OllamaClient(base_url=base_url, model=model)
                    out = client.generate(
                        prompt=f"""Task: {task}

Respond in three sections:
DRAFT:
[Write your first attempt.]

CRITIQUE:
[List concrete issues, missing steps, errors, ambiguities.]

FINAL:
[Fix every issue. Provide a clean, correct solution.]
""",
                    system="You are a careful reasoner. Produce a DRAFT answer, then CRITIQUE it, then FINAL. Keep critique concise and specific.",
                    temperature=temperature,
                    num_predict=max_tokens,
                )
                if out.startswith("Error:"):
                    st.error(out)
                    logger.error(out)
                else:
                    st.text_area("Output", out, height=300)
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")
                logger.error(f"An unexpected error occurred in Self-Check: {e}", exc_info=True)

# ReAct
with tabs[1]:
    st.subheader("ReAct")
    q = st.text_input("Question", "What time is it right now?")
    steps = st.slider("Max steps", 1, 10, 6)
    if st.button("Run ReAct", key="btn_react"):
        if validate_inputs(base_url, model, q):
            with st.spinner("Running..."):
                try:
                    client = OllamaClient(base_url=base_url, model=model)
                    out = react(client, q, max_steps=steps)
                    if out.startswith("Error:"):
                        st.error(out)
                        logger.error(out)
                    else:
                        st.text_area("Answer", out, height=300)
                except Exception as e:
                    st.error(f"An unexpected error occurred: {e}")
                    logger.error(f"An unexpected error occurred in ReAct: {e}", exc_info=True)

# Planner–Executor
with tabs[2]:
    st.subheader("Planner–Executor")
    t = st.text_input("Task", "Generate a bash one-liner to count unique IPs in access.log")
    if st.button("Run Planner–Executor", key="btn_pe"):
        if validate_inputs(base_url, model, t):
            with st.spinner("Planning & executing..."):
                try:
                    client = OllamaClient(base_url=base_url, model=model)
                    out = planner_executor(client, t)
                    if out.startswith("Error:"):
                        st.error(out)
                        logger.error(out)
                    else:
                        st.text_area("Result", out, height=300)
                except Exception as e:
                    st.error(f"An unexpected error occurred: {e}")
                    logger.error(f"An unexpected error occurred in Planner-Executor: {e}", exc_info=True)

# Reflection
with tabs[3]:
    st.subheader("Reflection")
    question = st.text_input("Question", "How to check primality efficiently?")
    attempt = st.text_area("Attempt", "Use a loop to test divisibility up to n.")
    if st.button("Run Reflection", key="btn_refl"):
        if validate_inputs(base_url, model, question, attempt):
            with st.spinner("Reflecting..."):
                try:
                    client = OllamaClient(base_url=base_url, model=model)
                    out = reflect(client, question, attempt)
                    if out.startswith("Error:"):
                        st.error(out)
                        logger.error(out)
                    else:
                        st.text_area("Improved Answer", out, height=300)
                except Exception as e:
                    st.error(f"An unexpected error occurred: {e}")
                    logger.error(f"An unexpected error occurred in Reflection: {e}", exc_info=True)

# RAG
with tabs[4]:
    st.subheader("RAG (local docs in ./data)")
    st.caption("Drop .txt/.md/.py or any plain-text docs into the data/ folder, then run. First run builds a tiny local vector DB.")
    question = st.text_input("RAG Question", "Summarize the key ideas in our local docs.")
    k = st.slider("Top K", 1, 10, 4)
    if st.button("Run RAG", key="btn_rag"):
        if validate_inputs(base_url, model, question):
            with st.spinner("Searching and answering..."):
                try:
                    client = OllamaClient(base_url=base_url, model=model)
                    out = answer_with_rag(client, question, k=k)
                    if out.startswith("Error:"):
                        st.error(out)
                        logger.error(out)
                    else:
                        st.text_area("Answer", out, height=300)
                except Exception as e:
                    st.error(f"An unexpected error occurred: {e}")
                    logger.error(f"An unexpected error occurred in RAG: {e}", exc_info=True)

st.markdown("---")
st.caption("Agentic AI Starter (Python + Ollama) — Streamlit UI")
