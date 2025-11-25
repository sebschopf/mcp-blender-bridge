# Quickstart: SOLID Audit

This guide explains how to run the architecture audit.

## Prerequisites

- Python 3.11+
- `uv` installed

## Running the Audit

1. **Navigate to the root directory.**
2. **Run the custom audit script:**
   ```bash
   uv run python dev_scripts/audit_architecture.py
   ```
   *(Note: This script will be created as part of the implementation)*

## Verifying Layered Architecture

1. **Check for Forbidden Imports:**
   Ensure `controller/` does not import `bpy`.
   ```bash
   grep -r "import bpy" controller/
   ```
   Expected output: Empty.

2. **Check for Circular Dependencies:**
   Run `ruff check` (already configured to detect some cycles) or the custom script.

## Verifying "God Classes"

1. **Count lines of code:**
   ```bash
   wc -l controller/app/*.py
   ```
   Any file significantly over 300 lines should be scrutinized.
