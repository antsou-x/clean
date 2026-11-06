# Provenance et validation

Base inspectée : commit `adfd25be93162d4fbad9950626726aa22f614ed0` de `antsou-x/clean`. Le dépôt contenait README.md, PROMPT.md et CHANGELOG.md. L’exemple PowerShell annoncé était absent. Le prompt v1.1 déléguait la suppression à du code généré, proposait notamment le vidage global des téléchargements et une fermeture forcée, et associait le mode lecture seule à l’écriture de rapports.

L’ancienne conversation décrivait une archive clean-v2 et quatre tests documentaires. La récupération du chat a fourni les liens et le résumé, sans pièces jointes accessibles. Les documents et les tests de cette livraison ont été reconstruits. Les quatre anciens résultats ne sont pas comptés.

## Exécution locale

Windows, Python 3.12.10 : 14 tests découverts, 13 réussis et un test de liens macOS réservé à son système. Les tests Windows ont créé une vraie jonction et ouvert un vrai fichier verrouillé. Les suppressions ont porté sur des fichiers factices en répertoire temporaire. Un audit réel en mode compteurs a trouvé zéro candidat et zéro anomalie.

La suite couvre aussi la confirmation, le refus hors terminal ou en mode élevé, les chemins imposés, la protection des dépôts Git, les liens physiques, les nouveaux fichiers apparus après prévisualisation, le changement de contenu, les refus d’accès et une seconde exécution. La matrice CI lance la même suite sous Windows et macOS avec Python 3.11 et 3.12. Les résultats distants sont consultables dans GitHub Actions pour le commit proposé.


## Exécution distante vérifiée

Les quatre combinaisons Windows/macOS × Python 3.11/3.12 ont réussi sur le fork au commit `4f047b5`. Sur chaque Windows, 13 cas réussissent et le cas macOS est écarté. Sur chaque Mac, 12 cas réussissent et les deux cas propres à Windows sont écartés. [Résultats des quatre tâches](https://github.com/TrisaaPro/clean/actions/runs/42222500416).
