# Plan d'implémentation: Injection contrôlée BPY via MCP

Feature: `001-inject-bpy-mcp`
Date: 2025-11-25
Owner: TBD

Résumé
-------
Implémenter un outil MCP permettant au LLM de fournir des scripts BPY validés et exécutés de façon contrôlée : extraction/normalisation de la sortie LLM, validation syntaxique + heuristique, vérification d'opérateurs via `inspect_tool`, exécution dans un environnement sandbox (Blender headless), puis proposition d'exécution live après confirmation utilisateur. Journaux et audit obligatoires.

Objectifs de la première itération (MVP)
- Recevoir une réponse LLM et extraire un script BPY (support fenced code/plain text).
- Valider syntaxe Python et blocages d'import non autorisés.
- Vérifier opérateurs détectés via `inspect_tool`.
- Exécuter le script dans une sandbox headless (ou simuler si infra manquante) et capturer erreurs.
- Interface minimale: preview + bouton `Apply to live` qui nécessite confirmation.

Milestones & estimation (rough)
- M1 (2d) — Scaffolding: templates prompts, ajouter endpoint MCP `inject_bpy_script` (2 jours).
- M2 (3d) — Validator initial (`ast.parse`, heuristiques, banned imports) and integration with `inspect_tool` (3 jours).
- M3 (3d) — Sandbox runner (docker headless Blender) + capture stdout/stderr (3 jours).
- M4 (2d) — UI for preview/confirm + audit logging (2 jours).
- M5 (1d) — End-to-end tests & CI (unit tests for validator + integration tests in sandbox) (1 jour).

Total estimé: ~11 jours (1.5-2 devs parallelizable; adjust selon infra availability)

Work breakdown (tasks)
- Task A — Prompts & config
  - Create `controller/resources/llm_prompts/contextual.md` and `.../format-to-bpy.md` (examples & guidelines).
  - Add `LLMContextConfig` schema and small loader.

- Task B — MCP endpoint & request handling
  - Add `inject_bpy_script` in `mcp_server.py` (accept `{mode, script_or_text}`), sanitize inputs, persist request record.

- Task C — Script extraction
  - Implement parser to extract code from fenced blocks, attachments, or raw text. Normalize indentation and encoding.

- Task D — Validator
  - Implement `controller/validators/bpy_validator.py`:
    - `validate_syntax(script)` → uses `ast.parse`.
    - `detect_forbidden_imports(ast)` → rejects `os`, `subprocess`, `socket`, `ctypes`, etc.
    - `find_bpy_operators(ast or regex)` → returns list of operator names.
    - `verify_operators_with_inspect(operator_list)` → calls MCP `inspect_tool`.

- Task E — Sandbox runner
  - Add job to run script in Docker image with Blender headless, time and resource limits, capture logs and return structured result.

- Task F — UI / Confirmation
  - Add preview endpoint and simple UI (or CLI prompt) to display script, validation result, sandbox output, and `Apply to live` button.

- Task G — Audit & logging
  - Persist `InjectScriptRequest`, `ValidationResult`, `BPYExecutionRecord` to logs/DB; redact secrets.

- Task H — Tests & CI
  - Unit tests for validator; integration tests for sandbox run.

Files to change / create (suggested)
- `controller/resources/llm_prompts/contextual.md`
- `controller/resources/llm_prompts/format-to-bpy.md`
- `controller/validators/bpy_validator.py`
- `controller/bridge_runner/sandbox_runner.py` (docker wrapper)
- `controller/mcp_server.py` (add `inject_bpy_script` handler)
- `ui/preview_bpy.py` or `blender_addon` UI hooks
- `specs/001-inject-bpy-mcp/plan.md` (this file)

Risques & mitigations
- Risk: Infra sandbox non-disponible → Mitigation: fail closed (no live execution), provide simulated sandbox run and require manual review.
- Risk: LLM outputs obfuscated or intentionally malicious code → Mitigation: strict banned-import checks, AST analysis, and mandatory sandbox execution.
- Risk: False positives on operator detection → Mitigation: combine AST-based detection with `inspect_tool` verification, present warnings to user.

Definition of Done (DoD)
- Endpoint accepts LLM output and extracts script reliably (95% of test prompts).
- Validator passes known-good scripts and rejects known-bad scripts (unit tests green).
- Sandbox runner executes scripts in isolated environment and returns structured results.
- UI displays preview, validation, sandbox output, and requires explicit confirmation before live run.
- Audit logs produced for every request and action.

Next immediate steps (today)
1. Create prompt templates (Task A). — assign 0.5d
2. Implement `bpy_validator.py` skeleton (Task D). — assign 1d
3. Add MCP endpoint `inject_bpy_script` skeleton (Task B). — assign 0.5d

Suggested owners
- Engineering: controller team (+1 infra engineer for sandbox)
- QA: provide test scripts and CI job

Notes
- If you want, j'implémente les fichiers `controller/resources/llm_prompts/contextual.md` et `format-to-bpy.md` maintenant, et je peux ajouter un squelette de `controller/validators/bpy_validator.py` pour démarrer.
