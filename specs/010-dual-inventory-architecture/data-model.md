# Data Model: Dual Inventory Architecture

This document defines the data structures for the `capabilities` and `knowledge_base` inventories. These structures will be enforced by Pydantic models within the Controller for validation at startup.

## 1. Capability Inventory (`capabilities/`)

The `capabilities/` directory contains YAML files that define the granular tools available to the AI.

### `CapabilityFile` Schema

Each YAML file in this inventory represents a collection of tools grouped under one or more categories.

**Example**: `capabilities/mesh/primitives.yaml`
```yaml
# Defines primitive creation tools
primitives:
  description: "Tools for creating basic geometric shapes."
  tools:
    - name: "mesh.create_cube"
      description: "Creates a new cube mesh at the 3D cursor."
      params:
        size:
          type: "float"
          description: "The size of the cube."
          default: 1.0
        location:
          type: "list"
          description: "The (x, y, z) coordinates for the cube's origin."
          default: [0, 0, 0]

    - name: "mesh.create_sphere"
      # ...
```

### Pydantic Models (Conceptual)

```python
class ToolParameter(BaseModel):
    type: str
    description: str
    required: bool = False
    default: Any | None = None

class Tool(BaseModel):
    name: str
    description: str
    params: dict[str, ToolParameter] = {}

class ToolCategory(BaseModel):
    description: str
    tools: list[Tool]

# A CapabilityFile is a dictionary of categories
# Example: dict[str, ToolCategory]
```

## 2. Knowledge Inventory (`knowledge_base/`)

The `knowledge_base/` directory contains YAML files that define high-level recipes.

### `RecipeFile` Schema

Each YAML file in this inventory represents a single, complete recipe.

**Example**: `knowledge_base/weapons/medieval/dagger.yaml`
```yaml
name: "Medieval Dagger"
category: "weapons/medieval"
version: "1.0"
tags: ["weapon", "blade", "medieval", "dagger"]
description: "Creates a simple medieval-style dagger with a blade, crossguard, and handle."

parameters:
  - name: "blade_length"
    type: "float"
    description: "The length of the dagger blade."
    default: 0.3
  - name: "handle_material"
    type: "str"
    description: "The name of the material to apply to the handle."
    default: "DarkWood"

steps:
  - operation: "mesh.create_cube"
    params:
      name: "Blade"
  - operation: "transform.resize"
    params:
      object_name: "Blade"
      value: [0.05, "{{ blade_length }}", 0.01] # Parameters are injectable
  # ... more steps to create the full dagger
```

### Pydantic Models (Conceptual)

```python
class RecipeParameter(BaseModel):
    name: str
    type: str
    description: str
    default: Any

class RecipeStep(BaseModel):
    operation: str
    params: dict[str, Any] = {}

class Recipe(BaseModel):
    name: str
    category: str
    version: str
    tags: list[str] = []
    description: str
    parameters: list[RecipeParameter] = []
    steps: list[RecipeStep]
```

## 3. Resource Inventory (`resources/`)

This directory does not have a data model as it simply stores asset files. The structure is a simple hierarchy of folders, for example:
- `resources/fonts/LiberationSans-Regular.ttf`
- `resources/textures/metal/scratched_metal.png`
