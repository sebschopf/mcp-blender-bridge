"""Loader for LLM prompts."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def load_prompt(name: str) -> str:
    """Load a prompt template by filename (without extension) from resources/llm_prompts."""
    p = ROOT / f"{name}.md"
    if not p.exists():
        raise FileNotFoundError(f"Prompt template not found: {p}")
    return p.read_text(encoding="utf-8")
