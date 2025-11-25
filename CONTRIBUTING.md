# Contributing to MCP Blender 02

Thank you for your interest in contributing to the MCP Blender 02 project! We welcome contributions from everyone.

## Extensible Classification Model Guidelines

This project utilizes an extensible classification model for its capabilities and knowledge base, structured as YAML files within the `controller/capabilities` and `controller/knowledge_base` directories. When adding new tools or recipes, please adhere to the following guidelines:

### 1. Directory Structure

-   **Capabilities (`controller/capabilities`)**: Organize tools into logical subdirectories based on their domain (e.g., `mesh`, `object`, `materials`, `internal`). Each subdirectory can contain one or more YAML files.
    -   Example: `controller/capabilities/mesh/primitives.yaml`
    -   Example: `controller/capabilities/object/transforms.yaml`

-   **Knowledge Base (`controller/knowledge_base`)**: Organize recipes into logical subdirectories based on their category (e.g., `furniture`, `weapons`, `architecture`). Each subdirectory should contain individual YAML files for each recipe.
    -   Example: `controller/knowledge_base/furniture/tables/simple_table.yaml`

### 2. YAML File Structure and Schema

All YAML files must conform to the Pydantic schemas defined in `controller/app/models.py`.

#### a. Capability Files (e.g., `controller/capabilities/mesh/primitives.yaml`)

Each capability YAML file should define one or more top-level categories, each containing a `description` and a list of `tools`.

```yaml
category_name:
  description: "A brief description of this tool category."
  tools:
    - name: "tool.name.here"
      description: "What this tool does."
      params:
        param_name:
          type: "string" # or float, int, bool, list, dict
          description: "Description of the parameter."
          required: true # or false
          default: "default_value" # Optional
```

-   **`category_name`**: A unique, lowercase, snake_case identifier for the category (e.g., `modeling`, `transform`).
-   **`description`**: A clear, concise description of the tools within this category.
-   **`tools`**: A list of tool definitions.
    -   **`name`**: The unique identifier for the tool (e.g., `bpy.ops.mesh.primitive_cube_add`, `materials.set_base_color`). Follow existing naming conventions.
    -   **`description`**: A detailed, user-friendly description of the tool's function. This is crucial for the AI to understand how to use the tool.
    -   **`params`**: (Optional) A dictionary where keys are parameter names and values are their definitions.
        -   **`type`**: The expected Python type of the parameter (e.g., `string`, `float`, `int`, `bool`, `list`, `dict`).
        -   **`description`**: A clear explanation of what the parameter controls.
        -   **`required`**: `true` if the parameter is mandatory, `false` otherwise (defaults to `false`).
        -   **`default`**: (Optional) The default value for the parameter if not provided.

#### b. Recipe Files (e.g., `controller/knowledge_base/furniture/tables/simple_table.yaml`)

Each recipe YAML file should define a single recipe.

```yaml
name: "Recipe Name Here"
category: "category/subcategory"
version: "1.0"
tags: ["tag1", "tag2"] # Optional
description: "A detailed description of what this recipe creates."

parameters: # Optional
  - name: "param_name"
    type: "float"
    description: "Description of recipe parameter."
    default: 1.0

steps:
  - operation: "tool.name.here"
    params: # Optional
      tool_param_name: "value" # Can be a direct value or an injectable parameter like "{{ recipe_param_name }}"
```

-   **`name`**: A unique, human-readable name for the recipe.
-   **`category`**: A hierarchical category path (e.g., `furniture/tables`).
-   **`version`**: The version of the recipe.
-   **`tags`**: (Optional) A list of keywords to help with searching.
-   **`description`**: A detailed explanation of what the recipe creates and its purpose.
-   **`parameters`**: (Optional) A list of parameters that can be passed to the recipe.
    -   **`name`**: The name of the recipe parameter.
    -   **`type`**: The expected Python type.
    -   **`description`**: Description of the recipe parameter.
    -   **`default`**: The default value.
-   **`steps`**: A list of operations (tool calls) that make up the recipe.
    -   **`operation`**: The `name` of a tool defined in the `capabilities/` inventory.
    -   **`params`**: (Optional) A dictionary of parameters for the tool operation. Values can be direct literals or injectable parameters using the `{{ param_name }}` syntax, where `param_name` refers to a parameter defined in the recipe's `parameters` section.

### 3. Code Style and Conventions

-   Follow PEP 8 for Python code.
-   Use clear and descriptive names for files, categories, tools, and parameters.
-   Ensure all new code is covered by appropriate unit and integration tests.

### 4. Testing

-   Before submitting any changes, run `run_tests.bat` to ensure all existing tests pass and your new contributions are validated.

## Token Optimization Strategy

To ensure the system is performant and cost-effective, the AI interacts with the Controller using a two-step tool discovery process.

1.  **Discover Categories**: The AI first calls the `/api/discover_categories` endpoint to get a list of all available tool categories (e.g., `["mesh", "object", "modifiers"]`).
2.  **Discover Tools by Category**: Based on the user's request, the AI determines which categories are relevant and then calls `/api/discover_capabilities?category=<category_name>` to retrieve only the tools for that specific category.

This prevents sending the entire tool library in every request, significantly reducing the token count. When adding new tools, ensure they are placed in a logical and well-named category to support this workflow.

By following these guidelines, we can maintain a consistent, extensible, and robust architecture for the MCP Blender 02 project.