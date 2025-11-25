# Feature Specification: Easy Installer for Blender Addon

**Feature Branch**: `002-easy-installer`  
**Created**: 2025-11-16  
**Status**: Draft  
**Input**: User description: "Le MCP est pas mal. Pas encore testé car compliqué à mettre en place. Il faut donc le rendre plus facile à configurer. Genre, on clic sur un fichier, cela l'ouvre et on entre les informations adéquate. Ou en tout cas il faut que cela soit plus simple."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Automated Addon Installation (Priority: P1)

A non-technical Blender user wants to install the Gemini MCP addon. They run a single, simple installer file. The installer automatically finds their Blender installation directory and copies the addon files to the correct location, then informs them of the success.

**Why this priority**: This is the core of the user's request. It removes the main friction point of manual installation.

**Independent Test**: A user can run the installer, and the "Gemini MCP Integration" addon appears in Blender's addon preferences without any manual file copying.

**Acceptance Scenarios**:

1. **Given** a standard Blender installation on Windows, **When** the user executes the installer file, **Then** the `blender_addon` directory is copied into the correct Blender scripts/addons folder.
2. **Given** the installation is successful, **When** the user opens Blender and navigates to `Edit > Preferences > Add-ons`, **Then** the "Gemini MCP Integration" addon is listed and can be enabled.
3. **Given** Blender is not found in standard locations, **When** the user runs the installer, **Then** a message is displayed informing the user that Blender could not be found and providing instructions for manual installation.

---

### User Story 2 - Guided API Key Configuration (Priority: P2)

A user has just installed the addon and now needs to configure the Controller with their Gemini API key. The installer script prompts them to enter their API key.

**Why this priority**: This removes the second major configuration hurdle, which is creating and editing the `.env` file manually.

**Independent Test**: After running the installer and providing an API key, the `controller/.env` file is created with the correct `GEMINI_API_KEY` value.

**Acceptance Scenarios**:

1. **Given** the addon has been successfully copied, **When** the installer prompts for the Gemini API key, **Then** the user can paste their key into the prompt.
2. **Given** the user has entered their API key, **When** the installation completes, **Then** the `controller/.env` file exists and contains the line `GEMINI_API_KEY="THE_USER_PROVIDED_KEY"`.
3. **Given** the user chooses to skip entering an API key, **When** the installation completes, **Then** the `controller/.env` file is still created but contains a placeholder value, e.g., `GEMINI_API_KEY="YOUR_API_KEY_HERE"`.

### Edge Cases

- **Multiple Blender Installations**: If multiple Blender versions are found, the script MUST list all detected versions and prompt the user to select which one(s) to install the addon to.
- **Pre-existing `.env` file**: The installer MUST check if a `GEMINI_API_KEY` is already set in `controller/.env`. If it is not, the installer will ask the user if they have a key. If they don't, it will provide instructions on how to obtain one before prompting for input.
- **Permissions**: The user might not have the necessary permissions to write to the Blender addons directory. The script should detect this, report the error gracefully, and suggest running the installer as an administrator.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST provide a single, executable installer file (`.exe`) for Windows users.
- **FR-002**: The installer MUST automatically search for Blender installation directories in standard locations on Windows (e.g., Program Files, AppData).
- **FR-003**: The installer MUST copy the entire `blender_addon` directory to the detected Blender `scripts/addons` directory.
- **FR-004**: The installer MUST prompt the user to enter their Gemini API key.
- **FR-005**: The installer MUST create or update a `.env` file in the `controller` directory with the provided API key.
- **FR-006**: The installer MUST display clear, user-friendly messages indicating its progress, success, or any errors encountered.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 95% of non-technical users can successfully install and configure the addon using the installer in under 2 minutes, without needing to manually copy files or edit configuration files.
- **SC-002**: The installer reduces the number of manual setup steps from (currently ~10) to 2 (run installer, paste API key).
- **SC-003**: Support requests related to installation and initial setup are reduced by 80%.