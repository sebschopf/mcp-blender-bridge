# Quickstart: Environnement de Test Robuste

Ce guide explique comment utiliser le nouveau script de test automatisé pour valider le code du projet `controller`.

## Prérequis

- Assurez-vous que `uv` est installé et accessible dans votre PATH.

## Lancement des Tests

Pour lancer la suite de tests complète du contrôleur, suivez ces étapes :

1.  **Ouvrez un terminal** à la racine du projet (`MCP_Blender_02`).
2.  **Exécutez le script de test** :

    ```bash
    .\run_tests.bat
    ```

## Fonctionnement

Le script `run_tests.bat` s'occupe de tout :

1.  Il vérifie que `uv` est bien installé.
2.  Il installe ou met à jour toutes les dépendances listées dans `controller/requirements.txt` dans l'environnement virtuel `controller/.venv`.
3.  Il installe le package `controller` en mode "éditable" pour que les tests puissent trouver les modules de l'application.
4.  Il lance `pytest`, qui découvre et exécute automatiquement tous les tests dans le répertoire `controller/tests/`.
5.  Il affiche le rapport final des tests directement dans votre terminal.

C'est la méthode à privilégier pour s'assurer que l'environnement de test est propre et que les résultats sont fiables.

