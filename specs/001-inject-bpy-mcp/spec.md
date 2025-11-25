```markdown
# Feature Specification: Injection contrôlée BPY via MCP

**Feature Branch**: `001-inject-bpy-mcp`  
**Created**: 2025-11-25  
**Status**: Draft  
**Input**: Le LLM écrit un script BPY complet ; le controller le reçoit, le vérifie (doit être du BPY et ne pas sortir de l'environnement Blender), puis l'envoie au pont pour exécution contrôlée.

## Contexte & Résumé

Le but est d'ajouter au MCP un outil sécurisé permettant au LLM de proposer des scripts Blender (BPY) complets. Le flux :

- Le LLM génère un script BPY (ou une réponse formatée produisant un fichier `.py`).
- Le controller reçoit la sortie, effectue des validations (syntaxe Python, usages `bpy`, vérification d'opérateurs via `inspect_tool`), puis exécute le script dans Blender via le Bridge seulement après validation et confirmation utilisateur.

Cette feature réduit les allers-retours manuels et permet au LLM d'explorer les outils MCP pour produire des scripts complexes tout en limitant les risques de sorties nuisibles hors de l'environnement Blender.

## User Scenarios & Testing

### User Story 1 — Génération et exécution d'un script BPY (P1)

En tant qu'utilisateur, je demande à l'IA de réaliser une opération Blender (ex. : "Créer une chaise simple").

Independent Test:
- Envoyer la demande via le MCP en `format-to-bpy`.
- Vérifier que la réponse contient un fichier `.py` ou un bloc de code clair.
- Valider syntaxe via `ast.parse` et détecter `bpy.ops.` via heuristique.
- Si validation OK, exécuter en sandbox et demander confirmation utilisateur pour exécution live.

Acceptance:
- Script valide (syntaxe) et n'utilise que APIs Blender attendues ; utilisateur confirme l'exécution live.

### User Story 2 — LLM s'appuie sur l'inspection outil (P2)

En tant que LLM, je peux appeler `inspect_tool(tool_name)` pour récupérer des paramètres d'un opérateur et les intégrer correctement dans mon script.

Independent Test:
- Appeler `inspect_tool` pour `bpy.ops.mesh.primitive_cube_add` et vérifier que le LLM utilise les paramètres retournés dans le script.

Acceptance:
- Le script contient des appels aux opérateurs avec noms et paramètres conformes à la sortie d'inspection.

### Edge Cases

- LLM renvoie prose ou instructions non-Python → déclencher reformattage automatique (max 2 tentatives), sinon signaler erreur.
- LLM référence opérateur inconnu → `inspect_tool` renvoie erreur et le controller refuse exécution.
- Script contenant appels système ou accès hors-Blender (IO, réseau, OS) → rejet formel.

## Requirements (Testables)

### Fonctionnelles

- **FR-001**: Ajouter un nouvel outil MCP `inject_bpy_script(script: str, mode: str = 'format-to-bpy')` exposé par `mcp_server`.
- **FR-002**: Le controller doit accepter une requête LLM contenant : `{mode, script_or_text}` où `mode` ∈ {`contextual`, `format-to-bpy`}.
- **FR-003**: Si la requête arrive en `format-to-bpy`, le controller doit extraire le script Python de la réponse (supporter fenced code, attachment, ou plain text).
- **FR-004**: Implémenter un validateur serveur avec étapes :
  - 1) Vérification syntaxique Python (`ast.parse`).
  - 2) Analyse heuristique : détecter tokens `bpy.ops.`, `bpy.data.`, import de modules non autorisés (`os`, `subprocess`, `socket`, etc.).
  - 3) Pour chaque opérateur détecté, appeler `inspect_tool` (MCP) pour vérifier existence et paramètres attendus.
  - 4) Vérification que le script n'effectue pas d'opérations hors-scope (accès FS non-Blender, network, processus externes).
- **FR-005**: Si le validateur renvoie des erreurs, le controller doit automatiquement re-demander au LLM de reformater (template strict) jusqu'à 2 fois ; si toujours invalide, renvoyer l'erreur à l'utilisateur.
- **FR-006**: Implémenter une exécution sandbox (headless Blender) pour exécuter les scripts validés et capturer erreurs d'exécution. Cette sandbox est OBLIGATOIRE : tout script validé doit d'abord être exécuté dans la sandbox avant d'être proposé pour exécution live; si l'infrastructure sandbox n'est pas disponible, le controller doit refuser l'exécution live et informer l'utilisateur.
- **FR-007**: Ne jamais exécuter un script dans la session live sans confirmation explicite de l'utilisateur (`Apply to live`).
- **FR-008**: Garder un journal (audit) de la requête, de la réponse brute, du résultat de validation, des actions sandbox, et de la confirmation utilisateur.

### Non-fonctionnelles

- **NFR-001**: Le validateur syntaxique et heuristique doit répondre en <2s en moyenne (hors sandbox).
- **NFR-002**: Les prompts système et templates doivent être stockés et révisables dans `controller/resources/llm_prompts/`.
- **NFR-003**: Les logs et artefacts de validation doivent être conservés au moins 30 jours (configurable).

## Key Entities

- **InjectScriptRequest**: `{id, requester, mode, script_raw, timestamp}`
- **ValidationResult**: `{is_valid: bool, errors: list, warnings: list, operator_list: list}`
- **BPYExecutionRecord**: `{request_id, sandbox_result, user_confirmed, live_result, logs}`

## Success Criteria

- **SC-001**: 95% des scripts fournis en `format-to-bpy` passent la validation syntaxique automatiquement.
- **SC-002**: Après validation sandbox, 98% des scripts validés n' échouent pas lors d'une exécution contrôlée dans un environnement d'essai.
- **SC-003**: 100% des exécutions live sont précédées d'une confirmation explicite utilisateur.

## Implementation Notes

- Templates prompts: `controller/resources/llm_prompts/contextual.md` et `format-to-bpy.md` (ex: "Return only a single Python file; no prose; use bpy.* only; do not import os/socket/subprocess").
- Étendre `gemini_client` pour permettre `system_instruction` spécifique par requête (déjà possible via `GenerateContentConfig.system_instruction`).
- Le validateur initial : `ast.parse` + AST walk to detect imports and name usages; regex for `bpy.ops.`. Use `inspect_tool` to validate operator names/params.
- Sandbox execution: idéalement via une image Docker contenant Blender headless; exécuter dans un time-limited, resource-limited container.

## Security & Safety

- Bloquer imports non autorisés (`os`, `subprocess`, `socket`, `ctypes`, etc.).
- Interdire écriture dans system directories ; autoriser écriture uniquement dans répertoires Blender contrôlés si nécessaire.
- Journaliser et alerter si script tente d'utiliser APIs non-Blender.

## Acceptance Tests (exemples)

- Test A: LLM génère script simple `bpy.ops.mesh.primitive_cube_add(size=2)` → passe validation, sandbox OK.
- Test B: LLM génère `import os; os.remove('/important')` → validation échoue, rejet.
- Test C: LLM référence `bpy.ops.nonexistent` → `inspect_tool` retourne erreur, controller refuse exécution.

## Assumptions

- Le bridge MCP et l'addon Blender peuvent transmettre et exécuter des scripts via une API sécurisée.
- `inspect_tool` existe et fournit un schéma structuré pour les opérateurs (déjà discuté dans `019-add-inspect-tool`).

## Clarifications enregistrées

- Session 2025-11-25: Politique d'exécution BPY → Option A (Sandbox obligatoire). Applied: `FR-006` mis à jour pour exiger l'exécution préalable en sandbox avant toute proposition d'exécution live.

## Clarifications à demander (si nécessaire)

- Q1: Souhaitez-vous un retry automatique plus élevé que 2 tentatives pour reformattage ? (recommandation : 2)
- Q2: Faut-il une fonctionnalité d'« approbation par rôle » (ex : certains utilisateurs peuvent exécuter sans sandbox) ? (recommandation : non, start strict)

---

**Fichier créé automatiquement:** `specs/001-inject-bpy-mcp/spec.md`

``` 
# Feature Specification: [FEATURE NAME]

