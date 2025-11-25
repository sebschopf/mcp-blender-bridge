# Feature Specification: Dynamic Tool Retrieval (RAG)

**Feature Branch**: `018-dynamic-tool-retrieval`
**Created**: 2025-11-23
**Status**: Draft
**Input**: Implement a RAG (Retrieval-Augmented Generation) system for MCP Tools to support a massive Blender tool library without token explosion.

## User Scenarios & Testing

### User Story 1 - AI-Driven Tool Discovery (Priority: P1)

The AI, when faced with a user request, searches for relevant tools instead of having them all pre-loaded.

**Why this priority**: P1. This is the core mechanism that enables scaling to thousands of tools. Without it, the context window limits are a hard blocker.

**Independent Test**: Can be fully tested by starting a session with a minimal context, asking a vague question like "create a chair", and verifying that the AI successfully finds and calls `mesh.create_cube` via the search tool.

**Acceptance Scenarios**:

1. **Given** an AI session with no pre-loaded Blender tools (except `search_tools`), **When** the user asks "Make a chair", **Then** the AI calls `search_tools("create object")` or similar.
2. **Given** the search results return `mesh.create_cube`, **When** the AI decides to use it, **Then** the AI executes the tool successfully (either by `execute_command` or a dynamically loaded tool).

---

### User Story 2 - Massive Tool Indexing (Priority: P2)

The system maintains a searchable index of all available Blender tools, including metadata like descriptions and keywords.

**Why this priority**: P2. Essential for the search mechanism to work effectively across a large dataset.

**Independent Test**: Can be tested by adding a dummy tool to the capabilities YAML and verifying it appears in search results for relevant keywords.

**Acceptance Scenarios**:

1. **Given** a capabilities library with 500+ tools, **When** the system starts, **Then** a lightweight index is built in memory (or loaded).
2. **Given** a search query "rotate", **When** `search_tools` is called, **Then** it returns relevant rotation tools sorted by relevance.

---

### Edge Cases

- **No results found**: What happens when `search_tools` returns nothing? The AI should be able to rephrase its query or inform the user.
- **Ambiguous queries**: Search "add" might return too many results. The search tool needs to limit the number of returned items to avoid flooding the context.
- **Token limits on search results**: Ensure the search results themselves don't exceed context limits.

## Requirements

### Functional Requirements

- **FR-001**: The `KnowledgeEngine` MUST build a searchable index of all tools defined in the `capabilities` directory at startup.
- **FR-002**: The index MUST support keyword-based search (e.g., TF-IDF or simple inclusion) using tool names, descriptions, and tags.
- **FR-003**: The system MUST expose a `search_tools(query: str)` tool to the AI via MCP.
- **FR-004**: `search_tools` MUST return a limited list of tool summaries (name, description, usage signature) to conserve tokens.
- **FR-005**: The system MUST provide a mechanism for the AI to execute a tool found via search. *Decision: Use a generic `execute_command(tool_name, params)` wrapper tool to avoid dynamic MCP tool registration complexities.*
- **FR-006**: The default toolset exposed to the AI MUST be minimal (e.g., `search_tools`, `execute_command`, `get_scene_state`).

### Key Entities

- **ToolMetadata**: Lightweight representation of a tool for the index (name, description, tags, signature).
- **ToolIndex**: The data structure holding the searchable metadata.

## Success Criteria

### Measurable Outcomes

- **SC-001**: The initial context sent to the AI (system prompt + tool definitions) is < 2000 tokens, regardless of the total library size.
- **SC-002**: When asking for a common operation (e.g., "create cube"), the AI successfully executes it in < 3 turns (User Request -> Search -> Execute).
- **SC-003**: Token usage per request remains O(1) relative to the total number of tools in the library (i.e., adding 1000 tools doesn't increase token usage for a simple "hello" message).
- **SC-004**: Search queries return relevant results in under 200ms.

## Assumptions

- We are using the official `mcp` Python SDK.
- We are not using a heavy vector database (e.g., Pinecone, Chroma) yet; a simple in-memory TF-IDF or keyword match is sufficient for the MVP.
- The AI model (Gemini) is capable of understanding the "Search -> Execute" workflow via system instructions.