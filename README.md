# HAI716I – Projet 2 (partie 1) : tournoi du dilemme du prisonnier itéré

Mohamed Amine EL KAMEL et Ethan Baudrand.

Le journal de bord de chacun est dans [`journal/journal_X.md`](journal/journal_X.md).

## Prérequis

- **Python 3** (testé avec Python 3.12). Le moteur, les stratégies et les tournois n'utilisent que la bibliothèque standard.
- **matplotlib**, seulement pour le graphique de la sélection. Sans lui, `selection.py` fonctionne quand même, mais ne produit pas de graphique.

```powershell
pip install matplotlib
```

## Relancer les tournois

Toutes les commandes se lancent **depuis la racine du dépôt**. Chaque script affiche ses résultats et les enregistre dans `resultats/`. La graine est fixée à 42 par défaut : relancer une commande redonne exactement les mêmes chiffres.

| But                                               | Commande                                       | Sortie                                                                   |
| ------------------------------------------------- | ---------------------------------------------- | ------------------------------------------------------------------------ |
| Vérifier le moteur et les stratégies              | `python src/verifier.py`                       | affichage seulement                                                      |
| Étape 1 : les 5 stratégies du cours               | `python src/etape1.py`                         | `resultats/etape1.txt`                                                   |
| Étape 1 avec auto-rencontres                      | `python src/etape1.py --auto`                  | `resultats/etape1_auto.txt`                                              |
| Étape 2 : 7 stratégies, comparaison avec l'étape 1 | `python src/etape2.py`                         | `resultats/etape2.txt`                                                   |
| Étape 2 avec auto-rencontres                      | `python src/etape2.py --auto`                  | `resultats/etape2_auto.txt`                                              |
| Bruit 5 %, 5 stratégies du cours                  | `python src/bruit.py --cours`                  | `resultats/bruit_5pct.txt`                                               |
| Bruit 10 %, 5 stratégies du cours                 | `python src/bruit.py --cours --bruit 0.10`     | `resultats/bruit_10pct.txt`                                              |
| Bruit 5 %, 7 stratégies                           | `python src/bruit.py`                          | `resultats/bruit_elargie_5pct.txt`                                       |
| Bruit 10 %, 7 stratégies                          | `python src/bruit.py --bruit 0.10`             | `resultats/bruit_elargie_10pct.txt`                                      |
| Sélection, 7 stratégies (100 générations)         | `python src/selection.py`                      | `resultats/selection_elargie.txt` + `journal/captures/ethan_selection_elargie.png` |
| Sélection, 5 stratégies du cours                  | `python src/selection.py --population cours`   | `resultats/selection_cours.txt` + `journal/captures/ethan_selection_cours.png`     |

Le graphique de la sélection n'est produit que si matplotlib est installé.

## Options

| Script         | Options (valeur par défaut)                                                                                    |
| -------------- | -------------------------------------------------------------------------------------------------------------- |
| `verifier.py`  | aucune                                                                                                         |
| `etape1.py`    | `--graine` (42), `--parties` (5), `--tours` (200), `--auto`                                                    |
| `etape2.py`    | `--graine` (42), `--parties` (5), `--tours` (200), `--auto`                                                    |
| `bruit.py`     | `--bruit` (0.05), `--graine` (42), `--parties` (5), `--tours` (200), `--cours` (seulement les 5 stratégies du cours) |
| `selection.py` | `--population` (`elargie` ou `cours`, par défaut `elargie`), `--generations` (100), `--graine` (42), `--parties` (5), `--tours` (200) |

Exemple : `python src/etape1.py --graine 7` relance l'étape 1 avec une autre graine.

Attention : relancer un script avec d'autres options que celles par défaut écrase le fichier de `resultats/` correspondant.

## Organisation

- `src/moteur.py` : matrice des gains, `partie()`, `tournoi()`, mise en forme des résultats.
- `src/strategies.py` : les 5 stratégies du cours (ALL-D, RANDOM, TIT-FOR-TAT, TESTER, JOSS).
- `src/strategies_nouvelles.py` : les 2 nouvelles stratégies (TF2T, PAVLOV).
- `src/etape1.py`, `src/etape2.py`, `src/bruit.py`, `src/selection.py` : un script par tournoi.
- `src/verifier.py` : tests sur des cas calculés à la main.
- `resultats/` : sorties texte des tournois.
- `journal/` : journal de bord et captures d'écran.
