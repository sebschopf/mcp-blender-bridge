# Research: Dual Inventory Architecture

**Objective**: Determine the most efficient and robust strategy for loading, parsing, and indexing a large number of YAML files from the `capabilities/` and `knowledge_base/` directories at application startup.

## 1. Core Problem

The Controller needs to scan two directory trees for YAML files, read them, validate their contents against Pydantic schemas, and store them in an in-memory data structure for fast access during runtime. Doing this naively (e.g., a simple recursive walk and load) could lead to slow startup times as the number of files grows.

## 2. Key Research Questions

1.  **Loading Strategy**: What is the most performant way to discover and read many small files in Python? (e.g., `os.walk`, `glob.glob`, `pathlib.rglob`)
2.  **Parsing & Validation**: Can we optimize the PyYAML parsing and Pydantic validation loop? Is there a benefit to using `CBaseLoader` over the standard `SafeLoader`?
3.  **Caching**: Should we implement a caching mechanism? For instance, create a single "index" file (e.g., in JSON or Pickle format) that is regenerated only when a change in the YAML files is detected.

## 3. Investigation & Findings

### Loading Strategy

-   **`os.walk`**: Generally considered the fastest for deep directory traversal. It is implemented in C and is very efficient.
-   **`pathlib.rglob`**: More modern and Pythonic, but known to be slightly slower than `os.walk` for very large numbers of files. The difference is likely negligible for our target of ~500-1000 files.
-   **Decision**: `pathlib.rglob` is the preferred choice. It offers better readability and a more modern API, and the minor performance difference is not critical for our scale.

### Parsing & Validation

-   **PyYAML Loaders**: `CBaseLoader` (if `libyaml` is installed) provides a significant performance boost (up to 5-10x) over the pure Python `SafeLoader`. We should use it where available and fall back gracefully.
-   **Pydantic Validation**: Validation is inherently CPU-bound. The most effective optimization is to validate once at startup and then rely on the validated models. For bulk loading, `pydantic.TypeAdapter` can be more efficient for validating lists of models compared to instantiating each model individually in a loop.
-   **Decision**: The loading process should attempt to use `yaml.CBaseLoader` and fall back to `yaml.SafeLoader`. We will use a `pydantic.TypeAdapter` to validate the lists of tools and recipes loaded from the files.

### Caching Mechanism

-   **Concept**:
    1.  On startup, get the last modification times of all `.yaml` files in the inventory directories.
    2.  Compare these timestamps against a stored manifest file (e.g., `index.json`).
    3.  If no files have changed, load the pre-processed `index.json` directly, bypassing all YAML parsing and validation. This would be extremely fast.
    4.  If any file has changed, perform the full scan/parse/validate process and then overwrite the `index.json` with the new, validated data.
-   **Complexity**: This adds significant complexity to the startup logic (cache validation, potential race conditions, etc.).
-   **Decision**: A caching mechanism is a premature optimization. We will start with a direct "load-all-at-startup" approach. If and only if startup time becomes a noticeable problem (i.e., exceeds the 50% degradation target), we will implement caching as a separate performance enhancement feature.

## 4. Final Technical Decisions

-   **File Discovery**: Use `pathlib.Path.rglob('**/*.yaml')` for its modern API and sufficient performance.
-   **YAML Parsing**: Use `yaml.load(stream, Loader=yaml.CBaseLoader)` if available, otherwise `yaml.SafeLoader`.
-   **Validation**: Use Pydantic models as the single source of truth for schema. Use `TypeAdapter` for validating collections.
-   **Caching**: Defer implementation. The initial approach will be a full reload on every startup.
