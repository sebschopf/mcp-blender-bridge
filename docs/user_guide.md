# MCP Blender User Guide

Welcome to the MCP Blender User Guide! This document will help you install, configure, and use the Gemini-powered AI assistant in Blender.

## Installation

### Method 1: Easy Installer (Windows)

The easiest way to get started on Windows is to use the provided installer.

1.  **Download/Locate the Installer**:
    *   Navigate to the `installer_build` directory in the project folder.
    *   Find `mcp_installer.exe`.

2.  **Run the Installer**:
    *   Double-click `mcp_installer.exe`.
    *   Follow the on-screen prompts.
    *   You will be asked to select your Blender executable (usually `C:\Program Files\Blender Foundation\Blender 4.x\blender.exe`).
    *   You will also be asked to provide your Google Gemini API Key.

3.  **Finish**:
    *   The installer will set up the necessary environment and configuration.

### Method 2: Manual Installation

If you prefer to set things up manually or are on a different operating system:

#### Prerequisites
*   Blender 4.0 or higher.
*   Python 3.11+ installed on your system.
*   A Google Gemini API Key.

#### Steps

1.  **Controller Setup**:
    *   Open a terminal in the `controller` directory.
    *   Create a virtual environment: `python -m venv .venv`
    *   Activate it: `.venv\Scripts\activate` (Windows) or `source .venv/bin/activate` (Mac/Linux).
    *   Install dependencies: `pip install -r requirements.txt` (or use `uv` if available).
    *   Create a `.env` file in `controller/` and add: `GEMINI_API_KEY=your_api_key_here`.

2.  **Blender Addon Setup**:
    *   Open Blender.
    *   Go to `Edit > Preferences > Add-ons`.
    *   Click `Install...` and navigate to the `blender_addon.zip` file (or the `blender_addon` folder if not zipped).
    *   Enable the "Gemini MCP Integration" addon.

## Configuration

Once installed, you can configure the addon within Blender:

1.  Go to `Edit > Preferences > Add-ons`.
2.  Search for "Gemini MCP".
3.  Expand the addon details.
4.  **API Key**: Ensure your API Key is set here if you didn't set it in the `.env` file.
5.  **Model**: Click "Refresh Models" to load available Gemini models. Select your preferred model (e.g., `gemini-1.5-pro`).

## Usage

### Connecting

1.  **Start the Server**:
    *   If you used the installer, there might be a shortcut or batch file to start the server.
    *   Manually: Run `uvicorn app.main:app --reload` in the `controller` directory.
2.  **Connect in Blender**:
    *   Open the 3D Viewport.
    *   Press `N` to open the sidebar.
    *   Click on the **Gemini MCP** tab.
    *   Click the **Connect** button. You should see a "Connected" status.

### Chatting with Gemini

1.  In the **Gemini MCP** tab, you will see a chat interface.
2.  Type your request in the input box.
    *   *Example: "Create a grid of 10x10 cubes."*
    *   *Example: "Make a red material and apply it to the selected object."*
    *   *Example: "Create a simple table."*
3.  Press **Enter** or click **Send**.
4.  Gemini will process your request, determine the necessary tools, and execute them in Blender.
5.  You will see the actions taking place in the 3D Viewport.

### Using Recipes

You can ask Gemini to save a sequence of actions as a "Recipe" for later use.

*   *Example: "That table looks great. Save it as a recipe called 'Modern Coffee Table'."*

Next time, you can simply ask:
*   *Example: "Create a Modern Coffee Table."*

## Troubleshooting

*   **"Connection Failed"**: Ensure the Controller server is running and listening on the correct port (default: 8000). Check the terminal output for errors.
*   **"API Key Invalid"**: Double-check your Google Gemini API Key in the Addon Preferences or `.env` file.
*   **Actions not appearing**: Make sure you are in the correct mode (Object Mode) and the viewport is updated.
