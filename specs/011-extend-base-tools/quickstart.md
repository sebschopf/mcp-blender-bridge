# Quickstart: Using Extended Modeling Tools with Token Optimization

This guide explains how the AI should leverage the new two-step discovery process to efficiently find and use the expanded set of modeling tools.

## The Two-Step Discovery Process

To minimize token usage, the AI should no longer ask for all capabilities at once. Instead, it should follow this sequence:

### Step 1: Discover Available Categories

First, the AI calls the new endpoint to see what types of tools are available.

**Request**:
`GET /discover_categories`

**Response**:
```json
[
    "mesh",
    "sculpt",
    "modifiers",
    "object",
    "materials",
    "internal"
]
```

### Step 2: Request Tools for a Specific Category

Based on the user's request, the AI determines which categories are relevant. For a modeling task, it might choose "mesh" and "object". It then requests the tools for that specific category.

**Request**:
`GET /discover_capabilities?category=mesh`

**Response**:
A JSON list containing only the tools from the `mesh` category (e.g., `mesh.extrude`, `mesh.bevel`, `mesh.primitive_cube_add`, etc.).

## Example AI Workflow

**Goal**: Create a simple archway from a cube.

**Conceptual AI Thought Process**:

1.  **User Request**: "Create a simple archway."
2.  **AI Thought**: "Archway is a modeling task. I'll need mesh and object tools."
3.  **AI Action 1**: Call `GET /discover_categories`.
4.  **AI Action 2**: See that `mesh` and `object` are valid categories.
5.  **AI Action 3**: Call `GET /discover_capabilities?category=mesh`.
6.  **AI Action 4**: Call `GET /discover_capabilities?category=object`.
7.  **AI Thought**: "Okay, now I have all the tools I need without the noise from `materials` or `sculpting`."
8.  **AI Action 5**: Construct the final Action Plan using the retrieved tools:
    -   `operation: "mesh.primitive_cube_add"`
    -   `operation: "object.select_face"`
    -   `operation: "mesh.extrude"`
    -   `operation: "mesh.inset"`
    -   ...and so on.

This process ensures that the context provided to the AI for generating the final plan is minimal and highly relevant, leading to faster, cheaper, and more accurate results.