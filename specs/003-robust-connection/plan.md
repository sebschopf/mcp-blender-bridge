# Implementation Plan: Robust Connection Handling

**Feature Branch**: `003-robust-connection`  
**Feature Spec**: `specs/003-robust-connection/spec.md`  
**Status**: In Progress

## 1. Technical Context

### 1.1. High-Level Approach

The implementation will focus entirely on the `blender_addon` component. The core idea is to decouple the user's "Connect" action from the actual HTTP request.

1.  **State Management**: A new state property (e.g., `mcp_connection_status`) will be added to Blender's `Scene` properties. This will track the current state: `DISCONNECTED`, `CONNECTING`, `CONNECTED`.
2.  **UI Update**: The addon's UI panel will be updated to read from this new state property, displaying the appropriate status ("Connecting...", "Connected", etc.) and enabling/disabling buttons accordingly.
3.  **Background Polling**: When the user clicks "Connect", instead of making a blocking HTTP request, the addon will change the state to `CONNECTING` and register a new, dedicated timer function with Blender's `bpy.app.timers`.
4.  **Timer Logic**: This timer will run periodically (e.g., every 3 seconds) in the background. Its sole job is to attempt a single, non-blocking connection to the Controller.
    -   If the connection is successful, it will change the state to `CONNECTED` and unregister itself, stopping the polling.
    -   If the connection fails, it will do nothing, allowing the timer to run again on the next interval.
5.  **Disconnection**: The "Disconnect" button will change the state to `DISCONNECTED` and unregister the connection timer, immediately stopping any further connection attempts.

This approach ensures the Blender UI remains fully responsive while the addon handles connection logic in the background.

### 1.2. Technology Choices

-   **State Management**: `bpy.props` will be used to store the connection state directly within Blender's scene data.
-   **Background Tasks**: `bpy.app.timers` is the standard, non-blocking way to run periodic tasks in Blender without freezing the UI.
-   **HTTP Client**: The existing `requests` library in `mcp_client.py` will be used, but with a short timeout to prevent long freezes on unresponsive servers.

### 1.3. Dependencies & Integrations

-   This feature only modifies the `blender_addon` and has no external dependencies. It will interact with the existing `mcp_client.py` and `ui.py` files.

## 2. Constitution Check

-   [PASS] **IV. User-Centric Control**: This plan enhances user control by providing clearer feedback and allowing the user to cancel connection attempts.
-   [PASS] **V. Blender-Native Integration**: The plan relies entirely on Blender's native APIs (`bpy.props`, `bpy.app.timers`) for its implementation.

**Result**: The plan is in full compliance with the project constitution.

## 3. Phase 0: Research & Prototyping

The technical approach is straightforward and uses standard Blender APIs. No significant research is required.

## 4. Phase 1: Core Design & Contracts

This feature does not introduce new data models or API contracts.

## 5. Phase 2: Implementation Stubs & Scaffolding

-   **State Enum**: Define an `EnumProperty` in `blender_addon/ui.py` for the `mcp_connection_status`.
-   **Timer Function**: Create a new placeholder function `attempt_connection()` in `blender_addon/__init__.py`.
-   **UI Logic**: Update the `draw()` method in `blender_addon/ui.py` to display different text and button states based on the new `mcp_connection_status`.