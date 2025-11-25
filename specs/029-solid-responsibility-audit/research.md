# Research: SOLID & Responsibility Audit

**Feature**: SOLID & Responsibility Audit
**Status**: COMPLETE

## Decision 1: Static Analysis Strategy

**Decision**: Use a combination of existing tools (`ruff`, `mypy`) and custom Python scripts to enforce architectural boundaries.

**Rationale**:
- `ruff` handles standard linting but doesn't inherently understand "Service vs Router" layers.
- A custom script (`dev_scripts/audit_architecture.py`) can specifically check for forbidden imports (e.g., `bpy` in `controller/`) and circular dependencies in a more targeted way than generic tools.
- `mypy` ensures type safety which aids in refactoring.

**Alternatives considered**:
- **Graphviz/pydeps**: Good for visualization, but harder to automate as a pass/fail gate in CI.
- **Module-level `__all__` exports**: Enforcing `__all__` is good practice but doesn't strictly prevent "God classes".

## Decision 2: Controller Layering

**Decision**: Enforce the following strict dependencies:
- `main.py` (Router) -> depends on `services.py`
- `services.py` (Service) -> depends on `gemini_client.py`, `knowledge_engine.py`, `models.py`
- `models.py` (Data) -> No dependencies on business logic.
- `gemini_client.py` (Infra) -> No dependencies on business logic.

**Rationale**: This is the standard layered architecture. It ensures the "core" logic is independent of the delivery mechanism (FastAPI).

## Decision 3: Blender Addon Exemption

**Decision**: The `blender_addon/` directory is explicitly EXEMPT from strict pure-Python SOLID rules regarding dependency injection and interface segregation where `bpy` is concerned.

**Rationale**:
- Blender's API (`bpy`) relies heavily on global state (`bpy.context`) and strict class registration patterns that violate standard OOP/SOLID principles.
- Trying to force `bpy` code into standard patterns often results in *more* complex and fragile code.
- We will still enforce separation of UI (`ui.py`) from Logic (`operators.py`) as much as possible.

## Decision 4: "God Class" Metric

**Decision**: A "God Class" is defined as any file > 300 lines or a class with > 10 public methods (excluding getters/setters), or a file that imports from more than 3 distinct "layers".

**Rationale**: 
- 300 lines is a reasonable soft limit for Python modules in this project scope.
- Imports from multiple layers usually indicate a violation of Single Responsibility.
