# Quickstart: Chat UI Improvements (Test Guide)

This guide validates the new chat interface responsiveness and backend stability.

## 1. Immediate Visibility Test

1.  **Open Blender** and the "Gemini MCP" panel.
2.  **Click "Connect"**.
3.  **Observe Immediately**: The chat box (history area) and input field should appear **instantly**, even while the status says "Connecting...". You should NOT have to wait for the "Connected" state.

## 2. System Messages Test

1.  **Connect**: Click "Connect".
2.  **Observe History**: You should see a message: `System: Connecting...` appearing immediately.
3.  **Wait for Connection**: Once connected, you should see: `System: Connected. Waiting for AI...`.
4.  **Disconnect**: Click "Disconnect".
5.  **Connect Again**: The history should clear and start fresh.

## 3. Empty State Test

1.  **Connect**: Click "Connect".
2.  **If History Empty**: If no messages have been exchanged yet (and before the system message appears), you might see "Waiting for instructions..." (though system messages usually appear fast).
3.  **Clear History (Simulated)**: If you restart Blender and connect, and for some reason no system message was injected (bug test), you should see "Waiting for instructions..." instead of an empty grey box.

## 4. Backend Stability Test (Deadlock Check)

1.  **Connect** to the MCP.
2.  **Send Command**: Type "Create a red cube" and press Send.
3.  **Monitor**: Watch the server log or system console.
4.  **Success**: The AI should reply (e.g., "Plan submitted") and the cube should appear.
5.  **Failure**: If the chat hangs on "Starting dynamic AI conversation..." and a timeout error appears in the log after ~5s, the deadlock fix failed.