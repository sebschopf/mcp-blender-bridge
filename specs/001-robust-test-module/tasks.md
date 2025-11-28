# Implementation Tasks: Environnement de Test Robuste

**Feature Branch**: `001-robust-test-module`
**Feature Spec**: `specs/001-robust-test-module/spec.md`
**Implementation Plan**: `specs/001-robust-test-module/plan.md`
**Created**: 2025-11-17

## Phase 1: Setup & Configuration

- [X] T001 Créer le fichier `controller/pyproject.toml` pour définir le projet `controller` comme un package Python installable.
- [X] T002 Mettre à jour le fichier `controller/requirements.txt` pour inclure `pytest`, `httpx`, et `google-generativeai`.
- [X] T003 Créer le script `run_tests.bat` à la racine du projet.

## Phase 2: User Story 1 - Developer Confidence (P0)

**Goal**: Un développeur peut lancer une seule commande pour exécuter tous les tests de manière fiable.
**Independent Test**: Le script `run_tests.bat` exécute tous les tests du contrôleur sans erreur de configuration.

- [X] T004 [US1] Implémenter la logique dans `run_tests.bat` pour installer les dépendances depuis `controller/requirements.txt` en utilisant `uv`.
- [X] T005 [US1] Implémenter la logique dans `run_tests.bat` pour installer le package `controller` en mode éditable.
- [X] T006 [US1] Implémenter la logique dans `run_tests.bat` pour lancer `pytest` sur le répertoire `controller/tests`.

## Phase 3: Polish & Cross-Cutting Concerns

- [X] T007 Valider que l'exécution de `run_tests.bat` produit un rapport de test propre et sans erreur d'importation.
- [X] T008 Mettre à jour le `README.md` principal pour documenter la nouvelle méthode de lancement des tests.

## Phase 4: Test Suite Reimplementation (US2)

- [X] T009 [US2] Identify missing components requiring tests. <!-- id: 9 -->
- [X] T010 [US2] Reimplement `test_main.py` (API integration tests). <!-- id: 10 -->
- [X] T011 [US2] Reimplement `test_chat_service.py` (Conversation logic). <!-- id: 11 -->
- [X] T012 [US2] Reimplement `test_knowledge_engine.py` (RAG & Embeddings). <!-- id: 12 -->
- [X] T013 [US2] Reimplement `test_bridge_api.py` (Blender communication). <!-- id: 13 -->

1.  **MVP**: Complete Phases 1 and 2 to have a functional test script.
2.  **Finalization**: Complete Phase 3 to ensure validation and documentation.
3.  **Reimplementation**: Complete Phase 4 to restore full test coverage.
