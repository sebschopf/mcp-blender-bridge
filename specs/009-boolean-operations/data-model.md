# Data Model: Boolean Operations

This feature extends the `capabilities.yaml` file with new tools for object selection and boolean modification.

## 1. `capabilities.yaml` Extension

The following tools will be added to the `capabilities.yaml` file.

```yaml
# In the 'scene' category
    - name: "object.select_by_name"
      description: "Selects a single object by its unique name, making it the active object. This is crucial for targeting operations."
      params:
        object_name:
          type: "str"
          description: "The name of the object to select (e.g., 'Cube', 'Sphere.001')."
          required: true

# In a new 'object' or existing 'modifiers' category
    - name: "object.apply_boolean"
      description: "Performs a boolean operation (engrave, weld) on the active object using another object as a tool. The tool object is consumed and deleted after the operation."
      params:
        target_object_name:
          type: "str"
          description: "The name of the object to use as the 'tool' for the operation."
          required: true
        operation:
          type: "str"
          description: "The type of boolean operation: 'DIFFERENCE' (to engrave/subtract), 'UNION' (to weld/join), or 'INTERSECT'."
          required: true
```
