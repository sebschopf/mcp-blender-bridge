# Research: Dynamic Tool Retrieval (RAG)

## 1. Unknowns & Clarifications

### 1.1 Search Implementation (TF-IDF vs Keywords)
- **Question**: How to implement an efficient search for tools without external dependencies like heavy vector DBs?
- **Findings**: 
    - `TF-IDF` (Term Frequency-Inverse Document Frequency) is robust for keyword matching but requires `scikit-learn` (heavy dependency).
    - `BM25` is a standard improvement over TF-IDF, lighter implementations exist.
    - `Simple Keyword Matching`: Checking if query words exist in tool tags/descriptions. Fast but lacks ranking/nuance.
- **Decision**: **In-memory TF-IDF or a custom weighted keyword scorer**.
    - *Why*: We want better relevance than simple boolean matching but avoid heavy ML libs.
    - *Approach*: A simple inverted index mapping words to tools + a scoring function (e.g., term overlap count weighted by field importance: Name > Tags > Description).

### 1.2 Dynamic Tool Loading in MCP
- **Question**: Does the `mcp` SDK support changing the list of available tools during a session?
- **Findings**:
    - The standard `tools/list` capability returns a static list. However, the MCP host (Gemini) can call `tools/list` periodically or when prompted.
    - **Crucial Constraint**: We can't "force" Gemini to refresh its tool list easily mid-turn.
    - **Solution**: We don't change the *exposed* tools constantly. We expose **FIXED meta-tools**:
        1. `search_tools(query)`: Returns text descriptions of relevant tools.
        2. `execute_command(tool_name, params)`: A generic executor.
    - *Refinement*: Can we let Gemini call the tool directly?
        - If `search_tools` returns the *signature* of `mesh.create_cube`, Gemini can't call it *via MCP* if `mesh.create_cube` isn't in the initial `tools/list`.
        - **Therefore**: We MUST use the `execute_command` wrapper OR register thousands of tools (which defeats the purpose).
        - **Wait**: If we register thousands of tools but provide *minimal* descriptions in `tools/list` (just name + "See search"), does that save tokens? No, the names alone for 2000 tools is too much.
        - **Verdict**: **Generic Executor approach**. `execute_command` will take the tool name (found via search) and its parameters.

### 1.3 Tool Metadata Structure
- **Question**: What data do we need for the index?
- **Decision**:
    - `name`: Unique ID (e.g., `mesh.create_cube`)
    - `label`: Human readable name
    - `description`: Full description (for indexing, not initial context)
    - `tags`: Categories/Keywords
    - `signature`: JSON schema of params (returned by search, used by AI to form `execute_command` payload).

## 2. Technology Choices

### 2.1 Search Engine
- **Choice**: Custom In-Memory Inverted Index.
- **Reason**: Zero extra dependencies, fast for < 10k items, sufficient for "exact/fuzzy keyword" matching.

### 2.2 Execution Pattern
- **Pattern**: Search -> Execute Wrapper.
- **Flow**:
    1. User: "Make a chair"
    2. AI: `search_tools("chair")` -> Returns `[{"name": "mesh.create_cube", "desc": "...", "params": {...}}]`
    3. AI: `execute_command("mesh.create_cube", {"size": 2})`
    4. Controller: Validates & Executes.

## 3. Architecture

### 3.1 Components
1.  **ToolIndex**: Class in `knowledge_engine.py`. Builds index on startup. Methods: `search(query) -> List[Tool]`.
2.  **Meta-Tools**: Defined in `mcp_server.py`.
    - `search_tools`: Proxies to `ToolIndex.search`.
    - `execute_command`: Validates tool existence, validates params against schema, sends to Bridge.
3.  **Gemini Client**: Updates system prompt to explain this workflow ("You have a search tool. Use it first.").

### 3.2 Security
- `execute_command` must rigorously validate that the requested `tool_name` exists in the allowed capabilities and that `params` match the schema (Pydantic validation). It must not execute arbitrary Python.

## 4. Migration Steps
1.  Update `KnowledgeEngine` to build the index.
2.  Implement `ToolIndex` logic.
3.  Update `mcp_server.py` to expose ONLY the meta-tools (plus essential navigation).
4.  Update Gemini system prompt.
