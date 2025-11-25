# Checklist d'Audit : Architecture à Double Inventaire

**Objectif** : Valider que les exigences de la fonctionnalité `010-dual-inventory-architecture` sont complètes, claires, mesurables et prêtes pour un audit.
**Créé le** : 2025-11-17
**Feature Spec**: [spec.md](../spec.md)

---

## Complétude des Exigences

- [ ] CHK001 - Les exigences de performance non fonctionnelles sont-elles explicitement définies, notamment le temps de démarrage maximal autorisé avec un grand nombre de fichiers d'inventaire ? [Gap]
- [ ] CHK002 - Le processus requis pour la gestion des fichiers YAML malformés (comparaison au modèle, tentative de correction, suppression si échec) est-il clairement documenté dans les exigences ? [Gap]
- [ ] CHK003 - Les exigences spécifient-elles que les outils et les recettes valides doivent être observables ou listables par les utilisateurs ou d'autres systèmes ? [Complétude]
- [ ] CHK004 - L'exigence de maintenir la compatibilité avec les fonctionnalités des outils existants est-elle formellement énoncée ? [Complétude, Spec §Backward Compatibility]
- [ ] CHK005 - Les exigences définissent-elles le comportement attendu lorsqu'une recette fait référence à un outil qui n'existe pas dans l'inventaire des capacités ? [Gap, Edge Case]

## Clarté et Mesurabilité des Exigences

- [ ] CHK006 - L'objectif de performance est-il quantifié avec des métriques précises (par exemple, "le temps de démarrage ne doit pas se dégrader de plus de 50%") ? [Clarté, Plan §Performance Goals]
- [ ] CHK007 - Les schémas de données pour `Tool`, `Recipe` et leurs sous-composants sont-ils définis sans ambiguïté dans `data-model.md` pour permettre une validation stricte ? [Clarté, Data Model]
- [ ] CHK008 - L'exigence de "supprimer si les corrections sont impossibles" pour un fichier malformé est-elle définie avec des critères objectifs pour déterminer quand une correction est jugée "impossible" ? [Ambiguïté]
- [ ] CHK009 - Les exigences relatives aux paramètres injectables dans les recettes (par exemple, `{{ table_width }}`) sont-elles clairement spécifiées, y compris la gestion des expressions mathématiques ? [Clarté, Data Model §RecipeFile Schema]

## Qualité des Critères d'Acceptation

- [ ] CHK010 - Les critères de succès pour le chargement de l'inventaire peuvent-ils être objectivement vérifiés (par exemple, "tous les fichiers YAML valides dans le répertoire X sont chargés en mémoire") ? [Mesurabilité]
- [ ] CHK011 - Le critère de succès pour la recherche de recettes (`knowledge.search_recipes`) est-il défini de manière mesurable (par exemple, "doit retourner toutes les recettes correspondant au mot-clé dans le nom, la description ou les tags") ? [Mesurabilité]

## Couverture des Scénarios

- [ ] CHK012 - Les exigences couvrent-elles le scénario où un fichier `.yaml` est syntaxiquement correct mais ne respecte pas le schéma Pydantic (par exemple, un champ obligatoire manquant) ? [Couverture, Exception Flow]
- [ ] CHK013 - Le comportement attendu est-il spécifié si un répertoire d'inventaire (`capabilities` ou `knowledge_base`) est vide ou n'existe pas au démarrage ? [Couverture, Edge Case]
- [ ] CHK014 - Les exigences spécifient-elles si le chargement de l'inventaire doit s'arrêter à la première erreur ou continuer en ignorant les fichiers invalides ? [Clarté, Exception Flow]
