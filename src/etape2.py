"""
Étape 2 : tournoi élargi avec les stratégies du cours + les nouvelles stratégies,
puis comparaison avec le classement de l'étape 1.

Utilisation :
    python src/etape2.py                  (graine 42, sans auto-rencontres)
    python src/etape2.py --graine 7       (autre graine)
    python src/etape2.py --auto           (avec auto-rencontres)
"""

import argparse
from pathlib import Path

from moteur import tournoi, texte_resultats, classement
from strategies import STRATEGIES_COURS
from strategies_nouvelles import STRATEGIES_NOUVELLES

DOSSIER_RESULTATS = Path(__file__).resolve().parent.parent / "resultats"


def main():
    """Lance le tournoi à 5 puis à 7 stratégies, affiche la comparaison des rangs
    et enregistre le tout dans resultats/."""
    parser = argparse.ArgumentParser(description="Étape 2 : tournoi élargi")
    parser.add_argument("--graine", type=int, default=42)
    parser.add_argument("--parties", type=int, default=5)
    parser.add_argument("--tours", type=int, default=200)
    parser.add_argument("--auto", action="store_true",
                        help="chaque stratégie joue aussi contre elle-même")
    args = parser.parse_args()

    population = {**STRATEGIES_COURS, **STRATEGIES_NOUVELLES}

    # Étape 1 relancée avec les mêmes options, pour comparer
    etape1 = tournoi(STRATEGIES_COURS, nb_parties=args.parties, nb_tours=args.tours,
                     graine=args.graine, auto_rencontres=args.auto)
    etape2 = tournoi(population, nb_parties=args.parties, nb_tours=args.tours,
                     graine=args.graine, auto_rencontres=args.auto)

    titre = (f"Étape 2 - {len(population)} stratégies, {args.parties} parties x "
             f"{args.tours} tours, graine {args.graine}, "
             f"auto-rencontres : {'oui' if args.auto else 'non'}")
    textes = [texte_resultats(etape2, titre)]

    # Comparaison des rangs et des scores avec l'étape 1
    rang1 = {nom: r for r, (nom, _) in enumerate(classement(etape1['totaux']), 1)}
    lignes = ["=== Comparaison avec l'étape 1 (5 stratégies) ===",
              f"{'Stratégie':<15}{'rang étape 1':>13}{'rang étape 2':>13}"
              f"{'score étape 1':>15}{'score étape 2':>15}"]
    for r2, (nom, s2) in enumerate(classement(etape2['totaux']), 1):
        if nom in rang1:
            lignes.append(f"{nom:<15}{rang1[nom]:>13}{r2:>13}"
                          f"{etape1['totaux'][nom]:>15}{s2:>15}")
        else:
            lignes.append(f"{nom:<15}{'-':>13}{r2:>13}{'-':>15}{s2:>15}")
    textes.append("\n".join(lignes))

    texte = "\n\n".join(textes)
    print(texte)

    DOSSIER_RESULTATS.mkdir(exist_ok=True)
    nom = "etape2_auto.txt" if args.auto else "etape2.txt"
    (DOSSIER_RESULTATS / nom).write_text(texte + "\n", encoding="utf-8")
    print(f"\nRésultats enregistrés dans resultats/{nom}")


if __name__ == "__main__":
    main()
