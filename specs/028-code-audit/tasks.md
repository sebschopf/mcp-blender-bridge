# Tasks: 028-code-audit

## Phase 1: Setup
- [x] T001 Verify installation of `ruff` and `mypy` in the development environment
- [x] T002 Update `controller/pyproject.toml` to ensure strict configuration (line-length 120, docstrings, type checking) matching FR-001/FR-004

## Phase 2: Foundational
- [x] T003 Ensure `run_tests.bat` or equivalent executes without error before starting audit

## Phase 3: Automated Code Quality Enforcement (US1)
**Goal**: Ensure the codebase passes a rigorous automated audit for style, formatting, complexity, and static analysis errors.
**Independent Test**: `ruff check .` returns 0 errors, `mypy .` returns 0 errors (controller).

### Controller Audit
- [x] T004 [US1] Run `ruff format controller/` to apply automatic formatting fixes
- [x] T005 [US1] Run `ruff check controller/ --fix` to apply automatic linting fixes
- [x] T006 [US1] Manually resolve remaining `ruff` errors in `controller/` (e.g., complex unused imports, naming violations)
- [x] T007 [US1] Run `mypy controller/` and fix type errors (add `Optional`, fix signatures, handle `Any`)

### Addon Audit
- [x] T008 [P] [US1] Run `ruff format blender_addon/` to apply automatic formatting fixes
- [x] T009 [P] [US1] Run `ruff check blender_addon/ --fix` to apply automatic linting fixes
- [x] T010 [P] [US1] Manually resolve remaining `ruff` errors in `blender_addon/`

### Refactoring & Complexity (FR-005)
- [x] T011 [US1] Analyze `controller/app/gemini_client.py` for "God class" violations (>300 lines) and refactor if needed
- [x] T012 [P] [US1] Analyze `controller/app/services.py` for "God class" violations and refactor if needed
- [x] T013 [P] [US1] Analyze `controller/app/main.py` for complexity and refactor if needed
- [x] T014 [US1] Verify and add missing docstrings to public modules/functions in `controller/` per FR-003

## Phase 4: Polish & Validation
- [x] T015 Run `run_validation_tests.bat` to ensure no functional regressions
- [x] T016 Remove any identified dead code (FR-006)
- [x] T017 Final run of `ruff check .` and `mypy controller/` to confirm zero violations

## Dependencies
- US1 (Automated Code Quality Enforcement) depends on Phase 1 & 2.

## Implementation Strategy
1.  **Start with Setup**: Ensure tools are ready and config is strict.
2.  **Automate First**: Run auto-fixers (`--fix`, `format`) to clear low-hanging fruit.
3.  **Tackle Types**: `mypy` often reveals logic bugs, so do this carefully in `controller/`.
4.  **Refactor Last**: Only refactor complex classes after linting/typing is stable to minimize conflict.
