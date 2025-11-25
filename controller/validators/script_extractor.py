import re
from typing import Optional

fenced_re = re.compile(r"```python\n([\s\S]+?)\n```", re.MULTILINE)

def extract_script_from_response(text: str) -> Optional[str]:
    """Extract Python code from LLM response. Supports fenced code blocks or returns raw text if it looks like code."""
    m = fenced_re.search(text)
    if m:
        return m.group(1)

    # Heuristic: if text starts with 'import bpy' or 'def ' or 'bpy.' assume it's code
    if text.strip().startswith(("import bpy", "from bpy", "def ", "bpy.")):
        return text

    return None
