# Quickstart: Blender-Gemini MCP Integration

This guide provides the basic steps to get the development environment up and running.

## Prerequisites

-   Python 3.10+
-   Blender 3.0+
-   An API key for the Google Gemini API

## 1. Controller Setup (FastAPI Server)

1.  **Clone the repository** (if you haven't already).
2.  **Navigate to the `controller` directory** (this will be created in the implementation phase).
    ```bash
    cd controller
    ```
3.  **Create a virtual environment**:
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```
4.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
5.  **Set up environment variables**:
    Create a `.env` file in the `controller` directory and add your Gemini API key:
    ```
    GEMINI_API_KEY="YOUR_API_KEY_HERE"
    ```
6.  **Run the server**:
    ```bash
    uvicorn main:app --reload
    ```
    The Controller will now be running at `http://127.0.0.1:8000`.

## 2. Peripheral Setup (Blender Addon)

1.  **Navigate to the `blender_addon` directory** (this will be created in the implementation phase).
2.  **Install the addon in Blender**:
    -   Open Blender.
    -   Go to `Edit > Preferences > Add-ons`.
    -   Click "Install..." and navigate to the `blender_addon` directory. Select the `.zip` file of the addon (or the main `.py` file).
    -   Enable the "Gemini MCP Integration" addon.
3.  **Connect to the Controller**:
    -   In the 3D View, press `N` to open the sidebar.
    -   Find the "Gemini MCP" tab.
    -   Click the "Connect" button.
    -   The status should change to "Connected", and you can now start typing prompts in the chat box.
