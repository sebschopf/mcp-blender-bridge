# Data Model: Extended Modeling Tools

This feature extends the `capabilities.yaml` file with five new tools for advanced object manipulation.

## 1. `capabilities.yaml` Extension

The following tools will be added to the `capabilities.yaml` file.

### New Category: `object`

A new category will be created for object-level operations that are not strictly transforms or modifiers.

```yaml
object:
  description: "Tools for managing and manipulating whole objects, such as renaming or joining."
  tools:
    - name: "object.rename"
      description: "Renames the currently active object. Crucial for scene organization."
      params:
        new_name:
          type: "str"
          description: "The new, unique name for the object."
          required: true

    - name: "object.select_multiple"
      description: "Selects multiple objects by their names. The last object in the list becomes the active object."
      params:
        object_names:
          type: "list"
          description: "A list of the names of the objects to select (e.g., ['Cube', 'Sphere.001'])."
          required: true

    - name: "object.join"
      description: "Merges all currently selected objects into the active object. This is a destructive operation for the other selected objects."
      params: {}
```

### Updates to `modifiers` Category

```yaml
modifiers:
  description: "Tools for applying non-destructive modifications to an object's geometry."
  tools:
    # ... existing modifiers ...
    - name: "object.apply_bevel"
      description: "Adds and applies a Bevel modifier to the active object to round its edges."
      params:
        width:
          type: "float"
          description: "The width of the bevel effect."
          default: 0.1
        segments:
          type: "int"
          description: "The number of segments in the bevel, controlling its smoothness."
          default: 1

    - name: "object.apply_subsurf"
      description: "Adds and applies a Subdivision Surface modifier to smooth the object's geometry."
      params:
        levels:
          type: "int"
          description: "The number of subdivision levels to apply in the viewport."
          default: 1
```
