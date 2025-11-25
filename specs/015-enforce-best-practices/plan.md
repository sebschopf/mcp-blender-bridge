# Implementation Plan - Enforce Project Best Practices

## 1. Technical Context

**Language/Framework**: Python 3.11+, FastAPI (Controller), `google-genai` (SDK), `ruff` (Linter/Formatter), `mypy` (Static Type Checker).

**Current State**:
- Project uses `ruff` (implied by previous context, but configuration needs verification).
- Codebase has grown with multiple features; potential for technical debt.
- `GeminiClient` was recently migrated but might still have residual complexity.
- `main.py` might be accumulating too much logic.

**Constraints**:
- Refactoring must be "safe" - no behavior changes.
- Existing tests must pass at all times.
- `ruff` and `mypy` configurations should be standardized in `pyproject.toml`.

## 2. Constitution Check

- [x] **I. Strict MCP Architecture**: Refactoring enforces this separation (Controller logic audit).
- [x] **II. Conversational Interface**: N/A (Code quality).
- [x] **III. Granular & Secure Tools**: N/A (Code quality).
- [x] **IV. User-Centric Control**: N/A.
- [x] **V. Blender-Native Integration**: Refactoring `blender_addon` ensures it remains a clean Peripheral.
- [x] **VI. Continuous Validation**: The core of this feature. We will add linting/type-checking as part of the validation process.

## 3. Gates

- [x] **Gate 1: Authorization**: Feature `015-enforce-best-practices` approved.
- [x] **Gate 2: Research**: Best practices (SOLID, Google Style) are standard industry knowledge. Specific tool configs (`ruff`, `mypy`) are standard.
- [x] **Gate 3: Constitution**: Checked above.

## Phase 0: Outline & Research

### 0.1 Research Tasks
- [x] **Task**: Review `pyproject.toml` for existing `ruff` and `mypy` settings.
- [x] **Task**: Identify key areas of duplication in `controller/app`.

### 0.2 Output
- **Artifact**: `specs/015-enforce-best-practices/research.md` (Audit findings).

## Phase 1: Design & Contracts

### 1.1 Data Model Changes
- No data model changes.

### 1.2 API Contract Updates
- No API contract changes.

### 1.3 Agent Context Update
- No agent context update needed as no new technology is introduced, just enforcement of existing ones.

### 1.4 Output
- **Artifact**: `specs/015-enforce-best-practices/quickstart.md` (Update with linting commands).

## Phase 2: Implementation

### 2.1 Configuration
- **Step 1**: Configure `ruff` in `controller/pyproject.toml` (rules: Google style docstrings, complexity limits).
- **Step 2**: Configure `mypy` in `controller/pyproject.toml`.

### 2.2 Controller Refactoring
- **Step 3**: Run `ruff check controller/` and fix stylistic issues (imports, whitespace, dead code).
- **Step 4**: Run `mypy controller/` and fix type errors.
- **Step 5**: Audit `controller/app/main.py`. If routing logic is mixed with business logic, extract Service classes (e.g., `ChatService`).
- **Step 6**: Audit `controller/app/gemini_client.py`. Ensure SRP.

### 2.3 Addon Refactoring
- **Step 7**: Audit `blender_addon/` for duplication (especially in `operators.py` regarding server communication).
- **Step 8**: Ensure all operators have docstrings.

### 2.4 Validation
- **Step 9**: Run full test suite.
- **Step 10**: Verify static analysis passes cleanly.

## 4. Dependencies

- `ruff`
- `mypy`