# MCP Blender Developer Guide

This guide is for developers who want to contribute to the MCP Blender project, extend its capabilities, or understand its codebase.

## Project Structure

The project is organized into the following main directories:

*   **`controller/`**: The Python-based MCP Server.
    *   `app/`: Main application logic (FastAPI).
    *   `capabilities/`: YAML definitions of low-level tools.
    *   `knowledge_base/`: YAML definitions of high-level recipes.
    *   `resources/`: Static assets.
*   **`blender_addon/`**: The Blender Addon source code.
    *   `__init__.py`: Addon entry point.
    *   `operators.py`: Blender operators.
    *   `panels.py`: UI panels.
    *   `client.py`: HTTP client for communicating with the Controller.
*   **`installer_build/`**: Scripts and assets for building the Windows installer.
*   **`specs/`**: Design documents and specifications.
*   **`tests/`**: Integration tests.

## Extending Capabilities

The core of the system is the "Dual Inventory" of tools. You can add new features by creating or modifying YAML files.

### Adding a Low-Level Tool (Capability)

1.  **Identify the Category**: Decide which category the tool belongs to (e.g., `mesh`, `material`, `transform`).
2.  **Create/Edit YAML**: Navigate to `controller/capabilities/<category>/`. Create a new YAML file or edit an existing one.
3.  **Define the Tool**:
    ```yaml
    category_name:
      description: "Description of the category"
      tools:
        - name: "my.new.tool"
          description: "What the tool does."
          params:
            param1:
              type: "string"
              description: "Description of param1"
              required: true
    ```
4.  **Implement Logic**: Ensure the corresponding logic exists in the Blender Addon (usually mapping `my.new.tool` to a `bpy.ops` call).

### Adding a Recipe (Knowledge Base)

Recipes allow you to combine multiple tools into a single action.

1.  **Identify the Category**: Navigate to `controller/knowledge_base/<category>/`.
2.  **Create YAML**: Create a new file (e.g., `my_recipe.yaml`).
3.  **Define the Recipe**:
    ```yaml
    name: "My Recipe"
    category: "furniture/chairs"
    steps:
      - operation: "mesh.create_cube"
        params:
          size: 2.0
      - operation: "transform.translate"
        params:
          z: 1.0
    ```

## Development Workflow

1.  **Environment**:
    *   Set up the `controller` environment as described in the User Guide.
    *   Install the addon in Blender in "Dev Mode" (linking to the source folder if possible, or reinstalling on change).

2.  **Running Tests**:
    *   **Controller**: Run `run_tests.bat` in the root directory.
    *   **Addon**: Testing the addon often requires running it inside Blender or mocking `bpy`. See `blender_addon/tests/` for examples.

3.  **Linting**:
    *   Use `ruff check .` and `ruff format .` in the `controller` directory to maintain code quality.

## Debugging

*   **Controller Logs**: Check the terminal where `uvicorn` is running. It shows all incoming requests and errors.
*   **Blender Console**: Window > Toggle System Console. This shows print statements from the addon and Python errors within Blender.
*   **MCP Inspector**: You can use the MCP Inspector tool (if available/configured) to inspect the MCP protocol messages.

## Contributing

Please refer to `CONTRIBUTING.md` for detailed contribution guidelines, including pull request processes and coding standards.
