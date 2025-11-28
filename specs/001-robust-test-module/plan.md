# Implementation Plan: Environnement de Test Robuste

**Branch**: `001-robust-test-module` | **Date**: 2025-11-17 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-robust-test-module/spec.md`

## Summary

Cette fonctionnalité met en place un environnement de test robuste et automatisé pour le projet `controller`. Elle inclut la configuration du package (`pyproject.toml`), le script de lancement (`run_tests.bat`), et la **réimplémentation complète** de la suite de tests (`test_*.py`) pour garantir une couverture fiable et moderne (AsyncMock, SecurityValidator).

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: `uv`, `pytest`, `fastapi`, `httpx`, `google-generativeai`
**Storage**: N/A
**Testing**: `pytest`
**Target Platform**: Windows (pour le script `.bat`)
**Project Type**: Infrastructure de test pour un projet Python existant.
**Performance Goals**: N/A
**Constraints**: Le script doit gérer l'environnement virtuel et les dépendances de manière autonome.
**Scale/Scope**: La solution doit couvrir tous les tests existants et futurs dans le répertoire `controller/tests`.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

-   ✅ **I. Strict MCP Architecture**: Compliant. Améliore la maintenabilité et la fiabilité du Contrôleur.
-   ✅ **II. Conversational Interface**: N/A. Concerne l'infrastructure de développement.
-   ✅ **III. Granular & Secure Tools**: N/A. Concerne l'infrastructure de développement.
-   ✅ **IV. User-Centric Control**: N/A. Concerne l'infrastructure de développement.
-   ✅ **V. Blender-Native Integration**: Compliant. Assure que le code du Contrôleur est de meilleure qualité, ce qui bénéficie à l'intégration finale.

## Project Structure

### Documentation (this feature)

```text
specs/001-robust-test-module/
├── plan.md              # This file
├── research.md          # N/A pour cette fonctionnalité
├── data-model.md        # N/A pour cette fonctionnalité
├── quickstart.md        # Guide pour lancer les tests
└── tasks.md             # Tâches d'implémentation
```

### Source Code (repository root)
```text
# Modifications principales
controller/
├── pyproject.toml       # A CREER : Définit le projet comme un package installable
├── requirements.txt     # A METTRE A JOUR : Liste complète des dépendances
└── tests/               # Contient les tests à exécuter
    ├── test_main.py             # A REIMPLEMENTER : Tests d'intégration API
    ├── test_chat_service.py     # A REIMPLEMENTER : Tests logique conversationnelle
    ├── test_knowledge_engine.py # A REIMPLEMENTER : Tests RAG/Embeddings
    ├── test_bridge_api.py       # A REIMPLEMENTER : Tests communication Blender
    └── test_mcp_server.py       # A REIMPLEMENTER : Tests outils MCP

run_tests.bat            # A CREER : Script pour lancer la suite de tests
2.  **Mocking**: Use `unittest.mock.AsyncMock` for all `async` functions (Gemini calls, Bridge, etc.). Never perform real network calls in unit tests.
3.  **Modernity**: Use `pytest` fixtures (`@pytest.fixture`) rather than `unittest.TestCase` classes where possible.
4.  **Security**: Ensure tests validate the `SecurityValidator` where relevant.

### Components to Cover

-   **`test_main.py`**:
    -   Verify `/` (Health check).
    -   Verify `/api/chat` with a `ChatService` mock.
-   **`test_chat_service.py`**:
    -   Mock `GeminiClient`.
    -   Verify the flow: User Message -> `process_message` -> AI Response.
    -   Verify history management.
-   **`test_knowledge_engine.py`**:
    -   Mock the vector database (do not load real heavy embeddings).
    -   Verify document addition and retrieval.
-   **`test_bridge_api.py`**:
    -   Verify `get_command` (long polling).
    -   Verify `post_result`.
    -   Mock `bridge_manager`.
