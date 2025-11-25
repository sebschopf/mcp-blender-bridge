# Research & Decisions: Easy Installer

This document records the key research findings and decisions made during the planning phase for the easy installer feature.

## 1. Detecting Blender Installations on Windows

-   **Decision**: The installer will search for Blender installations in the following standard locations:
    1.  `%PROGRAMFILES%\Blender Foundation`
    2.  `%LOCALAPPDATA%\Blender Foundation`
    3.  The Steam library location for Blender, by checking the registry key `HKEY_CURRENT_USER\Software\Valve\Steam` for `SteamPath` and then searching `SteamPath\steamapps\common\Blender`.
-   **Rationale**: These locations cover the most common installation methods for Blender on Windows (official installer, portable versions, and Steam). This multi-pronged approach maximizes the chances of automatically finding the user's installation.
-   **Alternatives Considered**:
    -   **Asking the user for the path**: This is a fallback option if no installations are found automatically, but the goal is to avoid this to keep the process simple.
    -   **Searching the entire file system**: This would be extremely slow and inefficient.

## 2. Packaging with PyInstaller

-   **Decision**: The installer will be packaged as a single executable using the `--onefile` flag in PyInstaller. The build process will be managed by a simple batch script.
-   **Rationale**:
    -   `--onefile` creates a single, easy-to-distribute `.exe` file, which is the most user-friendly option.
    -   A batch script (`build_installer.bat`) simplifies the build process for developers, ensuring consistent builds.
-   **Alternatives Considered**:
    -   **cx_Freeze**: Another popular packaging tool, but PyInstaller is generally considered more mature and has better support for a wide range of libraries.
    -   **Nuitka**: Compiles Python to C code for better performance, but is more complex to set up and overkill for a simple installer script.

## 3. User Interface Library

-   **Decision**: The installer will use Python's standard `input()` and `print()` functions for all user interaction. No external CLI libraries will be used.
-   **Rationale**: For a simple, sequential series of prompts, standard library functions are sufficient and avoid adding unnecessary dependencies to the project. This keeps the final executable as small as possible.
-   **Alternatives Considered**:
    -   **`rich` or `click`**: These libraries provide more advanced features like colored text, progress bars, and complex command parsing. While powerful, they are not necessary for this installer and would increase the final file size.
