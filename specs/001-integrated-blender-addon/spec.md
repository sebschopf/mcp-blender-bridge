# Feature Specification: Integrated Blender Addon

**Feature Branch**: `001-integrated-blender-addon`  
**Created**: mardi, 18 novembre 2025  
**Status**: Draft  

## Clarifications

### Session 2025-11-18
- Q: The spec mentions that if the connection to the server is lost, the addon should "attempt to reconnect or inform the user". How should this be handled? → A: Try to reconnect 3 times, then show a "Connection Lost, click to retry" button.
- Q: The spec assumes the server port `8000` is available. What should happen if that port is already in use when the user clicks "Activate MCP"? → A: Ask the user to enter a different port number.
- Q: The spec says the addon displays chat history. What's the maximum number of messages before truncation? → A: 50 messages.
- Q: The spec says the addon should display a message guiding the user to preferences if the API key isn't configured. What should the message be? → A: "Gemini API Key not configured. Please go to Edit > Preferences > Add-ons > MCP Gemini Assistant to set your API Key."
- Q: The spec mentions that if the API key is invalid, the server should return an error message that the addon displays. What is the expected format or content of this error message from the server? → A: A JSON object with `{"error": "Invalid API Key"}`.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Assistant IA Gemini intégré (Priority: P1)

En tant qu'utilisateur de Blender, je souhaite un assistant IA Gemini entièrement intégré, qui gère son propre processus serveur et permet une configuration dans l'application, offrant une expérience transparente et guidée.

**Why this priority**: Cette fonctionnalité est fondamentale pour l'utilisabilité et l'intégration de l'assistant Gemini dans Blender, transformant un outil à deux composants en une expérience unifiée et conviviale.

**Independent Test**: L'utilisateur peut installer l'addon, configurer la clé API dans les préférences de Blender, activer le MCP depuis le panneau de l'addon, interagir avec Gemini via le chat, et désactiver le MCP, le tout sans quitter Blender ni lancer de processus manuellement.

**Acceptance Scenarios**:

1.  **Given** l'addon est installé et la clé API Gemini n'est pas configurée, **When** l'utilisateur ouvre le panneau de l'addon, **Then** un message clair guide l'utilisateur vers les préférences de l'addon pour configurer la clé API: "Gemini API Key not configured. Please go to Edit > Preferences > Add-ons > MCP Gemini Assistant to set your API Key."
2.  **Given** la clé API Gemini est configurée et le serveur MCP est inactif, **When** l'utilisateur clique sur le bouton 'Activer MCP' dans le panneau de l'addon, **Then** le serveur FastAPI/Uvicorn démarre en arrière-plan, et le statut de l'addon passe à 'Actif'.
3.  **Given** le serveur MCP est actif, **When** l'utilisateur saisit un message dans le champ de chat et l'envoie, **Then** le message est envoyé à Gemini via le serveur MCP, la réponse de Gemini est affichée dans l'historique du chat, et les commandes Blender reçues sont exécutées.
4.  **Given** le serveur MCP est actif, **When** l'utilisateur clique sur le bouton 'Désactiver MCP', **Then** le processus serveur est proprement arrêté, et le statut de l'addon passe à 'Inactif'.
5.  **Given** le serveur MCP est actif, **When** l'utilisateur désactive l'addon ou ferme Blender, **Then** le processus serveur est automatiquement terminé pour éviter les processus zombies.
6.  **Given** l'addon est refactorisé, **When** un développeur examine la structure du code, **Then** il trouve des fichiers modulaires pour l'UI, les opérateurs, le gestionnaire de serveur et les préférences.

### Edge Cases

- Que se passe-t-il si le serveur ne démarre pas correctement (ex: port déjà utilisé) ? L'addon doit afficher un message d'erreur clair et demander à l'utilisateur d'entrer un port différent dans les préférences de l'addon.
- Comment le système gère-t-il la perte de connexion au serveur une fois qu'il est actif ? L'addon devrait tenter de se reconnecter automatiquement jusqu'à 3 fois. Si la reconnexion échoue, il doit informer l'utilisateur avec un bouton pour réessayer manuellement.
- Que se passe-t-il si la clé API est invalide ? Le serveur devrait renvoyer un message d'erreur au format JSON: `{"error": "Invalid API Key"}` que l'addon affiche.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: L'addon DOIT être refactorisé dans une structure de fichiers modulaire (`__init__.py`, `ui.py`, `operators.py`, `server_manager.py`, `preferences.py`).
- **FR-002**: L'addon DOIT disposer d'un panneau de préférences (`Édition > Préférences`) pour que l'utilisateur puisse entrer et sauvegarder sa clé API Gemini.
- **FR-003**: Au premier lancement ou si la clé API est manquante, le panneau de l'addon dans la vue 3D DOIT guider l'utilisateur pour qu'il configure sa clé API.
- **FR-004**: Un bouton 'Activer MCP' dans le panneau de l'addon DOIT démarrer le serveur FastAPI/Uvicorn en tant que processus d'arrière-plan non bloquant.
- **FR-005**: La clé API configurée DOIT être transmise de manière sécurisée au processus serveur lors de son démarrage via une variable d'environnement (`GEMINI_API_KEY`).
- **FR-006**: Un bouton 'Désactiver MCP' DOIT arrêter proprement le processus serveur en arrière-plan.
- **FR-007**: La désactivation de l'addon ou la fermeture de Blender DOIT terminer automatiquement tout processus serveur encore en cours d'exécution pour éviter les processus zombies.
- **FR-008**: Lorsque le MCP est actif, le panneau DOIT afficher l'historique de la conversation et un champ de saisie pour interagir avec Gemini.

### Key Entities *(include if feature involves data)*

- **Clé API Gemini**: Une chaîne de caractères secrète utilisée pour authentifier les requêtes auprès de l'API Gemini.
- **Processus Serveur MCP**: Le processus Python exécutant le serveur FastAPI/Uvicorn qui gère la logique d'intégration Gemini.
- **État de l'Addon**: Représente l'état actuel de l'intégration (ex: 'Non configuré', 'Inactif', 'Démarrage...', 'Actif', 'Arrêt...').
- **chat_history**: (`List[Tuple[String, String]]`)
    -   **Description**: A list of tuples representing the conversation, where each tuple is (speaker, message). Max 50 messages.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: L'installation et la première activation de l'addon, y compris le démarrage du serveur et la première interaction, DOIVENT être complétées en moins de 5 minutes pour un nouvel utilisateur.
- **SC-002**: Le processus serveur DOIT démarrer en moins de 10 secondes après avoir cliqué sur 'Activer MCP'.
- **SC-003**: L'arrêt du processus serveur DOIT être effectué en moins de 3 secondes.
- **SC-004**: L'addon DOIT maintenir une connexion stable au serveur MCP pendant au moins 8 heures d'utilisation continue de Blender.
- **SC-005**: Le taux de satisfaction des utilisateurs concernant la facilité d'installation et d'utilisation de l'addon DOIT être supérieur à 90%.

## Assumptions

- L'utilisateur dispose d'une installation fonctionnelle de Blender 3.0+ et d'un environnement Python compatible.
- Le port 8000 est disponible pour le serveur FastAPI/Uvicorn.
- Le serveur FastAPI/Uvicorn est configuré pour écouter sur `127.0.0.1:8000`.
- Le chemin vers l'environnement virtuel du contrôleur (`controller/.venv/Scripts/python.exe`) est prévisible et accessible depuis l'addon.