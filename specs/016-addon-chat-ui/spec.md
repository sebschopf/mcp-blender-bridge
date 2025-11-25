# Specification: Enhanced Addon Chat UI

## 1. Overview

### 1.1 Goal
Improve the user experience of the Blender Addon by creating a dedicated, readable chat interface directly within Blender. This update aims to provide a clear history of the conversation with the AI (Gemini), making it easier to follow the context and verify actions. Additionally, this feature verifies the end-to-end integration with the recently migrated `google-genai` library on the controller side.

### 1.2 Core Value
- **Usability**: A clear chat window prevents users from getting lost in the interaction loop.
- **Visibility**: Users can see exactly what the AI is "thinking" or outputting, beyond just the final Blender action.
- **Confidence**: Verifying the integration with the new SDK ensures the core value proposition (AI controlling Blender) remains functional.

### 1.3 Success Criteria
- [ ] A dedicated panel in the Blender UI displays the chat history.
- [ ] Chat history clearly distinguishes between "User" and "AI" messages (e.g., using prefixes or distinct formatting if possible in Blender UI).
- [ ] The UI supports scrolling or limits displayed messages to the most recent N to avoid clutter (e.g., last 50 messages).
- [ ] Users can type and send messages from this new UI.
- [ ] The addon successfully connects to the Controller running the new `google-genai` implementation.
- [ ] A full "round trip" (User Request -> Controller -> Gemini -> Action Plan -> Blender Execution) works and is reflected in the UI.

## 2. User Stories

### 2.1 As a 3D Artist
I want to see a clear log of my conversation with the AI
So that I can understand why it performed certain actions or if it misunderstood my request.

**Acceptance Criteria:**
- A panel in the 3D Viewport (N-panel) shows a list of messages.
- User messages are labeled (e.g., "You: ...").
- AI messages are labeled (e.g., "AI: ...").
- The layout is clean and readable.

### 2.2 As a System Integrator
I want to verify the addon works with the updated backend
So that I can confirm the migration to the new Google GenAI SDK didn't break the client-server contract.

**Acceptance Criteria:**
- Sending a message triggers a response from the Controller.
- No "404 Not Found" or connection errors occur during standard usage.
- The connection status indicator in the UI accurately reflects the server state.

## 3. Functional Requirements

### 3.1 Chat UI Implementation
- **FR 3.1.1**: Update `blender_addon/ui.py` to refine the `MCP_PT_Panel`.
- **FR 3.1.2**: Use a `UIList` or a custom drawing loop to render `context.scene.mcp_chat_history` items.
- **FR 3.1.3**: Ensure the chat input field (`mcp_chat_input`) is prominently displayed below the history.
- **FR 3.1.4**: Auto-scroll or display the *last* messages by default (Blender UI draws top-down, so ensuring the newest messages are visible is key).

### 3.2 Integration Verification
- **FR 3.2.1**: Manually verify the connection handshake.
- **FR 3.2.2**: Verify message sending and receipt via the `mcp_client`.

## 4. Technical Considerations

### 4.1 Blender UI Constraints
- Blender's standard UI (`bpy.types.Panel`) is static. Dynamic scrolling lists usually require `UIList`. However, for a simple chat log, iterating over a slice of the collection (e.g., `[-10:]`) in the `draw` method is a simpler and often sufficient approach for an N-panel.
- Text wrapping in Blender UI boxes (`layout.box()`) works automatically for `label(text=...)` if width permits, but long text can sometimes be cut off. Using `layout.label` multiple times or `layout.row().label` might be needed.

### 4.2 Data Persistence
- Chat history is stored in `bpy.context.scene.mcp_chat_history` (CollectionProperty). This is temporary per session (runtime) but persists as long as the file is open (or saved, if we don't exclude it). It should ideally be cleared or managed per session.

## 5. Assumptions
- The Controller is running and accessible on `localhost:8000`.
- The `mcp_chat_history` PropertyGroup already exists (from previous features). We are refining its display.

## 6. Out of Scope
- Advanced UI features like rich text (bold/italics) inside Blender (very hard to do in standard API).
- Saving chat history to disk.