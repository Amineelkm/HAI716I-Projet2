"""
Nouvelles stratégies (étape 2) - partie d'Ethan.

Interface : strategie(mon_historique, historique_adv, rng) -> 'C' ou 'D'
Ajouter chaque nouvelle stratégie dans le dictionnaire ci-dessous.
"""

from moteur import GAINS


def tit_for_two_tats(mon_hist, hist_adv, rng):
    """TF2T : coopère, et ne trahit que si l'adversaire a trahi aux deux derniers tours."""
    if len(hist_adv) >= 2 and hist_adv[-1] == 'D' and hist_adv[-2] == 'D':
        return 'D'
    return 'C'


def pavlov(mon_hist, hist_adv, rng):
    """PAVLOV (gagne-reste, perd-change) : coopère au premier tour. Ensuite, si le
    gain du tour précédent vaut 3 ou 5, rejoue le même coup ; s'il vaut 0 ou 2, change.

    Le gain du dernier tour se recalcule avec GAINS à partir des deux derniers coups
    (le moteur ne donne pas les gains, et une fonction n'a pas de mémoire propre).
    """
    if not mon_hist:
        return 'C'
    mon_coup = mon_hist[-1]
    mon_gain = GAINS[(mon_coup, hist_adv[-1])][0]
    if mon_gain >= 3:
        return mon_coup
    return 'D' if mon_coup == 'C' else 'C'


STRATEGIES_NOUVELLES = {
    "TF2T": tit_for_two_tats,
    "PAVLOV": pavlov,
}
