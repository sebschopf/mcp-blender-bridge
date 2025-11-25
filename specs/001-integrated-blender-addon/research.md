# Research: Integrated Blender Addon

**Objective**: Resolve the key unknowns identified in the implementation plan to ensure a robust and testable solution for managing the MCP server from within Blender.

## 1. Subprocess Management in Blender

-   **Unknown**: What is the best practice for managing a long-running, non-blocking subprocess (the FastAPI server) from within a Blender addon?
-   **Research Task**: "Investigate methods for launching and managing a Python subprocess from Blender's embedded Python environment, ensuring the UI remains responsive."

### Investigation & Findings

-   **`subprocess` module**: Python's standard `subprocess` module is available in Blender's Python. `subprocess.Popen` is the non-blocking call to start a process.
-   **Process Lifecycle**: The key challenge is ensuring the subprocess is reliably terminated when Blender closes or the addon is disabled. Blender's `atexit` module can be used to register a cleanup function. The `bpy.app.handlers.persistent` decorator can also be used for functions that should run on events like file load or Blender exit.
-   **Finding the Python Executable**: The addon needs to start the server using the *same* Python environment as the controller. Hardcoding paths is brittle. A better approach is to have a configuration setting in the addon's preferences where the user can specify the path to the controller's Python executable (e.g., `controller/.venv/Scripts/python.exe`).
-   **Passing API Key**: Using environment variables (`os.environ`) is a secure way to pass the API key from the addon (which reads it from preferences) to the server subprocess.

### Decision

1.  The `server_manager.py` module will use `subprocess.Popen` to start the FastAPI server. The `creationflags` parameter will be used on Windows to prevent a console window from appearing.
2.  The process handle returned by `Popen` will be stored in a global variable within the addon.
3.  A cleanup function will be registered with the `atexit` module. This function will check if the process handle exists and, if so, call `process.terminate()` to stop the server. This ensures cleanup on Blender exit.
4.  The addon preferences will include a `StringProperty` for the user to set the path to the controller's Python executable. This makes the addon more portable.
5.  The API key will be read from preferences and passed as an environment variable to the `Popen` call.

## 2. Testing Strategy for a Blender Addon

-   **Unknown**: How can we write automated tests for a Blender addon, covering UI, operators, and process management?
-   **Research Task**: "Design a testing strategy for the Blender addon that can be run automatically."

### Investigation & Findings

-   **Headless Blender**: Blender can be run in a headless mode (without a GUI) using the `-b` command-line flag. This is the standard way to run automated tests.
-   **Testing Frameworks**: While it's possible to use standard Python frameworks like `pytest`, integrating them with the Blender environment can be complex. A simpler, effective approach for this project is to write a dedicated test script that is executed by headless Blender.
-   **Test Script Logic**: The test script (`test_addon.py`) will be a standard Python script that uses `bpy`. It will:
    1.  Enable the addon (`bpy.ops.preferences.addon_enable`).
    2.  Set the necessary preferences (API key, path to python).
    3.  Call the operators (`bpy.ops.mcp.start_server()`, `bpy.ops.mcp.stop_server()`).
    4.  Use Python's `psutil` library (which can be installed into Blender's Python) to check if the server process was actually started and stopped.
    5.  Assert conditions to verify success or failure.
-   **Running the Test**: A batch script (`run_tests.bat` or similar) can be created to orchestrate the test run. It will call `blender -b --python /path/to/test_addon.py`.

### Decision

1.  A new `tests/` directory will be created inside the `blender_addon` directory.
2.  A test script, `test_addon.py`, will be created. This script will contain the logic to enable the addon, configure it, and test its core functionality (starting/stopping the server).
3.  The tests will be designed to be run inside a headless Blender instance.
4.  The `psutil` library will be used to verify that the server process is correctly managed. This will be a dependency for running the tests.
5.  The project's main `run_tests.bat` will be updated to include a step that executes the addon tests in headless Blender. This integrates addon testing into the project's main CI/validation workflow.
