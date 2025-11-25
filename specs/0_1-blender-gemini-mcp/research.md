# Research & Decisions: Blender-Gemini MCP Integration

This document records the key research findings and decisions made during the planning phase.

## 1. Controller-Peripheral Communication

-   **Decision**: Use a standard RESTful API over HTTP for communication. The Blender Addon will be the client, polling the Controller for new commands.
-   **Rationale**:
    -   HTTP is a well-understood, universal protocol.
    -   Using a client-polling model is simpler to implement and more robust for the Blender environment than trying to maintain a persistent WebSocket connection, which can be complex within Blender's event loop.
    -   FastAPI is purpose-built for creating REST APIs quickly and efficiently.
-   **Alternatives Considered**:
    -   **WebSockets**: Would provide real-time, bidirectional communication but adds significant complexity to the Blender addon, especially regarding connection management and error handling.
    -   **gRPC**: Offers high performance but requires protobuf definitions and more complex client/server setup, which is overkill for this project's needs.

## 2. Blender Addon UI

-   **Decision**: The addon will create a new tab in Blender's "N-Panel" (the sidebar in the 3D View). This panel will contain the connection status, a connect/disconnect button, a simple chat history log, and a text input field for the user's prompt.
-   **Rationale**:
    -   The N-Panel is the standard location for addon UIs in Blender, making it familiar and non-intrusive for users.
    -   Blender's UI toolkit (`bpy.types.Panel`) provides all the necessary components to build this interface natively.
-   **Alternatives Considered**:
    -   **Floating Modal**: A separate pop-up window could be used, but this is less integrated and can disrupt the user's workflow.

## 3. Handling Blender's Undo System

-   **Decision**: The addon will register an `undo_post` handler with Blender's application handlers (`bpy.app.handlers`). When the user triggers an undo, this handler will fire, sending a notification to the Controller (e.g., `POST /api/event/undo`). The Controller will then be responsible for attempting to rewind its state to match.
-   **Rationale**: This is the most robust and user-friendly approach. It leverages Blender's native event system to keep the Controller's state in sync with the user's actions, preventing errors that would arise from state desynchronization.
-   **Alternatives Considered**:
    -   **Ignoring Undo**: This was rejected as it would lead to a poor user experience, where the AI would be unaware of changes in the scene, causing subsequent commands to fail or behave unexpectedly.
