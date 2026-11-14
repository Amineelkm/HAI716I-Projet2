"""
Étape 3 - Modification « Sélection » (dynamique du réplicateur).

On part de parts égales. À chaque génération, le score d'une stratégie est la
somme sur j de part_j x matrice[i][j] (la matrice des duels avec auto-rencontres),
et sa nouvelle part = ancienne part x son score / score moyen de la population.

Utilisation :
    python src/selection.py                          (population élargie, 100 générations)
    python src/selection.py --population cours       (les 5 stratégies du cours)
    python src/selection.py --generations 200
"""

import argparse
from pathlib import Path

from moteur import tournoi
from strategies import STRATEGIES_COURS
from strategies_nouvelles import STRATEGIES_NOUVELLES

RACINE = Path(__file__).resolve().parent.parent
DOSSIER_RESULTATS = RACINE / "resultats"
DOSSIER_CAPTURES = RACINE / "journal" / "captures"


def evoluer(matrice, nb_generations):
    """Calcule l'évolution des parts. Renvoie une liste de dictionnaires
    {nom: part} : la génération 0 (parts égales), puis chaque génération."""
    noms = list(matrice)
    parts = {n: 1 / len(noms) for n in noms}
    historique = [dict(parts)]
    for _ in range(nb_generations):
        scores = {i: sum(parts[j] * matrice[i][j] for j in noms) for i in noms}
        moyenne = sum(parts[i] * scores[i] for i in noms)
        parts = {i: parts[i] * scores[i] / moyenne for i in noms}
        historique.append(dict(parts))
    return historique


def texte_selection(historique, noms, titre, pas=10):
    """Met en forme les parts toutes les `pas` générations et le classement final."""
    lignes = [f"=== {titre} ===", "", "Parts de chaque stratégie (en %) :"]
    lignes.append(f"{'génération':<12}" + "".join(f"{n:>13}" for n in noms))
    dernier = len(historique) - 1
    for g, parts in enumerate(historique):
        if g % pas == 0 or g == dernier:
            lignes.append(f"{g:<12}" + "".join(f"{parts[n] * 100:>13.2f}" for n in noms))
    lignes += ["", f"Classement final (génération {dernier}) :"]
    finales = sorted(historique[-1].items(), key=lambda x: x[1], reverse=True)
    for rang, (nom, part) in enumerate(finales, start=1):
        lignes.append(f"  {rang}. {nom:<15} {part * 100:6.2f} %")
    return "\n".join(lignes)


def tracer(historique, noms, titre, chemin):
    """Dessine la courbe des parts par génération. Renvoie False si matplotlib
    n'est pas installé."""
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        return False
    plt.figure(figsize=(9, 5))
    for nom in noms:
        plt.plot([p[nom] * 100 for p in historique], label=nom, linewidth=2)
    plt.xlabel("Génération")
    plt.ylabel("Part de la population (%)")
    plt.title(titre)
    plt.grid(alpha=0.3)
    plt.legend()
    plt.tight_layout()
    chemin.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(chemin, dpi=120)
    plt.close()
    return True


def main():
    """Lit les options, calcule la matrice puis l'évolution, affiche et enregistre."""
    parser = argparse.ArgumentParser(description="Étape 3 : sélection")
    parser.add_argument("--population", choices=["cours", "elargie"], default="elargie")
    parser.add_argument("--generations", type=int, default=100)
    parser.add_argument("--graine", type=int, default=42)
    parser.add_argument("--parties", type=int, default=5)
    parser.add_argument("--tours", type=int, default=200)
    args = parser.parse_args()

    if args.population == "cours":
        population = dict(STRATEGIES_COURS)
    else:
        population = {**STRATEGIES_COURS, **STRATEGIES_NOUVELLES}

    res = tournoi(population, nb_parties=args.parties, nb_tours=args.tours,
                  graine=args.graine, auto_rencontres=True)
    noms = list(population)
    historique = evoluer(res['matrice'], args.generations)

    titre = (f"Sélection - population {args.population} ({len(noms)} stratégies), "
             f"{args.generations} générations, graine {args.graine}")
    texte = texte_selection(historique, noms, titre)
    print(texte)

    DOSSIER_RESULTATS.mkdir(exist_ok=True)
    nom_fichier = f"selection_{args.population}.txt"
    (DOSSIER_RESULTATS / nom_fichier).write_text(texte + "\n", encoding="utf-8")
    print(f"\nRésultats enregistrés dans resultats/{nom_fichier}")

    nom_image = f"ethan_selection_{args.population}.png"
    nom_pop = "élargie" if args.population == "elargie" else "cours"
    if tracer(historique, noms, f"Sélection - population {nom_pop}",
              DOSSIER_CAPTURES / nom_image):
        print(f"Graphique enregistré dans journal/captures/{nom_image}")
    else:
        print("matplotlib n'est pas installé : pas de graphique "
              "(pip3 install --user matplotlib).")


if __name__ == "__main__":
    main()
