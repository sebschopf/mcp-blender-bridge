# Implementation Tasks: Robust Connection Handling

**Feature Branch**: `003-robust-connection`  
**Feature Spec**: `specs/003-robust-connection/spec.md`  
**Implementation Plan**: `specs/003-robust-connection/plan.md`  
**Created**: 2025-11-16

## Phase 1: Setup & Project Initialization

- [X] T001 Replace the `mcp_connected` `BoolProperty` with an `EnumProperty` for connection status in `blender_addon/__init__.py`
- [X] T002 Create a new timer function `attempt_connection()` in `blender_addon/__init__.py`

## Phase 2: User Story 1 - Graceful Connection Attempt (P1)

**Goal**: The addon gracefully handles connection attempts, providing clear UI feedback without errors.
**Independent Test**: Clicking "Connect" without the server running shows a "Connecting..." status and doesn't crash.

- [X] T003 [US1] Modify the `Connect` operator in `blender_addon/__init__.py` to set the status to `CONNECTING` and register the `attempt_connection` timer
- [X] T004 [US1] Implement the logic within the `attempt_connection()` timer in `blender_addon/__init__.py` to try connecting once
- [X] T005 [US1] If the connection in `attempt_connection()` is successful, set status to `CONNECTED` and unregister the timer in `blender_addon/__init__.py`
- [X] T006 [US1] Modify the `Disconnect` operator in `blender_addon/__init__.py` to set status to `DISCONNECTED` and unregister the connection timer
- [X] T007 [US1] Update the UI panel in `blender_addon/ui.py` to display different text and button states based on the new connection status enum
- [X] T008 [US1] Add a short timeout to the `requests` call in `blender_addon/mcp_client.py` to prevent UI freezes

## Phase 3: Polish & Cross-Cutting Concerns

- [X] T009 Review all user-facing status messages for clarity in `blender_addon/ui.py`
- [X] T010 Add logging to the connection attempt timer in `blender_addon/__init__.py`

## Dependencies

- Phase 1 must be completed before Phase 2.
- Phase 2 implements the core user story.
- Phase 3 can be done after Phase 2 is complete.

## Implementation Strategy

The implementation will be done in a single pass, focusing on the `blender_addon` directory. The changes are localized and build upon the existing structure.
