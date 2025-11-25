# Research: Dynamic Model Discovery

**Feature**: `012-dynamic-model-discovery`
**Date**: vendredi, 21 novembre 2025

## Decisions

### Model Discovery API
- **Decision**: Use `google.generativeai.list_models()` on the controller side.
- **Rationale**: This is the official SDK method to retrieve models accessible by the current API key. It allows filtering by supported generation methods (we need `generateContent`).
- **Alternatives**: Hardcoding list (rejected: high maintenance, brittle), scraping docs (rejected: unreliable).

### Environment Variable Fallback
- **Decision**: Check `os.environ.get("GEMINI_API_KEY")` in `preferences.py` ONLY if the `api_key` property is empty string.
- **Rationale**: Prioritizes user-configured key while allowing zero-config for power users. Standard practice for CLI/dev tools.

### Data Persistence
- **Decision**: Store the `available_models` list as a simple string list in the addon's runtime state (or a hidden StringProperty if persistence across sessions is needed, but runtime fetch is fresher). For the dropdown, we'll use a dynamic `items` callback in `EnumProperty`.
- **Rationale**: `EnumProperty(items=callback)` allows dynamic population. We will cache the list in a global variable or window manager property to avoid fetching on every UI redraw.

## Technical Unknowns Resolved

- **Q**: How to filter models?
- **A**: Iterate through `genai.list_models()` and check if `generateContent` is in `m.supported_generation_methods`. Also check if it supports tool calling (though most recent ones do).

- **Q**: How to update Blender UI asynchronously?
- **A**: Use a thread for the network request (handled by `requests` or `urllib`) and a callback or timer to update the UI/property when done. Since `requests` is blocking, running it in the main thread freezes Blender. We will use a `threading.Thread` that updates a global/scene property, and Blender's UI will pick it up on next redraw (force redraw with `tag_redraw`).
