# Feature Specification: Intelligent LLM Scenario Routing System

**Feature Branch**: `022-scenario-router`  
**Created**: 2025-11-25  
**Status**: Draft  
**Input**: User description: "Implémenter un système de routage intelligent pour le LLM. Le système doit pouvoir analyser la requêtes de l'utilisateur pour identifier l'intention et le typde de création par exemple un personnage, une architecture complexe, un objet, un objet sculté, organique, un style cartoon, réaliste, défini par des critères personnalisés décidé à l'avance. En fonction de l'intention le système choisi des scénario avec des structures stricte qui lui disent quoi faire et comment le faire. Des modèles par exemple si c'est humain, suivre telle scénario qui exige telle condition. Les conditions sont remplit ? ok alors go non ? préciser puis go. Le but est d'éviter de faire patauger le LLM qui au final ne sait pas quoi faire ni comment le faire."

## User Scenarios & Testing

### User Story 1 - Intent-Based Scenario Selection (Priority: P1)

Users want the system to intelligently understand *what* they are trying to create (e.g., a character vs. a building) and automatically apply the best "strategy" or "scenario" for that task, ensuring the LLM follows a proven workflow rather than guessing.

**Why this priority**: It solves the core problem of "LLM hallucinations" or inefficient workflows by enforcing structured best practices for specific creation types.

**Independent Test**:
- Send a prompt like "Create a realistic human character" to the API.
- Verify (via logs or response) that the system identifies the intent as `character_creation`.
- Verify that the system loads the `scenario_character.md` prompt template instead of the generic one.

**Acceptance Scenarios**:

1. **Given** the user asks for a "realistic character", **When** the request is processed, **Then** the system classifies the intent as "Character/Organic" and loads the Character Scenario.
2. **Given** the user asks for a "modern skyscraper", **When** the request is processed, **Then** the system classifies the intent as "Architecture" and loads the Architecture Scenario.
3. **Given** the user asks for a "simple wooden cube", **When** the request is processed, **Then** the system classifies the intent as "Basic Object" and loads the Prop Scenario.
4. **Given** the loaded scenario requires specific details (e.g., "Style" for characters), **And** the user hasn't provided them, **Then** the system asks clarifying questions before proceeding.

### Edge Cases

- **Ambiguous Request**: If the intent is unclear (e.g., "Make a thing"), the system should default to a general "Discovery" or "Basic" scenario or ask for clarification.
- **Mixed Intent**: If a request involves multiple types (e.g., "A character standing in a building"), the system should prioritize the dominant entity or choose a "Scene Assembly" scenario.

## Requirements

### Functional Requirements

- **FR-001**: The system MUST implement an "Intent Classification" step before generating the final response. This step analyzes the user's prompt to map it to a predefined category.
- **FR-002**: The system MUST support a library of "Scenario Definitions" (e.g., Markdown files). Initial scenarios should include:
    - `Character/Organic` (Requirements: Style, Anatomy type)
    - `Architecture` (Requirements: Dimensions, Style, Function)
    - `Prop/Object` (Requirements: Material, Complexity)
    - `Scripting/Utility` (Direct python coding)
- **FR-003**: The system MUST verify if the user's prompt satisfies the mandatory conditions of the selected scenario (e.g., "Style defined?").
- **FR-004**: If mandatory conditions are missing, the system MUST respond with a structured request for clarification instead of attempting to execute the task.
- **FR-005**: Once conditions are met, the system MUST execute the task using the strict guidelines defined in the Scenario's prompt template.

### Key Entities

- **IntentRouter**: Logic component that maps user input -> Scenario ID.
- **Scenario**: A definition containing: `id`, `description`, `trigger_keywords`, `mandatory_parameters`, `system_prompt_template`.

## Success Criteria

### Measurable Outcomes

- **SC-001**: 90% of unambiguous user prompts are correctly classified into the right Scenario (Character vs Arch vs Prop).
- **SC-002**: The system asks clarifying questions in 100% of cases where a mandatory parameter (defined in the scenario) is missing from the initial prompt.
- **SC-003**: Reduction of "I cannot do that" or "Generic/Broken result" errors by 50% for complex requests compared to the baseline generic prompt.