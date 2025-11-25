# Tasks: UI Chat Improvements

> **Feature**: 023-ui-chat-improvements
> **Status**: In Progress

## Phase 1: Setup
- [x] T001 Analyze existing tooltips in `blender_addon/operators.py` and list missing ones (mental or scratchpad) <!-- id: 0 -->

## Phase 2: Foundational
- [x] T002 Implement `draw_multiline_label` helper function in `blender_addon/ui.py` using `textwrap` module <!-- id: 1 -->
- [x] T003 Update `MCP_PT_Panel.draw` in `blender_addon/ui.py` to use `draw_multiline_label` for chat history items <!-- id: 2 -->

## Phase 3: User Story 1 - Responsive Chat Display (P1)
**Goal**: Chat messages wrap correctly within the N-Panel.
**Independent Test**: Resize panel and verify text reflows without truncation.
- [x] T004 [US1] Refine `draw_multiline_label` to attempt dynamic width calculation based on `context.region.width` if possible, or tune default char width <!-- id: 3 -->
- [x] T005 [US1] Verify chat history display with long messages manually in Blender <!-- id: 4 -->

## Phase 4: User Story 2 - Comprehensive Tooltips (P2)
**Goal**: All UI elements have descriptive tooltips.
**Independent Test**: Hover over all buttons/fields and verify descriptions.
- [x] T006 [US2] Add `bl_description` to `WM_OT_MCP_Connect` in `blender_addon/operators.py` <!-- id: 5 -->
- [x] T007 [US2] Add `bl_description` to `WM_OT_MCP_Disconnect` in `blender_addon/operators.py` <!-- id: 6 -->
- [x] T008 [US2] Add `bl_description` to `WM_OT_MCP_Send_Chat` in `blender_addon/operators.py` <!-- id: 7 -->
- [x] T009 [US2] Add `bl_description` to `WM_OT_MCP_OpenLog` in `blender_addon/operators.py` <!-- id: 8 -->
- [x] T010 [US2] Verify tooltips manually in Blender <!-- id: 9 -->

## Phase 5: Polish
- [x] T011 Run `run_blender_tests.ps1` to ensure no regressions in addon loading <!-- id: 10 -->
