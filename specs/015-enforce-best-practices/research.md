# Research: Codebase Audit

## 1. Tools Status
- `ruff` and `mypy` are NOT installed in the environment.
- `pyproject.toml` exists but needs configuration for these tools.

## 2. Duplication Audit

### Controller
- `main.py` seems to contain logic that could be moved (e.g., `gemini_client` initialization, session management).
- `gemini_client.py` has been refactored recently, likely clean, but needs type checking.

### Blender Addon
- `operators.py` often accumulates boilerplate for `execute` methods.
- `server_manager.py` handles process management, which is distinct.

## 3. Decisions
- **Decision**: Add `ruff` and `mypy` to `dev-dependencies` (or `test` dependencies in `pyproject.toml` if strict dev group isn't supported by the current setup).
- **Decision**: Use Google Docstring style convention for `ruff` (pydocstyle setting).
