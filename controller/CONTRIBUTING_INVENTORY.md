# Inventory Classification Guidelines

This short guide explains how to organize files under the new `capabilities/` and
`knowledge_base/` directories introduced by the Dual Inventory Architecture.

- `capabilities/`: contain YAML files that declare granular tools. Each file may
  declare one or more categories and a `tools` list. Choose filenames that reflect
  the contained domain (e.g., `mesh_editing.yaml`, `text_tools.yaml`).

- `knowledge_base/`: hierarchical directory structure for recipes. Use semantic
  categories as directories (e.g., `weapons/medieval/`, `vehicles/components/`).
  Each recipe should be a YAML file following the recipe schema described in
  `specs/010-dual-inventory-architecture/spec.md`.

- `resources/`: store fonts, textures, HDRIs and other binary assets. Use
  subdirectories by asset type (e.g., `fonts/`, `textures/`).

Naming guidance:
- Use snake_case for recipe filenames (e.g., `car_seat_standard.yaml`).
- Use semantic directory paths for categories (e.g., `vehicles/components`).

This document is intentionally brief; refer to `specs/010-dual-inventory-architecture/spec.md`
for schema and functional requirements.
