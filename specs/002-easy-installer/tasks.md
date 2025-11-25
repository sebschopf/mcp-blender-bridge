# Implementation Tasks: Easy Installer

**Feature Branch**: `002-easy-installer`  
**Feature Spec**: `specs/002-easy-installer/spec.md`  
**Implementation Plan**: `specs/002-easy-installer/plan.md`  
**Created**: 2025-11-16

## Phase 1: Setup & Project Initialization

- [X] T001 Create `installer/` directory for the installer script
- [X] T002 Create `installer/install.py` with a main function and placeholder functions
- [X] T003 Create `build_installer.bat` with a basic `pyinstaller` command
- [X] T004 Add `pyinstaller` to a new `installer/requirements.txt`

## Phase 2: Foundational Components (Blocking Prerequisites)

- [X] T005 [P] Implement `find_blender_installations()` in `installer/install.py` to search Program Files, AppData, and Steam directories
- [X] T006 [P] Implement `prompt_for_blender_version()` in `installer/install.py` to handle user selection if multiple versions are found
- [X] T007 [P] Implement `copy_addon_files()` in `installer/install.py` to copy the `blender_addon` directory
- [X] T008 [P] Implement `configure_api_key()` in `installer/install.py` to handle `.env` file creation and API key input
- [X] T009 [P] Implement basic command-line output for user feedback (e.g., "Searching for Blender...", "Addon installed successfully.") in `installer/install.py`

## Phase 3: User Story 1 - Automated Addon Installation (P1)

**Goal**: A user can run a single installer file to automatically find their Blender installation and copy the addon files.
**Independent Test**: Running the installer successfully copies the `blender_addon` folder to the correct Blender addons directory.

- [X] T010 [US1] Integrate `find_blender_installations()` and `prompt_for_blender_version()` into the main installer flow in `installer/install.py`
- [X] T011 [US1] Integrate `copy_addon_files()` into the main installer flow in `installer/install.py`
- [X] T012 [US1] Add error handling for when no Blender installations are found in `installer/install.py`
- [X] T013 [US1] Add error handling for file copy permission errors in `installer/install.py`, suggesting to run as administrator

## Phase 4: User Story 2 - Guided API Key Configuration (P2)

**Goal**: The installer guides the user through configuring their Gemini API key.
**Independent Test**: After running the installer, the `controller/.env` file is correctly populated with the user's API key.

- [X] T014 [US2] Integrate `configure_api_key()` into the main installer flow in `installer/install.py`
- [X] T015 [US2] Implement logic to check for an existing `GEMINI_API_KEY` in `controller/.env` in `installer/install.py`
- [X] T016 [US2] Implement prompts to ask the user if they have a key and provide instructions if they don't in `installer/install.py`

## Phase 5: Polish & Cross-Cutting Concerns

- [X] T017 Refine all user-facing messages for clarity and simplicity in `installer/install.py`
- [X] T018 Update `build_installer.bat` to use the `--onefile` flag and specify an output directory
- [X] T019 Add comments and docstrings to `installer/install.py`
- [X] T020 Update the main `README.md` to include instructions for using the new `install.exe`

## Dependencies

- Phase 1 must be completed before Phase 2.
- Phase 2 must be completed before Phase 3 and Phase 4.
- User Story 1 (Phase 3) should be completed before User Story 2 (Phase 4) for a logical user flow.
- Phase 5 can be addressed after the core functionality is complete.

## Parallel Execution Examples

- **After Phase 1**: 
    - T005, T006, T007, and T008 can be developed in parallel as they are independent functions within the same script.

## Implementation Strategy

1.  **MVP**: Complete Phase 1, 2, and 3 to create a functional installer that handles the addon copying.
2.  **Configuration**: Implement Phase 4 to add the guided API key setup.
3.  **Finalization**: Complete Phase 5 to polish the script and build process.
