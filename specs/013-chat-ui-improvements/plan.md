# Implementation Plan: Chat UI Improvements

**Branch**: `013-chat-ui-improvements` | **Date**: 2025-11-21 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/013-chat-ui-improvements/spec.md`

## Summary

This plan details the improvements to the Blender Addon's chat interface to enhance user feedback and responsiveness. Key changes include making the chat UI visible immediately upon connection attempt, adding explicit system messages to the chat history, and displaying a placeholder when the history is empty. Crucially, it includes a backend architectural refactoring to resolve a deadlock issue where internal tool calls caused HTTP timeouts.

## Technical Context

**Language/Version**: Python 3.11+ (Addon & Controller)
**Primary Dependencies**: `bpy`, `fastapi`
**Storage**: Blender `Scene` properties (temporary runtime state), `globals.py` (backend singleton)
**Testing**: `unittest` (via Blender)
**Target Platform**: Blender 3.0+ (Windows/macOS/Linux)
**Project Type**: Blender Addon UI Logic & Backend Architecture
**Performance Goals**: Immediate UI feedback (<0.1s) on user actions; Zero backend deadlocks.
**Constraints**: UI updates must happen in the main thread; backend internal calls must be direct, not via HTTP.
**Scale/Scope**: Single-user UI enhancements & core backend stability fix.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- ✅ **I. Strict MCP Architecture**: Compliant. Refactoring maintains the separation but optimizes internal communication.
- ✅ **II. Conversational Interface**: Compliant. Enhances the conversational experience with better feedback.
- ✅ **III. Granular & Secure Tools**: Compliant. Tools remain granular, access is just optimized.
- ✅ **IV. User-Centric Control**: Compliant. Improves user visibility into system state.
- ✅ **V. Blender-Native Integration**: Compliant. Uses standard Blender UI panels and operators.
- ✅ **VI. Continuous Validation Through Testing**: Compliant. UI logic and backend stability will be verified.

## Project Structure

### Documentation (this feature)

```text
specs/013-chat-ui-improvements/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
└── tasks.md             # Phase 2 output
```

### Source Code (repository root)

```text
blender_addon/
├── ui.py                # Update: Modify draw conditions and render logic
├── operators.py         # Update: Add system messages to chat history
├── __init__.py          # Update: Register/Unregister new properties if needed
└── tests/
    └── test_addon.py    # Update: Verify UI state changes

controller/
├── app/
│   ├── globals.py           # NEW: Singleton for KnowledgeEngine
│   ├── internal_tools.py    # Update: Use direct access instead of HTTP
│   └── main.py              # Update: Initialize globals
```

**Structure Decision**: Introducing `globals.py` in the controller to share the `KnowledgeEngine` instance, breaking the dependency cycle that forced HTTP calls.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Global State (Singleton) | To resolve HTTP deadlock | Passing instance everywhere would require massive refactoring of `main.py` |
