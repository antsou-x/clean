# Changelog

## v2 — proposition

- Audit par défaut, compteurs partageables et entretien adaptatif en français.
- Moteur Python commun à Windows et macOS pour les anciennes roues pip en cache.
- Politique restrictive, tests sur fichiers factices et matrice CI native.
- Les opérations plus larges de la v1.1 restent documentées dans l’historique.

## v1.1 — 2026-11-06

Corrections issues d'un premier test réel (Windows, cache Chrome).

- Réponse invalide : explication en une ligne et rappel de répondre par lettres (un chiffre comme « 1 » n'est pas accepté).
- Outil de questions utilisé seulement s'il accepte toutes les options d'une question (Q2, Q5 ont 9 options).
- Cohérence en direct : option logique signalée quand une question devient sans objet (ex. Q8 si Téléchargements non analysés).
- Récapitulatif : fautes de frappe évidentes acceptées (« valdier ») et liste des contradictions à vérifier, dont libérer de l'espace + Corbeille.
- Garde-fou de chemin avant chaque suppression ; caches navigateurs limités aux dossiers nommés.
- Rappels Corbeille (espace libéré après vidage, fenêtres Windows possibles).
- Point de restauration : limite d'un point par 24 h gérée.
- Bureau Windows via `[Environment]::GetFolderPath('Desktop')` (compatible OneDrive) dans le script et le mode d'emploi.
- V1 : contrôle « zéro caractère non ASCII » ; V2 : dire honnêtement si l'outil de test manque.

## v1.0

- Version initiale : questionnaire en 13 cartes, script PowerShell/bash, double vérification, livraison.
