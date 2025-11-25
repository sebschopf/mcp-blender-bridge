# Feature Specification: Blender-Gemini MCP Integration

**Feature Branch**: `001-blender-gemini-mcp`  
**Created**: 2025-11-16  
**Status**: Draft  
**Input**: User description: "Construit moi le projet qui permet d'avoir un MCP pour Blender et Gemini avec un Addon dans Blender qui écoute sur une adresse ip et un fichier qui une fois ouvert permet de réceptionner l'Addon dans Blender. Je veux dans mon projet une fois le fichier ouvert et connecté à l'addon pouvoir parler à Gemini et lui demander de me créer des choses avec Blender. Il se connecte au MCP pour traduir en BPY à l'addon et après, Blender construit la demande. Bien sur il y a plein d'étape avant pour valider la demande. C'est donc un dialogue avec Gemini pour établir les bonnes lignes de code et les bons outils à utiliser pour créer la demande initiale. Il faut bien sur respecter les conseil https://www.anthropic.com/engineering/code-execution-with-mcp"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Connect Blender to the MCP (Priority: P1)

A Blender artist wants to connect their Blender instance to the Gemini-powered MCP to enable AI-driven 3D modeling. They open a provided file that establishes the connection to the MCP Controller, which is listening on a specific network address.

**Why this priority**: This is the foundational step. Without a connection, no other functionality is possible.

**Independent Test**: The Blender Addon successfully registers and shows a "Connected" status to the MCP Controller. The Controller logs the connection from the Blender Peripheral.

**Acceptance Scenarios**:

1. **Given** the MCP Controller is running and listening, **When** the user opens the specific `.blend` file or activates the addon in Blender, **Then** the addon establishes a persistent connection to the Controller.
2. **Given** the MCP Controller is not running, **When** the user tries to connect from Blender, **Then** the addon displays an error message indicating the connection failed.

---

### User Story 2 - Generate a Simple Object via Conversation (Priority: P2)

A user wants to create a simple 3D object. They type a natural language prompt like "create a red cube" into the chat interface provided by the system. Gemini engages in a dialogue to clarify requirements (e.g., "What size should the cube be?"), translates the final request into a secure tool call, and sends it through the MCP for Blender to execute.

**Why this priority**: This demonstrates the core end-to-end workflow of the system: converting natural language to a 3D object through a secure, conversational process.

**Independent Test**: A user can type a simple command, answer clarifying questions, and see the corresponding object appear in their Blender scene.

**Acceptance Scenarios**:

1. **Given** Blender is connected to the MCP, **When** the user enters the prompt "make me a house", **Then** the Gemini model responds with clarifying questions like "What kind of house? What material should it be made of?".
2. **Given** the user has clarified their request for a "1-meter wooden cube", **When** they confirm the action, **Then** the MCP Controller sends a `create_cube(size=1, material='wood')` command to the Blender Addon, and a wooden cube appears in the scene.
3. **Given** the user provides an ambiguous prompt, **When** the system asks for clarification, **Then** the system does not execute any modeling actions until the user provides a clear and confirmed instruction.

---

### User Story 3 - Execute a Multi-Step Creation (Priority: P3)

A designer wants to create a slightly more complex scene, like "put a cone on top of a cylinder". The system must be able to break this down into multiple, sequential tool calls and execute them in the correct order.

**Why this priority**: This builds on the single-object generation by introducing planning and state management, which is crucial for more advanced tasks.

**Independent Test**: The user can issue a multi-part request, and the system correctly sequences the operations to produce the final desired scene in Blender.

**Acceptance Scenarios**:

1. **Given** Blender is connected and the scene is empty, **When** the user requests "place a sphere on a cube", **Then** the system first creates a cube at the origin, then creates a sphere positioned correctly on top of the cube's upper face.
2. **Given** an object already exists in the scene, **When** the user asks to modify it (e.g., "make the cube blue"), **Then** the system correctly identifies the target object and applies the modification.

### Edge Cases

- **Connection Loss**: If the connection between the Blender Addon (Peripheral) and the MCP Controller is lost, the addon must detect this, notify the user, and attempt to reconnect automatically.
- **Invalid Commands**: If the AI Model or Controller generates a command that is malformed or not recognized by the Blender Addon's toolset, the addon must reject the command and log an error without crashing.
- **User Undo**: If the user undoes an action in Blender (Ctrl+Z), the addon MUST attempt to detect this and inform the MCP Controller, which will then try to synchronize its internal state to reflect the change. This ensures consistency between Blender's scene and the AI's understanding.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST be composed of three distinct components: an AI Model (Gemini), a Controller, and a Peripheral (Blender Addon).
- **FR-002**: The Blender Addon (Peripheral) MUST listen for commands on a pre-defined network address and port.
- **FR-003**: The Controller MUST expose a secure set of tools to the AI model. These tools MUST NOT allow for arbitrary code execution.
- **FR-004**: The AI Model MUST use a conversational interface to clarify user requests before generating tool calls.
- **FR-005**: The Controller MUST validate all tool calls received from the AI model before translating them into `bpy` commands for the Peripheral.
- **FR-006**: The system MUST provide a chat-like interface for the user to interact with the AI Model.
- **FR-007**: The Blender Addon MUST only execute commands from its predefined, secure toolset.
- **FR-008**: The connection mechanism MUST be initiated by the user clicking a "Connect" button within the Blender Addon's user interface.

### Key Entities

- **User Prompt**: The natural language text input provided by the user.
- **Clarification Dialogue**: The conversational exchange between the AI and the user to refine the prompt.
- **Tool Call**: A structured, secure command generated by the AI Model (e.g., `{ "tool": "create_cube", "parameters": { "size": 2, "material": "glass" } }`).
- **BPY Command**: The low-level Blender Python script command translated by the Controller and executed by the Peripheral.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A user can successfully generate a primitive 3D shape (e.g., cube, sphere) using a natural language prompt within 5 conversational turns.
- **SC-002**: The system must prevent 100% of attempts to execute arbitrary, non-tool-based Python code sent from the AI model.
- **SC-003**: The time from user confirmation of a clarified prompt to the object appearing in Blender must be less than 2 seconds for simple primitive shapes.
- **SC-004**: 95% of users must be able to establish a successful connection between Blender and the MCP on their first attempt without consulting documentation.