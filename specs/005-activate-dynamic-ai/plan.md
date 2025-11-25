# Implementation Plan: Activate Dynamic AI Logic

**Feature Branch**: `005-activate-dynamic-ai`
**Feature Spec**: `specs/005-activate-dynamic-ai/spec.md`
**Created**: 2025-11-16

## Phase 0: Outline & Research

### Technical Context

-   **Controller**: The core logic will be implemented in the FastAPI application, specifically within `controller/app/main.py` and the `controller/app/gemini_client.py`. We will leverage the existing Gemini client and FastAPI framework.
-   **Internal Tools**: The new "internal tools" (`discover_capabilities`, `submit_action_plan`) will be standard Python functions defined within the Controller. They will be exposed to the Gemini model using its tool-calling feature.
-   **HTTP Client**: A simple HTTP client (like the `requests` library, which is already a dependency) will be used within the `discover_capabilities` and `submit_action_plan` tools to make requests to the Controller's own endpoints. This creates a clean separation of concerns.

### Constitution Check & Gate Evaluation

-   ✅ **I. Strict MCP Architecture**: This feature reinforces the architecture. The AI's actions are now channeled through two very specific, validated internal tools, further restricting its ability to perform arbitrary actions. The Controller remains in full control.
-   ✅ **II. Conversational Interface**: This plan directly implements the specified multi-step conversational flow, making the interaction more intelligent and robust.
-   ✅ **III. Granular & Secure Tools**: The new internal tools are granular and secure. They do not execute `bpy` code directly but orchestrate the flow of information, which is a safe and appropriate role for the AI.
-   ✅ **IV. User-Centric Control**: The end result of this process is a transparent `ActionPlan` that can be reviewed before execution, maintaining user control.
-   ✅ **V. Blender-Native Integration**: No changes are proposed that would violate this principle.

**Gate Evaluation**: The feature plan is fully compliant with the project's constitution.

### Research Tasks

No research is required. The implementation will use the existing Gemini API's tool-calling features and standard HTTP requests, which are well-understood patterns. A `research.md` file will be created to document this decision.

## Phase 1: Design & Contracts

### Data Model (`data-model.md`)

No new persistent data models are required. The key entities are the "Internal AI Tools," which are ephemeral and will be defined in the code. The `ActionPlan` and `CapabilityPalette` models from the previous feature will be used.

### API Contracts (`contracts/openapi.yaml`)

No changes are required to the external API contract. This feature concerns the *internal* logic of how the Controller uses its own API to interact with the Gemini model. The existing endpoints (`/api/mcp/capabilities` and `/api/chat`) will be consumed by the new internal tools.

### Quickstart Guide (`quickstart.md`)

The quickstart guide will be updated to explain the new end-to-end conversational flow from a developer's perspective, detailing how a simple user prompt now triggers the two-step "discover and plan" process.

### Agent Context Update

The `GEMINI.md` context file will be significantly updated. The new instructions will be more explicit, guiding the AI to use the `discover_capabilities` and `submit_action_plan` tools in the correct sequence.