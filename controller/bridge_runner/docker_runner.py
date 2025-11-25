from typing import Dict, Any
import shutil

from .sandbox_runner import run_in_sandbox


def run_in_docker(request_id: str, script: str, image: str = "blender:headless", timeout: int = 60) -> Dict[str, Any]:
    """Placeholder Docker runner.

    Attempts to invoke Docker if available. If Docker is not present, falls back to
    `run_in_sandbox` which performs a local simulation (syntax/runtime checks).

    In production this function should build a secure, resource-limited container
    that runs Blender in headless mode and executes the script.
    """
    docker_path = shutil.which("docker")
    if not docker_path:
        return {"fallback": True, **run_in_sandbox(request_id, script)}

    # Minimal placeholder: real implementation should create a container, mount volumes,
    # copy script, run `blender --background --python /path/to/script.py`, capture output.
    return {"success": False, "error": "Docker runner not implemented yet"}