**Feature Branch**: `[###-feature-name]`  
**Created**: [DATE]  
**Status**: Draft  
**Input**: User description: "$ARGUMENTS"

## User Scenarios & Testing *(mandatory)*

<!--
  IMPORTANT: User stories should be PRIORITIZED as user journeys ordered by importance.
  Each user story/journey must be INDEPENDENTLY TESTABLE - meaning if you implement just ONE of them,
  you should still have a viable MVP (Minimum Viable Product) that delivers value.
  
  Assign priorities (P1, P2, P3, etc.) to each story, where P1 is the most critical.
  Think of each story as a standalone slice of functionality that can be:
  - Developed independently
  - Tested independently
  - Deployed independently
  - Demonstrated to users independently
-->

### User Story 1 - [Brief Title] (Priority: P1)

[Describe this user journey in plain language]

**Why this priority**: [Explain the value and why it has this priority level]

**Independent Test**: [Describe how this can be tested independently - e.g., "Can be fully tested by [specific action] and delivers [specific value]"]

**Acceptance Scenarios**:

1. **Given** [initial state], **When** [action], **Then** [expected outcome]
2. **Given** [initial state], **When** [action], **Then** [expected outcome]

---

### User Story 2 - [Brief Title] (Priority: P2)

[Describe this user journey in plain language]

