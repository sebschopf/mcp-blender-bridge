# Tasks: SOLID & Responsibility Audit

## Phase 1: Setup & Analysis
- [x] T001 Create `dev_scripts/audit_architecture.py` to detect forbidden imports and circular dependencies
- [x] T002 Configure `audit_architecture.py` with layered architecture rules from `research.md`
- [x] T003 Run initial audit to identify existing violations in `controller/`

## Phase 2: Controller Refactoring (US1)
**Goal**: Ensure strictly layered architecture in `controller/`.
**Independent Test**: `python dev_scripts/audit_architecture.py` returns 0 errors.

### Infrastructure Layer
- [x] T004 [US1] Audit `controller/app/gemini_client.py` to ensure no business logic or circular deps
- [x] T005 [US1] Audit `controller/app/mcp_server.py` for dependency violations

### Service Layer
- [x] T006 [US1] Audit `controller/app/services.py` to ensure no route definitions or `bpy` imports
- [x] T007 [US1] Verify `controller/app/services.py` dependencies are injected where possible (FR-005)

### Router Layer
- [x] T008 [US1] Audit `controller/app/main.py` to ensure it only handles routing and delegates to services
- [x] T009 [US1] Extract any business logic found in `main.py` into `services.py`

### Models Layer
- [x] T010 [US1] Audit `controller/app/models.py` to ensure pure data structures (no logic)

## Phase 3: Blender Addon Verification (US2)
**Goal**: Verify internal consistency of `blender_addon/` without enforcing pure-Python SOLID rules.
**Independent Test**: Manual review or script check confirming UI separation.

- [x] T011 [US2] Scan `blender_addon/` for UI code mixed with heavy logic (e.g. in `operators.py`)
- [x] T012 [US2] Ensure `ui.py` contains primarily `draw` methods and panel definitions
- [x] T013 [US2] Verify `mcp_client.py` handles network communication and not UI logic

## Phase 4: Final Validation
- [x] T014 Run full test suite (`run_tests.bat`) to ensure refactoring caused no regressions
- [x] T015 Run `dev_scripts/audit_architecture.py` one final time to confirm 0 violations
- [x] T016 Document any accepted exceptions in `research.md` if strictly necessary

## Dependencies
- US1 depends on Phase 1 (Setup).
- US2 is independent of US1.

## Implementation Strategy
1.  **Tooling First**: Build the auditor script to have a measuring stick.
2.  **Refactor by Layer**: Start from the bottom (Models/Infra) up to Routers.
3.  **Addon Check**: Parallelizable, as it's mostly verifying existing separation.