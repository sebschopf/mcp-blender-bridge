# Data Model: Introspection & Recipes

## 1. Bridge Protocol

### 1.1 Bridge Command
Extended to support `get_rna_info`.

```python
class BridgeCommand(BaseModel):
    type: Literal["execute_script", "get_state", "get_rna_info"] # Added get_rna_info
    payload: Dict[str, Any]
```

### 1.2 Bridge Result (RNA Info)
Payload for `get_rna_info` response.

```json
{
  "rna_info": {
    "name": "Primitive Cube Add",
    "description": "Construct a cube mesh",
    "properties": [
      {
        "identifier": "size",
        "name": "Size",
        "type": "FLOAT",
        "description": "Cube size",
        "default": 2.0
      }
    ]
  }
}
```

## 2. Recipe Saving

### 2.1 Save Recipe Input
Arguments for the `save_recipe` tool.

```python
class SaveRecipeRequest(BaseModel):
    name: str = Field(..., description="Name of the recipe")
    description: str = Field(..., description="What the recipe does")
    steps: List[Dict[str, Any]] = Field(..., description="List of steps (operation, params)")
```
