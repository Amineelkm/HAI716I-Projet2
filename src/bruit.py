"""Étape 3 - Bruit : chaque coup est inversé avec une probabilité p.
Compare le tournoi sans et avec bruit (même population, même graine).

Population : 7 stratégies par défaut, 5 du cours avec --population cours (ou --cours).
Utilisation : python src/bruit.py [--population cours] [--bruit 0.10]   (5 % par défaut)
Sortie : resultats/bruit_<p>pct.txt (cours) ou bruit_elargie_<p>pct.txt"""

import argparse
from pathlib import Path

from moteur import tournoi, texte_resultats, classement
from strategies import STRATEGIES_COURS
from strategies_nouvelles import STRATEGIES_NOUVELLES

DOSSIER_RESULTATS = Path(__file__).resolve().parent.parent / "resultats"


def main():
    """Lance le tournoi sans puis avec bruit, affiche la comparaison des rangs
    et enregistre le tout dans resultats/."""
    parser = argparse.ArgumentParser(description="Étape 3 : tournoi avec bruit")
    parser.add_argument("--bruit", type=float, default=0.05)
    parser.add_argument("--graine", type=int, default=42)
    parser.add_argument("--parties", type=int, default=5)
    parser.add_argument("--tours", type=int, default=200)
    parser.add_argument("--population", choices=["cours", "elargie"], default="elargie")
    parser.add_argument("--cours", action="store_true",
                        help="raccourci pour --population cours")
    args = parser.parse_args()
    if args.cours:
        args.population = "cours"

    if args.population == "cours":
        population = dict(STRATEGIES_COURS)
    else:
        population = {**STRATEGIES_COURS, **STRATEGIES_NOUVELLES}

    sans = tournoi(population, args.parties, args.tours, args.graine, bruit=0.0)
    avec = tournoi(population, args.parties, args.tours, args.graine, bruit=args.bruit)

    pct = args.bruit * 100
    textes = [
        texte_resultats(sans, f"Sans bruit (graine {args.graine})"),
        texte_resultats(avec, f"Avec bruit de {pct:g} % (graine {args.graine})"),
    ]

    # Comparaison des rangs
    rang_sans = {nom: r for r, (nom, _) in enumerate(classement(sans['totaux']), 1)}
    lignes = ["=== Comparaison ===",
              f"{'Stratégie':<15}{'rang sans':>10}{'rang avec':>10}"
              f"{'score sans':>12}{'score avec':>12}{'coop sans':>11}{'coop avec':>11}"]
    for r_avec, (nom, s_avec) in enumerate(classement(avec['totaux']), 1):
        lignes.append(f"{nom:<15}{rang_sans[nom]:>10}{r_avec:>10}"
                      f"{sans['totaux'][nom]:>12}{s_avec:>12}"
                      f"{sans['taux_coop'][nom]*100:>10.1f}%{avec['taux_coop'][nom]*100:>10.1f}%")
    textes.append("\n".join(lignes))

    texte = "\n\n".join(textes)
    print(texte)

    DOSSIER_RESULTATS.mkdir(exist_ok=True)
    prefixe = "bruit" if args.population == "cours" else "bruit_elargie"
    nom_fichier = f"{prefixe}_{pct:g}pct.txt"
    (DOSSIER_RESULTATS / nom_fichier).write_text(texte + "\n", encoding="utf-8")
    print(f"\nRésultats enregistrés dans resultats/{nom_fichier}")


if __name__ == "__main__":
    main()
