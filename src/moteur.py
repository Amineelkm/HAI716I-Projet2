"""Moteur du dilemme du prisonnier itéré.
Une stratégie : strategie(mon_historique, historique_adv, rng) -> 'C' ou 'D'."""

import random

# Matrice des gains du cours : (coup de i, coup de j) -> (gain de i, gain de j)
GAINS = {
    ('C', 'C'): (3, 3),
    ('C', 'D'): (0, 5),
    ('D', 'C'): (5, 0),
    ('D', 'D'): (2, 2),
}


def inverser(coup):
    """Renvoie le coup opposé : 'C' -> 'D' et 'D' -> 'C'."""
    return 'D' if coup == 'C' else 'C'


def partie(strat_a, strat_b, nb_tours, rng, bruit=0.0, gains=GAINS):
    """Joue nb_tours tours entre deux stratégies (choix simultanés, bruit optionnel).
    Renvoie (score_a, score_b, historique_a, historique_b)."""
    hist_a, hist_b = [], []
    score_a, score_b = 0, 0

    for _ in range(nb_tours):
        # Chaque stratégie reçoit une copie : elle ne peut pas modifier l'historique
        coup_a = strat_a(list(hist_a), list(hist_b), rng)
        coup_b = strat_b(list(hist_b), list(hist_a), rng)

        if bruit > 0:
            if rng.random() < bruit:
                coup_a = inverser(coup_a)
            if rng.random() < bruit:
                coup_b = inverser(coup_b)

        gain_a, gain_b = gains[(coup_a, coup_b)]
        score_a += gain_a
        score_b += gain_b
        hist_a.append(coup_a)
        hist_b.append(coup_b)

    return score_a, score_b, hist_a, hist_b


def tournoi(strategies, nb_parties=5, nb_tours=200, graine=42, bruit=0.0, auto_rencontres=False, gains=GAINS):
    """Tournoi tous contre tous : chaque paire joue nb_parties parties de nb_tours tours.
    Renvoie les scores totaux, la matrice des duels et les taux de coopération."""
    rng = random.Random(graine)
    noms = list(strategies)

    totaux = {n: 0 for n in noms}
    matrice = {a: {b: 0 for b in noms} for a in noms}
    nb_c = {n: 0 for n in noms}
    nb_coups = {n: 0 for n in noms}

    for i, a in enumerate(noms):
        debut = i if auto_rencontres else i + 1
        for b in noms[debut:]:
            for _ in range(nb_parties):
                sa, sb, ha, hb = partie(strategies[a], strategies[b],
                                        nb_tours, rng, bruit, gains)
                if a == b:
                    totaux[a] += sa
                    matrice[a][a] += sa
                    nb_c[a] += ha.count('C')
                    nb_coups[a] += len(ha)
                else:
                    totaux[a] += sa
                    totaux[b] += sb
                    matrice[a][b] += sa
                    matrice[b][a] += sb
                    nb_c[a] += ha.count('C')
                    nb_c[b] += hb.count('C')
                    nb_coups[a] += len(ha)
                    nb_coups[b] += len(hb)

    taux_coop = {n: (nb_c[n] / nb_coups[n] if nb_coups[n] else 0.0) for n in noms}
    return {'totaux': totaux, 'matrice': matrice, 'taux_coop': taux_coop}


def classement(totaux):
    """Trie les stratégies par score total décroissant.
     Renvoie une liste [(nom, score), ...] du premier au dernier.
    """
    return sorted(totaux.items(), key=lambda x: x[1], reverse=True)


def texte_resultats(resultats, titre):
    """Met en forme le classement, la matrice des scores et les taux de
    coopération dans un texte prêt à afficher ou à enregistrer."""
    lignes = [f"=== {titre} ===", "", "Classement :"]
    for rang, (nom, score) in enumerate(classement(resultats['totaux']), start=1):
        coop = resultats['taux_coop'][nom] * 100
        lignes.append(f"  {rang}. {nom:<15} {score:>7}   (coopération : {coop:5.1f} %)")

    noms = list(resultats['matrice'])
    lignes += ["", "Matrice des scores (ligne = score de la stratégie contre la colonne) :"]
    lignes.append(" " * 15 + "".join(f"{n:>12}" for n in noms))
    for a in noms:
        lignes.append(f"{a:<15}" + "".join(f"{resultats['matrice'][a][b]:>12}" for b in noms))
    return "\n".join(lignes)
