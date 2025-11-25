# Checklist: QA Handoff for Integrated Blender Addon

**Purpose**: To validate that the feature specification is complete, clear, and testable before the QA team begins writing test cases.
**Created**: 2025-11-18
**Feature**: `specs/001-integrated-blender-addon/spec.md`

## Acceptance Criteria Quality

- [x] CHK001 - Can the "Independent Test" for User Story 1 be executed as a single, verifiable test case? [Measurability, Spec §User Story 1]
- [x] CHK002 - Is each "Acceptance Scenario" written in a testable Given/When/Then format? [Testability, Spec §Acceptance Scenarios]
- [x] CHK003 - Are the measurable outcomes in "Success Criteria" specific enough to be validated (e.g., "< 10 seconds")? [Clarity, Spec §Success Criteria]
- [x] CHK004 - Is the expected behavior for an invalid API key defined with a specific error message format? [Clarity, Spec §Edge Cases]
- [x] CHK005 - Is the reconnection logic for a lost server connection specified with an exact number of retries? [Clarity, Spec §Edge Cases]
- [x] CHK006 - Is the behavior for a port conflict defined with a clear user action? [Clarity, Spec §Edge Cases]

## Requirement Completeness

- [x] CHK007 - Are all states of the addon (`Non configuré`, `Inactif`, `Démarrage...`, `Actif`, `Arrêt...`) covered by an acceptance scenario? [Coverage, Spec §Key Entities]
- [x] CHK008 - Does the spec define the exact text for the message guiding users to the preferences? [Completeness, Spec §FR-003]
- [x] CHK009 - Is the maximum number of messages in the chat history explicitly stated? [Completeness, Spec §Key Entities]
- [x] CHK010 - Are there requirements for how the addon should behave if the user-provided `controller_python_path` is invalid? [Gap]

## Scenario and Edge Case Coverage

- [x] CHK011 - Does the spec address what happens if the server process crashes or becomes unresponsive while the addon state is 'Actif'? [Gap]
- [x] CHK012 - Are there requirements for handling very long messages in the chat input or history? [Gap]
- [x] CHK013 - Is the behavior defined for when a user tries to activate the MCP while it's already starting up? [Coverage, Edge Case]
- [x] CHK014 - Does the spec consider the case where the user revokes the addon's permissions or enters an invalid API key *after* the server is already running? [Gap]
