import subprocess
import tempfile
from typing import Dict, Any
import json

def run_in_sandbox(request_id: str, script: str, timeout_seconds: int = 30) -> Dict[str, Any]:
    """Run the provided `script` in sandboxed environment.

    This is a minimal placeholder that writes the script to a temp file and attempts
    to run it using the system python interpreter (NOT Blender). In production this
    should invoke Blender headless inside Docker and return structured results.
    """
    with tempfile.NamedTemporaryFile(suffix=".py", mode="w+", delete=False, encoding="utf-8") as tf:
        tf.write(script)
        script_path = tf.name

    try:
        # NOTE: running the script directly is only a local simulation and does not
        # execute Blender operators. It's useful for detecting syntax/runtime errors.
        proc = subprocess.run(["python", script_path], capture_output=True, text=True, timeout=timeout_seconds)
        return {
            "success": proc.returncode == 0,
            "stdout": proc.stdout,
            "stderr": proc.stderr,
            "returncode": proc.returncode,
        }
    except subprocess.TimeoutExpired as e:
        return {"success": False, "stdout": "", "stderr": "Timeout", "error": str(e)}
