"""
Étape 1 : tournoi de base avec les cinq stratégies du cours.

Utilisation :
    python src/etape1.py                  (graine 42, sans auto-rencontres)
    python src/etape1.py --graine 7       (autre graine)
    python src/etape1.py --auto           (avec auto-rencontres)
"""

import argparse
from pathlib import Path

from moteur import tournoi, texte_resultats
from strategies import STRATEGIES_COURS

DOSSIER_RESULTATS = Path(__file__).resolve().parent.parent / "resultats"


def main():
    """Lit les options, lance le tournoi, affiche et enregistre les résultats."""
    parser = argparse.ArgumentParser(description="Étape 1 : tournoi de base")
    parser.add_argument("--graine", type=int, default=42)
    parser.add_argument("--parties", type=int, default=5)
    parser.add_argument("--tours", type=int, default=200)
    parser.add_argument("--auto", action="store_true",
                        help="chaque stratégie joue aussi contre elle-même")
    args = parser.parse_args()

    res = tournoi(STRATEGIES_COURS, nb_parties=args.parties, nb_tours=args.tours,
                  graine=args.graine, auto_rencontres=args.auto)

    titre = (f"Étape 1 - {args.parties} parties x {args.tours} tours, "
             f"graine {args.graine}, auto-rencontres : {'oui' if args.auto else 'non'}")
    texte = texte_resultats(res, titre)
    print(texte)

    DOSSIER_RESULTATS.mkdir(exist_ok=True)
    nom = "etape1_auto.txt" if args.auto else "etape1.txt"
    (DOSSIER_RESULTATS / nom).write_text(texte + "\n", encoding="utf-8")
    print(f"\nRésultats enregistrés dans resultats/{nom}")


if __name__ == "__main__":
    main()
