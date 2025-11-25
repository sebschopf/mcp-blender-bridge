# Implementation Plan - 028-code-audit

**Feature**: Codebase Standards Audit
**Status**: DRAFT

## Technical Context

### Architecture Overview

This feature focuses on standardizing the Python codebase within the `controller/` and `blender_addon/` (if Python based) directories. The goal is to enforce PEP 8, type safety, and maintainability metrics.
We already have `ruff` and `mypy` configured in `controller/pyproject.toml`. The audit will involve running these tools, analyzing violations, and fixing them iteratively.

**Existing Components:**
- `controller/`: Main FastAPI application. Configured with `ruff` and `mypy`.
- `blender_addon/`: Blender Python scripts. Often exempt from strict standard Python tooling due to `bpy` dependency, but basic linting applies.

### Libraries & Dependencies

- **Dev Dependencies**: `ruff`, `mypy`.

### Project Structure

```text
controller/pyproject.toml  # Update: Refine rules if needed (line length 120, etc.)
```

## Constitution Check

### Privacy & Security
- **Data Handling**: No change.
- **Safety**: Code quality directly impacts stability.

### Technical Constraints
- **Blender API**: `bpy` module is not installable via pip. Type checking for `blender_addon/` requires `fake-bpy-module` or careful exclusion of `import bpy` errors.
- **Strictness**: We aim for strict compliance, but pragmatism is allowed for legacy code if refactoring risk is high (use `# noqa` sparingly).

## Phase 0: Research & Decisions

### Design Decisions

1.  **Config Strategy**: We will stick to the existing `controller/pyproject.toml` but review the line length (ensure 120) and enabled rules.
2.  **Blender Addon**: We will run `ruff` on `blender_addon/` but likely exclude `mypy` unless stubs are set up. For this pass, we focus linting on both, typing on controller.
3.  **Refactoring**: If we find "God classes" (e.g. `GeminiClient` growing too big), we will extract methods or classes.

## Phase 1: Design & Contracts

### API Changes

- No API changes.

## Phase 2: Implementation

### Dependencies

- Ensure `ruff` and `mypy` are installed (they are in `requirements.txt` / `pyproject.toml` presumably).

### Strategy

1.  **Configure**: Update `pyproject.toml` to enforce line-length 120 and ensure docstring rules (D) are enabled if not annoying.
2.  **Audit Controller**:
    - Run `ruff check controller/ --fix`.
    - Run `ruff format controller/`.
    - Run `mypy controller/`.
    - Fix type errors (missing `Optional`, etc.).
3.  **Audit Addon**:
    - Run `ruff check blender_addon/ --fix`.
    - Run `ruff format blender_addon/`.
    - (Skip `mypy` for addon for now unless easy).
4.  **Complexity**: Manually review largest files (`gemini_client.py`, `services.py`) for function length violations (>50 lines).

## Phase 3: Polish

- Verify CI/CD pipeline (if exists) uses these commands.
- Ensure no regression in tests.