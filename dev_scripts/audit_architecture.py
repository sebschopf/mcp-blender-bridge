import os
import ast
import sys
from pathlib import Path
from typing import List, Dict, Set, Tuple

# Configuration
FORBIDDEN_IMPORTS = {
    "controller": ["bpy"],
}

LAYER_DEPENDENCIES = {
    "main.py": {"services", "models", "bridge_api", "logging_utils", "mcp_server", "globals", "gemini_client"},
    "services.py": {"gemini_client", "knowledge_engine", "models", "logging_utils", "mcp_server"},
    "models.py": set(),  # Should be pure
    "gemini_client.py": {"models", "logging_utils"},
    "bridge_api.py": {"bridge_models", "logging_utils"},
    "mcp_server.py": {"globals", "bridge_api", "models", "logging_utils"},
    "tool_index.py": {"models"},
    "knowledge_engine.py": {"tool_index", "models", "logging_utils"},
}

# Allow some leeway for utility imports
ALLOWED_UTILS = {"typing", "logging", "json", "os", "sys", "datetime", "uuid", "re", "collections", "asyncio", "fastapi", "pydantic", "mcp", "yaml"}

def check_forbidden_imports(root_dir: str) -> List[str]:
    errors = []
    for dir_name, forbidden in FORBIDDEN_IMPORTS.items():
        scan_dir = os.path.join(root_dir, dir_name)
        if not os.path.exists(scan_dir):
            continue
            
        for root, _, files in os.walk(scan_dir):
            for file in files:
                if not file.endswith(".py"):
                    continue
                
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    try:
                        tree = ast.parse(f.read())
                    except SyntaxError:
                        continue # Skip invalid python files
                        
                    for node in ast.walk(tree):
                        if isinstance(node, ast.Import):
                            for name in node.names:
                                if name.name in forbidden:
                                    errors.append(f"[FORBIDDEN IMPORT] {file_path}: Imports '{name.name}'")
                        elif isinstance(node, ast.ImportFrom):
                            if node.module and node.module in forbidden:
                                errors.append(f"[FORBIDDEN IMPORT] {file_path}: Imports from '{node.module}'")
    return errors

def get_local_imports(file_path: str, app_root: str) -> Set[str]:
    """Extracts local module imports from a file."""
    with open(file_path, "r", encoding="utf-8") as f:
        try:
            tree = ast.parse(f.read())
        except SyntaxError:
            return set()

    imports = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            if node.module:
                # Check if it's a relative import or app import
                if node.level > 0: # Relative import
                    # Simplified relative resolution for audit
                    imports.add(node.module if node.module else "parent") # Approximation
                elif node.module.startswith("app.") or node.module.startswith("."):
                     imports.add(node.module.split('.')[-1])
                elif node.module in ["models", "services", "gemini_client", "main"]: # Top level app imports if any
                     imports.add(node.module)
        # Ignore direct 'import app.x' for now as code uses 'from . import' mostly
    
    return imports

def check_layered_architecture(app_dir: str) -> List[str]:
    errors = []
    for filename, allowed_deps in LAYER_DEPENDENCIES.items():
        file_path = os.path.join(app_dir, filename)
        if not os.path.exists(file_path):
            continue
            
        actual_imports = get_local_imports(file_path, app_dir)
        
        # Filter actual imports to only those we track in LAYER_DEPENDENCIES keys (stripped of .py)
        tracked_modules = {k.replace(".py", "") for k in LAYER_DEPENDENCIES.keys()}
        
        for imp in actual_imports:
            # Clean up import name
            clean_imp = imp
            if clean_imp in tracked_modules:
                if clean_imp not in allowed_deps:
                     # Exception for models (often circular if not careful, but strict rule says models is pure)
                     # Exception for main (router)
                     errors.append(f"[LAYER VIOLATION] {filename} imports '{clean_imp}' which is not in allowed dependencies: {allowed_deps}")

    return errors

def detect_circular_dependencies(app_dir: str) -> List[str]:
    # Simple graph cycle check
    graph = {}
    files = [f for f in os.listdir(app_dir) if f.endswith(".py")]
    
    for f in files:
        module_name = f.replace(".py", "")
        imports = get_local_imports(os.path.join(app_dir, f), app_dir)
        # Filter to local modules only
        local_imports = {i for i in imports if f"{i}.py" in files}
        graph[module_name] = local_imports

    # DFS for cycles
    visited = set()
    recursion_stack = set()
    cycles = []

    def dfs(node, path):
        visited.add(node)
        recursion_stack.add(node)
        path.append(node)

        if node in graph:
            for neighbor in graph[node]:
                if neighbor not in visited:
                    if dfs(neighbor, path):
                        return True
                elif neighbor in recursion_stack:
                    cycles.append(list(path) + [neighbor])
                    return True
        
        recursion_stack.remove(node)
        path.pop()
        return False

    for node in graph:
        if node not in visited:
            dfs(node, [])
            
    return [f"[CIRCULAR DEP] {' -> '.join(c)}" for c in cycles]

def main():
    root_dir = os.getcwd()
    controller_app_dir = os.path.join(root_dir, "controller", "app")
    
    print("--- Starting Architecture Audit ---")
    
    # 1. Forbidden Imports
    forbidden_errors = check_forbidden_imports(root_dir)
    for err in forbidden_errors:
        print(err)
        
    # 2. Layered Architecture
    layer_errors = check_layered_architecture(controller_app_dir)
    for err in layer_errors:
        print(err)

    # 3. Circular Dependencies
    circle_errors = detect_circular_dependencies(controller_app_dir)
    for err in circle_errors:
        print(err)

    if not forbidden_errors and not layer_errors and not circle_errors:
        print("✅ Audit Passed: No violations found.")
        sys.exit(0)
    else:
        print(f"❌ Audit Failed: Found {len(forbidden_errors) + len(layer_errors) + len(circle_errors)} violations.")
        sys.exit(1)

if __name__ == "__main__":
    main()
