# Quickstart: Code Quality Tools

## Installation

1.  **Install Dev Dependencies:**
    ```bash
    cd controller
    uv pip install ruff mypy
    ```

## Usage

### Linting
To check for style issues and errors:
```bash
ruff check controller/
```

To automatically fix issues:
```bash
ruff check controller/ --fix
```

### Type Checking
To check for type errors:
```bash
mypy controller/
```

### Testing
Run the full suite to ensure no regressions:
```bash
pytest controller/
```
