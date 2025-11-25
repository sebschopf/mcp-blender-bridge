# Data Model: Dynamic Tool Retrieval

## 1. Tool Indexing

### 1.1 ToolMetadata
Lightweight structure for the search index.

```python
class ToolMetadata(BaseModel):
    name: str
    label: str
    description: str
    tags: List[str]
    category: str
    # The full schema is stored in the main KnowledgeEngine registry, 
    # this lightweight model is for search ranking.
```

### 1.2 Tool Search Result
What the AI sees when it calls `search_tools`.

```python
class ToolSearchResult(BaseModel):
    name: str
    description: str
    usage: str # e.g. "create_cube(size=1.0)" - A compact signature hint
    match_reason: str # Debug info (e.g. "Matched tag 'chair'")
```

## 2. Execution

### 2.1 Generic Execution Payload
Input for `execute_command`.

```python
class ExecuteCommandRequest(BaseModel):
    tool_name: str = Field(..., description="The exact name of the tool to execute (e.g., 'mesh.create_cube')")
    params: Dict[str, Any] = Field(default_factory=dict, description="Parameters for the tool")
```

## 3. Updated Knowledge Engine

### 3.1 Inverted Index Structure
```python
# Mapping: Token -> Set of Tool Names
index: Dict[str, Set[str]] = {
    "cube": {"mesh.create_cube", "mesh.bevel"},
    "create": {"mesh.create_cube", "mesh.create_sphere"},
    ...
}
```
