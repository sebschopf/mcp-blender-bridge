# Feature Specification: SOLID & Responsibility Audit

**Feature Branch**: `029-solid-responsibility-audit`  
**Created**: 2025-11-25  
**Status**: Draft  
**Input**: User description: "Je veux vérifier pour que le projet soit SOLID et qu'il n'y est pas de mélange de responsabilité (entre autre) dans les fichiers, sauf pour l'addon qui est BPY et donc qui est différent."

## User Scenarios & Testing

### User Story 1 - Standardize Controller Architecture (Priority: P1)

As a maintainer, I want the `controller/` codebase to adhere strictly to SOLID principles and a layered architecture (e.g., Services vs. Models vs. Controllers) so that future features can be added without introducing regressions or tight coupling.

**Why this priority**: Essential for long-term project health. The controller is the brain of the operation; if it's messy, the whole bridge becomes unstable.

**Independent Test**:
- Run a static analysis tool (e.g., custom script or manual review checklist) that flags circular imports or "God classes" in `controller/`.
- Verify that `controller/app/services.py` (if it exists) does not contain direct HTTP route definitions (should be in `main.py` or `routers/`).
- Verify that data models (Pydantic) are separated from business logic.

**Acceptance Scenarios**:

1. **Given** the `controller/` directory, **When** analyzed for Single Responsibility Principle, **Then** no file should contain both API route definitions and complex business logic implementations (logic should be delegated to services).
2. **Given** the dependency graph of `controller/`, **When** visualized, **Then** there should be no circular dependencies between modules.
3. **Given** the project structure, **When** a new developer looks for "where X logic lives", **Then** the folder structure (e.g., `models/`, `services/`, `routers/`) clearly indicates the location.

### User Story 2 - Isolate Blender Addon Complexity (Priority: P2)

As a maintainer, I want to ensure that while `blender_addon/` is exempt from strict pure-Python standards due to `bpy`, it still maintains internal consistency and does not leak `bpy` dependencies into the controller or shared libraries.

**Why this priority**: Prevents the "addon" specific hacks from polluting the clean "controller" backend.

**Independent Test**:
- Scan `controller/` for any imports of `bpy`.
- Verify that `blender_addon/` files are reasonably organized (e.g., UI code separate from operator logic).

**Acceptance Scenarios**:

1. **Given** the `controller/` codebase, **When** searched for `import bpy`, **Then** zero occurrences are found.
2. **Given** the `blender_addon/`, **When** inspected, **Then** UI panels are defined in separate files/modules from the core operator execution logic where feasible.

## Requirements

### Functional Requirements

- **FR-001**: The `controller/` application MUST follow a layered architecture:
    - **Router Layer**: Handles HTTP requests/responses (e.g., `main.py` or `routers/*.py`).
    - **Service Layer**: Contains business logic (e.g., `services.py`).
    - **Model Layer**: Contains data structures (e.g., `models.py`).
    - **Infrastructure Layer**: Handles external communication (e.g., `gemini_client.py`).
- **FR-002**: Circular dependencies MUST be eliminated from `controller/`.
- **FR-003**: "God classes" (classes > 300 lines or handling multiple distinct responsibilities) in `controller/` MUST be refactored into smaller, focused classes.
- **FR-004**: The `blender_addon/` MUST NOT be imported by the `controller/`.
- **FR-005**: Code in `controller/` MUST use Dependency Injection where applicable to improve testability (e.g., passing clients to services instead of hardcoding instantiations).

### Key Entities

- **Service**: A stateless class/module containing pure business logic.
- **Controller/Router**: The entry point for API calls, responsible *only* for parsing requests and calling services.
- **Client**: A wrapper for external APIs (Gemini, etc.).

## Success Criteria

### Measurable Outcomes

- **SC-001**: 0 circular dependencies detected in `controller/`.
- **SC-002**: 100% of API routes in `controller/` delegate logic to a Service or Utility function (api functions < 20 lines of logic themselves).
- **SC-003**: `controller/` code coverage (if tests exist) does not decrease during refactoring.
- **SC-004**: All files in `controller/` have a clear, single responsibility as defined by their module name.