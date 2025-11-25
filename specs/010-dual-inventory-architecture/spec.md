# Feature Specification: Dual Inventory Architecture

**Author**: Gemini AI Agent
**Date**: 2025-11-17
**Version**: 1.0

## 1. Summary

This specification outlines a foundational change to the Controller's architecture, introducing a "Dual Inventory" system. The goal is to drastically improve token efficiency for complex tasks and ensure long-term scalability by separating high-level creative solutions ("Recipes") from low-level atomic operations ("Tools"). This enables the AI to choose the most efficient method for any given task: executing a pre-defined recipe for common objects or assembling a new solution from granular tools for novel or modification requests.

The architecture is composed of four pillars:
1.  **Knowledge Inventory (`knowledge_base/`)**: A structured, hierarchical library of "Recipes" for creating complex objects.
2.  **Capability Inventory (`capabilities/`)**: A refactored, structured library of granular "Tools" representing atomic Blender operations.
3.  **Knowledge & Resource Engine**: A set of meta-tools enabling the AI to search, execute, and learn new recipes, supported by a resource management system.
4.  **Extensible Classification Model**: A clear set of guidelines for organizing both inventories to ensure logical and consistent growth.

## 2. User Scenarios & Testing

### Scenario 1: High-Efficiency Creation via Recipe

-   **Given** an artist wants to create a common but complex object.
-   **When** the artist prompts the AI: "Create a medieval dagger."
-   **Then** the AI searches the Knowledge Inventory for a matching recipe.
-   **And** it finds and executes the `dagger_medieval` recipe with a single command in its Action Plan.
-   **And** a complete, textured dagger appears in the Blender scene.

### Scenario 2: Granular Modification of an Existing Object

-   **Given** a dagger object already exists in the scene.
-   **When** the artist prompts the AI: "Now, engrave the name 'Merlin' onto the blade."
-   **Then** the AI searches the Knowledge Inventory for an "engrave" recipe and finds none.
-   **And** it switches to the Capability Inventory to build a multi-step Action Plan using granular tools (e.g., `text.create_3d`, `object.transform`, `object.modifiers.apply_boolean`).
-   **And** the name "Merlin" is visibly engraved onto the dagger's blade.

### Scenario 3: Learning and Saving a New Recipe

-   **Given** the AI has just created a novel object, like a car seat, using a 25-step granular Action Plan.
-   **When** the user is satisfied with the result and prompts: "This is a great car seat, save it for later."
-   **Then** the AI uses the `knowledge.save_recipe` meta-tool.
-   **And** it provides the 25-step Action Plan, a proposed name ("car_seat_standard"), and suggests a category (`vehicles/components`).
-   **And** a new `car_seat_standard.yaml` file is created in the `knowledge_base/vehicles/components/` directory, ready for future use.

## 3. Functional Requirements

### FR-001: Directory Structure
-   The Controller MUST contain three new root directories:
    1.  `knowledge_base/`: For recipe files.
    2.  `capabilities/`: For granular tool files.
    3.  `resources/`: For external assets.

### FR-002: Hierarchical Inventories
-   Both `knowledge_base/` and `capabilities/` MUST support a hierarchical structure of nested subdirectories for semantic classification (e.g., `knowledge_base/weapons/medieval/`, `capabilities/mesh/editing/`).

### FR-003: Recipe Schema
-   A recipe MUST be a YAML file containing a root object with the following keys:
    -   `name` (string, required): Human-readable name.
    -   `category` (string, required): The semantic path where the file is located (e.g., `weapons/medieval`).
    -   `version` (string, required): Semantic version (e.g., `1.0`).
    -   `tags` (list of strings, optional): Searchable keywords.
    -   `description` (string, required): A brief explanation of the recipe.
    -   `parameters` (list of objects, optional): A list of input variables the AI can control, each with `name`, `type`, `description`, and `default`.
    -   `steps` (list of objects, required): A sequence of granular tool calls that constitute the recipe.

### FR-004: Capability Schema
-   A capability file MUST be a YAML file containing a root object where each key is a category name (e.g., `primitives`, `editing`).
-   Each category MUST contain a list of `tools`, where each tool has a `name`, `description`, and `params`, mirroring the current `capabilities.yaml` structure.

### FR-005: Knowledge Engine Meta-Tools
-   The Controller MUST expose a new `knowledge` tool category to the AI with the following tools:
    -   `knowledge.search_recipes(query: str)`: Searches recipe metadata and returns a list of matching recipe names.
    -   `knowledge.execute_recipe(name: str, params: dict)`: Executes the `steps` from a named recipe, substituting any provided `params`.
    -   `knowledge.save_recipe(name: str, category: str, steps: list, ...)`: Creates a new recipe YAML file in the specified category within the `knowledge_base`.

### FR-006: Resource Management
-   The `resources/` directory MUST be structured with subdirectories for asset types (e.g., `fonts/`, `textures/`, `hdri/`).
-   Tools requiring external assets (e.g., `text.create_3d`) MUST accept a resource filename (e.g., `font_name: "LiberationSans-Regular.ttf"`) as a parameter.

### FR-007: Extensible Classification Model
-   The project MUST include a document (`CONTRIBUTING.md` or similar) that defines the guidelines for naming and organizing new categories and files within both inventories to ensure consistency.

## 4. Success Criteria

-   **Token Efficiency**: A complex creation task that previously took >20 steps (e.g., creating a detailed object) can now be accomplished with a single `knowledge.execute_recipe` step, achieving a >95% reduction in Action Plan length for known objects.
-   **System Scalability**: The Controller's startup time MUST NOT increase by more than 50% after loading and indexing 500 individual recipe and capability files.
-   **Architectural Extensibility**: A developer can add a new suite of granular tools (e.g., for sculpting) by adding a single new YAML file in the `capabilities/` directory, without any changes to the core Controller code.
-   **AI Learning Loop**: The AI can successfully use granular tools to create a novel object and then use `knowledge.save_recipe` to persist it, and subsequently re-create the object using `knowledge.execute_recipe`.

## 5. Assumptions

-   The initial implementation will focus on creating the architectural framework. The population of the inventories with a comprehensive set of recipes and tools will be an ongoing, incremental process covered by future features.
-   The `knowledge.save_recipe` tool will initially save the exact sequence of steps. The ability for the AI to automatically parameterize a saved recipe is a future enhancement.
-   The classification model will be enforced by developer convention and documentation, not by a programmatic linter in its first version.