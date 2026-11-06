# Clean • Windows et macOS

Clean aide à estimer la place occupée par les anciennes archives de paquets Python (« roues ») dans le cache standard de pip. Si vous utilisez pip, ces archives peuvent servir à réinstaller un paquet sans le reconstruire. Si vous ne l’utilisez pas, un résultat de zéro est normal.

## Premier audit

Extrayez le ZIP. Ouvrez un terminal ordinaire dans le dossier contenant `clean.py`. Utilisez Python 3.11 ou 3.12. Aucun paquet supplémentaire à installer.

| Action | Windows (PowerShell) | macOS (Terminal) |
|---|---|---|
| Estimer le volume | `py -3 -B clean.py` | `python3 -B clean.py` |
| Voir les noms sur votre écran | `py -3 -B clean.py --detail` | `python3 -B clean.py --detail` |
| Obtenir les seuls compteurs à partager | `py -3 -B clean.py --share` | `python3 -B clean.py --share` |
| Examiner la liste puis décider | `py -3 -B clean.py --clean` | `python3 -B clean.py --clean` |

`--share` affiche trois nombres dans le terminal. Vous décidez si vous les copiez ailleurs. `--detail` et `--clean` affichent des noms de paquets potentiellement privés.

## Décider de nettoyer

Attendez la fin des installations et constructions pip. Vérifiez que vous pouvez retélécharger ou reconstruire chaque paquet. Conservez une copie si vous comptez travailler hors ligne. Lancez ensuite la dernière commande du tableau. Vérifiez toute la liste avant de taper exactement `OUI`. Entrée seule annule. Pour conserver un seul des fichiers proposés, annulez tout le lot.

La suppression est définitive. Le total annoncé mesure la taille logique des fichiers, pas l’espace effectivement libéré. Un code de sortie 1 signale un refus, une interruption ou une opération incomplète. En cas d’erreur, refaites l’audit avant toute nouvelle tentative.

## Assistant, règles et validation

Le [prompt français](PROMPT.md) guide l’entretien. La [politique](POLICY.md) détaille les critères d’admission et les [limites](SECURITY.md) expliquent les risques résiduels. La [fiche de validation](VALIDATION.md) donne les tests et leur provenance.

Pour reproduire les tests, lancez `py -3 -B -m unittest discover -s tests -v` sous Windows ou `python3 -B -m unittest discover -s tests -v` sous macOS. Les essais de suppression utilisent des dossiers temporaires.

