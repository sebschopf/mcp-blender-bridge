# Tasks: 015-enforce-best-practices

## Phase 1: Setup
Goal: Install and configure code quality tools.

- [x] T001 Update `controller/pyproject.toml` to include `ruff` and `mypy` configuration (google style docstrings, etc.)
- [x] T002 Install dev dependencies (`ruff`, `mypy`) in the controller environment

## Phase 2: Foundational
Goal: Fix low-hanging fruit (style and types) to establish a baseline.

- [x] T003 Run `ruff check controller/ --fix` to address auto-fixable linting errors
- [x] T004 Run `mypy controller/` and fix critical type errors to ensure type safety
- [x] T005 [P] Audit and fix docstrings in `controller/app` modules to match Google Style

## Phase 3: User Story 1 (Lead Developer - SOLID/MCP)
Goal: Enforce architectural separation and single responsibility.

- [x] T006 [US1] Refactor `controller/app/main.py`: Extract business logic (chat orchestration) into a new `ChatService` class
- [x] T007 [US1] Audit `GeminiClient` in `controller/app/gemini_client.py` to ensure it only handles API communication (SRP check)
- [x] T008 [US1] Audit `blender_addon/operators.py` to ensure it contains no business logic (Peripheral check)

## Phase 4: User Story 2 (Contributor - Deduplication)
Goal: Remove redundancy and improve readability.

- [x] T009 [US2] Deduplicate common logic in `controller/app` (if identified during audit)
- [x] T010 [US2] Deduplicate common logic in `blender_addon` (e.g., server communication helpers)
- [x] T011 [US2] Scan for and remove commented-out/dead code in `controller/` and `blender_addon/`

## Phase 5: Polish
Goal: Verify integrity.

- [x] T012 Run full test suite `pytest controller/` to ensure no regressions
- [x] T013 Verify static analysis passes cleanly (`ruff check` and `mypy`)

## Dependencies

1. Setup (T001-T002) is required for tools to work.
2. Foundational cleanup (T003-T005) makes refactoring (Phase 3-4) clearer.
3. Tests (T012) must run after any code changes.

## Implementation Strategy
- **MVP**: Steps T001-T005 (Tooling & Cleanup) immediately improve quality.
- **Incremental**: Refactor `main.py` (T006) as a separate step to ensure routing still works.