**Why this priority**: [Explain the value and why it has this priority level]

**Independent Test**: [Describe how this can be tested independently]

**Acceptance Scenarios**:

1. **Given** [initial state], **When** [action], **Then** [expected outcome]

---

### User Story 3 - [Brief Title] (Priority: P3)

[Describe this user journey in plain language]

**Why this priority**: [Explain the value and why it has this priority level]

**Independent Test**: [Describe how this can be tested independently]

**Acceptance Scenarios**:

1. **Given** [initial state], **When** [action], **Then** [expected outcome]

---

[Add more user stories as needed, each with an assigned priority]

### Edge Cases

<!--
  ACTION REQUIRED: The content in this section represents placeholders.
  Fill them out with the right edge cases.
-->

- What happens when [boundary condition]?
- How does system handle [error scenario]?

## Requirements *(mandatory)*

<!--
  ACTION REQUIRED: The content in this section represents placeholders.
  Fill them out with the right functional requirements.
-->

### Functional Requirements

- **FR-001**: System MUST [specific capability, e.g., "allow users to create accounts"]
- **FR-002**: System MUST [specific capability, e.g., "validate email addresses"]  
- **FR-003**: Users MUST be able to [key interaction, e.g., "reset their password"]
- **FR-004**: System MUST [data requirement, e.g., "persist user preferences"]
- **FR-005**: System MUST [behavior, e.g., "log all security events"]

*Example of marking unclear requirements:*

- **FR-006**: System MUST authenticate users via [NEEDS CLARIFICATION: auth method not specified - email/password, SSO, OAuth?]
- **FR-007**: System MUST retain user data for [NEEDS CLARIFICATION: retention period not specified]

### Key Entities *(include if feature involves data)*

- **[Entity 1]**: [What it represents, key attributes without implementation]
- **[Entity 2]**: [What it represents, relationships to other entities]

## Success Criteria *(mandatory)*

<!--
  ACTION REQUIRED: Define measurable success criteria.
  These must be technology-agnostic and measurable.
-->

### Measurable Outcomes

- **SC-001**: [Measurable metric, e.g., "Users can complete account creation in under 2 minutes"]
- **SC-002**: [Measurable metric, e.g., "System handles 1000 concurrent users without degradation"]
- **SC-003**: [User satisfaction metric, e.g., "90% of users successfully complete primary task on first attempt"]
- **SC-004**: [Business metric, e.g., "Reduce support tickets related to [X] by 50%"]
