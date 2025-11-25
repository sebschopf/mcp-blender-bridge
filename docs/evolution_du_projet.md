# L'Odyssée du MCP Blender : De la Rigidité à l'Injection Contrôlée

Ce document retrace l'évolution technique du projet MCP Blender. Contrairement à une progression linéaire simple, notre parcours a été fait d'expérimentations, d'échecs et de remises en question pour trouver l'équilibre parfait entre **sécurité**, **flexibilité** et **communication réelle** avec Blender.

## Le Point de Départ : L'Injection "Naïve" (et Dangereuse)

Le projet est né d'un constat sur les implémentations existantes (comme `ahujasid/blender-mcp`) : elles reposaient souvent sur une injection directe de code Python généré par le LLM.
*   **Avantage** : Flexibilité totale.
*   **Problème** : Dangerosité absolue (accès OS, suppression de fichiers) et instabilité (hallucinations d'API).

Notre objectif initial était donc clair : **Séparer les responsabilités** et sécuriser les échanges.

## L'Impasse de la "Rigidité" (Specs 004 - 018)

Pour sécuriser le système, nous avons d'abord pris le contre-pied total de l'injection : tout définir sous forme d'**Outils (Tools)** statiques et rigides.

### 1. La Palette d'Outils (Spec 004)
Nous avons tenté de définir une "palette" d'opérations `bpy` autorisées. Le LLM devait construire des plans d'action étape par étape.
*   *Échec* : Trop verbeux, trop lent, et limitant pour la créativité.

### 2. La Structuration YAML (Spec 006)
Nous avons organisé ces outils dans des fichiers YAML pour mieux les gérer.
*   *Avantage* : Plus propre.
*   *Problème* : La maintenance de milliers d'outils Blender à la main est impossible.

### 3. Le "RAG" d'Outils (Spec 018)
Face à l'explosion du nombre d'outils (Token Explosion), nous avons implémenté un système de recherche (`search_tools`).
*   Le LLM devait : Chercher un outil -> Charger sa définition -> L'utiliser.
*   **Le Mur** : À cette étape, nous avions un système complexe de gestion d'outils... qui **ne communiquait pas réellement avec Blender**. Le Controller tournait en vase clos, validant des plans théoriques, mais l'exécution réelle et fluide dans le viewport manquait. Nous avions recréé une usine à gaz pour éviter d'écrire du code.

## La Synthèse : L'Injection Contrôlée (Spec 001)

C'est finalement en revenant à la source, mais avec les leçons apprises, que nous avons trouvé la solution (décrite dans la Spec `001-inject-bpy-mcp`, paradoxalement la plus récente).

Nous avons compris que le LLM est un excellent générateur de code, et que vouloir le contraindre à utiliser des boutons pré-cablés était une erreur. La solution n'était pas d'interdire le code, mais de le **contrôler**.

### Le Nouveau Paradigme

1.  **Recherche Intelligente** : Le LLM utilise le système de recherche (hérité de nos essais précédents) non pas pour exécuter un outil, mais pour **apprendre** comment l'utiliser (via `inspect_tool`).
2.  **Génération de Code** : Fort de cette connaissance, il génère un script Python (BPY).
3.  **Validation Stricte** : Ce script passe dans un sas de sécurité draconien :
    *   Pas d'imports système (`os`, `socket` interdits).
    *   Analyse syntaxique (AST).
    *   Vérification des arguments.
4.  **Exécution via le Bridge** : Une fois validé, le script est envoyé à Blender via notre protocole de communication robuste.

### Conclusion

Nous sommes passés d'une **anarchie dangereuse** (injection directe) à une **bureaucratie inefficace** (outils rigides), pour finir par une **administration contrôlée** (injection contrôlée).

C'est cette architecture hybride qui permet aujourd'hui à MCP Blender d'être à la fois créatif (grâce au code) et sûr (grâce au contrôle), tout en maintenant une véritable séparation des responsabilités entre le Cerveau (Gemini) et le Muscle (Blender).
