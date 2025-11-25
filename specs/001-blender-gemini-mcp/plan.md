# Implementation Plan: Blender-Gemini MCP Integration

**Feature Branch**: `001-blender-gemini-mcp`  
**Feature Spec**: `specs/001-blender-gemini-mcp/spec.md`  
**Status**: In Progress

## 1. Technical Context

### 1.1. High-Level Approach

The project will be implemented as three distinct components following the MCP (Model-Controller-Peripheral) architecture:

1.  **Model (Gemini)**: The core intelligence, accessed via its API. It will be responsible for understanding user prompts, maintaining a conversation, and generating structured tool calls.
2.  **Controller (Python/FastAPI)**: A standalone web server that acts as the central hub. It exposes a secure API for the Model to use, validates all incoming requests, manages the conversation state, and translates high-level tool calls into low-level, specific `bpy` commands for Blender.
3.  **Peripheral (Blender Addon)**: A standard Python addon within Blender. It will provide the user interface (a "Connect" button and a chat window), communicate with the Controller via HTTP, and execute the received `bpy` commands safely.

Communication will be unidirectional in terms of commands: `Model -> Controller -> Peripheral`. The Peripheral will send status updates and results back to the Controller.

### 1.2. Technology Choices

-   **Controller**: Python 3.10+ with the FastAPI web framework. This provides a modern, fast, and well-documented platform for building the API.
-   **Peripheral**: Python 3.10+ (using Blender's bundled Python interpreter). The addon will use standard Python libraries (`requests`, `json`).
-   **Communication Protocol**: RESTful API over HTTP. The Blender Addon will act as the client, and the FastAPI Controller will be the server.
-   **Data Format**: JSON will be used for all data exchange between the components.

### 1.3. Dependencies & Integrations

-   **External**:
    -   Google Gemini API: For the natural language processing and tool generation. Requires an API key.
-   **Internal**:
    -   Blender's Python API (`bpy`): The addon will interact heavily with this to manipulate the 3D scene.

## 2. Constitution Check

This plan is checked against the principles defined in `.specify/memory/constitution.md`.

-   [PASS] **I. Strict MCP Architecture**: The plan explicitly separates the Model, Controller, and Peripheral.
-   [PASS] **II. Conversational Interface**: The workflow is centered around a chat interface for clarifying user intent.
-   [PASS] **III. Granular & Secure Tools**: The Controller's API will expose only specific, validated actions. The Blender addon will not execute arbitrary code.
-   [PASS] **IV. User-Centric Control**: The conversational model and explicit "Connect" button ensure the user is in control.
-   [PASS] **V. Blender-Native Integration**: The peripheral is designed as a standard Blender addon using the `bpy` API.

**Result**: The plan is in full compliance with the project constitution.

## 3. Phase 0: Research & Prototyping

All major technology choices have been made. Research will focus on implementation details and best practices.

**Outputs**:
-   `specs/001-blender-gemini-mcp/research.md`

## 4. Phase 1: Core Design & Contracts

This phase defines the core data structures, API endpoints, and setup instructions.

### 4.1. Data Model

Defines the key data structures used in the system.

**Outputs**:
-   `specs/001-blender-gemini-mcp/data-model.md`

### 4.2. API Contracts

Defines the REST API endpoints for communication between the Blender Addon and the FastAPI Controller.

**Outputs**:
-   `specs/001-blender-gemini-mcp/contracts/openapi.yaml`

### 4.3. Quickstart Guide

Provides initial setup and running instructions for developers.

**Outputs**:
-   `specs/001-blender-gemini-mcp/quickstart.md`

### 4.4. Agent Context Update

The project's core technologies will be added to the agent's context for future reference.

## 5. Phase 2: Implementation Stubs & Scaffolding

This phase involves creating the basic file structure and placeholder code for each component.

-   **Controller**:
    -   Set up a new FastAPI project.
    -   Create placeholder files for API endpoints (`/chat`, `/command`).
    -   Implement basic Pydantic models for request/response validation.
-   **Blender Addon**:
    -   Create the basic structure of a Blender addon (`__init__.py`, etc.).
    -   Implement the UI panel with a "Connect" button and a simple text area for chat.
    -   Create placeholder functions for sending requests to the Controller.