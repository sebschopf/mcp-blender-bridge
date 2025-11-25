# Data Model: YAML Capabilities Management

## 1. Pydantic Validation Schemas

To ensure the integrity of the `capabilities.yaml` file, the following Pydantic models will be used for validation upon loading. These will be defined in a new file, `controller/config/schema.py`.

```python
from pydantic import BaseModel, Field
from typing import Dict, List, Any

class ParameterDefinition(BaseModel):
    type: str
    description: str
    required: bool = False
    default: Any = None

class ToolDefinition(BaseModel):
    name: str
    description: str
    params: Dict[str, ParameterDefinition] = Field(default_factory=dict)

class CategoryDefinition(BaseModel):
    description: str
    tools: List[ToolDefinition]

class CapabilitiesSchema(BaseModel):
    modeling: CategoryDefinition
    transform: CategoryDefinition
    materials: CategoryDefinition
    # Future categories can be added here
```

## 2. `capabilities.yaml` Structure

The `capabilities.yaml` file will be the source of truth for the MCP's capabilities. It must conform to the schema defined by the Pydantic models above.

### Example Structure

```yaml
# controller/config/capabilities.yaml

modeling:
  description: "Tools for creating new primitive geometries."
  tools:
    - name: "bpy.ops.mesh.primitive_cube_add"
      description: "Adds a cube to the scene."
      params:
        size:
          type: "float"
          description: "The size of the cube."
          default: 1.0
        location:
          type: "tuple"
          description: "Initial position of the cube."
          default: [0, 0, 0]

transform:
  description: "Tools for moving, rotating, and scaling objects."
  tools:
    - name: "bpy.ops.transform.translate"
      description: "Moves the selected object."
      params:
        value:
          type: "tuple"
          description: "Translation vector [x, y, z]."
          required: true

# ... other categories ...
```
