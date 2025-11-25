# Implementation Plan - 025-enhanced-logging

**Feature**: Enhanced Debug Logging
**Status**: DRAFT

## Technical Context

### Architecture Overview

This feature introduces structured logging (with precise timestamps and duration tracking) on the server side and configurable request timeouts on the client side to improve diagnosability of performance issues.

**Existing Components:**
- `controller/app/main.py`: Configures basic logging. Needs update to use structured formatting.
- `controller/app/services.py`: Main business logic. Needs to instrument calls with start/end logs.
- `blender_addon/preferences.py`: Stores user settings. Needs new `request_timeout` property.
- `blender_addon/mcp_client.py`: Handles HTTP requests. Needs to use the dynamic timeout.

**New Components:**
- `controller/app/logging_utils.py`: A helper module to provide a `PerformanceLogger` class that simplifies measuring duration and formatting logs consistently (e.g., `[TAG] Message (Duration: X.XXs)`).

### Libraries & Dependencies

- **Python Standard Library**: `time`, `logging`. No new external dependencies.

### Project Structure

```text
controller/
  app/
    logging_utils.py       # New: PerformanceLogger class
    services.py            # Update: Instrument process_message
    gemini_client.py       # Update: Instrument API calls
blender_addon/
  preferences.py         # Update: Add timeout property
  mcp_client.py          # Update: Use timeout property
```

## Constitution Check

### Privacy & Security
- **Data Handling**: Logs will contain timestamps and operation names. User prompt content is already logged (debug level), but we should ensure no PII is added to the structured tags.
- **Safety**: Improved observability allows faster incident response.

### Technical Constraints
- **Performance**: Logging itself must be lightweight.
- **Compatibility**: Blender Addon must handle cases where preferences are not yet initialized (fallback to default timeout).

## Phase 0: Research & Decisions

### Design Decisions

1.  **Log Format**: We will stick to a text-based structured format for readability in the text file, rather than full JSON lines, as it's easier for users to read directly. Format: `[TAG] TIMESTAMP - Message (Duration: Xs)`.
2.  **PerformanceLogger**: A context manager `with PerformanceLogger("TAG", "Message") as pl:` is the cleanest Pythonic way to handle start/end logs and duration calculation automatically.

## Phase 1: Design & Contracts

### Data Model (`data-model.md`)

- **AddonPreferences**: Added `request_timeout` (int, default 60).

### API Changes

- No external API changes.

## Phase 2: Implementation

### Dependencies

- None.

### Strategy

1.  **Server Logging**: Implement `logging_utils.py` first. Then update `services.py` and `gemini_client.py` to use it.
2.  **Client Config**: Update `preferences.py` to add the property.
3.  **Client Logic**: Update `mcp_client.py` to read the property and use it in `requests`.

## Phase 3: Polish

- Verify the logs are readable and timestamps are accurate.