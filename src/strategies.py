"""
Les cinq stratégies du cours 4 (diapositive 64).

Interface : strategie(mon_historique, historique_adv, rng) -> 'C' ou 'D'
"""


def all_d(mon_hist, hist_adv, rng):
    """ALL-D : trahit à chaque tour."""
    return 'D'


def random_strat(mon_hist, hist_adv, rng):
    """RANDOM : C ou D avec une probabilité de 50 % chacun."""
    return 'C' if rng.random() < 0.5 else 'D'


def tit_for_tat(mon_hist, hist_adv, rng):
    """TIT-FOR-TAT : coopère au premier tour, puis copie le dernier coup adverse."""
    if not hist_adv:
        return 'C'
    return hist_adv[-1]


def tester(mon_hist, hist_adv, rng):
    """TESTER : « Si l'adversaire riposte, joue TIT-FOR-TAT ; sinon répète C, C, D ».

    Conventions choisies (le cours ne les précise pas) :
      - tour 1 : D (la provocation) ;
      - tour 2 : C (on ne sait pas encore si l'adversaire riposte) ;
      - riposte = l'adversaire joue D au tour 2, juste après notre trahison ;
      - s'il a riposté : TIT-FOR-TAT à partir du tour 3 ;
      - sinon : cycle C, C, D à partir du tour 2 (tours 2, 3, 4 = C, C, D, etc.).
    """
    tour = len(mon_hist)          # 0 = premier tour
    if tour == 0:
        return 'D'
    if tour == 1:
        return 'C'
    if hist_adv[1] == 'D':        # l'adversaire a riposté au tour 2
        return hist_adv[-1]       # TIT-FOR-TAT
    cycle = ['C', 'C', 'D']
    return cycle[(tour - 1) % 3]


def joss(mon_hist, hist_adv, rng):
    """JOSS : « TIT-FOR-TAT, mais remplace C par D une fois sur dix ».

    Convention choisie : les 10 % s'appliquent à chaque tour où TFT jouerait C,
    y compris le premier tour (lecture littérale de la règle).
    """
    coup = tit_for_tat(mon_hist, hist_adv, rng)
    if coup == 'C' and rng.random() < 0.10:
        return 'D'
    return coup


# Population de base utilisée par les tournois
STRATEGIES_COURS = {
    "ALL-D": all_d,
    "RANDOM": random_strat,
    "TIT-FOR-TAT": tit_for_tat,
    "TESTER": tester,
    "JOSS": joss,
}
