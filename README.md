# Prompt nettoyage ordi

Un prompt pour assistant IA (Claude, ChatGPT…) qui génère un **script sur mesure** pour auditer puis nettoyer un PC Windows ou un Mac, en sécurité.

## Comment ça marche

1. Colle le contenu de [`PROMPT.md`](PROMPT.md) dans ton assistant IA.
2. Réponds aux 13 questions (une par carte, par lettres : `A`, `AC`…). `retour` revient en arrière, `passer` garde l'option la plus prudente.
3. Valide le récapitulatif.
4. L'IA génère un script PowerShell (Windows) ou bash (Mac), vérifié deux fois, avec son mode d'emploi.
5. Lance d'abord **l'audit seul** (lecture seule), fais-le analyser, puis seulement le nettoyage (`-Clean` / `--clean`).

## Garanties de sécurité

- Audit par défaut : rien n'est modifié sans `-Clean` / `--clean` et une confirmation `OUI`.
- Jamais touchés : mots de passe, trousseau, cookies, historique, favoris, fichiers système hors caches, zones déclarées intouchables.
- Admin / sudo seulement si nécessaire, et annoncé.
- Aucun contournement de SIP, TCC ou fichiers verrouillés.

## Contenu

| Fichier | Rôle |
|---|---|
| `PROMPT.md` | Le prompt à jour |
| `CHANGELOG.md` | Historique des versions |
| `exemples/nettoyage-cache-chrome-windows.ps1` | Exemple de script généré (Windows, cache Chrome, Corbeille) |

> 😄 Si après l'exécution de ce prompt rien ne change, c'est de ta faute !!! Pas de la faute d'Antsou.
