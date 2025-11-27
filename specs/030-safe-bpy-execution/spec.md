# Feature Specification: Safe BPY Execution

**Feature Branch**: `030-safe-bpy-execution`  
**Created**: 2025-11-27  
**Status**: Implemented  
**Input**: Generated Python Scripts

## User Scenarios & Testing

### User Story 1 - Prevent Malicious Code Injection (Priority: P1)

As a user, I want to ensure that the AI cannot execute arbitrary system commands (like deleting files or accessing the network) so that my computer remains safe.

**Why this priority**: Critical security requirement.

**Independent Test**:
- Attempt to execute a script with `import os` or `os.system(...)`.
- The system must reject it with a security error.

**Acceptance Scenarios**:

1. **Given** a script with `import bpy`, **When** executed, **Then** it runs successfully.
2. **Given** a script with `import os`, **When** executed, **Then** it is rejected.
3. **Given** a script with `eval(...)`, **When** executed, **Then** it is rejected.
4. **Given** a script accessing `__builtins__`, **When** executed, **Then** it is rejected.

## Requirements

### Functional Requirements

- **FR-001**: The system MUST validate all generated Python scripts before execution.
- **FR-002**: The validation MUST use an AST (Abstract Syntax Tree) parser to analyze the code structure.
- **FR-003**: The system MUST enforce a **whitelist** of allowed modules (`bpy`, `math`, `mathutils`, `bmesh`, `gpu`, `random`, `typing`, `enum`).
- **FR-004**: The system MUST explicitly **ban** dangerous functions (`eval`, `exec`, `open`, `__import__`, `getattr`, `setattr`, `delattr`).
- **FR-005**: The system MUST explicitly **ban** access to internal attributes (`__builtins__`, `__globals__`, `__subclasses__`, `__class__`).

## Success Criteria

### Measurable Outcomes

- **SC-001**: 100% of scripts containing `import os` or `subprocess` are blocked.
- **SC-002**: Legitimate Blender scripts (using `bpy`) are not blocked.
