# Quickstart: Easy Installer

This guide provides the basic steps for developers to run the installer script and package it into a standalone executable.

## Prerequisites

-   Python 3.10+
-   `pyinstaller` package (`pip install pyinstaller`)

## 1. Running the Installer Script Directly

This is useful for testing and development.

1.  **Navigate to the `installer` directory** (this will be created in the implementation phase).
    ```bash
    cd installer
    ```
2.  **Run the script**:
    ```bash
    python install.py
    ```
    The script will execute in your terminal, and you can interact with the prompts directly.

## 2. Building the Executable (`.exe`)

This packages the script into a single file for distribution to end-users.

1.  **Navigate to the project root directory**.
2.  **Run the build script** (this will be created in the implementation phase):
    ```bash
    build_installer.bat
    ```
3.  **Find the executable**:
    -   PyInstaller will create a `dist` directory.
    -   Inside `dist`, you will find `install.exe`. This is the standalone installer that can be shared with users.
