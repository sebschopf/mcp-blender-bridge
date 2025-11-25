# Implementation Plan - Enhanced Addon Chat UI

## 1. Technical Context

**Language/Framework**: Python 3.11+ (Blender Addon), Blender Python API (`bpy`).
**Dependencies**: None new.
**Existing Components**:
- `blender_addon/ui.py`: Contains `MCP_PT_Panel` and basic UI drawing logic.
- `blender_addon/properties.py`: Defines `MCP_ChatHistoryItem` (if not in UI).
- `bpy.context.scene.mcp_chat_history`: Existing CollectionProperty.

**Constraints**:
- Blender UI is immediate mode.
- Limited styling options in standard panels.
- Must work with existing data structures.

## 2. Constitution Check

- [x] **I. Strict MCP Architecture**: UI changes only, no architecture violation.
- [x] **II. Conversational Interface**: Directly enhances this principle.
- [x] **III. Granular & Secure Tools**: N/A.
- [x] **IV. User-Centric Control**: Improves feedback and visibility.
- [x] **V. Blender-Native Integration**: Uses standard Blender UI panels.
- [x] **VI. Continuous Validation**: Integration test included.

## 3. Gates

- [x] **Gate 1: Authorization**: Feature `016-addon-chat-ui` approved.
- [x] **Gate 2: Research**: Blender UI patterns are well-understood.
- [x] **Gate 3: Constitution**: Checked above.

## Phase 0: Outline & Research

### 0.1 Research Tasks
- [x] **Task**: Review `blender_addon/ui.py` to see current implementation.
- [x] **Task**: Confirm `mcp_chat_history` structure.

### 0.2 Output
- **Artifact**: `specs/016-addon-chat-ui/research.md`

## Phase 1: Design & Contracts

### 1.1 Data Model Changes
- No schema changes needed for `MCP_ChatHistoryItem`. It already has `message` (and maybe `source`? Need to check). If `source` is missing, we might parse "You: " / "AI: " or add a field.
- **Decision**: Check if `MCP_ChatHistoryItem` has `role` or `source`. If not, rely on string prefix or add it. Adding a `role` field is cleaner.

### 1.2 API Contract Updates
- No API changes.

### 1.3 Agent Context Update
- Update `blender_addon` context if new UI classes are added.

### 1.4 Output
- **Artifact**: `specs/016-addon-chat-ui/data-model.md` (Updates to `MCP_ChatHistoryItem`).
- **Artifact**: `specs/016-addon-chat-ui/quickstart.md` (Usage guide).

## Phase 2: Implementation

### 2.1 Data Model Update
- **Step 1**: Check `blender_addon/ui.py` (or wherever `MCP_ChatHistoryItem` is).
- **Step 2**: Add `role` EnumProperty ('USER', 'AI', 'SYSTEM') to `MCP_ChatHistoryItem` if not present.

### 2.2 UI Implementation
- **Step 3**: Update `MCP_PT_Panel.draw` in `blender_addon/ui.py`.
- **Step 4**: Implement a loop that draws messages with distinct formatting (e.g., alignment or icons) based on `role`.
- **Step 5**: Limit display to last N messages.

### 2.3 Integration Verification
- **Step 6**: Run the addon and connect.
- **Step 7**: Send a message and verify the UI updates correctly with distinct styles.

### 2.4 Validation
- **Step 8**: Run `run_tests.bat` to ensure no regressions.