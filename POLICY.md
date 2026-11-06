# Politique d’exécution

| Condition | Décision |
|---|---|
| Aucun argument | Audit local des métadonnées, affichage des compteurs |
| Racine absente | Zéro candidat, aucun dossier créé |
| Windows | Profil courant obtenu auprès de Windows, sous-dossier fixe `AppData/Local/pip/Cache/wheels` |
| macOS | Profil du compte effectif, sous-dossier fixe `Library/Caches/pip/wheels` |
| Structure pip reconnue | Quatre dossiers hexadécimaux minuscules de 2, 2, 2 et 50 caractères puis un nom de roue compatible |
| Fichier admissible | Fichier ordinaire, un seul lien, identifiant disponible, dernière modification datant d’au moins 30 jours |
| Autre fichier ou autre arborescence | Ignoré. Aucun parcours général des dossiers personnels ou du cache HTTP |
| Répertoire redirigé, point de montage intermédiaire détecté, marqueur Git dans la chaîne | Refus de la branche. Toute anomalie détectée pendant l’audit bloque le lot |
| Lien symbolique, point de réanalyse ou lien physique multiple au niveau du fichier | Exclu |
| Nettoyage | Terminal interactif, compte sans élévation, liste locale complète, confirmation exacte `OUI` |
| Avant chaque retrait | Revérifier les parents, l’appareil, l’identifiant, la taille et les horodatages. Écarter les entrées modifiées ou disparues |
| Erreur pendant le retrait | Compter l’omission, continuer avec le reste du plan et rendre un code non nul |

Les chemins libres, les profils redirigés par des variables de configuration pip, la suppression récursive et le vidage de la Corbeille sont hors périmètre. Les installations, les documents, les navigateurs, le trousseau et les fichiers de diagnostic ne font l’objet d’aucune opération prévue. Les privilèges supplémentaires et les changements de permissions sont exclus.

