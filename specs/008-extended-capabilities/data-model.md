# Data Model: Extended Capabilities

This feature consists entirely of extending the `controller/config/capabilities.yaml` file. Below are the new categories and tools to be added.

## 1. New Categories and Tools

The following sections should be added or merged into the `capabilities.yaml` file.

```yaml
# In modeling:
    - name: "bpy.ops.mesh.primitive_cylinder_add"
      description: "Creates a new cylinder mesh. Useful for columns, pipes, or wheels."
      params:
        radius: { type: "float", description: "The radius of the cylinder.", default: 1.0 }
        depth: { type: "float", description: "The height of the cylinder.", default: 2.0 }
        location: { type: "tuple", description: "The [X, Y, Z] coordinates for the center of the cylinder.", default: [0, 0, 0] }

    - name: "bpy.ops.mesh.primitive_plane_add"
      description: "Creates a new flat plane. Ideal for floors, walls, or as a base for other objects."
      params:
        size: { type: "float", description: "The length of each side of the plane.", default: 2.0 }
        location: { type: "tuple", description: "The [X, Y, Z] coordinates for the center of the plane.", default: [0, 0, 0] }

    - name: "bpy.ops.mesh.primitive_torus_add"
      description: "Creates a new torus (donut) mesh."
      params:
        major_radius: { type: "float", description: "The radius from the center to the middle of the torus ring.", default: 1.0 }
        minor_radius: { type: "float", description: "The radius of the torus ring itself.", default: 0.25 }
        location: { type: "tuple", description: "The [X, Y, Z] coordinates for the center of the torus.", default: [0, 0, 0] }

# In transform:
    - name: "bpy.ops.transform.rotate"
      description: "Rotates the active object around its origin."
      params:
        value: { type: "float", description: "The angle of rotation in radians.", required: true }
        orient_axis: { type: "str", description: "The axis to rotate around ('X', 'Y', 'Z').", required: true }

    - name: "bpy.ops.transform.resize"
      description: "Scales (resizes) the active object."
      params:
        value: { type: "tuple", description: "A scale factor vector [X, Y, Z]. e.g., [2, 1, 1] makes the object twice as long on the X-axis.", required: true }

# New Category: scene
scene:
  description: "Tools for managing the objects and elements within the entire scene."
  tools:
    - name: "bpy.ops.object.select_all"
      description: "Selects or deselects objects in the scene."
      params:
        action: { type: "str", description: "The selection action: 'SELECT', 'DESELECT', 'INVERT', 'TOGGLE'.", default: "TOGGLE" }

    - name: "bpy.ops.object.duplicate"
      description: "Duplicates the currently selected object(s). The new object(s) will be selected."
      params: {}

    - name: "bpy.ops.object.delete"
      description: "Deletes the currently selected object(s)."
      params:
        use_global: { type: "bool", description: "Set to False to delete without user confirmation.", default: false }

# New Category: modifiers
modifiers:
  description: "Tools for applying non-destructive modifications to an object's geometry."
  tools:
    - name: "bpy.ops.object.modifier_add"
      description: "Adds a modifier to the active object. Note: This only adds the modifier with default settings. Further configuration requires more advanced tools."
      params:
        type: { type: "str", description: "The type of modifier to add, e.g., 'SUBSURF' (for smoothing) or 'BEVEL' (for edges).", required: true }

# New Category: staging
staging:
  description: "Tools for adding lights and cameras to prepare the scene for rendering."
  tools:
    - name: "bpy.ops.object.light_add"
      description: "Adds a new light source to the scene."
      params:
        type: { type: "str", description: "The type of light: 'POINT', 'SUN', 'SPOT', 'AREA'.", default: "POINT" }
        location: { type: "tuple", description: "The [X, Y, Z] coordinates for the new light.", default: [0, 0, 0] }

    - name: "bpy.ops.object.camera_add"
      description: "Adds a new camera to the scene."
      params:
        location: { type: "tuple", description: "The [X, Y, Z] coordinates for the new camera.", default: [0, 0, 0] }
        rotation: { type: "tuple", description: "The [X, Y, Z] Euler rotation for the camera's initial orientation.", default: [0, 0, 0] }
```
