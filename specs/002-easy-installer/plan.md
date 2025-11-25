# Implementation Plan: Easy Installer

**Feature Branch**: `002-easy-installer`  
**Feature Spec**: `specs/002-easy-installer/spec.md`  
**Status**: In Progress

## 1. Technical Context

### 1.1. High-Level Approach

The project will be a command-line application written in Python, packaged into a single executable (`.exe`) for Windows using PyInstaller. The script will guide the user through a series of prompts to locate their Blender installation and configure the Gemini API key.

The installer will perform the following steps:
1.  **Detect Blender Installations**: Scan standard Windows directories to find all installed Blender versions.
2.  **User Selection**: If multiple versions are found, prompt the user to choose which one(s) to install the addon to.
3.  **Copy Addon Files**: Copy the `blender_addon` directory from the project's root to the selected Blender version's `scripts/addons` folder.
4.  **Configure API Key**: Check for the existence of `controller/.env` and a `GEMINI_API_KEY`. If not found, prompt the user for their key and create/update the file.
5.  **Provide Feedback**: Display clear success or error messages to the user.

### 1.2. Technology Choices

-   **Installer Scripting**: Python 3.10+. It provides the necessary libraries for file system operations, user input, and environment variable management.
-   **Executable Packaging**: PyInstaller. This tool will bundle the Python script and its dependencies into a single, standalone `.exe` file, removing the need for the user to have Python installed.
-   **User Interface**: Standard command-line interface (CLI) using Python's built-in `input()` and `print()` functions.

### 1.3. Dependencies & Integrations

-   **External**:
    -   `PyInstaller`: To package the Python script into an executable.
-   **Internal**:
    -   The installer script will need to be aware of the project's directory structure to locate the `blender_addon` and `controller/.env` files.

## 2. Constitution Check

This plan is checked against the principles defined in `.specify/memory/constitution.md`.

-   [PASS] **I. Strict MCP Architecture**: This feature is a utility for the existing architecture and does not modify it.
-   [PASS] **II. Conversational Interface**: The installer uses a conversational CLI, which aligns with the principle of user interaction.
-   [PASS] **III. Granular & Secure Tools**: Not directly applicable, but the installer does not introduce any new security risks.
-   [PASS] **IV. User-Centric Control**: The installer prompts the user for choices (Blender version, API key), keeping them in control of the process.
-   [PASS] **V. Blender-Native Integration**: The installer's goal is to correctly place the addon for native integration.

**Result**: The plan is in full compliance with the project constitution.

## 3. Phase 0: Research & Prototyping

Research will focus on the specifics of finding Blender installations on Windows and packaging with PyInstaller.

**Outputs**:
-   `specs/002-easy-installer/research.md`

## 4. Phase 1: Core Design & Contracts

This feature is a standalone script and does not have a data model or API contracts in the traditional sense. The "contract" is the command-line interface presented to the user.

### 4.1. Quickstart Guide

Provides instructions for developers on how to run the installer script and package it into an executable.

**Outputs**:
-   `specs/002-easy-installer/quickstart.md`

### 4.2. Agent Context Update

The project's core technologies will be updated in the agent's context.

## 5. Phase 2: Implementation Stubs & Scaffolding

This phase involves creating the main installer script file and the PyInstaller build script.

-   **Installer Script**:
    -   Create `installer/install.py`.
    -   Implement placeholder functions for `find_blender_installations()`, `prompt_for_blender_version()`, `copy_addon_files()`, `configure_api_key()`.
-   **Build Script**:
    -   Create `build_installer.bat` to run PyInstaller with the correct options to generate the `.exe`.