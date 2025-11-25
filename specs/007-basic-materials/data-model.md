# Data Model: Basic Material Capabilities

This feature extends the `capabilities.yaml` file with new tools for material manipulation.

## 1. New Helper Module

Because material manipulation in modern Blender requires interacting with node trees, it's too complex for single-line `bpy` commands. A new helper module will be implicitly created to contain this logic, and the capabilities will call functions from this module.

## 2. `capabilities.yaml` Extension

The `materials` category in `controller/config/capabilities.yaml` will be populated with the following tools. These names correspond to helper functions that will be created.

```yaml
materials:
  description: "Tools for creating and modifying object materials."
  tools:
    - name: "materials.create_and_assign"
      description: "Creates a new material and assigns it to the active object. If a material with the same name exists, it will be reused."
      params:
        material_name:
          type: "str"
          description: "The name for the new material."
          required: true

    - name: "materials.set_base_color"
      description: "Sets the base color of the active object's material. Assumes a Principled BSDF shader."
      params:
        color:
          type: "tuple"
          description: "The color as an RGBA tuple (e.g., [0.8, 0.1, 0.1, 1.0])."
          required: true

    - name: "materials.set_metallic"
      description: "Sets the metallic value of the active object's material. Assumes a Principled BSDF shader."
      params:
        value:
          type: "float"
          description: "The metallic value, from 0.0 (non-metal) to 1.0 (fully metallic)."
          required: true

    - name: "materials.set_roughness"
      description: "Sets the roughness value of the active object's material. Assumes a Principled BSDF shader."
      params:
        value:
          type: "float"
          description: "The roughness value, from 0.0 (smooth) to 1.0 (rough)."
          required: true
```
